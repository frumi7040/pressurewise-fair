"""Evaluation and Pareto filtering for candidate PRV schedules.

The evaluator is injected: callers supply a hydraulic simulation function
that applies a schedule and returns validated metrics. This module does not
claim to implement time-varying PRV controls itself.
"""
from collections.abc import Callable, Iterable, Mapping
from pathlib import Path
import math

from pressurewise_fair.metrics import calculate_dsr, calculate_equity_indicator
from pressurewise_fair.schedules import generate_prv_schedules
from pressurewise_fair.simulation import (
    calculate_emitter_discharge_results,
    get_customer_delivered_demand,
    run_prv_schedule_simulation,
)


def _finite_number(name: str, value: float) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise TypeError(f"{name} must be numeric.")
    if not math.isfinite(value):
        raise ValueError(f"{name} must be finite.")
    return float(value)


def evaluate_schedules(
    schedules: Iterable[tuple[float, ...]],
    evaluator: Callable[[tuple[float, ...]], Mapping[str, float]],
) -> list[dict[str, object]]:
    """Evaluate schedules with a caller-supplied hydraulic evaluator."""
    if not callable(evaluator):
        raise TypeError("evaluator must be callable.")

    records = []
    for schedule in schedules:
        normalized = tuple(
            _finite_number("schedule setting", setting)
            for setting in schedule
        )
        metrics = evaluator(normalized)
        if not isinstance(metrics, Mapping):
            raise TypeError("evaluator must return a mapping.")
        if "leakage" not in metrics or "equity" not in metrics:
            raise ValueError("evaluator must return leakage and equity.")

        record = {
            "schedule": normalized,
            "leakage": _finite_number("leakage", metrics["leakage"]),
            "equity": _finite_number("equity", metrics["equity"]),
        }
        if record["leakage"] < 0:
            raise ValueError("leakage cannot be negative.")
        if "minimum_pressure" in metrics:
            record["minimum_pressure"] = _finite_number(
                "minimum_pressure", metrics["minimum_pressure"]
            )
        if "feasible" in metrics:
            if not isinstance(metrics["feasible"], bool):
                raise TypeError("feasible must be a boolean.")
            record["feasible"] = metrics["feasible"]
        records.append(record)
    return records


def pareto_front(
    results: Iterable[Mapping[str, object]],
) -> list[Mapping[str, object]]:
    """Return non-dominated results: minimize leakage, maximize equity."""
    candidates = []
    for result in results:
        leakage = _finite_number("leakage", result["leakage"])
        equity = _finite_number("equity", result["equity"])
        if leakage < 0:
            raise ValueError("leakage cannot be negative.")
        feasible = result.get("feasible", True)
        if not isinstance(feasible, bool):
            raise TypeError("feasible must be a boolean.")
        if feasible:
            candidates.append((result, leakage, equity))

    front = []
    for candidate, leakage, equity in candidates:
        dominated = any(
            other_leakage <= leakage
            and other_equity >= equity
            and (other_leakage < leakage or other_equity > equity)
            for other, other_leakage, other_equity in candidates
            if other is not candidate
        )
        if not dominated:
            front.append(candidate)

    return sorted(
        front,
        key=lambda item: (
            float(item["leakage"]),
            -float(item["equity"]),
        ),
    )


