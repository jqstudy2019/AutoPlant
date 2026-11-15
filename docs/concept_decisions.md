# Concept-Phase Decision Record

How the architecture got from the first concept (commit `de00f96`, April 2026) to v1. Each row is a decision made before DR-0; after DR-1, changes go through `dhf/08_change_log.md`.

| # | Decision | Alternatives considered | Rationale |
|---|---|---|---|
| CD-01 | **One planter in v1**, designed to scale to N | 2 plants (expandable to 4) in the first build | Cuts build risk and time; one fully verified module is a stronger demonstration than two half-tested ones. Scaling is kept as a requirement (DI-25). |
| CD-02 | **One ESP32-CAM per planter** does sensing, pumping and camera | (a) ESP32-WROOM-32 driver node + separate ESP32-CAM camera node; (b) WROOM-32 only, no camera | Each planter becomes a self-contained repeatable module; fewer boards and less wiring. Cost: tight GPIO budget on the ESP32-CAM, accepted with the microSD slot unused. The WROOM-32 stays as a spare. |
| CD-03 | **I2C capacitive soil sensor** (Adafruit STEMMA, seesaw) | Analog capacitive sensor on the ESP32 ADC; analog sensor via ADS1115 I2C ADC | ESP32-CAM's free analog pins are on ADC2, which is unavailable while Wi-Fi runs. An I2C sensor avoids the ADC entirely and needs no extra ADC board. |
| CD-04 | **12 V mini submersible pump**, one per planter | Peristaltic pump; shared pump with solenoid valve manifold; household sump pump | Cheap, simple to switch with a MOSFET, right flow scale. One pump per planter keeps calibration and fault isolation simple. Valve manifold deferred. |
| CD-05 | **Side-mount PP float switch** for reservoir low | Vertical float; ultrasonic level sensor | Simple digital input, mounts exactly at the refill level, wired fail-safe. |
| CD-06 | **ROS 2 moved to phase 2** | ROS 2 Jazzy as the core from day one | Target role (medical-device NPD) weighs design controls, drawings and risk management far above ROS 2. Topic-style naming is kept so ROS 2 can be adopted later as a rename. See `phase2_ros2.md`. |
| CD-07 | **Design controls as the project spine** (DHF, ISO 14971-style risk file) | Software-first build with a test plan | Makes the project direct evidence for the Stryker Sage Staff Engineer posting and similar roles. |
| CD-08 | **Tailscale, no port forwarding** for remote access | Router port forwarding; raw WireGuard; Tailscale Funnel | Unchanged from the first concept: encrypted, identity-based, minimal admin. Funnel only for short public demos. |
| CD-09 | **Hobby scope, no Agile ceremony** | Scrum backlog, sprints, user stories | Solo project; phase gates and a task list are enough. |
