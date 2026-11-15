"""CSV data logger (DO-10, satisfies DI-16).

Two files per planter: readings (every sample) and events (every decision that
waters, every fault change). Each event carries a reason code.
"""
from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path

from .controller import Decision, Reading

READING_FIELDS = ["iso_time", "t", "planter_id", "moisture_pct", "reservoir_low",
                  "temp_c", "rh_pct"]
EVENT_FIELDS = ["iso_time", "t", "planter_id", "action", "runtime_s", "reason", "faults"]


class DataLog:
    def __init__(self, root: str | Path):
        self.root = Path(root)
        self.root.mkdir(parents=True, exist_ok=True)

    def _append(self, name: str, fields: list[str], row: dict) -> None:
        path = self.root / name
        new = not path.exists()
        with path.open("a", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=fields)
            if new:
                w.writeheader()
            w.writerow(row)

    @staticmethod
    def _iso(t: float) -> str:
        return datetime.fromtimestamp(t, tz=timezone.utc).isoformat(timespec="seconds")

    def reading(self, planter_id: int, r: Reading, temp_c: float | None = None,
                rh_pct: float | None = None) -> None:
        self._append(f"readings_p{planter_id}.csv", READING_FIELDS, {
            "iso_time": self._iso(r.t), "t": r.t, "planter_id": planter_id,
            "moisture_pct": "" if r.moisture_pct is None else round(r.moisture_pct, 2),
            "reservoir_low": int(r.reservoir_low),
            "temp_c": "" if temp_c is None else temp_c,
            "rh_pct": "" if rh_pct is None else rh_pct,
        })

    def event(self, planter_id: int, t: float, d: Decision) -> None:
        self._append(f"events_p{planter_id}.csv", EVENT_FIELDS, {
            "iso_time": self._iso(t), "t": t, "planter_id": planter_id,
            "action": d.action.value, "runtime_s": round(d.runtime_s, 2),
            "reason": d.reason, "faults": ";".join(sorted(f.value for f in d.faults)),
        })
