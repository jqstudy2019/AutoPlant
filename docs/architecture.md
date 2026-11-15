# Architecture

## Nodes

| Node | Hardware | Software | Responsibilities |
|---|---|---|---|
| Supervisor | Raspberry Pi 4/5 | Python 3, Flask, Tailscale (ROS 2 Jazzy in phase 2) | Watering decisions, calibration (raw → %), logging, image archive, dashboard, alerts, remote access |
| Planter node (×N) | ESP32-CAM (AI-Thinker) | C++, Arduino core on FreeRTOS | Sensor sampling, pump execution with hard safety limits, camera snapshots, telemetry |
| Client | Phone / laptop | Browser + Tailscale app | View dashboard, manual water, acknowledge faults |

## Split of safety responsibility

Decisions live on the supervisor; **limits live on the node**. The node never trusts a command blindly: it clamps runtime to 30 s, refuses to start or keeps stopped while the reservoir is low, and turns the pump off if the supervisor goes silent for 2 minutes. A one-shot hardware timer and a second series switch back up the pump task (see `firmware/src/main.cpp`, RC-01, RC-04).

## Messages (provisional, phase 3)

Node → supervisor, every 60 s:
```json
{"node": 1, "moisture_raw": 812, "temp_c": 22.4, "rh_pct": 41.0, "reservoir_low": false, "pump": false}
```
Supervisor → node:
```json
{"cmd": "water", "ms": 10000}
```
Topic-style names are used even before ROS 2 (`planter/1/telemetry`, `planter/1/cmd`) so the move to ROS 2 or MQTT topics is a rename, not a redesign.

## Image archive (DI-30)

The supervisor pulls a snapshot from each node hourly and within 5 min after each watering cycle, and stores it on the Pi under `supervisor/data/images/<planter>/<date>/`. Images never leave the Pi except through the authenticated dashboard (HAZ-09, RC-14).

## Network and security (DO-15, DI-26)

- All devices on the home Wi-Fi. Nodes are never reachable from outside the LAN.
- Flask binds to `127.0.0.1`; `tailscale serve` exposes it to the tailnet only.
- No router port forwarding. Dashboard login required even inside the tailnet.

Setup checklist (carried from the concept-phase notes):

- [ ] Pi: install Tailscale, sign into the tailnet, run the dashboard as a systemd service
- [ ] Pi: `tailscale serve` the dashboard; confirm it is not reachable from the public internet (VER-16)
- [ ] Phone: install Tailscale, join the same tailnet, test the dashboard on cellular data
- [ ] Log every remote manual action with user and time
- [ ] Keep Wi-Fi credentials and dashboard secrets in environment variables or an untracked file, never in git

## Power

12 V listed adapter → inline fuse → pump circuit; 12 V → buck converter → 5 V → ESP32-CAM. Common ground. Pi on its own USB-C supply.

## I2C bus

The soil sensor and BME280 share one I2C bus on the node. Check address compatibility before adding any other I2C device.
