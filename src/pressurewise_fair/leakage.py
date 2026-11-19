
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
    """Calculate leakage using Q = C * p**N1.

    All inputs must use a consistent unit system.
    """
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
    """Assign EPANET emitter coefficients to selected junctions.

    Args:
        wn: A WNTR WaterNetworkModel.
        emitter_coefficients: Mapping of junction IDs to emitter
            coefficients. Coefficients must use units consistent
            with the network's flow and pressure units.

    Returns:
        The modified water network model.

    Note:
        Standard EPANET emitters use a fixed pressure exponent
        of 0.5. They do not implement an arbitrary N1 exponent.
    """
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
    
import math

import pytest

from pressurewise_fair.leakage import calculate_emitter_discharge


def test_emitter_discharge_calculation():
    result = calculate_emitter_discharge(pressure=16, emitter_coefficient=0.5)

    assert result == pytest.approx(2.0)


def test_zero_pressure_gives_zero_discharge():
    result = calculate_emitter_discharge(pressure=0, emitter_coefficient=0.5)

    assert result == 0.0


def test_zero_coefficient_gives_zero_discharge():
    result = calculate_emitter_discharge(pressure=16, emitter_coefficient=0)

    assert result == 0.0


def test_negative_pressure_is_rejected():
    with pytest.raises(ValueError):
        calculate_emitter_discharge(pressure=-1, emitter_coefficient=0.5)


def test_negative_coefficient_is_rejected():
    with pytest.raises(ValueError):
        calculate_emitter_discharge(pressure=16, emitter_coefficient=-0.5)


def test_non_finite_pressure_is_rejected():
    with pytest.raises(ValueError):
        calculate_emitter_discharge(pressure=float("nan"), emitter_coefficient=0.5)


def test_non_numeric_pressure_is_rejected():
    with pytest.raises(TypeError):
        calculate_emitter_discharge(pressure="invalid", emitter_coefficient=0.5)


