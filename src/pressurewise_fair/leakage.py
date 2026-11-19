
"""Pressure-driven leakage calculations and EPANET emitter utilities."""

import math
from collections.abc import Mapping


def _validate_number(name: str, value: float) -> float:
    """Validate and return a finite numeric value."""
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise TypeError(f"{name} must be a number.")

    if not math.isfinite(value):
        raise ValueError(f"{name} must be finite.")

    return float(value)


def calculate_leakage(
    pressure: float,
    coefficient: float,
    exponent: float,
) -> float:
    """Calculate leakage using Q = C * p**N1."""
    pressure = _validate_number("pressure", pressure)
    coefficient = _validate_number("coefficient", coefficient)
    exponent = _validate_number("exponent", exponent)

    if pressure < 0:
        raise ValueError("Pressure cannot be negative.")
    if coefficient < 0:
        raise ValueError("Coefficient cannot be negative.")
    if exponent <= 0:
        raise ValueError("Exponent must be greater than zero.")

    return coefficient * pressure**exponent


def apply_emitters(
    wn,
    emitter_coefficients: Mapping[str, float],
):
    """Assign EPANET emitter coefficients to selected junctions."""
    if not isinstance(emitter_coefficients, Mapping):
        raise TypeError("emitter_coefficients must be a mapping.")

    for junction_id, coefficient in emitter_coefficients.items():
        if not isinstance(junction_id, str) or not junction_id.strip():
            raise ValueError("Junction IDs must be non-empty strings.")

        coefficient = _validate_number(
            f"Emitter coefficient for {junction_id}",
            coefficient,
        )

        if coefficient < 0:
            raise ValueError(
                f"Emitter coefficient for {junction_id} cannot be negative."
            )

        try:
            junction = wn.get_node(junction_id)
        except KeyError as exc:
            raise KeyError(
                f"Junction {junction_id!r} does not exist in the network."
            ) from exc

        if not hasattr(junction, "emitter_coefficient"):
            raise TypeError(
                f"Node {junction_id!r} does not support emitter coefficients."
            )

        junction.emitter_coefficient = coefficient

    return wn


def calculate_emitter_discharge(
    pressure: float,
    emitter_coefficient: float,
) -> float:
    """Calculate EPANET emitter discharge using Q = C * sqrt(P)."""
    pressure = _validate_number("pressure", pressure)
    emitter_coefficient = _validate_number(
        "emitter_coefficient",
        emitter_coefficient,
    )

    if pressure < 0:
        raise ValueError("Pressure cannot be negative.")
    if emitter_coefficient < 0:
        raise ValueError("Emitter coefficient cannot be negative.")

    return emitter_coefficient * math.sqrt(pressure)


