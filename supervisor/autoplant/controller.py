"""Watering decision logic (DO-04, DO-05).

Pure logic with no I/O and no clock: every call receives a timestamped
reading, so the whole behaviour is testable with simulated time.

Requirements implemented here:
  DI-04  hysteresis watering episodes (dry / wet thresholds)
  DI-05  dose -> pump runtime from calibrated flow
  DI-06  max automatic cycles per rolling 24 h
  DI-07  minimum cooldown between automatic cycles
  DI-09  no watering while reservoir is low (firmware also enforces this)
  DI-10  sensor-invalid and implausible-jump faults inhibit auto watering
  DI-13  "no moisture response" fault after 3 ineffective cycles
"""
from __future__ import annotations

from collections import deque
from dataclasses import dataclass, field
from enum import Enum

from .config import MAX_PUMP_RUNTIME_S, PlanterConfig

DAY_S = 24 * 3600
IMPLAUSIBLE_RATE_PCT_PER_MIN = 20.0  # DI-10
WATERING_EXEMPT_WINDOW_S = 15 * 60    # a fast rise this soon after watering is expected
RESPONSE_WINDOW_S = 10 * 60           # wait this long after a cycle before judging response
MIN_RESPONSE_RISE_PCT = 3.0           # DI-13
NO_RESPONSE_LIMIT = 3                 # DI-13


class Action(str, Enum):
    NONE = "none"
    WATER = "water"


class Fault(str, Enum):
    SENSOR_INVALID = "sensor_invalid"      # clears when valid data returns
    IMPLAUSIBLE_JUMP = "implausible_jump"  # latched until acknowledged
    NO_RESPONSE = "no_response"            # latched until acknowledged
    RESERVOIR_LOW = "reservoir_low"        # clears when reservoir refilled


LATCHED = {Fault.IMPLAUSIBLE_JUMP, Fault.NO_RESPONSE}


@dataclass(frozen=True)
class Reading:
    t: float                      # seconds (any epoch, monotonic)
    moisture_pct: float | None    # None = sensor read failed
    reservoir_low: bool = False


@dataclass(frozen=True)
class Decision:
    action: Action
    reason: str
    runtime_s: float = 0.0
    faults: frozenset[Fault] = frozenset()


@dataclass
class PlanterController:
    cfg: PlanterConfig
    in_episode: bool = False
    faults: set[Fault] = field(default_factory=set)
    _auto_cycles: deque = field(default_factory=deque)  # times of automatic cycles
    _last_water_t: float | None = None                   # any cycle, auto or manual
    _prev: tuple[float, float] | None = None             # (t, moisture) of last valid reading
    _pending_response: tuple[float, float] | None = None # (cycle t, moisture before cycle)
    _no_response_count: int = 0

    # ------------------------------------------------------------------ public
    def step(self, r: Reading) -> Decision:
        """Evaluate one reading and decide whether to water automatically."""
        self._update_reservoir(r)
        m = self._validate(r)
        if m is not None:
            self._check_rate(r.t, m)
            self._check_response(r.t, m)
            self._update_episode(m)
            self._prev = (r.t, m)

        if not self.cfg.enabled:
            return self._none("planter disabled")
        if self.faults:
            return self._none("inhibited by fault: " + ", ".join(sorted(f.value for f in self.faults)))
        if not self.in_episode:
            return self._none("moisture ok")

        self._expire_cycles(r.t)
        if len(self._auto_cycles) >= self.cfg.max_cycles_per_24h:
            return self._none("daily cycle limit reached")
        if self._auto_cycles and r.t - self._auto_cycles[-1] < self.cfg.cooldown_h * 3600:
            return self._none("cooldown active")

        self._auto_cycles.append(r.t)
        return self._water(r.t, m, "moisture below dry threshold" if m < self.cfg.dry_threshold_pct
                           else "continuing episode below wet threshold")

    def manual(self, r: Reading) -> Decision:
        """Manual water request (DI-17). Bounded by reservoir and runtime limits,
        not counted against the automatic cycle limit."""
        self._update_reservoir(r)
        if Fault.RESERVOIR_LOW in self.faults:
            return self._none("manual refused: reservoir low")
        m = r.moisture_pct if r.moisture_pct is not None and 0 <= r.moisture_pct <= 100 else None
        return self._water(r.t, m, "manual request", track_response=False)

    def acknowledge(self) -> None:
        """User acknowledges latched faults after fixing the cause."""
        self.faults -= LATCHED
        self._no_response_count = 0
        self._pending_response = None

    # ----------------------------------------------------------------- helpers
    def _water(self, t: float, m: float | None, reason: str, track_response: bool = True) -> Decision:
        runtime = min(self.cfg.pump_runtime_s, MAX_PUMP_RUNTIME_S)
        self._last_water_t = t
        if track_response and m is not None:
            self._pending_response = (t, m)
        return Decision(Action.WATER, reason, runtime, frozenset(self.faults))

    def _none(self, reason: str) -> Decision:
        return Decision(Action.NONE, reason, 0.0, frozenset(self.faults))

    def _update_reservoir(self, r: Reading) -> None:
        if r.reservoir_low:
            self.faults.add(Fault.RESERVOIR_LOW)
        else:
            self.faults.discard(Fault.RESERVOIR_LOW)

    def _validate(self, r: Reading) -> float | None:
        m = r.moisture_pct
        if m is None or not 0.0 <= m <= 100.0:
            self.faults.add(Fault.SENSOR_INVALID)
            return None
        self.faults.discard(Fault.SENSOR_INVALID)
        return m

    def _check_rate(self, t: float, m: float) -> None:
        if self._prev is None:
            return
        t0, m0 = self._prev
        dt_min = (t - t0) / 60.0
        if dt_min <= 0:
            return
        recently_watered = self._last_water_t is not None and t - self._last_water_t <= WATERING_EXEMPT_WINDOW_S
        if abs(m - m0) / dt_min > IMPLAUSIBLE_RATE_PCT_PER_MIN and not recently_watered:
            self.faults.add(Fault.IMPLAUSIBLE_JUMP)

    def _check_response(self, t: float, m: float) -> None:
        if self._pending_response is None:
            return
        t_cycle, m_before = self._pending_response
        if t - t_cycle < RESPONSE_WINDOW_S:
            return
        self._pending_response = None
        if m - m_before < MIN_RESPONSE_RISE_PCT:
            self._no_response_count += 1
            if self._no_response_count >= NO_RESPONSE_LIMIT:
                self.faults.add(Fault.NO_RESPONSE)
        else:
            self._no_response_count = 0

    def _update_episode(self, m: float) -> None:
        if m < self.cfg.dry_threshold_pct:
            self.in_episode = True
        elif m > self.cfg.wet_threshold_pct:
            self.in_episode = False

    def _expire_cycles(self, t: float) -> None:
        while self._auto_cycles and t - self._auto_cycles[0] >= DAY_S:
            self._auto_cycles.popleft()
