
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
