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

    # Explicitly select EPANET 2.2 pressure-dependent demand (PDA).
    wn.options.hydraulic.demand_model = "PDA"
    wn.options.hydraulic.minimum_pressure = 3.516
    wn.options.hydraulic.required_pressure = 21.097
    wn.options.hydraulic.pressure_exponent = 0.5

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
    print("\nAll junction pressures (m):")
    print(pressures.to_string())
    print("\nAll junction reported demand (L/s):")
    print(total_demand.to_string())
    print("\nEmitter discharge at J1 (L/s):")
    print(emitter_discharge["J1"].to_string())
    print("\nEstimated customer-delivered demand at J1 (L/s):")
    print(delivered_demand["J1"].to_string())
    print("\nPRV link status:")
    print(results.link["status"]["V1"].to_string())
    print("\nPRV link flowrate:")
    print(results.link["flowrate"]["V1"].to_string())
    print("\nPRV link setting:")
    print(results.link["setting"]["V1"].to_string())

    assert not pressures.empty
    assert not total_demand.empty
    assert not emitter_discharge.empty
    assert not delivered_demand.empty
    assert (emitter_discharge["J1"] >= 0).all()
