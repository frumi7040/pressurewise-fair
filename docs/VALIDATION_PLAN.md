# Validation Plan

## Automated software checks

- Dependency installation and Python 3.11 test suite in GitHub Actions.
- Network loading for baseline and PRV fixtures.
- Emitter coefficient validation and SI-unit discharge calculations.
- Hydraulic simulation diagnostics with pressure-dependent demand.
- PRV time-control checks at each schedule boundary.
- Customer-demand accounting checks.
- Schedule enumeration, objective calculation, feasibility filtering, and Pareto-front tests.

## Hydraulic checks still required for a competition-grade study

1. Confirm the EPANET 2.2 engine version and all model options used in each run.
2. Verify PRV orientation, operating status, downstream setpoint, and positive flow.
3. Check pressure and demand at every customer junction and every hydraulic time step.
4. Confirm emitter coefficients are dimensionally consistent and independently justified.
5. Compare baseline and optimized schedules using identical demand and network assumptions.
6. Confirm numerical convergence and inspect all warnings and disconnected nodes.
7. Repeat the workflow on a larger benchmark network.
8. Calibrate against utility data and validate with field measurements before making real-world performance claims.

## Current evidence

The CI workflow has verified the synthetic fixture's baseline hydraulic behavior and, after correcting the WNTR SI emitter coefficient, the PRV diagnostic case. The integrated time-varying schedule optimizer is under automated verification. Synthetic results are not field validation.
