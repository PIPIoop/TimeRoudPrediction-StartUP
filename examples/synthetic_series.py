"""Создание безопасного демонстрационного временного ряда.

Модуль не содержит рабочих данных или кода прогнозирующих моделей.
"""

from __future__ import annotations

import numpy as np
import pandas as pd


def make_demo_series(days: int = 120, seed: int = 42) -> pd.DataFrame:
    """Возвращает дневной ряд с трендом, недельностью и небольшим шумом."""
    if days < 14:
        raise ValueError("Для демонстрации требуется не менее 14 дней")

    rng = np.random.default_rng(seed)
    dates = pd.date_range("2025-01-01", periods=days, freq="D")
    index = np.arange(days, dtype=float)

    trend = 100.0 + index * 0.35
    weekly = 8.0 * np.sin(2.0 * np.pi * index / 7.0)
    noise = rng.normal(0.0, 2.0, size=days)

    return pd.DataFrame(
        {
            "date": dates,
            "series_id": "demo-series",
            "value": np.round(trend + weekly + noise, 2),
        }
    )


if __name__ == "__main__":
    print(make_demo_series().head())

