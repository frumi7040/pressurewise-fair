
"""Service-level and equity metrics."""

import math
from typing import Sequence


def calculate_dsr(
    delivered_demand: float,
    requested_demand: float,
) -> float:
    """Calculate the demand satisfaction ratio for one junction.

    DSR = delivered demand / requested demand.

    Values above 1.0 are retained rather than silently capped.
    """
    for name, value in (
        ("delivered_demand", delivered_demand),
        ("requested_demand", requested_demand),
    ):
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise TypeError(f"{name} must be a number.")
        if not math.isfinite(value):
            raise ValueError(f"{name} must be finite.")
        if value < 0:
            raise ValueError(f"{name} cannot be negative.")

    if requested_demand == 0:
        raise ValueError("Requested demand must be greater than zero.")

    return delivered_demand / requested_demand


def calculate_percentile(
    values: Sequence[float],
    percentile: float,
) -> float:
    """Calculate a percentile using linear interpolation.

    This implementation uses the inclusive method:
    position = (n - 1) * percentile / 100.
    """
    if not values:
        raise ValueError("At least one value is required.")

    if isinstance(percentile, bool) or not isinstance(percentile, (int, float)):
        raise TypeError("percentile must be a number.")

    if not math.isfinite(percentile) or not 0 <= percentile <= 100:
        raise ValueError("percentile must be between 0 and 100.")

    numbers = []
    for value in values:
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise TypeError("All values must be numbers.")
        if not math.isfinite(value):
            raise ValueError("All values must be finite.")
        numbers.append(float(value))

    numbers.sort()

    position = (len(numbers) - 1) * percentile / 100
    lower_index = math.floor(position)
    upper_index = math.ceil(position)

    if lower_index == upper_index:
        return numbers[lower_index]

    fraction = position - lower_index
    return (
        numbers[lower_index] * (1 - fraction)
        + numbers[upper_index] * fraction
    )


def calculate_equity_indicator(dsr_values: Sequence[float]) -> float:
    """Return the 10th-percentile DSR across eligible junctions."""
    return calculate_percentile(dsr_values, 10)
