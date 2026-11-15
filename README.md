# AutoPlant — Modular Automated Plant Watering and Monitoring System

A single-planter automated watering system built as a **design-control case study**: user needs → design inputs → design outputs → verification → validation, with an ISO 14971-style risk file and full traceability. The planter is also a daily-use, data-rich device for my own plants.

> **Framing note:** AutoPlant is not a regulated device. This repo applies medical-device design-control *practices* (ISO 13485 cl. 7.3, ISO 14971) to a personal project to demonstrate the workflow.

## Status

| Phase  State |
|---|---|---|
| 1. Define (user needs, design inputs, risk) | In progress |
| 2. Design (CAD, GD&T, stack-up, FEA, DFM) | Not started |
| 3. Build (bring-up, firmware, supervisor)  | Skeleton code only |
| 4. Verify & validate | Not started |
| 5. Package | Not started |

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
| `mechanical/` | CAD exports (STEP), drawing PDFs, BOM |
| `analysis/` | Calibration data and notebooks |
| `tests/` | pytest suite for the supervisor |

## Background and roadmap

- `docs/concept_decisions.md` — how the design moved from the first concept (2 plants, separate WROOM-32 driver node, ROS 2 first) to v1, and why
- `docs/phase2_ros2.md` — the planned ROS 2 Jazzy node graph and topics

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
