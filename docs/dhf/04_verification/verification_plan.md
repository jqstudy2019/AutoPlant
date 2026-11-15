# Verification Plan

Rev A (draft) · 2026-10-18

Each protocol gets its own file (`VER-xx_protocol.md`) before execution and a report (`VER-xx_report.md`) after. Sample sizes are small because this is a single prototype; they are chosen to show the method, and each report states its statistical limits.

| ID | Protocol | Verifies | Method summary | Acceptance criteria | Sample |
|---|---|---|---|---|---|
| VER-01 | Moisture sensor calibration and repeatability | DI-01 | Readings in air, dry soil, field-capacity soil, saturated soil; 30 readings per state; fit calibration curve | Monotonic curve; σ ≤ 3 % index per state; ≥ 1 sample/min logged | 4 states × 30 |
| VER-02 | Environmental sensor check | DI-02 | Compare BME280 to reference thermometer/hygrometer over 24 h | Mean error ≤ 1 °C and ≤ 3 % RH | 288 pairs |
| VER-03 | Reservoir-low detection level | DI-03 | Drain reservoir in 25 mL steps; record trip volume | Trip leaves ≥ 150 mL above intake in 5/5 trials | 5 drains |
| VER-04 | Watering logic (hysteresis, cycle limit, cooldown) | DI-04, DI-06, DI-07 | Automated unit tests (pytest, simulated time) + bench check with potentiometer-simulated sensor | All tagged tests pass; bench behaviour matches | Full suite |
| VER-05 | Dose accuracy | DI-05 | Gravimetric: weigh water per cycle at 3 reservoir levels | All doses within ±15 % of 50 mL; report mean, σ, Cpk | 3 levels × 10 |
| VER-06 | Firmware pump limits and switch thermal check | DI-08, DI-09, DI-29 | Send 120 s run command; trigger float mid-run; scope on MOSFET gate; thermocouple on MOSFET case; measure pump current | Pump off at ≤ 30 s; off within 1 s of float trip; current ≤ 50 % of MOSFET rating; case < 60 °C | 10 each |
| VER-07 | Fault handling | DI-10, DI-11, DI-13 | Unplug sensor; inject out-of-range and step data; drop Wi-Fi; simulate no moisture response | Auto watering inhibited and fault shown in every case; pump off on link loss | 1 per fault × 3 |
| VER-08 | Single-fault pump cutoff | DI-12 | Short the primary MOSFET with a jumper; command run | Independent cutoff stops pump ≤ 60 s | 3 |
| VER-09 | Dashboard and alerts | DI-14, DI-15, DI-17, DI-18 | Timed checks from phone on LTE via Tailscale; power off the node to check stale flag | Load < 3 s; alert < 60 s; manual start < 5 s; image ≤ 15 min old; stale flag within 10 min | 10 each |
| VER-10 | Logging | DI-16 | Inspect logs after 7 days; count samples and events | ≥ 1 sample/5 min, no gaps > 10 min; every pump event has a reason code | 7 days |
| VER-11 | Electrical and splash | DI-19, DI-20 | Inspect supply labels and voltages; 250 mL splash test with indicator paper inside enclosure | ≤ 12 V DC everywhere; indicator paper dry | 3 splashes |
| VER-12 | 14-day endurance | DI-21, DI-23 | Run unattended 14 days; inspect fittings daily with paper towel | No leaks; no reboot or intervention; uptime log continuous | 1 run |
| VER-13 | Reservoir sizing analysis | DI-22 | Calculation from measured usable volume and consumption logs | Usable volume ≥ 1.5 L and ≥ 14 days at measured use | Analysis |
| VER-14 | Physical inspection, stability and refill | DI-24, DI-27, DI-28 | Measure footprint, opening and tray volume; 10° tilt test loaded; time 5 refills by a household member | Within limits; no tip; tray ≥ 500 mL; all refills < 2 min, no tools | 5 refills |
| VER-15 | Add-a-planter demonstration | DI-25 | Bring up a second node (spare ESP32-CAM) with config change only | Second planter appears and reports; `git diff` shows no supervisor code change | 1 |
| VER-16 | Network security check | DI-26 | Router port scan from outside; attempt access without login; access via tailnet | No open inbound ports; unauthenticated request rejected; tailnet works | 1 each |

## Validation

| ID | Activity | Validates | Acceptance |
|---|---|---|---|
| VAL-01 | 14-day in-home use with a real plant, author away ≥ 3 days | UN-01–UN-08 | Plant healthy (photo record); no overwatering; at least one refill alert acted on; remote checks done from outside home |
| VAL-02 | Household user feedback (refill, dashboard) | UN-04, UN-05, UN-09, UN-12 | ≥ 2 users complete tasks unaided; feedback logged and dispositioned |
