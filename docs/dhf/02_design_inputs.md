# 02 — Design Inputs

Rev A (draft) · 2026-10-18

Each design input is a measurable requirement that traces to one or more user needs and has a verification method: **T** test, **A** analysis, **I** inspection, **D** demonstration. Numeric values marked † are initial estimates to be confirmed during phase 2–4 calibration; changes after DR-1 go through `08_change_log.md`.

## Sensing

| ID | Requirement | Traces to | Method | Verified by |
|---|---|---|---|---|
| DI-01 | The system shall report a soil moisture index (0–100 %, calibrated dry-to-saturated) at least once per minute, with repeatability of ±3 % index (1σ) at a fixed soil state.† | UN-01, UN-04 | T | VER-01 |
| DI-02 | The system shall report ambient temperature (±1 °C) and relative humidity (±3 % RH) at least once per 5 minutes. | UN-04 | T | VER-02 |
| DI-03 | The system shall detect reservoir-low state when water falls below the level that leaves ≥ 150 mL above the pump intake.† | UN-03, UN-06 | T | VER-03 |

## Watering control

| ID | Requirement | Traces to | Method | Verified by |
|---|---|---|---|---|
| DI-04 | The system shall begin a watering episode when moisture falls below the dry threshold (default 35 %), continue cycles (subject to DI-06 and DI-07) until moisture exceeds the wet threshold (default 42 %), and shall not begin a new episode while moisture is between the thresholds. Thresholds are configurable per planter. | UN-01, UN-02 | T | VER-04 |
| DI-05 | Each watering cycle shall deliver the configured dose (default 50 mL) within ±15 %.† | UN-01, UN-02 | T | VER-05 |
| DI-06 | The system shall perform no more than the configured maximum automatic cycles per planter per rolling 24 h (default 2). | UN-02 | T | VER-04 |
| DI-07 | The system shall enforce a minimum interval between automatic cycles on the same planter (default 6 h). | UN-02 | T | VER-04 |
| DI-08 | The edge node firmware shall stop the pump no later than 30 s after any start command, independent of the supervisor. | UN-02, UN-06 | T | VER-06 |
| DI-09 | The pump shall not run, and any running pump shall stop within 1 s, while reservoir-low is detected. | UN-03, UN-06 | T | VER-06 |
| DI-10 | On sensor read failure or implausible moisture data (outside 0–100 % after calibration, or change > 20 %/min without a watering event), automatic watering shall be inhibited and a fault raised. | UN-02 | T | VER-07 |
| DI-11 | On loss of communication with the supervisor, the edge node shall turn the pump off and start no new cycles until the link is restored. | UN-02, UN-06 | T | VER-07 |
| DI-12 | A single-point failure in the pump switching circuit (e.g. MOSFET shorted) shall not cause pumping to continue beyond 60 s. | UN-02, UN-06 | T | VER-08 |
| DI-13 | If three consecutive watering cycles produce < 3 % moisture rise, the system shall inhibit automatic watering and raise a "no response" fault. | UN-02 | T | VER-07 |

## User interface and data

| ID | Requirement | Traces to | Method | Verified by |
|---|---|---|---|---|
| DI-14 | The dashboard shall show current moisture, temperature, humidity, reservoir state, pump state, last watering time and a 7-day moisture trend, shall flag any value older than 10 min as stale, and shall load in < 3 s over Tailscale. | UN-04, UN-01 | T | VER-09 |
| DI-15 | The system shall show a reservoir-low alert on the dashboard within 60 s of detection and send a push notification. | UN-03 | T | VER-09 |
| DI-16 | The system shall log every sensor reading (≥ 1 per 5 min) and every pump event with a reason code, and retain logs ≥ 90 days. | UN-04 | I, T | VER-10 |
| DI-17 | A manual water command from the dashboard shall start the pump within 5 s, subject to DI-08 and DI-09. | UN-05 | T | VER-09 |
| DI-18 | The dashboard shall show a camera image of the planter (≥ 640 × 480) no older than 15 min. | UN-07 | T | VER-09 |

## Physical, safety and security

| ID | Requirement | Traces to | Method | Verified by |
|---|---|---|---|---|
| DI-19 | All circuits shall operate at ≤ 12 V DC, powered by an external listed AC adapter, with a fuse on the 12 V line. | UN-06 | I | VER-11 |
| DI-20 | The electronics enclosure shall sit above the reservoir's maximum water line, and no water shall reach the electronics in a 250 mL splash test onto the enclosure top.† | UN-06 | T | VER-11 |
| DI-21 | The fluid path shall show no leaks over a 14-day run. | UN-06 | T | VER-12 |
| DI-22 | The reservoir shall hold enough water for ≥ 14 days at nominal use (≥ 1.5 L usable at 100 mL/day).† | UN-08 | A | VER-13 |
| DI-23 | The system shall run 14 days continuously without manual intervention or reboot. | UN-08 | T | VER-12 |
| DI-24 | The reservoir shall be refillable without tools in < 2 min through an opening ≥ 50 mm. | UN-09 | T, I | VER-14 |
| DI-25 | Adding planter N shall require only flashing the node firmware with its node ID and adding one config entry; no supervisor code change. | UN-10 | D | VER-15 |
| DI-26 | The dashboard shall be reachable only from the LAN and the tailnet, with no inbound router ports opened, and shall require login. | UN-11 | I, T | VER-16 |
| DI-27 | Footprint ≤ 300 × 200 mm; height ≤ 350 mm excluding the plant; the loaded unit shall not tip when tilted 10°. | UN-12, UN-06 | I, T | VER-14 |
| DI-28 | A drip tray under the planter and reservoir shall contain ≥ 500 mL.† | UN-06 | I | VER-14 |
| DI-29 | Pump switching components shall operate at ≤ 50 % of rated current and stay below 60 °C case temperature during a 30 s run. | UN-06 | T | VER-06 |
