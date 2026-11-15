"""Flask dashboard skeleton (DO-09).

Phase 3 work: wire to live node telemetry, add login (DI-26), camera image
(DI-18), 7-day trend (DI-14) and push alerts (DI-15). For now it renders the
latest logged reading per planter so the page can be tried on the Pi.

    pip install -e ".[dashboard]"
    python -m autoplant.dashboard     # binds to 127.0.0.1; expose via `tailscale serve`
"""
from __future__ import annotations

import csv
import time
from pathlib import Path

from flask import Flask, render_template_string

from . import config

HERE = Path(__file__).resolve().parent.parent
DATA = HERE / "data" / "sim"
STALE_S = 10 * 60  # DI-14

PAGE = """<!doctype html><meta name=viewport content="width=device-width,initial-scale=1">
<title>AutoPlant</title>
<style>body{font-family:system-ui;margin:16px;max-width:640px}
.card{border:1px solid #ccc;border-radius:8px;padding:12px;margin:12px 0}
.stale{color:#b00}</style>
<h1>AutoPlant</h1>
{% for p in planters %}<div class=card><h2>{{p.name}}</h2>
{% if p.row %}<p>Moisture: <b>{{p.row.moisture_pct}} %</b>
 {% if p.stale %}<span class=stale>(stale)</span>{% endif %}</p>
<p>Reservoir: {{ 'LOW — refill' if p.row.reservoir_low == '1' else 'OK' }}</p>
<p>Updated: {{p.row.iso_time}}</p>{% else %}<p>No data yet.</p>{% endif %}
</div>{% endfor %}"""

app = Flask(__name__)


def latest(planter_id: int) -> dict | None:
    path = DATA / f"readings_p{planter_id}.csv"
    if not path.exists():
        return None
    with path.open(encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    return rows[-1] if rows else None


@app.route("/")
def index():
    out = []
    for cfg in config.load(HERE / "config" / "planters.json"):
        row = latest(cfg.id)
        stale = row is None or time.time() - float(row["t"]) > STALE_S
        out.append({"name": cfg.name, "row": row, "stale": stale})
    return render_template_string(PAGE, planters=out)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)
