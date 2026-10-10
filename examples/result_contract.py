"""Публичный формат результата без реализации прогнозирующего ядра."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import date


@dataclass(frozen=True)
class ForecastPoint:
    timestamp: date
    value: float
    lower: float | None = None
    upper: float | None = None


@dataclass(frozen=True)
class ForecastResult:
    series_id: str
    created_at: str
    horizon: int
    points: tuple[ForecastPoint, ...]
    diagnostics: dict[str, float | int | str] = field(default_factory=dict)

    def to_dict(self) -> dict[str, object]:
        payload = asdict(self)
        for point in payload["points"]:
            point["timestamp"] = point["timestamp"].isoformat()
        return payload

