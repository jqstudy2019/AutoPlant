#pragma once
// ESP32-CAM (AI-Thinker) pin map — PROVISIONAL until phase 3 bench bring-up.
//
// The camera claims most GPIOs. With the microSD slot unused, 2, 4, 12, 13,
// 14, 15 become available. 2 and 12 are boot strapping pins: both must be LOW
// at reset, so each gate has a 10 k pull-down and firmware drives it LOW first.
// GPIO 4 drives the on-board flash LED; avoid it. GPIO 16 is PSRAM; avoid it.

constexpr int PIN_I2C_SDA      = 14;  // soil sensor (0x36) + BME280 (0x76)
constexpr int PIN_I2C_SCL      = 15;
constexpr int PIN_FLOAT        = 13;  // INPUT_PULLUP; float closes to GND when water OK.
                                      // Open circuit (broken wire) reads HIGH = LOW WATER (fail-safe).
constexpr int PIN_PUMP_GATE    = 2;   // primary low-side MOSFET gate
constexpr int PIN_PUMP_CUTOFF  = 12;  // independent series switch (RC-04 / DI-12)
