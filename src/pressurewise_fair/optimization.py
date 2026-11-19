"""Evaluation and Pareto filtering for candidate PRV schedules.

The evaluator is injected: callers supply a hydraulic simulation function
that applies a schedule and returns validated metrics. This module does not
claim to implement time-varying PRV controls itself.
"""
from collections.abc import Callable, Iterable, Mapping
import math


def _finite_number(name: str, value: float) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise TypeError(f"{name} must be numeric.")
    if not math.isfinite(value):
        raise ValueError(f"{name} must be finite.")
    return float(value)


def evaluate_schedules(
    schedules: Iterable[tuple[float, ...]],
    evaluator: Callable[[tuple[float, ...]], Mapping[str, float]],
) -> list[dict[str, object]]:
    """Evaluate schedules with a caller-supplied hydraulic evaluator."""
    if not callable(evaluator):
        raise TypeError("evaluator must be callable.")

    records = []
    for schedule in schedules:
        normalized = tuple(
            _finite_number("schedule setting", setting)
            for setting in schedule
        )
        metrics = evaluator(normalized)
        if not isinstance(metrics, Mapping):
            raise TypeError("evaluator must return a mapping.")
        if "leakage" not in metrics or "equity" not in metrics:
            raise ValueError("evaluator must return leakage and equity.")

        record = {
            "schedule": normalized,
            "leakage": _finite_number("leakage", metrics["leakage"]),
            "equity": _finite_number("equity", metrics["equity"]),
        }
        if record["leakage"] < 0:
            raise ValueError("leakage cannot be negative.")
        if "minimum_pressure" in metrics:
            record["minimum_pressure"] = _finite_number(
                "minimum_pressure", metrics["minimum_pressure"]
            )
        if "feasible" in metrics:
            if not isinstance(metrics["feasible"], bool):
                raise TypeError("feasible must be a boolean.")
            record["feasible"] = metrics["feasible"]
        records.append(record)
    return records


def pareto_front(
    results: Iterable[Mapping[str, object]],
) -> list[Mapping[str, object]]:
    """Return non-dominated results: minimize leakage, maximize equity."""
    candidates = []
    for result in results:
        leakage = _finite_number("leakage", result["leakage"])
        equity = _finite_number("equity", result["equity"])
        if leakage < 0:
            raise ValueError("leakage cannot be negative.")
        feasible = result.get("feasible", True)
        if not isinstance(feasible, bool):
            raise TypeError("feasible must be a boolean.")
        if feasible:
            candidates.append((result, leakage, equity))

    front = []
    for candidate, leakage, equity in candidates:
        dominated = any(
            other_leakage <= leakage
            and other_equity >= equity
            and (other_leakage < leakage or other_equity > equity)
            for other, other_leakage, other_equity in candidates
            if other is not candidate
        )
        if not dominated:
            front.append(candidate)

    return sorted(
        (item[0] for item in front),
        key=lambda item: (
            float(item["leakage"]),
            -float(item["equity"]),
        ),
    )
