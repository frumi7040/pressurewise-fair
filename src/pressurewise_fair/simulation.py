
"""Hydraulic simulation utilities for PressureWise-Fair."""

from pathlib import Path
import math

import pandas as pd
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
    """Return EPANET-reported junction demand.

    This may include emitter discharge and must not automatically
    be interpreted as customer-delivered demand.
    """
    if "demand" not in results.node:
        raise ValueError("Demand results are unavailable.")

    return results.node["demand"]


def calculate_emitter_discharge_results(
    results,
    emitter_coefficients,
):
    """Calculate emitter discharge time series for selected junctions.

    EPANET's standard emitter exponent is 0.5.
    """
    if not isinstance(emitter_coefficients, dict):
        raise TypeError("emitter_coefficients must be a dictionary.")

    pressures = get_pressure_results(results)
    discharge = pd.DataFrame(
        0.0,
        index=pressures.index,
        columns=pressures.columns,
    )

    for junction_id, coefficient in emitter_coefficients.items():
        if junction_id not in pressures.columns:
            raise KeyError(
                f"Junction {junction_id!r} is missing from pressure results."
            )

        if (
            isinstance(coefficient, bool)
            or not isinstance(coefficient, (int, float))
        ):
            raise TypeError(
                f"Emitter coefficient for {junction_id} must be numeric."
            )

        if not math.isfinite(coefficient) or coefficient < 0:
            raise ValueError(
                f"Emitter coefficient for {junction_id} "
                "must be finite and non-negative."
            )

        pressure = pressures[junction_id]

        if (pressure < 0).any():
            raise ValueError(
                f"Negative pressure encountered at {junction_id}."
            )

        discharge[junction_id] = coefficient * pressure.pow(0.5)

    return discharge


def get_customer_delivered_demand(
    results,
    emitter_coefficients,
):
    """Estimate customer-delivered demand by subtracting emitter flow.

    This calculation assumes EPANET-reported demand includes emitter
    discharge and that the supplied coefficients match the simulated
    network. Verify this accounting convention against the installed
    EPANET/WNTR version before using results for research conclusions.
    """
    total_demand = get_demand_results(results)
    emitter_discharge = calculate_emitter_discharge_results(
        results,
        emitter_coefficients,
    )

    return total_demand - emitter_discharge


