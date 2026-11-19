
"""Pressure-driven leakage calculations."""

import math


def calculate_leakage(
    pressure: float,
    coefficient: float,
    exponent: float,
) -> float:
    """Calculate leakage using Q = C * p**N1."""

    values = {
        "pressure": pressure,
        "coefficient": coefficient,
        "exponent": exponent,
    }

    for name, value in values.items():
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise TypeError(f"{name} must be a number.")
        if not math.isfinite(value):
            raise ValueError(f"{name} must be finite.")

    if pressure < 0:
        raise ValueError("Pressure cannot be negative.")

    if coefficient < 0:
        raise ValueError("Coefficient cannot be negative.")

    if exponent <= 0:
        raise ValueError("Exponent must be greater than zero.")

    return coefficient * pressure**exponent
