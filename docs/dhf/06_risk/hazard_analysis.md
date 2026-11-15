# Hazard Analysis

Rev A (draft) · 2026-10-18 · Scales and acceptability: `risk_management_plan.md`. Probabilities are engineering judgement for a single prototype and are revisited with VER and VAL-01 data.

## Hazards and risk evaluation

| ID | Hazard / sequence of events | Harm | S | P | Initial | Risk controls | S | P | Residual |
|---|---|---|---|---|---|---|---|---|---|
| HAZ-01 | Software fault or stuck command keeps pump running → pot overflows | Water damage to furniture/floor | 4 | 3 | Unacc. | RC-01, RC-02, RC-03 | 4 | 1 | Acc. |
| HAZ-02 | Primary MOSFET fails shorted → pump runs until reservoir is empty | Water damage (up to ~2 L) | 4 | 2 | ALARP | RC-04, RC-03 | 4 | 1 | Acc. |
| HAZ-03 | Soil sensor reads falsely dry (disconnected, corroded, moved out of soil) → repeated watering | Overflow, root rot | 4 | 3 | Unacc. | RC-02, RC-05, RC-06, RC-03 | 3 | 1 | Acc. |
| HAZ-04 | Plant not watered: sensor reads falsely wet, Wi-Fi/link down, or reservoir empty unnoticed | Plant death | 3 | 3 | ALARP | RC-07, RC-08 | 3 | 2 | Acc. |
| HAZ-05 | Pump runs dry | Pump overheats/burns out | 2 | 3 | Acc. | RC-09 | 2 | 1 | Acc. |
| HAZ-06 | Water reaches electronics (splash, leak, condensation) | Short circuit; fire at supply | 5 | 2 | Unacc. | RC-10, RC-11 | 5 | 1 | ALARP — see note 1 |
| HAZ-07 | Tube slips off fitting or fitting leaks | Water damage | 4 | 3 | Unacc. | RC-12, RC-03 | 3 | 2 | Acc. |
| HAZ-08 | MOSFET, wiring or regulator overheats | Burn, fire | 5 | 2 | Unacc. | RC-11, RC-13 | 5 | 1 | ALARP — see note 1 |
| HAZ-09 | Unauthorized remote access | Camera privacy breach; malicious pump commands | 3 | 3 | ALARP | RC-14, RC-01 | 3 | 1 | Acc. |
| HAZ-10 | Loaded unit tips over on shelf | Spill, broken pot | 3 | 2 | Acc. | RC-15, RC-03 | 3 | 1 | Acc. |

**Note 1 (ALARP rationale):** Severity stays 5 because fire is the worst credible outcome of any powered device. Probability is reduced to 1 by a listed 12 V adapter with its own protection, a fuse on the 12 V line, derated switching parts, and electronics placed above the water line. Further reduction (e.g. potting the electronics) would block debugging and add little, so the residual risk is accepted.

## Risk controls

| ID | Control | Type | Implemented by (DI) | Verified by |
|---|---|---|---|---|
| RC-01 | Firmware hard pump runtime limit (30 s), independent of supervisor | Protective | DI-08 | VER-06 |
| RC-02 | Supervisor cycle limit (2/24 h) and 6 h cooldown | Protective | DI-06, DI-07 | VER-04 |
| RC-03 | Drip tray ≥ 500 mL under planter and reservoir | Inherent design | DI-28 | VER-14 |
| RC-04 | Independent series cutoff in pump circuit (second switch driven by a separate pin/watchdog) | Inherent design | DI-12 | VER-08 |
| RC-05 | Moisture plausibility checks inhibit auto watering | Protective | DI-10 | VER-07 |
| RC-06 | "No moisture response" detection after 3 cycles | Protective | DI-13 | VER-07 |
| RC-07 | Reservoir-low detection, dashboard alert and push notification | Information | DI-03, DI-15 | VER-03, VER-09 |
| RC-08 | Link-loss fail-off, fault alerts, stale-data flag | Protective + information | DI-11, DI-14 | VER-07, VER-09 |
| RC-09 | Float-switch interlock stops pump within 1 s | Protective | DI-09 | VER-06 |
| RC-10 | Electronics enclosure above max water line; splash-resistant lid | Inherent design | DI-20 | VER-11 |
| RC-11 | ≤ 12 V DC from listed adapter; fuse on 12 V line | Inherent design | DI-19 | VER-11 |
| RC-12 | Barbed fittings with clamps; tube retention clips | Inherent design | DI-21 | VER-12 |
| RC-13 | Switching parts derated to ≤ 50 % current; thermal check | Inherent design | DI-29 | VER-06 |
| RC-14 | Tailscale-only remote access, no open ports, dashboard login | Protective | DI-26 | VER-16 |
| RC-15 | Low centre of gravity, footprint limit, anti-slip feet, tilt test | Inherent design | DI-27 | VER-14 |

## Risks introduced by controls

| Control | New risk | Disposition |
|---|---|---|
| RC-05, RC-06 | False fault inhibits watering → plant stress (HAZ-04) | Alerts (RC-08) tell the user; accepted |
| RC-04 | Second switch fails open → no watering (HAZ-04) | Detected by no-response logic and alerts; accepted |
| RC-14 | Locked out of own dashboard | Local LAN access retained as fallback |
