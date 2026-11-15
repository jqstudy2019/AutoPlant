# AutoPlant — Modular Automated Plant Watering and Monitoring System

A single-planter automated watering system built as a **design-control case study**: user needs → design inputs → design outputs → verification → validation, with an ISO 14971-style risk file and full traceability. The planter is also a daily-use, data-rich device for my own plants.

> **Framing note:** AutoPlant is not a regulated device. This repo applies medical-device design-control *practices* (ISO 13485 cl. 7.3, ISO 14971) to a personal project to demonstrate the workflow.

## Status

| Phase | State | Deliverables |
|---|---|---|
| 1. Define (user needs, design inputs, risk) | In progress: documents drafted (Rev A); DR-0 pre-review held 2026-10-18, 9 findings open | [User needs](docs/dhf/01_user_needs.md) · [Design inputs](docs/dhf/02_design_inputs.md) · [Verification plan](docs/dhf/04_verification/verification_plan.md) · [Hazard analysis](docs/dhf/06_risk/hazard_analysis.md) · [dFMEA](docs/dhf/06_risk/dfmea.csv) · [DR-0](docs/dhf/07_design_reviews/DR-0_design_input_review.md) |
| 2. Design (CAD, GD&T, stack-up, FEA, DFM) | Not started | — |
| 3. Build (bring-up, firmware, supervisor) | Control and pump-safety logic implemented with 21 passing tests; drivers and dashboard not yet built | [tests/](tests/) · [traceability matrix](docs/dhf/traceability_matrix.csv) |
| 4. Verify & validate | Not started | — |
| 5. Package | Not started | — |

## Architecture (v1)

```
Phone/laptop ──Tailscale──▶ Raspberry Pi (Flask dashboard, control logic, logging)
                                   │  Wi-Fi (telemetry up, pump commands down)
                                   ▼
                     ESP32-CAM planter node (C++ / FreeRTOS)
           ┌──────────────┬──────────────┬───────────────┬──────────────┐
      Soil sensor (I2C)  BME280 (I2C)  Float switch    MOSFET → 12V mini pump
           │                              │                 │
        Planter ◀──────── tube line ──── Reservoir ◀────────┘
```

Each additional planter = one more ESP32-CAM node with the same firmware and a new entry in `supervisor/config/planters.json`.

## Repository layout

| Path | Contents |
|---|---|
| `docs/dhf/` | Design History File: plan, user needs, design inputs/outputs, verification, validation, risk, reviews, change log, traceability matrix |
| `firmware/` | ESP32-CAM firmware (PlatformIO, C++, FreeRTOS tasks) |
| `supervisor/` | Raspberry Pi Python package: control logic, safety interlocks, logging, Flask dashboard |
| `mechanical/` | BOM; CAD exports (STEP) and drawing PDFs from phase 2 |
| `analysis/` | Calibration data and notebooks (phase 4) |
| `tests/` | pytest suite for the supervisor |

## Quick start (supervisor, no hardware)

```bash
cd supervisor
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
pytest ../tests
python -m autoplant.sim        # runs the control loop against a simulated planter
```

## Traceability ID scheme

`UN-xx` user needs · `DI-xx` design inputs · `DO-xx` design outputs · `VER-xx` verification · `VAL-xx` validation · `HAZ-xx` hazards · `RC-xx` risk controls. The master map is `docs/dhf/traceability_matrix.csv`; `tools/check_trace.py` verifies every ID resolves.

## Design history and future work

- [docs/concept_decisions.md](docs/concept_decisions.md): how the design moved from the first concept (2 plants, separate WROOM-32 driver node, ROS 2 first) to v1, and why
- Future work, outside v1 scope: [ROS 2 Jazzy integration](docs/phase2_ros2.md) and additional planter modules
