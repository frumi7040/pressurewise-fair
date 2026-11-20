# PressureWise-Fair Technical Blueprint

## Purpose

PressureWise-Fair is a research prototype for exploring pressure management in water distribution networks while explicitly tracking customer service equity.

## Implemented prototype workflow

1. Load an EPANET INP network through WNTR.
2. Configure the network's demand model and pressure thresholds in the INP file.
3. Assign EPANET emitter coefficients at selected junctions to represent pressure-driven leakage.
4. Apply a time-varying PRV setting schedule using WNTR time controls.
5. Run the schedule through the EPANET 2.2 hydraulic engine.
6. Calculate emitter discharge from simulated pressure and subtract it from EPANET-reported junction demand to estimate customer-delivered demand.
7. Calculate junction demand-satisfaction ratios and the 10th-percentile equity indicator.
8. Integrate emitter flow over time to estimate leakage volume.
9. Mark a schedule feasible only when its minimum pressure at the eligible customer junctions meets the supplied threshold.
10. Compare feasible candidates using a Pareto filter that minimizes leakage volume and maximizes the equity indicator.

## Units

WNTR stores flow in m^3/s, pressure/head in metres, length in metres, and time in seconds. Emitter coefficients must therefore use m^3/s/sqrt(m) for the standard 0.5 emitter exponent. Convert LPS inputs to m^3/s by dividing by 1,000.

## Time-varying PRV operation

The schedule simulator sets the initial PRV setting at simulation start and adds WNTR simulation-time controls for subsequent period boundaries. The current default is four equal six-hour periods over 24 hours. PRV settings are downstream pressure targets in metres.

## Optimization

The optimizer enumerates the Cartesian product of candidate PRV settings. Six candidate settings over four periods produce 1,296 schedules. Each schedule is independently simulated; it is not treated as a completed evaluation merely because it was generated.

The current optimizer accepts constant requested demand values for eligible junctions. Networks with time-varying demand patterns require requested-demand time series to be supplied by a future extension before equity scores can be interpreted correctly.

## Reproducibility

The included EPANET fixture is synthetic. Its parameters are illustrative software-test inputs, not calibrated utility data. See [Limitations](LIMITATIONS.md) and [Validation Plan](VALIDATION_PLAN.md).
