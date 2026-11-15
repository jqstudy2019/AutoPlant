# Project Plan

## Project objective
Build a single working modular smart-planter prototype using an ESP32-CAM planter edge node, an I2C capacitive soil moisture sensor, a cheap mini submersible pump, and a Raspberry Pi supervisory stack with ROS 2, dashboarding, logging, and secure remote access.

## Success criteria
- moisture reading visible on dashboard
- camera snapshot visible on dashboard
- float switch blocks watering when reservoir is low
- manual pump actuation works
- automatic watering logic works for one planter
- remote dashboard access works securely
- system documentation is complete enough to replicate the module

## Build phases

### Phase 1 — Setup and architecture
- finalize node architecture
- create repository and documentation structure
- define wiring and fluidic diagrams
- set up Raspberry Pi environment

### Phase 2 — Connectivity and dashboard
- install ROS 2 on Raspberry Pi
- install Tailscale
- bring up starter dashboard
- verify remote access

### Phase 3 — ESP32-CAM firmware baseline
- camera bring-up
- Wi-Fi connectivity
- telemetry framework
- local command handling

### Phase 4 — Sensing and actuation
- integrate I2C soil sensor
- integrate BME280
- integrate float switch
- integrate pump driver and mini submersible pump

### Phase 5 — Control logic
- threshold logic
- hysteresis
- cooldown
- safety interlocks
- manual override

### Phase 6 — Calibration and test
- moisture calibration
- pump timing calibration
- fault testing
- reliability testing

### Phase 7 — Documentation and polish
- photos
- final diagrams
- sample logs and screenshots
- resume bullets
- roadmap for additional planter modules
