# Phase 2 — ROS 2 Integration (planned)

Carried forward from the first concept (commit `de00f96`) and updated for the one-node-per-planter architecture. Phase 2 starts after DR-3; nothing here is needed for v1.

## Target stack

- Raspberry Pi: Ubuntu 24.04, ROS 2 Jazzy (LTS)
- Planter nodes: stay on lightweight Wi-Fi messaging first; micro-ROS on the ESP32 is an optional later step
- The Pi bridges node telemetry into ROS 2 topics, so firmware does not change when ROS 2 arrives

## Node layout on the Pi

| Node | Replaces (v1) | Role |
|---|---|---|
| `node_bridge` | comms code in supervisor | Talks to planter nodes over Wi-Fi; publishes telemetry, forwards commands |
| `irrigation_controller` | `autoplant/controller.py` | Same decision logic, wrapped as a node; one controller instance per planter |
| `logger` | `autoplant/datalog.py` | Subscribes broadly, writes CSV/JSONL |
| `alert` | dashboard alerts | Reservoir-low, faults, stale data → push notification |
| `camera_client` | dashboard image fetch | Pulls snapshots on schedule and around watering events |
| `dashboard_bridge` | Flask data access | Caches latest state for the Flask app |

`controller.py` is pure logic with no I/O, so wrapping it in a ROS 2 node is a thin adapter, and its pytest suite keeps working unchanged.

## Topics

Per planter (namespace `/planter/<id>/`):

| Topic | Type (draft) | Direction |
|---|---|---|
| `/planter/<id>/moisture` | `std_msgs/Float32` (%) | bridge → controller, logger |
| `/planter/<id>/reservoir_low` | `std_msgs/Bool` | bridge → controller, alert |
| `/planter/<id>/water_cmd` | custom `WaterCommand` (runtime_ms, reason) | controller → bridge |
| `/planter/<id>/events` | custom `IrrigationEvent` | controller → logger, alert |
| `/planter/<id>/status` | custom `PlanterStatus` (faults, in_episode, pump) | controller → dashboard_bridge |
| `/planter/<id>/camera/snapshot` | `sensor_msgs/CompressedImage` | camera_client → dashboard_bridge |

System-wide: `/environment/temperature`, `/environment/humidity`, `/system/faults`.

Custom messages live in an `autoplant_interfaces` package.

## Workspace layout

```text
ros2_ws/src/
├── autoplant_interfaces/
├── autoplant_bridge/
├── autoplant_controller/
├── autoplant_logger/
├── autoplant_alert/
└── autoplant_camera/
```

## Exit criteria

- Same VER-04 / VER-07 tests pass against the ROS 2 controller node
- A second planter appears by launching one more controller with a new namespace (DI-25 still holds)
- `ros2 bag` recording of a 24 h run committed to `analysis/`
