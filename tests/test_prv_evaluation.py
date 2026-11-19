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
        emitter_coefficients={"J2": 0.00005},
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
            emitter_coefficients={"J2": 0.00005},
            requested_demands={},
            minimum_pressure_m=3.516,
        )


def test_exhaustive_optimizer_runs_candidate_through_hydraulic_evaluator():
    from pressurewise_fair.optimization import optimize_prv_schedules

    result = optimize_prv_schedules(
        inp_file=FIXTURE,
        valve_id="V1",
        candidate_settings=[30.0],
        emitter_coefficients={"J2": 0.00005},
        requested_demands={
            "J1": 0.0005,
            "J2": 0.0004,
            "J3": 0.0003,
        },
        minimum_pressure_m=3.516,
    )

    assert result["evaluated_schedule_count"] == 1
    assert len(result["results"]) == 1
    assert len(result["pareto_front"]) == 1
    assert result["results"][0]["feasible"] is True


def test_lower_prv_setting_reduces_downstream_leakage_and_service():
    from pressurewise_fair.optimization import evaluate_prv_schedule

    common = {
        "inp_file": FIXTURE,
        "valve_id": "V1",
        "emitter_coefficients": {"J2": 0.00005},
        "requested_demands": {
            "J1": 0.0005,
            "J2": 0.0004,
            "J3": 0.0003,
        },
        "minimum_pressure_m": 3.516,
    }
    low = evaluate_prv_schedule(
        **common,
        schedule=(15.0, 15.0, 15.0, 15.0),
    )
    high = evaluate_prv_schedule(
        **common,
        schedule=(30.0, 30.0, 30.0, 30.0),
    )

    assert low["leakage_volume_m3"] < high["leakage_volume_m3"]
    assert low["equity"] < high["equity"]
    assert low["feasible"] is True
    assert high["feasible"] is True
