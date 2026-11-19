
from pathlib import Path

import wntr

from pressurewise_fair.leakage import apply_emitters
from pressurewise_fair.simulation import (
    calculate_emitter_discharge_results,
    get_customer_delivered_demand,
    get_demand_results,
)


FIXTURE = (
    Path(__file__).parent
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
    delivered_demand = get_customer_delivered_demand(
        results,
        coefficients,
    )

    print("\n=== PRESSUREWISE-FAIR HYDRAULIC DIAGNOSTICS ===")
    print("\nJ1 pressure:")
    print(pressures["J1"].to_string())

    print("\nJ1 total reported demand:")
    print(total_demand["J1"].to_string())

    print("\nJ1 calculated emitter discharge:")
    print(emitter_discharge["J1"].to_string())

    print("\nJ1 estimated customer-delivered demand:")
    print(delivered_demand["J1"].to_string())

    assert not pressures.empty
    assert not total_demand.empty
    assert not emitter_discharge.empty
    assert not delivered_demand.empty
    assert (emitter_discharge["J1"] >= 0).all()

