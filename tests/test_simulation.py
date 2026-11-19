
from pathlib import Path

import wntr

from pressurewise_fair.leakage import apply_emitters
from pressurewise_fair.simulation import (
    calculate_emitter_discharge_results,
    get_customer_delivered_demand,
    get_demand_results,
)


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]

FIXTURE = (
    REPOSITORY_ROOT
    / "tests"
    / "fixtures"
    / "synthetic_network_prv.inp"
)


def test_emitter_hydraulic_diagnostics():
    wn = wntr.network.WaterNetworkModel(str(FIXTURE))

    coefficients = {"J1": 0.05}
    apply_emitters(wn, coefficients)

    results = wntr.sim.EpanetSimulator(wn).run_sim()

    pressures = results.node["pressure"]
    total_demand = get_demand_results(results)

    emitter_discharge = calculate_emitter_discharge_results(
        results,
        coefficients,
    )

    delivered = get_customer_delivered_demand(
        results,
        coefficients,
    )

    print("\n=== PRESSURES ===")
    print(pressures[["J1", "J2", "J3"]].head())

    print("\n=== EPANET TOTAL DEMAND ===")
    print(total_demand[["J1", "J2", "J3"]].head())

    print("\n=== EMITTER DISCHARGE ===")
    print(emitter_discharge.head())

    print("\n=== CUSTOMER DELIVERED DEMAND ===")
    print(delivered[["J1", "J2", "J3"]].head())

    print("\n=== PRV STATUS ===")
    print(results.link["status"].head())

    assert not pressures.empty
    assert not total_demand.empty
    assert not delivered.empty
