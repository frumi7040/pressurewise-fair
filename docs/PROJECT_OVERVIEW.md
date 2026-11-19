# PressureWise-Fair — Project Overview

**Project title:** PressureWise-Fair  
**Tagline:** Save Water. Protect Every Community.  
**Category:** Water Quantity  
**Project type:** Software-based hydraulic modeling and optimization concept  
**Proposed tools:** EPANET 2.2, WNTR, Python  
**Optimization approach:** Deterministic exhaustive search

---

## 1. Executive Summary

PressureWise-Fair is a proposed equity-aware pressure management approach for water distribution networks.

Water utilities must manage pipeline leakage while maintaining sufficient water pressure for customers. Reducing excessive pressure can help limit leakage, but pressure reductions can also negatively affect locations that already experience inadequate service.

PressureWise-Fair explores how these competing concerns can be evaluated together.

The proposed system uses hydraulic simulation to investigate pressure-dependent customer demand, pressure-driven leakage, and controlled pressure reduction through a Pressure Reducing Valve (PRV).

It evaluates candidate daily pressure-control schedules against two objectives:

1. Reduce simulated water leakage.
2. Protect water service equity, particularly in the least-served portions of the modeled network.

The project proposes deterministic optimization and Pareto analysis to examine the trade-offs between these objectives.

Its central principle is:

> Water conservation should not come at the expense of communities that already receive insufficient service.

**Evidence status:** This document describes a proposed technical approach. Hydraulic simulations, optimization outcomes, and field validation have not yet been completed or verified.

---

## 2. Background and Motivation

Water distribution systems are designed to transport treated water from supply sources to consumers through interconnected pipes, pumps, valves, tanks, and junctions.

One challenge is water lost through leakage.

Pipeline leakage can be influenced by operating pressure. In many modeled leakage relationships, higher pressure produces greater leakage.

Pressure management can therefore be an important component of water-loss reduction.

However, a water distribution network does not provide identical service conditions everywhere.

Pressure can vary because of:

- Elevation differences.
- Distance from supply sources.
- Pipe friction and hydraulic resistance.
- Demand variation.
- Network configuration.
- Pump and valve operating conditions.

A pressure reduction that appears beneficial at the network level may negatively affect vulnerable locations.

This creates the need for an approach that evaluates water conservation and service equity together.

---

## 3. Problem Statement

Conventional leakage-focused pressure optimization can overlook how pressure reductions affect different customer locations.

A strategy that minimizes total modeled leakage may not necessarily preserve adequate customer demand satisfaction throughout the network.

The project investigates the following problem:

**How can pressure-management strategies reduce simulated pipeline leakage while protecting the demand satisfaction of poorly served locations in a water distribution network?**

This question forms the foundation of PressureWise-Fair.

---

## 4. Project Objectives

### Primary objective

Develop and evaluate a proposed hydraulic optimization framework that considers both simulated leakage reduction and equitable customer service.

### Supporting objectives

1. Represent water distribution network behavior using hydraulic simulation.
2. Model pressure-dependent customer demand.
3. Represent pressure-driven leakage using emitter-based modeling.
4. Evaluate controlled pressure reduction through a suitable PRV.
5. Compare different pressure-control schedules across daily operating periods.
6. Measure demand satisfaction across network junctions.
7. Give particular attention to the lower-performing portion of the network.
8. Identify trade-offs between leakage and service equity through Pareto analysis.
9. Establish a transparent validation process for future implementation.

---

## 5. Proposed System Concept

PressureWise-Fair is organized around five connected stages.

### Stage 1 — Network Representation

Represent the selected water distribution network using:

- Junctions.
- Pipes.
- Water demands.
- Elevations.
- Hydraulic characteristics.
- Supply and operating conditions.

### Stage 2 — Hydraulic Simulation

Use EPANET 2.2 through WNTR to investigate:

- Pressure distribution.
- Customer demand satisfaction.
- Network flow behavior.
- Pressure-driven leakage.

### Stage 3 — Controlled Pressure Reduction

Introduce a candidate Pressure Reducing Valve at a suitable district inlet.

Evaluate different downstream pressure settings while checking that the valve actually controls the intended supply paths.

### Stage 4 — Schedule Evaluation

Consider four daily operating periods, with six candidate PRV settings in each period.

The number of possible schedules is:

\[
6^4 = 1,296
\]

A deterministic exhaustive search is proposed to evaluate these schedules for each scenario.

### Stage 5 — Equity-Aware Comparison

Compare candidate schedules using:

- Simulated leakage.
- Customer demand satisfaction.
- Lower-tail service equity.
- Minimum-pressure constraints.

Use Pareto analysis to examine the competing objectives.

---

## 6. Proposed Technical Components

