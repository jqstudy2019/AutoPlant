# Risk Management Plan

Rev A (draft) · 2026-10-18 · Concepts from ISO 14971:2019, applied to a non-regulated product.

## Scope

Harm to people, property and the plant from AutoPlant v1 over its intended use: indoor, one planter, unattended up to 14 days, household members present.

## Severity scale

| S | Name | Example |
|---|---|---|
| 5 | Catastrophic | Fire; injury needing medical care |
| 4 | Critical | Water damage to floor or furniture (> 1 L released) |
| 3 | Serious | Plant death; minor water release (< 1 L) contained by tray |
| 2 | Minor | Plant stress; device damaged (e.g. pump burnt out) |
| 1 | Negligible | Nuisance alert, missing data |

## Probability scale (per 14-day deployment)

| P | Name | Guide |
|---|---|---|
| 5 | Frequent | Expected most deployments |
| 4 | Probable | Likely within a few deployments |
| 3 | Occasional | Could happen within a year of use |
| 2 | Remote | Unlikely but conceivable |
| 1 | Improbable | Requires multiple independent failures |

## Acceptability matrix

| S \ P | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|
| **5** | ALARP | Unacc. | Unacc. | Unacc. | Unacc. |
| **4** | Acc. | ALARP | Unacc. | Unacc. | Unacc. |
| **3** | Acc. | Acc. | ALARP | Unacc. | Unacc. |
| **2** | Acc. | Acc. | Acc. | ALARP | ALARP |
| **1** | Acc. | Acc. | Acc. | Acc. | Acc. |

**Unacceptable** risks must be reduced by risk controls before DR-1. **ALARP** risks need controls where practicable and a written rationale. Order of control preference: (1) inherent safety by design, (2) protective measures, (3) information/alerts.

## dFMEA scoring

`dfmea.csv` uses the conventional 1–10 severity, occurrence and detection scales. Its RPN only ranks design actions; acceptability is always judged in the hazard analysis using the 1–5 scales above.

## Activities

| Activity | Output | When |
|---|---|---|
| Hazard analysis | `hazard_analysis.md` | Phase 1 |
| Design FMEA | `dfmea.csv` | Phase 1, updated phase 2 and 4 |
| Risk control verification | VER reports linked from RC rows | Phase 4 |
| Residual risk and overall evaluation | Section in DR-3 record | Phase 4 |
| Field observations | Change log entries from VAL-01 and later use | Ongoing |
