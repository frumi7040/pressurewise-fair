
import math
import pytest

from pressurewise_fair.leakage import calculate_leakage


def test_basic_leakage_calculation():
    assert calculate_leakage(10, 2, 0.5) == pytest.approx(
        2 * math.sqrt(10)
    )


def test_zero_pressure_produces_zero_leakage():
    assert calculate_leakage(0, 2, 0.5) == 0


def test_zero_coefficient_produces_zero_leakage():
    assert calculate_leakage(10, 0, 0.5) == 0


@pytest.mark.parametrize(
    "pressure, coefficient, exponent",
    [
        (-1, 2, 0.5),
        (10, -2, 0.5),
        (10, 2, 0),
    ],
)
def test_invalid_parameters_are_rejected(
    pressure, coefficient, exponent
):
    with pytest.raises(ValueError):
        calculate_leakage(pressure, coefficient, exponent)


def test_non_finite_pressure_is_rejected():
    with pytest.raises(ValueError):
        calculate_leakage(float("nan"), 2, 0.5)


def test_boolean_input_is_rejected():
    with pytest.raises(TypeError):
        calculate_leakage(True, 2, 0.5)
