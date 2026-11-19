
import pytest

from pressurewise_fair.metrics import (
    calculate_dsr,
    calculate_percentile,
    calculate_equity_indicator,
)


def test_basic_dsr():
    assert calculate_dsr(80, 100) == pytest.approx(0.8)


def test_dsr_above_one_is_not_capped():
    assert calculate_dsr(120, 100) == pytest.approx(1.2)


def test_zero_delivered_demand():
    assert calculate_dsr(0, 100) == 0


def test_zero_requested_demand_is_rejected():
    with pytest.raises(ValueError):
        calculate_dsr(50, 0)


def test_negative_demand_is_rejected():
    with pytest.raises(ValueError):
        calculate_dsr(-10, 100)


def test_tenth_percentile():
    values = [0.5, 0.6, 0.7, 0.8, 0.9]
    assert calculate_equity_indicator(values) == pytest.approx(0.54)


def test_percentile_interpolation():
    assert calculate_percentile([0, 10], 25) == pytest.approx(2.5)


def test_empty_percentile_input_is_rejected():
    with pytest.raises(ValueError):
        calculate_percentile([], 10)


def test_invalid_percentile_is_rejected():
    with pytest.raises(ValueError):
        calculate_percentile([0.5, 0.8], 110)


def test_non_finite_dsr_input_is_rejected():
    with pytest.raises(ValueError):
        calculate_dsr(float("inf"), 100)
