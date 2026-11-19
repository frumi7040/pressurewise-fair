# PressureWise-Fair — Mathematical Model

**Document type:** Mathematical Formulation and Optimization Specification  
**Project:** PressureWise-Fair  
**Version:** 1.0

> **Status:** This document defines the proposed mathematical formulation. Numerical parameters, calibrated values, simulation outputs, and optimization results have not yet been established or validated.

---

## 1. Mathematical Objective

PressureWise-Fair investigates how to reduce pressure-driven water leakage while protecting customer demand satisfaction across a water distribution network.

The proposed optimization has two competing objectives:

1. Minimize total simulated leakage.
2. Maximize lower-tail customer demand satisfaction.

The model must also satisfy hydraulic feasibility and designated minimum-pressure constraints.

---

## 2. Notation and Variables

| Symbol | Definition |
|---|---|
| \(i\) | Demand junction index |
| \(j\) | Operating period index |
| \(k\) | Candidate PRV setting index |
| \(t\) | Simulation time |
| \(p_i(t)\) | Pressure head at junction \(i\) |
| \(q_{\mathrm{leak},i}(t)\) | Emitter leakage flow at junction \(i\) |
| \(C_i\) | Emitter coefficient |
| \(N_1\) | Leakage pressure exponent |
| \(D_i^{\mathrm{req}}(t)\) | Required customer demand |
| \(D_i^{\mathrm{del}}(t)\) | Delivered customer demand |
| \(DSR_i\) | Demand Satisfaction Ratio |
| \(E\) | Lower-tail service equity indicator |
| \(s_j\) | Selected PRV setting for operating period \(j\) |

All variables must use consistent units and clearly documented time conventions.

---

## 3. Pressure-Driven Leakage Model

The proposed leakage relationship is:

\[
q_{\mathrm{leak},i}(t)
=
C_i\,[p_i(t)]^{N_1}
\]

Where:

- \(q_{\mathrm{leak},i}(t)\) is the modeled emitter discharge.
- \(C_i\) is the emitter coefficient for location \(i\).
- \(p_i(t)\) is the applicable pressure head.
- \(N_1\) is the leakage pressure exponent.

For this relationship, pressure must be nonnegative and expressed in the units used to define the emitter coefficient.

### Total simulated leakage

For a network with \(m\) leakage locations:

\[
Q_{\mathrm{leak,total}}(t)
=
\sum_{i=1}^{m}q_{\mathrm{leak},i}(t)
\]

For a simulation horizon from \(0\) to \(T\), total leakage volume is:

\[
V_{\mathrm{leak}}
=
\int_0^T Q_{\mathrm{leak,total}}(t)\,dt
\]

For discrete simulation intervals:

\[
V_{\mathrm{leak}}
\approx
\sum_{r=1}^{R}
Q_{\mathrm{leak,total}}(t_r)\Delta t_r
\]

The time interval and flow units must be converted consistently to obtain a volume.

**Accounting requirement:** Emitter discharge represents modeled leakage, not customer-delivered water.

---

## 4. Pressure-Dependent Customer Demand

Customer demand may depend on the pressure available at a junction.

A general pressure-dependent demand representation is:

\[
D_i^{\mathrm{del}}(t)
=
D_i^{\mathrm{req}}(t)\,f(p_i(t))
\]

Where:

- \(D_i^{\mathrm{req}}(t)\) is the required demand.
- \(f(p_i(t))\) is the selected pressure-response function.

The exact pressure-response function and its parameters must be defined in the hydraulic model.

They must not be assumed to be universal across all networks.

The function should be consistent with the pressure-dependent demand configuration used by the selected simulation engine.

---

## 5. Demand Satisfaction Ratio

For each eligible demand junction:

\[
DSR_i(t)
=
\frac{D_i^{\mathrm{del}}(t)}
{D_i^{\mathrm{req}}(t)}
\]

When required demand is positive, the ratio describes the fraction of demand delivered.

Interpretation:

- \(DSR_i=1\): Required demand is fully satisfied.
- \(DSR_i<1\): Required demand is not fully satisfied.
- \(DSR_i>1\): Requires investigation of the model's demand accounting or interpretation.

Junctions with zero required demand must be excluded from the ratio calculation for that time interval.

### Customer-demand accounting

The delivered-demand quantity must exclude emitter discharge.

If the hydraulic simulator reports a combined junction outflow that includes emitter flow, the post-processing procedure must separate the two components using a verified and documented method.

---

## 6. Service Equity Indicator

PressureWise-Fair proposes using the 10th percentile of eligible demand-junction DSR values.

\[
E(t)=P_{10}
\left(
DSR_1(t),DSR_2(t),\ldots,DSR_n(t)
\right)
\]

Where:

- \(P_{10}\) is the 10th percentile.
- \(n\) is the number of eligible demand junctions.

A higher value indicates better demand satisfaction among the lower-performing portion of the modeled network.

### Evaluation horizon

For a multi-period simulation, the implementation must define how time is handled.

One possible evaluation is to calculate the 10th percentile at each simulation interval and then use a documented aggregation method over the evaluation horizon.

Another possible approach is to calculate a time-weighted demand satisfaction ratio for each junction before calculating the percentile.

These approaches are not interchangeable. The selected method must be stated before results are compared.

---

## 7. PRV Schedule Representation

The proposed schedule contains four operating periods.

Each period has six candidate PRV settings.

Let:

\[
S=(s_1,s_2,s_3,s_4)
\]

Each \(s_j\) is selected from a defined candidate set:

\[
s_j\in\mathcal{P}
\]

Where \(\mathcal{P}\) contains six candidate downstream pressure settings.

