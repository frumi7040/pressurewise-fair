"""Run the full synthetic 1,296-schedule PressureWise-Fair example."""

import json
from pathlib import Path

from pressurewise_fair.optimization import optimize_prv_schedules


ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "tests" / "fixtures" / "synthetic_network_prv.inp"
OUTPUT = ROOT / "results" / "synthetic_optimization.json"


def main():
    result = optimize_prv_schedules(
        inp_file=FIXTURE,
        valve_id="V1",
        candidate_settings=[15.0, 18.0, 21.0, 24.0, 27.0, 30.0],
        emitter_coefficients={"J2": 0.00005},
        requested_demands={
            "J1": 0.0005,
            "J2": 0.0004,
            "J3": 0.0003,
        },
        minimum_pressure_m=3.516,
        period_hours=6,
        simulation_hours=24,
    )

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "scenario": "synthetic software-validation network; not utility data",
        "engine": "EPANET 2.2 through WNTR 1.5.0",
        "flow_units": "m^3/s",
        "pressure_units": "m",
        "candidate_settings_m": [15.0, 18.0, 21.0, 24.0, 27.0, 30.0],
        "period_hours": 6,
        "simulation_hours": 24,
        "evaluated_schedule_count": result["evaluated_schedule_count"],
        "pareto_front": result["pareto_front"],
        "results": result["results"],
    }
    OUTPUT.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(f"Evaluated schedules: {result['evaluated_schedule_count']}")
    print(f"Feasible Pareto solutions: {len(result['pareto_front'])}")
    print(f"Results written to: {OUTPUT}")


if __name__ == "__main__":
    main()
