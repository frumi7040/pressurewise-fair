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

    # WNTR stores all hydraulic quantities in SI units:
    # pressure/head in metres and flow in m^3/s.
    wn.options.hydraulic.demand_model = "PDA"
    wn.options.hydraulic.minimum_pressure = 3.516
    wn.options.hydraulic.required_pressure = 21.097
    wn.options.hydraulic.pressure_exponent = 0.5

    # 0.05 L/s/sqrt(m) expressed in WNTR SI flow units (m^3/s/sqrt(m)).
    coefficients = {"J1": 0.00005}
    apply_emitters(wn, coefficients)

    results = wntr.sim.EpanetSimulator(wn).run_sim()

    pressures_m = results.node["pressure"]
    total_demand_m3s = get_demand_results(results)
    emitter_m3s = calculate_emitter_discharge_results(
        results,
        coefficients,
    )
    delivered_m3s = get_customer_delivered_demand(
        results,
        coefficients,
    )

    print("\n=== PRESSUREWISE-FAIR HYDRAULIC DIAGNOSTICS ===")
    print("\nJunction pressures (m):")
    print(pressures_m[["J1", "J2", "J3"]].to_string())
    print("\nTotal reported junction demand (L/s):")
    print((total_demand_m3s[["J1", "J2", "J3"]] * 1000).to_string())
    print("\nEmitter discharge at J1 (L/s):")
    print((emitter_m3s["J1"] * 1000).to_string())
    print("\nEstimated customer-delivered demand at J1 (L/s):")
    print((delivered_m3s["J1"] * 1000).to_string())
    print("\nPRV status (1=open):")
    print(results.link["status"]["V1"].to_string())
    print("\nPRV flowrate (L/s):")
    print((results.link["flowrate"]["V1"] * 1000).to_string())
    print("\nPRV setting (m):")
    print(results.link["setting"]["V1"].to_string())

    assert not pressures_m.empty
    assert not total_demand_m3s.empty
    assert not emitter_m3s.empty
    assert not delivered_m3s.empty
    assert (pressures_m[["J1", "J2", "J3"]] >= 0).all().all()
    assert (emitter_m3s["J1"] >= 0).all()
    assert (results.link["status"]["V1"] > 0).all()
    assert (results.link["flowrate"]["V1"] > 0).all()
    assert (delivered_m3s["J1"] >= -1e-9).all()
