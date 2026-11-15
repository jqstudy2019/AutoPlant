"""Planter configuration (DO-14, satisfies DI-25).

Adding a planter = adding one entry to config/planters.json. No code change.
"""
from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

# Firmware enforces this independently (DI-08); the supervisor never asks for more.
MAX_PUMP_RUNTIME_S = 30.0


class ConfigError(ValueError):
    pass


@dataclass(frozen=True)
class PlanterConfig:
    id: int
    name: str
    node_host: str
    enabled: bool = True
    dry_threshold_pct: float = 35.0
    wet_threshold_pct: float = 42.0
    dose_ml: float = 50.0
    pump_flow_ml_per_s: float = 5.0  # from pump calibration, VER-05
    cooldown_h: float = 6.0
    max_cycles_per_24h: int = 2

    def __post_init__(self) -> None:
        if not 0 <= self.dry_threshold_pct < self.wet_threshold_pct <= 100:
            raise ConfigError(
                f"planter {self.id}: need 0 <= dry < wet <= 100 "
                f"(got dry={self.dry_threshold_pct}, wet={self.wet_threshold_pct})"
            )
        if self.dose_ml <= 0 or self.pump_flow_ml_per_s <= 0:
            raise ConfigError(f"planter {self.id}: dose and flow must be positive")
        if self.dose_ml / self.pump_flow_ml_per_s > MAX_PUMP_RUNTIME_S:
            raise ConfigError(
                f"planter {self.id}: dose needs "
                f"{self.dose_ml / self.pump_flow_ml_per_s:.1f} s, above the "
                f"{MAX_PUMP_RUNTIME_S:.0f} s pump limit"
            )
        if self.cooldown_h < 0 or self.max_cycles_per_24h < 1:
            raise ConfigError(f"planter {self.id}: bad cooldown or cycle limit")

    @property
    def pump_runtime_s(self) -> float:
        return self.dose_ml / self.pump_flow_ml_per_s


def load(path: str | Path) -> list[PlanterConfig]:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    planters = [PlanterConfig(**p) for p in data["planters"]]
    ids = [p.id for p in planters]
    if len(ids) != len(set(ids)):
        raise ConfigError(f"duplicate planter ids: {ids}")
    return planters
