
from pathlib import Path

import pytest
import wntr


FIXTURE_DIR = Path(__file__).parent / "fixtures"


def load_network(filename):
    """Load a synthetic EPANET network fixture."""
    path = FIXTURE_DIR / filename

    if not path.is_file():
        raise FileNotFoundError(f"Network fixture not found: {path}")

    return wntr.network.WaterNetworkModel(str(path))


def test_baseline_network_loads():
    wn = load_network("synthetic_network.inp")

    assert wn.get_node("R1") is not None
    assert wn.get_node("J1") is not None
    assert wn.get_node("J2") is not None
    assert wn.get_node("J3") is not None

    assert wn.get_link("P1") is not None
    assert wn.get_link("P2") is not None
    assert wn.get_link("P3") is not None


def test_prv_network_loads():
    wn = load_network("synthetic_network_prv.inp")

    assert wn.get_node("R1") is not None
    assert wn.get_node("J1") is not None
    assert wn.get_node("J2") is not None
    assert wn.get_node("J3") is not None

    assert wn.get_link("P1") is not None
    assert wn.get_link("P3") is not None
    assert wn.get_link("V1") is not None


def test_prv_network_contains_pressure_reducing_valve():
    wn = load_network("synthetic_network_prv.inp")

    valve = wn.get_link("V1")

    assert valve.valve_type == "PRV"
    assert valve.setting == pytest.approx(30.0)
