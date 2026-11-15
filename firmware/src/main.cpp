// AutoPlant planter node firmware — ESP32-CAM, Arduino core on FreeRTOS.
//
// Task layout (DO-16):
//   sensorTask   1 Hz   soil moisture, BME280, float switch -> shared state
//   pumpTask     20 Hz  executes run commands; enforces DI-08/09/11 via pump_logic.h
//   commsTask    -      Wi-Fi, telemetry to supervisor, receives commands   (phase 3)
//   cameraTask   -      snapshot endpoint                                    (phase 3)
//
// Defence in depth for the pump (HAZ-01, HAZ-02):
//   1. pumpTask checks pump::must_stop() every 50 ms.
//   2. A one-shot esp_timer, armed at start, forces both switches off at the
//      hard limit even if pumpTask is starved (dFMEA action).
//   3. PIN_PUMP_CUTOFF is a second, series switch so a shorted primary MOSFET
//      can still be interrupted (RC-04).
//
// STATUS: skeleton. Compiles once libraries are installed; sensor drivers,
// Wi-Fi and camera are stubbed and filled in during phase 3.

#include <Arduino.h>
#include <Wire.h>
#include <esp_timer.h>
#include "pins.h"
#include "pump_logic.h"

#ifndef NODE_ID
#define NODE_ID 1
#endif

struct NodeState {
    float    moisture_raw   = NAN;   // seesaw capacitive reading (200..2000)
    float    temp_c         = NAN;
    float    rh_pct         = NAN;
    bool     reservoir_low  = true;  // assume low until first read (fail-safe)
    bool     pump_running   = false;
    uint32_t last_link_ms   = 0;
};

static NodeState state;
static SemaphoreHandle_t stateMutex;
static QueueHandle_t pumpQueue;          // uint32_t requested run time in ms
static esp_timer_handle_t hardStopTimer;

// ------------------------------------------------------------------ pump I/O
static void IRAM_ATTR pumpOutputsOff() {
    digitalWrite(PIN_PUMP_GATE, LOW);
    digitalWrite(PIN_PUMP_CUTOFF, LOW);
}

static void pumpOutputsOn() {
    digitalWrite(PIN_PUMP_CUTOFF, HIGH);  // close series switch first
    digitalWrite(PIN_PUMP_GATE, HIGH);
}

static void hardStopCallback(void*) {
    pumpOutputsOff();                     // runs from esp_timer task, independent of pumpTask
}

// --------------------------------------------------------------------- tasks
static void sensorTask(void*) {
    for (;;) {
        // Float: INPUT_PULLUP, closed-to-GND = water OK, open = LOW WATER (fail-safe).
        const bool low = digitalRead(PIN_FLOAT) == HIGH;

        // TODO(phase 3): read Adafruit seesaw soil sensor (0x36) and BME280 (0x76).
        // Raw-to-% conversion lives on the supervisor so calibration is in one place.

        xSemaphoreTake(stateMutex, portMAX_DELAY);
        state.reservoir_low = low;
        xSemaphoreGive(stateMutex);
        vTaskDelay(pdMS_TO_TICKS(1000));
    }
}

static void pumpTask(void*) {
    pump::Inputs in{};
    for (;;) {
        uint32_t requested = 0;
        xSemaphoreTake(stateMutex, portMAX_DELAY);
        in.reservoir_low = state.reservoir_low;
        in.last_link_ms  = state.last_link_ms;
        xSemaphoreGive(stateMutex);
        in.now_ms = millis();

        if (!in.running && xQueueReceive(pumpQueue, &requested, 0) == pdTRUE) {
            if (pump::may_start(in)) {
                in.requested_ms = pump::clamp_runtime(requested);
                in.started_ms   = in.now_ms;
                in.running      = true;
                esp_timer_start_once(hardStopTimer, (uint64_t)pump::MAX_RUNTIME_MS * 1000ULL);
                pumpOutputsOn();
                log_i("pump start %u ms", in.requested_ms);
            } else {
                log_w("pump start refused (reservoir_low=%d)", in.reservoir_low);
            }
        }

        if (pump::must_stop(in)) {
            pumpOutputsOff();
            esp_timer_stop(hardStopTimer);
            in.running = false;
            log_i("pump stop after %u ms", in.now_ms - in.started_ms);
        }

        xSemaphoreTake(stateMutex, portMAX_DELAY);
        state.pump_running = in.running;
        xSemaphoreGive(stateMutex);
        vTaskDelay(pdMS_TO_TICKS(50));
    }
}

static void commsTask(void*) {
    // TODO(phase 3): connect Wi-Fi, publish telemetry JSON every 60 s
    //   {"node":NODE_ID,"moisture_raw":..,"temp_c":..,"rh_pct":..,"reservoir_low":..,"pump":..}
    // and accept {"cmd":"water","ms":10000}. Each valid supervisor message
    // updates state.last_link_ms. Transport (MQTT vs HTTP) is an open decision.
    for (;;) vTaskDelay(pdMS_TO_TICKS(1000));
}

// --------------------------------------------------------------------- setup
void setup() {
    // Strapping pins 2 and 12: drive LOW immediately.
    pinMode(PIN_PUMP_GATE, OUTPUT);
    pinMode(PIN_PUMP_CUTOFF, OUTPUT);
    pumpOutputsOff();
    pinMode(PIN_FLOAT, INPUT_PULLUP);

    Serial.begin(115200);
    Wire.begin(PIN_I2C_SDA, PIN_I2C_SCL);
    log_i("AutoPlant node %d booting", NODE_ID);

    stateMutex = xSemaphoreCreateMutex();
    pumpQueue  = xQueueCreate(1, sizeof(uint32_t));
    const esp_timer_create_args_t args = {.callback = &hardStopCallback, .name = "pump_hard_stop"};
    esp_timer_create(&args, &hardStopTimer);

    xTaskCreatePinnedToCore(pumpTask,   "pump",   4096, nullptr, 5, nullptr, 1);  // highest priority
    xTaskCreatePinnedToCore(sensorTask, "sensor", 4096, nullptr, 3, nullptr, 1);
    xTaskCreatePinnedToCore(commsTask,  "comms",  8192, nullptr, 2, nullptr, 0);
}

void loop() { vTaskDelay(portMAX_DELAY); }
