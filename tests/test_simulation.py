
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


def test_emitter_discharge_from_hydraulic_simulation():
    wn = wntr.network.WaterNetworkModel(str(FIXTURE))

    coefficients = {"J1": 0.05}
    apply_emitters(wn, coefficients)

    results = wntr.sim.EpanetSimulator(wn).run_sim()

    discharge = calculate_emitter_discharge_results(
        results,
        coefficients,
    )

    assert not discharge.empty
    assert "J1" in discharge.columns
    assert (discharge["J1"] > 0).all()


def test_epanet_demand_includes_emitter_discharge():
    wn = wntr.network.WaterNetworkModel(str(FIXTURE))

    coefficients = {"J1": 0.05}
    apply_emitters(wn, coefficients)

    results = wntr.sim.EpanetSimulator(wn).run_sim()

    total_demand = get_demand_results(results)

    emitter_discharge = calculate_emitter_discharge_results(
        results,
        coefficients,
    )

    expected_j1 = 0.50 + emitter_discharge["J1"]

    assert (
        total_demand["J1"] - expected_j1
    ).abs().max() < 1e-5


def test_customer_delivered_demand_excludes_emitter_flow():
    wn = wntr.network.WaterNetworkModel(str(FIXTURE))

    coefficients = {"J1": 0.05}
    apply_emitters(wn, coefficients)

    results = wntr.sim.EpanetSimulator(wn).run_sim()

    delivered = get_customer_delivered_demand(
        results,
        coefficients,
    )
    print("\nTOTAL DEMAND:")
print(get_demand_results(results).head())

print("\nPRESSURE:")
print(results.node["pressure"].head())

print("\nEMITTER DISCHARGE:")
print(
    calculate_emitter_discharge_results(
        results,
        coefficients,
    ).head()
)

print("\nCUSTOMER DELIVERED DEMAND:")
print(delivered.head())

    assert (
        delivered["J1"] - 0.50
    ).abs().max() < 1e-5

    assert (
        delivered["J2"] - 0.40
    ).abs().max() < 1e-5

    assert (
        delivered["J3"] - 0.30
    ).abs().max() < 1e-5
