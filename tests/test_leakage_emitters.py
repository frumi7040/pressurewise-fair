
from pathlib import Path

import pytest
import wntr

from pressurewise_fair.leakage import apply_emitters


FIXTURE = (
    Path(__file__).parent
    / "fixtures"
    / "synthetic_network.inp"
)


def load_test_network():
    return wntr.network.WaterNetworkModel(str(FIXTURE))


def test_emitter_coefficient_is_assigned():
    wn = load_test_network()

    apply_emitters(wn, {"J1": 0.5})

    assert wn.get_node("J1").emitter_coefficient == pytest.approx(0.5)


def test_multiple_emitters_are_assigned():
    wn = load_test_network()

    apply_emitters(wn, {"J1": 0.5, "J2": 0.25})

    assert wn.get_node("J1").emitter_coefficient == pytest.approx(0.5)
    assert wn.get_node("J2").emitter_coefficient == pytest.approx(0.25)


def test_zero_emitter_coefficient_is_allowed():
    wn = load_test_network()

    apply_emitters(wn, {"J1": 0.0})

    assert wn.get_node("J1").emitter_coefficient == 0.0


def test_negative_emitter_coefficient_is_rejected():
    wn = load_test_network()

    with pytest.raises(ValueError):
        apply_emitters(wn, {"J1": -0.5})


def test_unknown_junction_is_rejected():
    wn = load_test_network()

    with pytest.raises(KeyError):
        apply_emitters(wn, {"UNKNOWN": 0.5})


def test_non_numeric_emitter_coefficient_is_rejected():
    wn = load_test_network()

    with pytest.raises(TypeError):
        apply_emitters(wn, {"J1": "invalid"})


def test_non_finite_emitter_coefficient_is_rejected():
    wn = load_test_network()

    with pytest.raises(ValueError):
        apply_emitters(wn, {"J1": float("nan")})


def test_invalid_mapping_is_rejected():
    wn = load_test_network()

    with pytest.raises(TypeError):
        apply_emitters(wn, [("J1", 0.5)])
