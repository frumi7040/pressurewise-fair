
"""Hydraulic simulation utilities for PressureWise-Fair."""

from pathlib import Path
import math

import wntr


def load_network(inp_file: str | Path):
    """Load an EPANET input network."""
    path = Path(inp_file)

    if not path.is_file():
        raise FileNotFoundError(
            f"EPANET network file not found: {path}"
        )

    return wntr.network.WaterNetworkModel(str(path))


def run_hydraulic_simulation(inp_file: str | Path):
    """Run an EPANET-based hydraulic simulation."""
    wn = load_network(inp_file)

    try:
        simulator = wntr.sim.EpanetSimulator(wn)
        results = simulator.run_sim()
    except Exception as exc:
        raise RuntimeError(
            f"Hydraulic simulation failed for {inp_file}: {exc}"
        ) from exc

    if "pressure" not in results.node:
        raise ValueError(
            "Simulation results do not contain junction pressures."
        )

    pressures = results.node["pressure"]

    if pressures.empty:
        raise ValueError("Simulation returned no pressure results.")

    values = pressures.to_numpy()

    if not all(
        math.isfinite(float(value))
        for value in values.flat
    ):
        raise ValueError(
            "Simulation returned non-finite pressure values."
        )

    return results


def get_pressure_results(results):
    """Return the junction pressure time series."""
    if "pressure" not in results.node:
        raise ValueError("Pressure results are unavailable.")

    return results.node["pressure"]


def get_demand_results(results):
    """Return the junction demand time series.

    Demand must not automatically be interpreted as
    customer-delivered demand when emitter leakage is present.
    """
    if "demand" not in results.node:
        raise ValueError("Demand results are unavailable.")

    return results.node["demand"]

