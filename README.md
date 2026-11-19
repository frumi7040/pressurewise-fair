# PressureWise-Fair

### Save Water. Protect Every Community.

PressureWise-Fair is a research prototype for exploring equity-aware pressure management in water distribution networks. It evaluates pressure-driven leakage alongside customer demand satisfaction, so that pressure reduction is not judged on leakage alone.

> **Evidence status:** The repository contains implemented hydraulic simulation, emitter accounting, time-varying PRV schedule controls, schedule evaluation, and Pareto-analysis components. These are being tested on a small synthetic network. The prototype has not been calibrated against utility data, field-validated, or deployed. No real-world water savings or service improvements are claimed.

## The problem

Excessive pressure can increase leakage in water distribution networks. However, reducing pressure without considering customer service can worsen supply for locations that already experience low pressure.

PressureWise-Fair explores two objectives together:

1. Minimize simulated leakage volume.
2. Protect demand satisfaction at eligible customer junctions, emphasizing the lower tail of service.

## Implemented prototype components

| Component | Current implementation |
|---|---|
| EPANET 2.2 / WNTR 1.5.0 | Hydraulic network loading and simulation |
| Pressure-dependent demand | Configurable through EPANET network options |
| Emitter-based leakage | Junction emitters and pressure-based discharge accounting |
| Customer-demand accounting | Subtracts emitter discharge from EPANET-reported junction demand |
| PRV control | Time-varying PRV setpoints through WNTR time controls |
| Schedule generation | Cartesian enumeration of candidate settings across periods |
| Schedule evaluation | Runs each schedule through the EPANET simulator |
| Equity metric | 10th percentile of junction-level demand satisfaction ratios |
| Pareto analysis | Minimizes leakage volume and maximizes the equity indicator |

The optimization is deterministic; it does not use an AI or machine-learning optimizer.

## Mathematical approach

### Pressure-driven leakage

The generalized relationship is:

\[
Q_{leak}=C p^{N_1}
\]

The EPANET emitter implementation uses the configured emitter exponent. The current helper models the standard square-root case:

\[
Q_{emitter}=C\sqrt{p}
\]

WNTR stores flow in m^3/s and pressure head in metres. Emitter coefficients must use consistent SI units: m^3/s/sqrt(m).

### Customer-delivered demand

EPANET reports normal junction demand plus emitter discharge. At emitter junctions, the prototype estimates customer delivery as:

\[
D_i^{del}(t)=D_i^{reported}(t)-Q_{emitter,i}(t)
\]

### Demand satisfaction and equity

\[
DSR_i=\frac{\overline{D_i^{del}}}{D_i^{req}}
\]

The equity indicator is the 10th percentile of eligible junction DSR values. The current schedule evaluator expects constant requested demand values per eligible junction; demand-pattern-aware evaluation remains a limitation.

### Leakage objective

Emitter flow is integrated over the simulation horizon using the trapezoidal rule to estimate leakage volume in cubic metres.

### Feasibility and Pareto comparison

A schedule is feasible only if the minimum simulated pressure across eligible customer junctions meets the supplied minimum-pressure threshold. Pareto analysis minimizes leakage volume and maximizes the 10th-percentile DSR.

## Daily schedule search

The current schedule simulator applies one PRV setting per operating period using simulation-time controls. The default configuration is four six-hour periods over 24 hours.

With six candidate settings per period:

\[
6^4=1,296
\]

This is the number of candidate schedules. It is not a claim that 1,296 hydraulic runs have already completed. A complete optimization run must record all evaluated candidates and its Pareto set.

## Synthetic test network

The repository includes two small synthetic EPANET fixtures:

- `tests/fixtures/synthetic_network.inp`
- `tests/fixtures/synthetic_network_prv.inp`

They are software-test networks, not measured or calibrated representations of a real water utility. The example leakage coefficient, pressure thresholds, demands, and PRV settings are illustrative.

## Reproducibility and tests

Install the project and run the automated tests:

```bash
python -m pip install -e .
python -m pip install pytest
python -m pytest -v -s
```

GitHub Actions runs the same test suite. Passing software tests demonstrates only the behaviors covered by those tests; it does not establish field performance or utility-scale validity.

## Limitations and validation

- The current emitter implementation uses EPANET's square-root pressure relationship; arbitrary leakage exponents are not implemented in the EPANET hydraulic engine.
- The schedule evaluator currently assumes constant requested demand per eligible junction.
- Candidate PRV placement and all alternate supply paths must be assessed for each real network.
- Pressure thresholds and leakage coefficients require network-specific justification and calibration.
- A full 1,296-schedule run can be computationally expensive.
- No utility calibration, field validation, operational deployment, measured water savings, or real-world equity improvement has been completed.

See:
- [Technical blueprint](docs/TECHNICAL_BLUEPRINT.md)
- [Mathematical model](docs/MATHEMATICAL_MODEL.md)
- [Validation plan](docs/VALIDATION_PLAN.md)
- [Limitations](docs/LIMITATIONS.md)
- [Synthetic fixture notes](tests/fixtures/README.md)

## Long-term objective

PressureWise-Fair aims to help water-system decision-makers consider water conservation and equitable service together, rather than treating leakage reduction as the only measure of success.

**PressureWise-Fair — Save Water. Protect Every Community.**
