
from pathlib import Path

import pytest

from pressurewise_fair.simulation import (
    load_network,
    run_hydraulic_simulation,
    get_pressure_results,
    get_demand_results,
)


FIXTURE_DIR = Path(__file__).parent / "fixtures"
BASELINE_NETWORK = FIXTURE_DIR / "synthetic_network.inp"


def test_baseline_network_loads_through_simulation_module():
    wn = load_network(BASELINE_NETWORK)

    assert wn.get_node("R1") is not None
    assert wn.get_node("J1") is not None
    assert wn.get_node("J2") is not None
    assert wn.get_node("J3") is not None


def test_missing_network_file_raises_error():
    missing_file = FIXTURE_DIR / "does_not_exist.inp"

    with pytest.raises(FileNotFoundError):
        load_network(missing_file)


def test_baseline_hydraulic_simulation_runs():
    results = run_hydraulic_simulation(BASELINE_NETWORK)

    assert results is not None
    assert "pressure" in results.node


def test_pressure_results_are_available():
    results = run_hydraulic_simulation(BASELINE_NETWORK)

    pressures = get_pressure_results(results)

    assert not pressures.empty
    assert "J1" in pressures.columns
    assert "J2" in pressures.columns
    assert "J3" in pressures.columns


def test_demand_results_are_available():
    results = run_hydraulic_simulation(BASELINE_NETWORK)

    demands = get_demand_results(results)

    assert not demands.empty
    assert "J1" in demands.columns
    assert "J2" in demands.columns
    assert "J3" in demands.columns
