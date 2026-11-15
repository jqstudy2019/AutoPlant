# 00 — Design and Development Plan

| Field | Value |
|---|---|
| Project | AutoPlant v1 — single-planter automated watering system |
| Owner | Project author (sole designer, builder, reviewer) |
| Revision | A (draft) |
| Date | 2026-10-18 |
| Model | ISO 13485:2016 cl. 7.3 design controls, applied voluntarily to a non-regulated hobby product |

## 1. Purpose and scope

Design, build, verify and validate one planter module (sensing, pumping, reservoir, edge node) plus a Raspberry Pi supervisor with a remote dashboard. Multi-planter support is an architectural requirement (DI-21) but only one module is built in v1.

Out of scope for v1: ROS 2 node graph, valve manifold, cloud hosting, light sensing, regulatory submission of any kind.

## 2. Design stages and reviews

| Stage | Weeks | Key outputs | Review / gate | Gate criteria |
|---|---|---|---|---|
| 1. Define | 1–2 | User needs, design inputs, hazard analysis, verification plan | DR-0 Design input review | Every DI is measurable, traces to ≥1 UN, has a verification method; hazards have initial risk estimates |
| 2. Design | 3–6 | SolidWorks assembly, GD&T drawings, tolerance stack-up, FEA, DFM review, schematic, BOM | DR-1 Design review | Every DI has a DO; risk controls implemented in design; drawings checked |
| 3. Build | 5–9 | Bench prototype, firmware, supervisor, dashboard | DR-2 Integration review | Closed-loop watering on bench; interlocks demonstrated |
| 4. Verify & validate | 10–13 | VER protocols + reports, calibration, 14-day validation run, updated risk file | DR-3 Final review | All VER pass or deviations dispositioned; residual risk acceptable; VAL-01 complete |
| 5. Package | 14 | README, photos, plots, portfolio entries | — | Links live |

Because there is only one engineer, each review is a self-review against a written checklist, recorded in `07_design_reviews/`. Where possible, one outside reviewer (friend or colleague) checks the drawings and the risk file.

## 3. Responsibilities

| Activity | Responsible |
|---|---|
| Design, build, test | Author |
| Independent drawing check | Outside reviewer (TBD) |
| Validation users | Author + household members |

## 4. Document control

- All DHF documents live in git; the commit hash is the revision record.
- Released revisions are tagged (`dhf-revA`, `dhf-revB` …).
- Changes after DR-1 are logged in `08_change_log.md` with reason, affected IDs, and impact on risk.

## 5. Risk management

Risk management follows ISO 14971:2019 concepts: hazard identification → risk estimation → risk control → residual risk evaluation. See `06_risk/`. Acceptability criteria are defined in `06_risk/risk_management_plan.md`.

## 6. Verification and validation strategy

- **Verification** (did we build it right?): one protocol per design input or small group of inputs, listed in `04_verification/verification_plan.md`. Automated software checks run through pytest; each test is tagged with its VER ID.
- **Validation** (did we build the right thing?): VAL-01, a 14-day in-home run with a real plant, judged against the user needs; VAL-02, structured feedback from household users.

## 7. Design transfer

Not applicable in the manufacturing sense. The equivalent is the release package: tagged repo, BOM, drawings, build instructions sufficient for someone else to build a second module.
