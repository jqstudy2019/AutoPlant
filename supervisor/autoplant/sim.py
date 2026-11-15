"""Run the controller against a simulated planter for a few days.

    python -m autoplant.sim [--days 5] [--log-dir data/sim]

The plant model is deliberately simple: moisture decays exponentially toward a
dry floor, each watering adds dose_ml * gain, and the reservoir drains by the
dose. Useful for sanity-checking thresholds before hardware exists.
"""
from __future__ import annotations

import argparse
import math
from pathlib import Path

from . import config
from .controller import Action, PlanterController, Reading
from .datalog import DataLog

SAMPLE_S = 5 * 60


def run(days: float, log_dir: Path, cfg_path: Path) -> None:
    cfg = config.load(cfg_path)[0]
    ctl = PlanterController(cfg)
    log = DataLog(log_dir)

    moisture, reservoir_ml = 45.0, 1800.0
    decay_per_day, floor, gain_pct_per_ml = 0.35, 10.0, 0.18
    reservoir_low_ml = 300.0
    waterings = 0
    t = 0.0
    while t < days * 86400:
        moisture = floor + (moisture - floor) * math.exp(-decay_per_day * SAMPLE_S / 86400)
        r = Reading(t=t, moisture_pct=moisture, reservoir_low=reservoir_ml < reservoir_low_ml)
        d = ctl.step(r)
        log.reading(cfg.id, r)
        if d.action is Action.WATER:
            delivered = d.runtime_s * cfg.pump_flow_ml_per_s
            reservoir_ml -= delivered
            moisture = min(100.0, moisture + delivered * gain_pct_per_ml)
            waterings += 1
            log.event(cfg.id, t, d)
        t += SAMPLE_S

    print(f"Simulated {days:g} days: {waterings} waterings, "
          f"final moisture {moisture:.1f} %, reservoir {reservoir_ml:.0f} mL, "
          f"faults: {sorted(f.value for f in ctl.faults) or 'none'}")
    print(f"Logs in {log_dir}")


def main() -> None:
    here = Path(__file__).resolve().parent.parent
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--days", type=float, default=5)
    p.add_argument("--log-dir", type=Path, default=here / "data" / "sim")
    p.add_argument("--config", type=Path, default=here / "config" / "planters.json")
    a = p.parse_args()
    run(a.days, a.log_dir, a.config)


if __name__ == "__main__":
    main()
