
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



def run_prv_schedule_simulation(
    inp_file: str | Path,
    valve_id: str,
    settings: list[float] | tuple[float, ...],
    emitter_coefficients: dict[str, float] | None = None,
    period_hours: int = 6,
    simulation_hours: int = 24,
):
    """Run a hydraulic simulation with one PRV setting per time period.

    The first setting is applied at simulation start. Subsequent settings
    are applied by WNTR time controls at each period boundary. Settings
    are downstream pressure targets in metres. WNTR inputs and outputs
    use SI units.

    This function runs the actual time-varying controls through EPANET;
    it does not estimate schedule performance from static simulations.
    """
    import math
    import wntr.network.controls as controls

    if not isinstance(valve_id, str) or not valve_id.strip():
        raise ValueError("valve_id must be a non-empty string.")
    if isinstance(period_hours, bool) or not isinstance(period_hours, int):
        raise TypeError("period_hours must be an integer.")
    if isinstance(simulation_hours, bool) or not isinstance(simulation_hours, int):
        raise TypeError("simulation_hours must be an integer.")
    if period_hours <= 0 or simulation_hours <= 0:
        raise ValueError("period_hours and simulation_hours must be positive.")
    if simulation_hours % period_hours:
        raise ValueError("simulation_hours must be divisible by period_hours.")
    if len(settings) != simulation_hours // period_hours:
        raise ValueError("settings must contain one value per time period.")

    normalized = []
    for setting in settings:
        if isinstance(setting, bool) or not isinstance(setting, (int, float)):
            raise TypeError("PRV settings must be numeric.")
        if not math.isfinite(setting) or setting <= 0:
            raise ValueError("PRV settings must be finite and positive.")
        normalized.append(float(setting))

    wn = load_network(inp_file)
    if emitter_coefficients is not None:
        from pressurewise_fair.leakage import apply_emitters

        apply_emitters(wn, emitter_coefficients)

    try:
        valve = wn.get_link(valve_id)
    except KeyError as exc:
        raise KeyError(f"PRV {valve_id!r} does not exist in the network.") from exc

    if getattr(valve, "valve_type", None) not in {"PRV", "PRValve"}:
        raise ValueError(f"Link {valve_id!r} is not a PRV.")

    wn.options.time.duration = simulation_hours * 3600
    valve.initial_setting = normalized[0]

    for period_index, setting in enumerate(normalized[1:], start=1):
        boundary_seconds = period_index * period_hours * 3600
        action = controls.ControlAction(valve, "setting", setting)
        condition = controls.SimTimeCondition(
            wn,
            "=",
            boundary_seconds,
        )
        control = controls.Control(
            condition,
            action,
            name=f"{valve_id}_setting_period_{period_index + 1}",
        )
        wn.add_control(
            f"{valve_id}_schedule_{period_index + 1}",
            control,
        )

    try:
        simulator = wntr.sim.EpanetSimulator(wn)
        results = simulator.run_sim(version=2.2)
    except Exception as exc:
        raise RuntimeError(
            f"PRV schedule simulation failed for {inp_file}: {exc}"
        ) from exc

    if "pressure" not in results.node or valve_id not in results.link["setting"]:
        raise ValueError("Simulation results are missing required hydraulic outputs.")
    return results

def get_pressure_results(results):
    """Return the junction pressure time series."""
    if "pressure" not in results.node:
        raise ValueError("Pressure results are unavailable.")

    return results.node["pressure"]


def get_demand_results(results):
    """Return EPANET-reported nodal demand in WNTR SI units (m^3/s).

    EPANET-reported demand includes both customer demand and emitter
    discharge at emitter junctions. Convert to customer delivery by
    subtracting the matching emitter-discharge time series.
    """
    if "demand" not in results.node:
        raise ValueError("Demand results are unavailable.")

    return results.node["demand"]


def calculate_emitter_discharge_results(
    results,
    emitter_coefficients,
):
    """Calculate emitter discharge time series in m^3/s.

    WNTR inputs use SI units: pressure in metres and emitter coefficient
    in m^3/s/sqrt(m). EPANET's standard emitter exponent is 0.5.
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
    """Estimate customer-delivered demand in m^3/s by subtracting emitter flow.

    EPANET reports normal junction demand plus emitter discharge. The
    supplied coefficients must match those used in the simulation.
    """
    total_demand = get_demand_results(results)
    emitter_discharge = calculate_emitter_discharge_results(
        results,
        emitter_coefficients,
    )

    return total_demand - emitter_discharge