The number of possible schedules is:

\[
N_{\mathrm{schedule}}=6^4=1,296
\]

This is the number of candidate combinations per scenario.

The candidate settings must be specified in consistent pressure-head units and must be suitable for the modeled PRV and network.

The four operating periods must cover the intended simulation horizon without unintended gaps or overlaps.

---

## 8. Hydraulic Feasibility

Every candidate schedule must be evaluated against the hydraulic model.

A candidate is not automatically feasible merely because its settings fall within the candidate set.

It must satisfy the applicable simulation and network constraints.

These include:

- Valid hydraulic network configuration.
- Successful simulation execution.
- Appropriate PRV operation.
- Acceptable pressure conditions.
- Valid customer-demand accounting.
- Required minimum-pressure conditions.

Failed or non-convergent simulations must be classified as invalid rather than treated as successful candidates.

---

## 9. Minimum-Pressure Constraints

Let \(\mathcal{C}\) represent the set of critical junctions.

For every critical junction \(i\) and required evaluation time \(t\):

\[
p_i(t)\geq p_i^{\min}
\]

Where \(p_i^{\min}\) is the specified minimum pressure head for that junction.

The values must be justified using the selected network and applicable service requirements.

A single universal minimum-pressure value must not be assumed for all networks.

---

## 10. Two-Objective Optimization Formulation

The proposed optimization problem is:

\[
\min_S V_{\mathrm{leak}}(S)
\]

and simultaneously:

\[
\max_S E(S)
\]

Subject to:

\[
p_i(t;S)\geq p_i^{\min}
\]

for all required critical junctions and evaluation times.

Additional constraints include:

- Hydraulic feasibility.
- Valid PRV operation.
- Defined operating periods.
- Consistent leakage accounting.
- Valid demand-satisfaction calculations.

Here, \(S\) represents a candidate daily PRV schedule.

The two objectives may conflict. A schedule that reduces leakage may also reduce demand satisfaction at some locations.

For that reason, the project proposes Pareto analysis rather than assuming that one objective alone determines the best schedule.

---

## 11. Pareto Dominance

Consider two feasible candidate schedules, \(A\) and \(B\).

Schedule \(A\) dominates schedule \(B\) if:

\[
V_{\mathrm{leak}}(A)
\leq
V_{\mathrm{leak}}(B)
\]

and:

\[
E(A)\geq E(B)
\]

with at least one strict inequality.

A schedule is non-dominated if no other feasible schedule dominates it.

The collection of non-dominated schedules forms the Pareto set.

The resulting Pareto frontier can help decision-makers compare leakage and service-equity trade-offs.

No actual Pareto frontier can be claimed until the corresponding hydraulic evaluations have been completed.

---

## 12. Baseline Comparison

A baseline scenario should be established before evaluating candidate pressure-control schedules.

Let:

- \(V_{\mathrm{base}}\) be baseline simulated leakage volume.
- \(V_{\mathrm{candidate}}\) be candidate simulated leakage volume.

The relative modeled leakage change may be calculated as:

\[
R_{\mathrm{leak}}
=
\frac{
V_{\mathrm{base}}-V_{\mathrm{candidate}}
}{
V_{\mathrm{base}}
}
\times100\%
\]

This calculation is meaningful only when:

- Both scenarios use comparable simulation horizons.
- Both scenarios use consistent demand assumptions.
- Both scenarios use comparable leakage parameters.
- Both simulations are valid.
- Baseline leakage is greater than zero.

A positive value indicates a reduction in modeled leakage relative to the baseline.

It does not establish real-world water savings.

---

## 13. Parameter Consistency

The following parameters must be recorded for each scenario:

| Parameter | Required documentation |
|---|---|
| Leakage coefficient | Value, units, and source |
| Leakage exponent | Value and justification |
| Pressure thresholds | Values and rationale |
| PRV settings | Six candidate values |
| Critical pressure limits | Junction-specific requirements |
| Demand patterns | Time-dependent inputs |
| Simulation duration | Start, end, and time steps |
| Network configuration | Input model and version |

If the leakage exponent is changed, the emitter coefficient must be reviewed.

Keeping the coefficient fixed while changing the exponent can change the modeled leakage relationship substantially.

Where comparisons require a common reference leakage rate, coefficients should be normalized against a documented reference pressure.

---

## 14. Reproducibility Requirements

Each evaluated candidate schedule should have a unique identifier.

The stored record should include:

- Scenario identifier.
- Schedule identifier.
- Four selected PRV settings.
- Simulation status.
- Total simulated leakage volume.
- Lower-tail service equity indicator.
- Critical-pressure constraint status.
- Model configuration.
- Parameter set.
- Warnings and error details.

This information is required to reproduce and audit future optimization results.

---

## 15. Mathematical Model Limitations

The proposed formulation is subject to the limitations of its hydraulic model.

These include:

1. Uncertain network input data.
2. Uncalibrated leakage coefficients.
3. Uncertain pressure exponents.
4. Simplified pressure-dependent demand assumptions.
5. PRV placement and alternate flow-path limitations.
6. Numerical simulation and convergence limitations.
7. Sensitivity to time aggregation and percentile calculation.
8. Differences between modeled and real-world network behavior.

The mathematical formulation alone does not demonstrate performance.

Simulation, testing, and appropriate validation evidence are required.

---

## 16. Final Mathematical Principle

PressureWise-Fair treats pressure management as a multi-objective problem.

The intended optimization is not simply:

**Minimize leakage.**

It is:

**Minimize modeled leakage while protecting the demand satisfaction of the least-served locations, subject to hydraulic and pressure constraints.**

---

*End of Mathematical Model Specification.*
