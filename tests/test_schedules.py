
import pytest

from pressurewise_fair.schedules import generate_prv_schedules


def test_four_periods_six_settings_produce_1296_schedules():
    settings = [10, 15, 20, 25, 30, 35]

    schedules = generate_prv_schedules(settings, periods=4)

    assert len(schedules) == 1296


def test_each_schedule_has_one_setting_per_period():
    schedules = generate_prv_schedules([10, 20], periods=3)

    assert all(len(schedule) == 3 for schedule in schedules)


def test_schedule_generation_is_deterministic():
    settings = [10, 20, 30]

    first = generate_prv_schedules(settings, periods=2)
    second = generate_prv_schedules(settings, periods=2)

    assert first == second


def test_two_settings_across_two_periods():
    schedules = generate_prv_schedules([10, 20], periods=2)

    assert schedules == [
        (10.0, 10.0),
        (10.0, 20.0),
        (20.0, 10.0),
        (20.0, 20.0),
    ]


def test_empty_settings_are_rejected():
    with pytest.raises(ValueError):
        generate_prv_schedules([], periods=4)


def test_zero_periods_are_rejected():
    with pytest.raises(ValueError):
        generate_prv_schedules([10, 20], periods=0)


def test_duplicate_settings_are_rejected():
    with pytest.raises(ValueError):
        generate_prv_schedules([10, 10, 20], periods=2)


def test_non_positive_setting_is_rejected():
    with pytest.raises(ValueError):
        generate_prv_schedules([0, 20], periods=2)


def test_boolean_setting_is_rejected():
    with pytest.raises(TypeError):
        generate_prv_schedules([10, True], periods=2)