def evaluate_prv_schedule(
    inp_file: str | Path,
    valve_id: str,
    schedule: tuple[float, ...],
    emitter_coefficients: Mapping[str, float],
    requested_demands: Mapping[str, float],
    minimum_pressure_m: float,
    period_hours: int = 6,
    simulation_hours: int = 24,
) -> dict[str, object]:
    """Hydraulically evaluate one schedule and calculate leakage/equity.

    All flow inputs are WNTR SI units (m^3/s); pressure and PRV settings
    are metres. requested_demands must provide constant requested
    customer demand for each eligible junction. The model INP file must
    define its intended demand model and pressure thresholds.
    """
    if not isinstance(emitter_coefficients, Mapping):
        raise TypeError("emitter_coefficients must be a mapping.")
    if not isinstance(requested_demands, Mapping) or not requested_demands:
        raise ValueError("requested_demands must be a non-empty mapping.")

    minimum_pressure_m = _finite_number(
        "minimum_pressure_m", minimum_pressure_m
    )
    if minimum_pressure_m < 0:
        raise ValueError("minimum_pressure_m cannot be negative.")

    requested = {}
    for node_id, demand in requested_demands.items():
        if not isinstance(node_id, str) or not node_id.strip():
            raise ValueError("Customer junction IDs must be non-empty strings.")
        demand = _finite_number(f"requested demand for {node_id}", demand)
        if demand <= 0:
            raise ValueError(f"Requested demand for {node_id} must be positive.")
        requested[node_id] = demand

    results = run_prv_schedule_simulation(
        inp_file,
        valve_id,
        schedule,
        period_hours=period_hours,
        simulation_hours=simulation_hours,
    )
    pressures = results.node["pressure"]
    missing = set(requested) - set(pressures.columns)
    if missing:
        raise KeyError(f"Customer junctions missing from results: {sorted(missing)}")

    delivered = get_customer_delivered_demand(
        results,
        dict(emitter_coefficients),
    )
    dsr_values = []
    dsr_by_junction = {}
    for node_id, requested_flow in requested.items():
        mean_delivered = float(delivered[node_id].mean())
        if mean_delivered < -1e-9:
            raise ValueError(
                f"Calculated customer delivery is negative at {node_id}."
            )
        mean_delivered = max(0.0, mean_delivered)
        dsr = calculate_dsr(mean_delivered, requested_flow)
        dsr_values.append(dsr)
        dsr_by_junction[node_id] = dsr

    emitter_flow = calculate_emitter_discharge_results(
        results,
        dict(emitter_coefficients),
    )
    times = [float(value) for value in emitter_flow.index]
    if len(times) < 2:
        raise ValueError("At least two hydraulic time points are required.")
    leakage_volume_m3 = 0.0
    for node_id in emitter_flow.columns:
        flow = [float(value) for value in emitter_flow[node_id]]
        leakage_volume_m3 += sum(
            0.5 * (flow[i] + flow[i + 1]) * (times[i + 1] - times[i])
            for i in range(len(times) - 1)
        )

    minimum_observed_pressure = float(
        pressures[list(requested)].min().min()
    )
    return {
        "schedule": tuple(float(value) for value in schedule),
        "leakage": leakage_volume_m3,
        "leakage_volume_m3": leakage_volume_m3,
        "equity": calculate_equity_indicator(dsr_values),
        "minimum_pressure": minimum_observed_pressure,
        "feasible": minimum_observed_pressure >= minimum_pressure_m,
        "dsr_by_junction": dsr_by_junction,
    }


def optimize_prv_schedules(
    inp_file: str | Path,
    valve_id: str,
    candidate_settings: Iterable[float],
    emitter_coefficients: Mapping[str, float],
    requested_demands: Mapping[str, float],
    minimum_pressure_m: float,
    period_hours: int = 6,
    simulation_hours: int = 24,
) -> dict[str, object]:
    """Run every candidate schedule through EPANET and return its Pareto set.

    Four six-hour periods and six candidate settings produce 6^4 = 1,296
    independent hydraulic simulations. This can be computationally
    expensive; no results are cached or fabricated.
    """
    if period_hours <= 0 or simulation_hours <= 0:
        raise ValueError("period_hours and simulation_hours must be positive.")
    if simulation_hours % period_hours:
        raise ValueError("simulation_hours must be divisible by period_hours.")
    schedules = generate_prv_schedules(
        list(candidate_settings),
        periods=simulation_hours // period_hours,
    )
    records = evaluate_schedules(
        schedules,
        lambda schedule: evaluate_prv_schedule(
            inp_file,
            valve_id,
            schedule,
            emitter_coefficients,
            requested_demands,
            minimum_pressure_m,
            period_hours=period_hours,
            simulation_hours=simulation_hours,
        ),
    )
    return {
        "evaluated_schedule_count": len(records),
        "results": records,
        "pareto_front": pareto_front(records),
    }
