"""Automated verification of supervisor control logic.

Each test is marked with the VER protocol it supports; `pytest -m ver -v`
output is attached to the VER-04 / VER-07 reports as objective evidence.
"""
import json

import pytest

from autoplant.config import ConfigError, PlanterConfig, load
from autoplant.controller import (
    Action, Fault, PlanterController, Reading, DAY_S, RESPONSE_WINDOW_S,
)

H = 3600.0


def cfg(**kw):
    base = dict(id=1, name="P1", node_host="n1", dry_threshold_pct=35, wet_threshold_pct=42,
                dose_ml=50, pump_flow_ml_per_s=5, cooldown_h=6, max_cycles_per_24h=2)
    base.update(kw)
    return PlanterConfig(**base)


def ctl(**kw):
    return PlanterController(cfg(**kw))


# ---------------------------------------------------------------- DI-04 hysteresis
@pytest.mark.ver("VER-04")
def test_no_watering_above_dry_threshold():
    c = ctl()
    assert c.step(Reading(0, 50)).action is Action.NONE
    assert c.step(Reading(60, 36)).action is Action.NONE


@pytest.mark.ver("VER-04")
def test_waters_below_dry_threshold_with_calibrated_runtime():
    d = ctl().step(Reading(0, 30))
    assert d.action is Action.WATER
    assert d.runtime_s == pytest.approx(10.0)  # DI-05: 50 mL / 5 mL/s


@pytest.mark.ver("VER-04")
def test_episode_continues_between_thresholds_after_cooldown():
    c = ctl()
    assert c.step(Reading(0, 30)).action is Action.WATER
    # dose lifted moisture to 38 %: between thresholds, episode still open
    assert c.step(Reading(1 * H, 38)).action is Action.NONE  # cooldown
    assert c.step(Reading(6 * H, 38)).action is Action.WATER  # cooldown over, still < wet


@pytest.mark.ver("VER-04")
def test_no_new_episode_between_thresholds():
    c = ctl()
    c.step(Reading(0, 50))
    assert c.step(Reading(60, 38)).action is Action.NONE  # fell into band from above


@pytest.mark.ver("VER-04")
def test_episode_ends_above_wet_threshold():
    c = ctl()
    c.step(Reading(0, 30))
    c.step(Reading(600, 45))
    assert not c.in_episode
    assert c.step(Reading(7 * H, 38)).action is Action.NONE


# ------------------------------------------------------- DI-06 / DI-07 limits
@pytest.mark.ver("VER-04")
def test_cooldown_blocks_repeat_watering():
    c = ctl()
    c.step(Reading(0, 30))
    d = c.step(Reading(5.9 * H, 30))
    assert d.action is Action.NONE and d.reason == "cooldown active"


@pytest.mark.ver("VER-04")
def test_daily_cycle_limit_on_rolling_window():
    c = ctl(cooldown_h=1, max_cycles_per_24h=2)
    # keep moisture rising enough that no-response logic stays quiet
    assert c.step(Reading(0, 20)).action is Action.WATER
    assert c.step(Reading(1 * H, 24)).action is Action.WATER
    d = c.step(Reading(2 * H, 28))
    assert d.action is Action.NONE and d.reason == "daily cycle limit reached"
    assert c.step(Reading(DAY_S + 1, 30)).action is Action.WATER  # first cycle expired


# ------------------------------------------------------------- DI-09 reservoir
@pytest.mark.ver("VER-04")
def test_reservoir_low_blocks_auto_and_manual():
    c = ctl()
    d = c.step(Reading(0, 20, reservoir_low=True))
    assert d.action is Action.NONE and Fault.RESERVOIR_LOW in d.faults
    assert c.manual(Reading(10, 20, reservoir_low=True)).action is Action.NONE
    assert c.step(Reading(20, 20)).action is Action.WATER  # refilled


# ----------------------------------------------------------- DI-10 plausibility
@pytest.mark.ver("VER-07")
@pytest.mark.parametrize("bad", [None, -5.0, 120.0])
def test_invalid_reading_inhibits_and_clears(bad):
    c = ctl()
    d = c.step(Reading(0, bad))
    assert d.action is Action.NONE and Fault.SENSOR_INVALID in d.faults
    assert c.step(Reading(60, 30)).action is Action.WATER


@pytest.mark.ver("VER-07")
def test_implausible_drop_latches_until_acknowledged():
    c = ctl()
    c.step(Reading(0, 60))
    d = c.step(Reading(60, 20))  # 40 %/min drop, no watering: probe pulled out?
    assert d.action is Action.NONE and Fault.IMPLAUSIBLE_JUMP in d.faults
    assert c.step(Reading(120, 20)).action is Action.NONE  # still latched
    c.acknowledge()
    assert c.step(Reading(180, 20)).action is Action.WATER


@pytest.mark.ver("VER-07")
def test_fast_rise_right_after_watering_is_not_a_fault():
    c = ctl()
    c.step(Reading(0, 30))
    d = c.step(Reading(60, 55))
    assert Fault.IMPLAUSIBLE_JUMP not in d.faults


# ---------------------------------------------------------- DI-13 no response
@pytest.mark.ver("VER-07")
def test_three_ineffective_cycles_raise_no_response():
    c = ctl(cooldown_h=1, max_cycles_per_24h=10)
    t = 0.0
    for _ in range(3):
        assert c.step(Reading(t, 30)).action is Action.WATER
        c.step(Reading(t + RESPONSE_WINDOW_S, 30.5))  # < 3 % rise
        t += 1 * H
    d = c.step(Reading(t, 30))
    assert d.action is Action.NONE and Fault.NO_RESPONSE in d.faults


@pytest.mark.ver("VER-07")
def test_effective_cycle_resets_no_response_count():
    c = ctl(cooldown_h=1, max_cycles_per_24h=10)
    c.step(Reading(0, 30)); c.step(Reading(RESPONSE_WINDOW_S, 30.5))
    c.step(Reading(1 * H, 30)); c.step(Reading(1 * H + RESPONSE_WINDOW_S, 34))  # good
    assert c._no_response_count == 0


# ------------------------------------------------------- DI-08 / DI-17 manual
@pytest.mark.ver("VER-04")
def test_manual_request_is_runtime_bounded_and_not_counted():
    c = ctl(max_cycles_per_24h=1)
    d = c.manual(Reading(0, 60))
    assert d.action is Action.WATER and d.runtime_s <= 30
    assert c.step(Reading(60, 30)).action is Action.WATER  # auto quota untouched


# ------------------------------------------------------------- config / DI-25
@pytest.mark.ver("VER-04")
@pytest.mark.parametrize("kw", [
    dict(dry_threshold_pct=45, wet_threshold_pct=40),  # inverted thresholds
    dict(dose_ml=500, pump_flow_ml_per_s=5),            # needs 100 s > 30 s limit
    dict(max_cycles_per_24h=0),
])
def test_bad_config_rejected(kw):
    with pytest.raises(ConfigError):
        cfg(**kw)


@pytest.mark.ver("VER-15")
def test_second_planter_needs_config_only(tmp_path):
    p = tmp_path / "planters.json"
    p.write_text(json.dumps({"planters": [
        dict(id=1, name="A", node_host="n1"), dict(id=2, name="B", node_host="n2")]}))
    planters = load(p)
    controllers = {c.id: PlanterController(c) for c in planters}
    assert controllers[2].step(Reading(0, 20)).action is Action.WATER
    assert controllers[1].step(Reading(0, 60)).action is Action.NONE
