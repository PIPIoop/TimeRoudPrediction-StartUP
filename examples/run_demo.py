"""Запуск открытой части showcase без прогнозирующего ядра."""

from __future__ import annotations

from pprint import pprint
import sys

from data_quality import inspect_daily_series
from synthetic_series import make_demo_series


def main() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    frame = make_demo_series(days=120, seed=42)
    report = inspect_daily_series(frame)

    print("Первые строки синтетического набора:")
    print(frame.head().to_string(index=False))
    print("\nПроверка качества:")
    pprint(report.to_dict(), sort_dicts=False)
    print("\nПрогнозирующее ядро в showcase-репозиторий не включено.")


if __name__ == "__main__":
    main()

