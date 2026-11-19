import pytest

from pressurewise_fair.optimization import evaluate_schedules, pareto_front


def test_evaluate_schedules_records_metrics():
    schedules = [(10.0, 20.0), (20.0, 30.0)]
    results = evaluate_schedules(
        schedules,
        lambda schedule: {
            "leakage": sum(schedule),
            "equity": 0.9,
            "minimum_pressure": 12.0,
        },
    )
    assert len(results) == 2
    assert results[0]["leakage"] == 30.0
    assert results[0]["minimum_pressure"] == 12.0


def test_evaluator_requires_both_objectives():
    with pytest.raises(ValueError):
        evaluate_schedules([(10.0,)], lambda _: {"leakage": 1.0})


def test_pareto_front_minimizes_leakage_and_maximizes_equity():
    results = [
        {"name": "A", "leakage": 10, "equity": 0.8},
        {"name": "B", "leakage": 12, "equity": 0.9},
        {"name": "C", "leakage": 13, "equity": 0.7},
        {"name": "D", "leakage": 9, "equity": 0.7},
    ]
    front = pareto_front(results)
    assert {item["name"] for item in front} == {"A", "B", "D"}


def test_infeasible_result_is_excluded():
    results = [
        {"leakage": 1, "equity": 1.0, "feasible": False},
        {"leakage": 2, "equity": 0.8, "feasible": True},
    ]
    assert pareto_front(results) == [results[1]]


def test_negative_leakage_is_rejected():
    with pytest.raises(ValueError):
        pareto_front([{"leakage": -1, "equity": 0.8}])


def test_non_finite_objective_is_rejected():
    with pytest.raises(ValueError):
        pareto_front([{"leakage": 1, "equity": float("nan")}])
