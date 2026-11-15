# 03 — Design Outputs

Rev A (draft) · 2026-10-18

Design outputs are the drawings, schematics, code and specifications that satisfy the design inputs. Entries marked *planned* do not exist yet; they are filled in during phases 2–3.

| ID | Output | Satisfies | Location | State |
|---|---|---|---|---|
| DO-01 | Soil sensor driver + calibration curve | DI-01, DI-10 | `firmware/src/sensors.cpp`, `analysis/moisture_cal/` | Planned |
| DO-02 | BME280 driver | DI-02 | `firmware/src/sensors.cpp` | Planned |
| DO-03 | Float switch mount drawing + debounce input | DI-03, DI-09 | `mechanical/drawings/`, `firmware/src/main.cpp` | Planned |
| DO-04 | Supervisor control logic (hysteresis, limits, cooldown, plausibility) | DI-04, DI-06, DI-07, DI-10, DI-13 | `supervisor/autoplant/controller.py` | Skeleton + tests |
| DO-05 | Pump dose calibration (mL/s) and runtime calculation | DI-05 | `supervisor/autoplant/controller.py`, `analysis/pump_cal/` | Skeleton |
| DO-06 | Firmware pump task with hard runtime limit and reservoir interlock | DI-08, DI-09 | `firmware/src/pump.cpp` | Skeleton |
| DO-07 | Firmware link-loss watchdog | DI-11 | `firmware/src/main.cpp` | Skeleton |
| DO-08 | Pump circuit schematic with independent series cutoff, fuse and derated MOSFET selection | DI-12, DI-19, DI-29 | `mechanical/drawings/schematic.pdf` | Planned |
| DO-09 | Flask dashboard + alerting | DI-14, DI-15, DI-17, DI-18 | `supervisor/autoplant/dashboard.py` | Skeleton |
| DO-10 | Data logger | DI-16 | `supervisor/autoplant/datalog.py` | Skeleton |
| DO-11 | Enclosure, reservoir lid, stand and drip tray drawings (GD&T) | DI-20, DI-24, DI-27, DI-28 | `mechanical/drawings/` | Planned |
| DO-12 | Fluid path spec (tubing, fittings, routing) | DI-21 | `mechanical/drawings/` | Planned |
| DO-13 | Reservoir volume analysis | DI-22 | `analysis/reservoir_sizing.md` | Planned |
| DO-14 | Planter config schema | DI-25 | `supervisor/config/planters.json` | Draft |
| DO-15 | Network/security configuration (Tailscale, auth) | DI-26 | `docs/architecture.md` | Planned |
| DO-16 | Firmware main loop / task structure | DI-23 | `firmware/src/main.cpp` | Skeleton |
