from pathlib import Path

import pytest

from pressurewise_fair.optimization import evaluate_prv_schedule


FIXTURE = (
    Path(__file__).parent
    / "fixtures"
    / "synthetic_network_prv.inp"
)


def test_prv_schedule_returns_hydraulic_objectives():
    result = evaluate_prv_schedule(
        inp_file=FIXTURE,
        valve_id="V1",
        schedule=(30.0, 30.0, 30.0, 30.0),
        emitter_coefficients={"J1": 0.00005},
        requested_demands={
            "J1": 0.0005,
            "J2": 0.0004,
            "J3": 0.0003,
        },
        minimum_pressure_m=3.516,
    )

    assert result["leakage_volume_m3"] > 0
    assert result["equity"] == pytest.approx(1.0, abs=0.01)
    assert result["minimum_pressure"] >= 3.516
    assert result["feasible"] is True
    assert set(result["dsr_by_junction"]) == {"J1", "J2", "J3"}


def test_prv_schedule_evaluation_rejects_empty_customer_set():
    with pytest.raises(ValueError, match="non-empty mapping"):
        evaluate_prv_schedule(
            inp_file=FIXTURE,
            valve_id="V1",
            schedule=(30.0, 30.0, 30.0, 30.0),
            emitter_coefficients={"J1": 0.00005},
            requested_demands={},
            minimum_pressure_m=3.516,
        )
