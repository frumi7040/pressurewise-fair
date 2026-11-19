"""Pressure-driven leakage calculations."""

import math


def calculate_leakage(
    pressure: float,
    coefficient: float,
    exponent: float,
) -> float:
    """Calculate leakage using Q = C * p**N1.

    All inputs must use a consistent unit system.
    The returned flow rate uses the units implied by C.
    """
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
    
def calculate_emitter_discharge(pressure, emitter_coefficient):
    """
    Calculate EPANET emitter discharge using the standard exponent of 0.5.

    Formula:
        Q = C * sqrt(P)

    Pressure must be non-negative, and the emitter coefficient
    must be non-negative.
    """
    import math

    _validate_number(pressure, "pressure")
    _validate_number(emitter_coefficient, "emitter_coefficient")

    if pressure < 0:
        raise ValueError("Pressure cannot be negative.")

    if emitter_coefficient < 0:
        raise ValueError("Emitter coefficient cannot be negative.")

    return emitter_coefficient * math.sqrt(pressure)

