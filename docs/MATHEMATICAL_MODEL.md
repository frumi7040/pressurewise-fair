# Mathematical Model

## Pressure-driven leakage

For a generalized leakage relationship:

\[
Q_{leak}=C p^{N_1}
\]

EPANET emitters use the configured emitter exponent, whose standard default is 0.5. The current prototype's emitter-discharge helper therefore uses:

\[
Q_{emitter}=C\sqrt{p}
\]

The coefficient must use consistent units. In WNTR, flow is m^3/s and pressure is metres, so the coefficient is m^3/s/sqrt(m).

## Customer-delivered demand

EPANET reports normal junction demand plus emitter discharge. For a junction with an emitter:

\[
D_i^{del}(t)=D_i^{reported}(t)-Q_{emitter,i}(t)
\]

This is an accounting estimate based on the emitter coefficients used in the same simulation. Small floating-point residuals can occur.

## Demand satisfaction ratio

For positive requested demand:

\[
DSR_i=\frac{\overline{D_i^{del}}}{D_i^{req}}
\]

The current evaluator uses the time-average delivered demand and a caller-supplied constant requested demand for each eligible junction. DSR values above 1 are retained rather than silently capped.

## Equity indicator

\[
E=P_{10}(DSR_i)
\]

The 10th percentile is calculated across the eligible customer junctions using linear interpolation.

## Leakage objective

Emitter discharge is integrated over the simulation time series using the trapezoidal rule:

\[
V_{leak}=\sum_i\sum_{k=0}^{n-1}
\frac{Q_{i,k}+Q_{i,k+1}}{2}(t_{k+1}-t_k)
\]

The resulting leakage objective is a volume in cubic metres.

## Feasibility and Pareto objectives

A schedule is marked feasible when its minimum simulated pressure across eligible customer junctions is at least the user-supplied minimum-pressure threshold. The Pareto filter minimizes leakage volume and maximizes the 10th-percentile DSR. It excludes schedules explicitly marked infeasible.