| Component | Role |
|---|---|
| EPANET 2.2 | Hydraulic simulation engine |
| WNTR | Python interface for water network modeling |
| Pressure-dependent demand | Represents demand response to pressure |
| Emitter model | Represents pressure-driven leakage |
| PRV | Represents controlled downstream pressure |
| Python | Proposed implementation environment |
| Exhaustive search | Evaluates candidate daily schedules |
| Pareto analysis | Compares competing objectives |

The proposed approach does not depend on an AI or machine-learning optimizer.

---

## 7. Key Performance Indicators

### 7.1 Simulated leakage

The proposed leakage relationship is:

\[
Q_{\text{leak}}=C p^{N_1}
\]

Where:

- \(Q_{\text{leak}}\) is modeled leakage flow.
- \(C\) is the emitter coefficient.
- \(p\) is pressure head.
- \(N_1\) is the leakage pressure exponent.

The selected coefficient, exponent, units, and leakage locations must be documented for each scenario.

### 7.2 Demand Satisfaction Ratio

For each demand junction:

\[
DSR_i =
\frac{\text{Delivered Customer Demand}_i}
{\text{Required Customer Demand}_i}
\]

This indicator represents the proportion of required customer demand delivered in the model.

Emitter discharge must be excluded from customer-delivered demand.

### 7.3 Lower-tail service equity

The proposed equity indicator is:

\[
E = P_{10}(DSR_1,DSR_2,\ldots,DSR_n)
\]

Where \(P_{10}\) represents the 10th percentile of demand-junction DSR values.

This indicator focuses attention on the lower-performing portion of the modeled network.

### 7.4 Minimum-pressure protection

Critical junctions must satisfy their specified minimum-pressure constraints.

These thresholds must be justified using the selected network and applicable service requirements.

---

## 8. Proposed Optimization Strategy

PressureWise-Fair proposes a two-objective optimization problem.

**Objective A:** Minimize simulated leakage.

**Objective B:** Protect lower-tail demand satisfaction.

Subject to:

- Hydraulic feasibility.
- PRV operating constraints.
- Critical-junction minimum-pressure requirements.
- Valid network topology and boundary conditions.
- Consistent demand and leakage accounting.

The optimization should not assume that minimizing leakage alone produces the best overall outcome.

Instead, Pareto analysis will be used to examine the trade-offs between leakage reduction and service equity.

---

## 9. Important Technical Considerations

The project must address the following issues before reporting reliable results:

1. **PRV placement:** The relevant district supply paths must pass through the controlled PRV.
2. **Alternative flow paths:** Bypasses and additional supply connections must be identified.
3. **Customer and leakage accounting:** Emitter discharge must not be counted as customer-delivered water.
4. **Pressure-dependent demand:** Model parameters must be selected and documented.
5. **Leakage calibration:** Emitter coefficients and exponents must be justified.
6. **Simulation convergence:** Failed or non-convergent runs must not be treated as valid optimization outcomes.
7. **Reproducibility:** Inputs, parameter choices, schedules, and outputs must be preserved.

---

## 10. Project Scope

### Included in the proposed scope

- Software-based hydraulic analysis.
- EPANET 2.2 and WNTR.
- Pressure-dependent demand modeling.
- Emitter-based leakage modeling.
- PRV-based pressure control.
- Four-period daily schedules.
- Deterministic exhaustive search.
- Demand satisfaction analysis.
- Lower-tail equity measurement.
- Pareto trade-off analysis.

### Outside the current verified scope

- Physical installation of PRVs.
- Live utility network integration.
- Field measurements.
- Deployment in an operating water distribution network.
- Verified real-world water savings.
- Verified improvements in customer service.

These may be considered future directions, but they are not established project achievements.

---

## 11. Validation Roadmap

The proposed validation process consists of:

| Gate | Required evidence |
|---|---|
| Baseline hydraulic model | Successful, interpretable baseline simulation |
| Leakage verification | Controlled emitter-flow check |
| Demand accounting | Separation of customer demand and emitter discharge |
| PRV verification | Demonstrated valve behavior and pressure response |
| Network suitability | Verified placement, flow paths, and constraints |
| Optimization verification | Reproducible schedule evaluation and objective calculations |
| Pareto analysis | Trade-off analysis generated from verified simulation outputs |

**Current status:** These are planned validation activities. No gate is claimed as passed.

---

## 12. Expected Contribution

The intended contribution of PressureWise-Fair is a framework for evaluating pressure management using two connected perspectives:

- How much modeled water is lost through leakage?
- What happens to customer service, particularly in the least-served locations?

By explicitly including service equity in the proposed optimization process, the project seeks to make water conservation more responsible and transparent.

---

## 13. Conclusion

PressureWise-Fair explores a central challenge in water distribution management: reducing water loss without worsening unequal access.

It proposes combining hydraulic simulation, controlled pressure reduction, deterministic schedule evaluation, and equity-aware performance measurement.

The project is guided by one principle:

**Saving water matters. Protecting equitable access to water matters just as much.**

---

*PressureWise-Fair — Save Water. Protect Every Community.*
