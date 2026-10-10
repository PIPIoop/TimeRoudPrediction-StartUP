"""Небольшой публичный пример проверки временного ряда."""

from __future__ import annotations

from dataclasses import asdict, dataclass

import pandas as pd


@dataclass(frozen=True)
class DataQualityReport:
    rows: int
    start: str
    end: str
    duplicate_dates: int
    missing_values: int
    missing_days: int
    is_daily_grid: bool

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


def inspect_daily_series(
    frame: pd.DataFrame,
    *,
    date_column: str = "date",
    value_column: str = "value",
) -> DataQualityReport:
    """Проверяет минимальный контракт дневного временного ряда."""
    required = {date_column, value_column}
    missing_columns = required.difference(frame.columns)
    if missing_columns:
        names = ", ".join(sorted(missing_columns))
        raise ValueError(f"Отсутствуют обязательные колонки: {names}")

    prepared = frame[[date_column, value_column]].copy()
    prepared[date_column] = pd.to_datetime(prepared[date_column], errors="coerce")
    prepared[value_column] = pd.to_numeric(prepared[value_column], errors="coerce")

    invalid_dates = int(prepared[date_column].isna().sum())
    if invalid_dates:
        raise ValueError(f"Некорректных дат: {invalid_dates}")

    prepared = prepared.sort_values(date_column)
    duplicate_dates = int(prepared[date_column].duplicated().sum())
    missing_values = int(prepared[value_column].isna().sum())

    unique_dates = pd.DatetimeIndex(prepared[date_column].drop_duplicates())
    expected = pd.date_range(unique_dates.min(), unique_dates.max(), freq="D")
    missing_days = int(len(expected.difference(unique_dates)))

    return DataQualityReport(
        rows=len(prepared),
        start=unique_dates.min().date().isoformat(),
        end=unique_dates.max().date().isoformat(),
        duplicate_dates=duplicate_dates,
        missing_values=missing_values,
        missing_days=missing_days,
        is_daily_grid=duplicate_dates == 0 and missing_days == 0,
    )

