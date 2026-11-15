# DR-0 — Design Input Review

| Field | Value |
|---|---|
| Stage gate | End of phase 1 (Define) |
| Documents reviewed | `01_user_needs.md` Rev A, `02_design_inputs.md` Rev A, `04_verification/verification_plan.md` Rev A, `06_risk/hazard_analysis.md` Rev A, `06_risk/risk_management_plan.md` Rev A |
| Baseline commit | `53c254e` |
| Reviewer | Author (self-review); outside reviewer TBD |
| Status | **Open** — pre-review done 2026-10-18; gate not passed until Voice of Customer interviews are complete and the findings below are closed |

## Gate criteria (from `00_design_plan.md`)

| # | Criterion | Result | Evidence |
|---|---|---|---|
| G1 | Every DI is measurable | Partial | F-03, F-04 |
| G2 | Every DI traces to ≥ 1 UN | Pass | `tools/check_trace.py`: no broken links |
| G3 | Every DI has a verification method | Partial | All DIs map to a VER; F-05 (retention not covered) |
| G4 | Hazards have initial risk estimates | Pass | All 10 hazards scored; S×P ratings match the acceptability matrix |
| G5 | User needs confirmed with users | Not met | VoC interviews not done; UN-09, UN-12 provisional |

Supporting checks: `pytest tests` 21 passed; traceability matrix regenerated with no broken links.

## Findings

| # | Severity | Finding | Proposed action | Owner | Status |
|---|---|---|---|---|---|
| F-01 | **Major** | Worst-case pump run volume can be larger than the drip tray. A typical 12 V mini submersible pump delivers ~1.5–4 L/min. At that rate, the 30 s firmware limit (DI-08) releases ~0.75–2 L and the 60 s single-fault limit (DI-12) ~1.5–4 L, against a 500 mL tray (DI-28). The HAZ-07 residual severity of 3 ("contained by tray") and the HAZ-01 control argument therefore depend on a flow rate that isn't specified anywhere. It also affects DI-05: at 3 L/min a 50 mL dose is a ~1 s run, so spin-up variation will make ±15 % hard to meet. | Add a DI stating that the worst-case volume of a single run at the firmware limit is ≤ the tray capacity. Then do one of: (a) pick a low-flow pump (≤ 1 L/min → ≤ 500 mL in 30 s), (b) derive the firmware limit from the measured flow (e.g. 2 × dose time), or (c) increase the tray size. Re-score HAZ-01, HAZ-02 and HAZ-07 once the pump flow is measured. | Author | Open |
| F-02 | Major | UN-10 (add planters) and UN-11 (access control) are not covered by any validation activity. VAL-01 covers UN-01–08, and VAL-02 covers UN-04, 05, 09 and 12. | Extend VAL-02, or add a VAL-03: a household member adds the second planter using the docs, and a user confirms an invited person can reach the dashboard while others cannot. | Author | Open |
| F-03 | Minor | DI-13 has no time window for measuring the "moisture rise". The code uses a 10 min window (`controller.py` `RESPONSE_WINDOW_S`), but the requirement doesn't state one, so it isn't measurable as written. | Add "measured 10 min after the cycle ends" to DI-13. | Author | Open |
| F-04 | Minor | DI-15 gives no time limit or channel for the push notification. The MQTT vs HTTP choice is still open. | State the latency (e.g. ≤ 5 min) and leave the channel to the design output. | Author | Open |
| F-05 | Minor | DI-16 requires ≥ 90-day retention, but VER-10 only inspects 7 days of logs. | Add an analysis step to VER-10: projected storage for 90 days at the measured log rate, plus a check of the retention/rotation config. | Author | Open |
| F-06 | Minor | VER-02 judges DI-02 by *mean* error, so a sensor with zero mean error but a large spread would pass. | Make the criterion: 95 % of pairs within ±1 °C / ±3 % RH. | Author | Open |
| F-07 | Minor | No hazard covers a pump pulse at power-up or reset. GPIO 2 and 12 are strapping pins and both drive pump switches. The series cutoff (RC-04) means both would have to glitch together, but this isn't recorded. | Add HAZ-11 "pump energised during boot/brown-out", controlled by RC-04 plus the gate pull-downs. Check during bench bring-up with a scope on both gates across 10 power cycles. | Author | Open |
| F-08 | Obs. | `00_design_plan.md` §1 cites multi-planter support as DI-21, but it is DI-25 (DI-21 is leaks). The plan also names SolidWorks while the CAD tool (Creo?) is still undecided. | Fix the reference; settle the CAD tool before phase 2. | Author | Open |
| F-09 | Obs. | The April-2026 docs carried over from the first concept (`docs/project_plan.md`, `test_plan.md`, `bill_of_materials.md`, `wiring_notes.md` …) overlap with or contradict the DHF. For example, `project_plan.md` puts ROS 2 in v1 scope. | Archive them or mark them superseded so the DHF is the only source of truth. | Author | Closed 2026-11-15: moved to `docs/archive/` with a superseded note; `architecture.md` kept (DO-15) and its merge conflict resolved |

## Disposition

Not passed. To close DR-0: complete the VoC interviews and update the UNs; resolve F-01 and F-02; fold F-03 to F-08 into Rev B of the affected documents; tag `dhf-revB`.
