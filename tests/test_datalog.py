import csv

import pytest

from autoplant.controller import Action, Decision, Fault, Reading
from autoplant.datalog import DataLog


@pytest.mark.ver("VER-10")
def test_every_event_has_reason_code(tmp_path):
    log = DataLog(tmp_path)
    log.reading(1, Reading(0, 30.123))
    log.event(1, 0, Decision(Action.WATER, "moisture below dry threshold", 10.0,
                             frozenset({Fault.RESERVOIR_LOW})))
    rows = list(csv.DictReader((tmp_path / "events_p1.csv").open()))
    assert rows[0]["reason"] == "moisture below dry threshold"
    assert rows[0]["faults"] == "reservoir_low"
    readings = list(csv.DictReader((tmp_path / "readings_p1.csv").open()))
    assert readings[0]["moisture_pct"] == "30.12"
