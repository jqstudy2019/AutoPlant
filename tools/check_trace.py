"""Build and check the AutoPlant traceability matrix.

Reads the markdown tables in docs/dhf/, writes docs/dhf/traceability_matrix.csv,
and exits non-zero if any link is broken:
  - every DI traces to at least one existing UN
  - every UN is covered by at least one DI
  - every DI has a VER that exists in the verification plan
  - every DI is satisfied by at least one DO
  - every RC points at existing DIs, and every HAZ has at least one RC

Usage:  python tools/check_trace.py
"""
from __future__ import annotations

import csv
import re
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DHF = ROOT / "docs" / "dhf"
ID = re.compile(r"\b(UN|DI|DO|VER|VAL|HAZ|RC)-\d{2}\b")


def table_rows(path: Path) -> list[list[str]]:
    """Return data rows (cells stripped) of every markdown table in a file."""
    rows = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line.startswith("|") or set(line) <= set("|-: "):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if ID.fullmatch(cells[0] or ""):
            rows.append(cells)
    return rows


def ids_in(text: str, prefix: str) -> list[str]:
    return [m.group(0) for m in ID.finditer(text) if m.group(1) == prefix]


def main() -> int:
    errors: list[str] = []

    un = {r[0] for r in table_rows(DHF / "01_user_needs.md")}

    di = {}  # DI -> (requirement, UNs, VERs)
    for r in table_rows(DHF / "02_design_inputs.md"):
        di[r[0]] = (r[1], ids_in(r[2], "UN"), ids_in(r[4], "VER"))

    do_for = defaultdict(list)
    for r in table_rows(DHF / "03_design_outputs.md"):
        for d in ids_in(r[2], "DI"):
            do_for[d].append(r[0])

    ver = {}
    for r in table_rows(DHF / "04_verification" / "verification_plan.md"):
        if r[0].startswith("VER"):
            ver[r[0]] = ids_in(r[2], "DI")

    hazards = {}
    rc_to_di = {}
    for r in table_rows(DHF / "06_risk" / "hazard_analysis.md"):
        if r[0].startswith("HAZ"):
            hazards[r[0]] = ids_in(r[6], "RC")
        elif r[0].startswith("RC") and len(r) >= 5:  # skip "risks introduced" table
            rc_to_di[r[0]] = ids_in(r[3], "DI")

    # --- checks
    for d, (_, uns, vers) in di.items():
        if not uns:
            errors.append(f"{d}: no user need")
        for u in uns:
            if u not in un:
                errors.append(f"{d}: traces to unknown {u}")
        if not vers:
            errors.append(f"{d}: no verification")
        for v in vers:
            if v not in ver:
                errors.append(f"{d}: unknown {v}")
            elif d not in ver[v]:
                errors.append(f"{d}: {v} does not list {d} back")
        if not do_for.get(d):
            errors.append(f"{d}: no design output")
    covered = {u for _, uns, _ in di.values() for u in uns}
    for u in sorted(un - covered):
        errors.append(f"{u}: not covered by any design input")
    for h, rcs in hazards.items():
        if not rcs:
            errors.append(f"{h}: no risk control")
        for rc in rcs:
            if rc not in rc_to_di:
                errors.append(f"{h}: unknown {rc}")
    for rc, dis in rc_to_di.items():
        for d in dis:
            if d not in di:
                errors.append(f"{rc}: unknown {d}")

    # --- matrix
    di_to_rc = defaultdict(list)
    for rc, dis in rc_to_di.items():
        for d in dis:
            di_to_rc[d].append(rc)
    rc_to_haz = defaultdict(list)
    for h, rcs in hazards.items():
        for rc in rcs:
            rc_to_haz[rc].append(h)

    out = DHF / "traceability_matrix.csv"
    with out.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["DI", "Requirement", "User needs", "Design outputs",
                    "Verification", "Risk controls", "Hazards"])
        for d in sorted(di, key=lambda s: int(s[3:])):
            req, uns, vers = di[d]
            rcs = sorted(di_to_rc.get(d, []))
            hz = sorted({h for rc in rcs for h in rc_to_haz.get(rc, [])})
            w.writerow([d, req, "; ".join(uns), "; ".join(do_for.get(d, [])),
                        "; ".join(vers), "; ".join(rcs), "; ".join(hz)])

    print(f"{len(un)} user needs, {len(di)} design inputs, {len(ver)} VER protocols, "
          f"{len(hazards)} hazards, {len(rc_to_di)} risk controls")
    print(f"Wrote {out.relative_to(ROOT)}")
    if errors:
        print(f"\n{len(errors)} traceability problem(s):")
        for e in errors:
            print("  -", e)
        return 1
    print("Traceability complete: no broken links.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
