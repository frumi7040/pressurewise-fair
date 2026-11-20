from pathlib import Path

import pytest

from pressurewise_fair.simulation import run_prv_schedule_simulation


FIXTURE = (
    Path(__file__).parent
    / "fixtures"
    / "synthetic_network_prv.inp"
)


def test_time_varying_prv_schedule_is_applied_by_epanet():
    settings = [25.0, 27.0, 29.0, 31.0]
    results = run_prv_schedule_simulation(
        FIXTURE,
        "V1",
        settings,
        period_hours=6,
        simulation_hours=24,
    )

    actual = results.link["setting"]["V1"]
    for hour, expected in zip((0, 6, 12, 18), settings):
        assert actual.loc[hour * 3600] == pytest.approx(expected)


def test_prv_schedule_requires_one_setting_per_period():
    with pytest.raises(ValueError, match="one value per time period"):
        run_prv_schedule_simulation(
            FIXTURE,
            "V1",
            [25.0, 30.0],
            period_hours=6,
            simulation_hours=24,
        )


def test_prv_schedule_rejects_non_positive_settings():
    with pytest.raises(ValueError, match="finite and positive"):
        run_prv_schedule_simulation(
            FIXTURE,
            "V1",
            [25.0, 0.0, 29.0, 31.0],
        )


def test_prv_schedule_rejects_non_prv_link():
    with pytest.raises(ValueError, match="is not a PRV"):
        run_prv_schedule_simulation(
            FIXTURE,
            "P1",
            [25.0, 27.0, 29.0, 31.0],
        )
