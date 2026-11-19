
from pathlib import Path

import pandas as pd
import wntr

from pressurewise_fair.leakage import apply_emitters
from pressurewise_fair.simulation import (
    calculate_emitter_discharge_results,
    get_customer_delivered_demand,
    get_demand_results,
)


FIXTURE_DIR = Path(__file__).resolve().parents[1] / "tests" / "fixtures"
FIXTURE = FIXTURE_DIR / "synthetic_network.inp"
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
    assert (discharge["J1"] > 0).any()


def test_customer_delivered_demand_accounting():
    wn = wntr.network.WaterNetworkModel(str(FIXTURE))

    coefficients = {"J1": 0.05}
    apply_emitters(wn, coefficients)

    results = wntr.sim.EpanetSimulator(wn).run_sim()

    total_demand = get_demand_results(results)
    delivered_demand = get_customer_delivered_demand(
        results,
        coefficients,
    )
    emitter_discharge = calculate_emitter_discharge_results(
        results,
        coefficients,
    )

    expected = total_demand - emitter_discharge

    pd.testing.assert_frame_equal(
        delivered_demand,
        expected,
    )
