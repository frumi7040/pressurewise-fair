# PressureWise-Fair

### Save Water. Protect Every Community.

**PressureWise-Fair** is a proposed software-based approach to equity-aware pressure management in water distribution networks. Its purpose is to investigate how pressure-driven water leakage can be reduced while protecting water service for communities that may already experience insufficient pressure.

> **Project status:** Technical concept and proposed design. Hydraulic simulations, optimization results, and field validation have not yet been completed or verified. No measured water savings or service improvements are claimed.

---

## 1. The Problem

Water distribution networks can lose treated freshwater through pipeline leakage. Excessive pressure can increase leakage, making pressure management an important water-conservation strategy.

However, simply reducing pressure across a network can create another problem: locations that already experience low pressure may receive even less water.

This creates two connected challenges:

- **Water loss:** Treated freshwater escapes through pipeline leaks.
- **Service inequality:** Poorly planned pressure reductions may worsen water access in already underserved locations.

PressureWise-Fair explores how these two challenges can be addressed together.

## 2. Our Core Idea

Instead of optimizing pressure reduction solely to minimize leakage, PressureWise-Fair proposes evaluating two competing objectives:

1. Minimize simulated pipeline leakage.
2. Protect demand satisfaction in poorly served areas.

The guiding principle is:

**Save water without making water access worse for the communities that already receive the least.**

## 3. Proposed Technical Architecture

The proposed system uses the following components:

| Component | Purpose |
|---|---|
| EPANET 2.2 | Hydraulic network simulation |
| WNTR | Python-based water network modeling and analysis |
| Pressure-dependent demand | Represent customer demand as pressure changes |
| Emitter-based leakage | Estimate pressure-driven leakage |
| Pressure Reducing Valve (PRV) | Model controlled downstream pressure |
| Deterministic search | Evaluate candidate pressure schedules |
| Pareto analysis | Examine leakage and equity trade-offs |

No AI or machine-learning optimizer is proposed.

## 4. Hydraulic Modeling

The proposed hydraulic model uses EPANET 2.2 through WNTR.

It represents:

- Network junctions and elevations.
- Pipes and hydraulic characteristics.
- Customer demand.
- Pressure-dependent demand behavior.
- Pressure-driven leakage.
- Pressure control through a candidate PRV.

The model must be configured with appropriate network data, demand assumptions, pressure parameters, and boundary conditions before meaningful results can be reported.

## 5. Leakage Modeling

Pressure-driven leakage is represented using an emitter relationship:

`Q_leak = C × p^N1`

Where:

- `Q_leak` = modeled leakage flow.
- `C` = emitter coefficient.
- `p` = pressure head at the leakage location.
- `N1` = pressure exponent.

The coefficient, exponent, units, and leakage locations must be specified and justified for each scenario.

## 6. Pressure Control Strategy

The proposed approach introduces a Pressure Reducing Valve (PRV) at a suitable district inlet.

The PRV is intended to regulate downstream pressure while allowing the system to examine how different pressure settings affect leakage and customer service.

An important modeling requirement is that the relevant supply paths must pass through the controlled PRV. Bypasses and alternative supply routes must be identified before evaluating district-level pressure control.

## 7. Daily Optimization Schedule

The proposed schedule evaluates:

- Four daily operating periods.
- Six candidate PRV settings per period.

The total number of possible schedules is:

`6 × 6 × 6 × 6 = 1,296`

These represent possible schedules per scenario, not verified improvements.

A deterministic exhaustive search is proposed to evaluate the candidate schedules.

## 8. Measuring Water Service Equity

PressureWise-Fair proposes using the Demand Satisfaction Ratio (DSR):

`DSR_i = Delivered Customer Demand_i / Required Customer Demand_i`

The proposed equity indicator is the 10th percentile of demand-junction DSR values.

This lower-tail measure helps evaluate whether the least-served portions of the modeled network experience unacceptable deterioration.

**Important:** Customer-delivered demand must be separated from emitter discharge. Leakage must not be counted as water delivered to customers.

## 9. Minimum Pressure Protection

The proposed optimization also includes minimum-pressure constraints at designated critical junctions.

These constraints are intended to prevent pressure-control strategies from violating specified service requirements.

The thresholds must be selected and justified for the network under study; they are not universal values.

## 10. Comparing Competing Strategies

The proposed system uses Pareto analysis to examine the relationship between:

- Simulated leakage reduction.
- Demand satisfaction and service equity.

Rather than assuming that one strategy is best in every respect, the analysis will identify trade-offs between water conservation and equitable service.

Any future Pareto graph must be generated from actual, documented simulation outputs. Illustrative diagrams must be labeled conceptual.

## 11. Validation Plan

Before optimization results can be considered credible, the following checks are required:

1. **Baseline simulation:** Confirm that the selected hydraulic network runs and produces interpretable results.
2. **Emitter isolation:** Verify emitter discharge against the specified leakage relationship in a controlled test.
3. **Demand and leakage accounting:** Confirm that customer delivery and emitter flow are separated consistently.
4. **PRV behavior:** Check valve operation, flow, and downstream pressure response.
5. **Network suitability:** Verify PRV placement, alternative flow paths, pressure constraints, and simulation convergence.
6. **Optimization verification:** Reproduce schedule counts, objective calculations, and Pareto comparisons from saved model inputs and outputs.

**Current validation status:** These checks are planned. They are not represented as completed or passed.

## 12. Project Status

The repository will distinguish between three evidence levels:

- **Proposed:** Included in the design but not yet implemented.
- **Implemented:** A component has been built, but may not have passed validation.
- **Validated:** A defined test has been completed and supporting evidence is documented.

This distinction is essential to maintaining technical accuracy and transparency.

## 13. Long-Term Vision

PressureWise-Fair aims to explore a more responsible approach to water distribution pressure management.

Its long-term objective is to help decision-makers consider water conservation and equitable service together, rather than treating leakage reduction as the only measure of success.

**PressureWise-Fair — Save Water. Protect Every Community.**
