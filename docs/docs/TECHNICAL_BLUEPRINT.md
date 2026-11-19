# PressureWise-Fair — Technical Blueprint

**Document type:** Proposed System Architecture and Engineering Specification  
**Project:** PressureWise-Fair  
**Version:** 1.0  
**Category:** Water Quantity

> **Implementation status:** This document defines the proposed technical architecture. It is not evidence that the complete system has been implemented, simulated, or validated.

---

## 1. System Overview

PressureWise-Fair is designed as a software-based hydraulic analysis and optimization framework.

Its purpose is to evaluate pressure-management strategies that reduce modeled water leakage while protecting customer demand satisfaction across a water distribution network.

The proposed architecture consists of six major modules:

1. Network Data and Configuration
2. Hydraulic Model Preparation
3. Leakage and Demand Simulation
4. PRV Control and Schedule Generation
5. Equity-Aware Optimization
6. Validation and Results Analysis

The modules are intended to operate as a reproducible computational pipeline.

---

## 2. High-Level Architecture

```text
       NETWORK INPUT DATA
                |
                v
      NETWORK CONFIGURATION
                |
                v
       HYDRAULIC MODEL
        EPANET 2.2 + WNTR
                |
                v
      BASELINE SIMULATION
                |
                v
    DEMAND AND LEAKAGE ANALYSIS
                |
                v
       PRV CONTROL MODEL
                |
                v
      SCHEDULE GENERATOR
       4 periods × 6 settings
                |
                v
       1,296 CANDIDATE
           SCHEDULES
                |
                v
      HYDRAULIC EVALUATION
                |
                v
       OBJECTIVE CALCULATION
          /           \
         v             v
    SIMULATED       SERVICE
     LEAKAGE         EQUITY
         \             /
          v           v
         PARETO ANALYSIS
                |
                v
       VALIDATION AND REPORT
```

This is the proposed logical architecture, not a representation of a completed software implementation.

---

## 3. Module 1 — Network Data and Configuration

### Purpose

Define the water distribution network and its operating assumptions before simulation.

### Required inputs

| Input | Description |
|---|---|
| Junction data | Node identifiers, elevations, and demands |
| Pipe data | Connectivity, length, diameter, and roughness |
| Supply data | Reservoirs, tanks, and boundary conditions |
| Pump data | Pump characteristics and operating controls |
| Valve data | Existing valve configuration |
| Demand patterns | Time-dependent customer demand |
| Leakage assumptions | Candidate leakage locations and parameters |
| PRV configuration | Candidate location and operating settings |

### Input validation

Before simulation, the model should check:

- Unique network identifiers.
- Valid pipe endpoint references.
- Positive pipe lengths and diameters.
- Valid junction and supply connections.
- Consistent units.
- Defined operating patterns.
- Valid leakage and pressure parameters.

Missing or inconsistent inputs should cause the model to stop or flag the affected scenario rather than silently inventing values.

---

## 4. Module 2 — Hydraulic Model Preparation

### Proposed technology

- EPANET 2.2
- WNTR
- Python

WNTR is intended to prepare, inspect, and manage the network model.

The EPANET hydraulic simulation interface is intended to use WNTR's `EpanetSimulator` when the selected model features are supported by the installed software versions.

### Hydraulic model requirements

The model should represent:

- Network connectivity.
- Elevation.
- Pipe hydraulic resistance.
- Water supply conditions.
- Time-varying demand.
- Pressure-dependent customer demand.
- Pressure-driven leakage.

### Pressure-dependent demand

Customer demand should respond to available pressure according to the selected pressure-dependent demand configuration.

The model must document the pressure thresholds and demand assumptions used.

The selected parameters must be appropriate to the scenario being studied; they should not be presented as universal constants.

---

## 5. Module 3 — Leakage Modeling

### Emitter relationship

The proposed leakage representation is:

\[
Q_{\text{leak}}=C p^{N_1}
\]

Where:

- \(Q_{\text{leak}}\) is emitter discharge.
- \(C\) is the emitter coefficient.
- \(p\) is pressure head.
- \(N_1\) is the pressure exponent.

### Implementation considerations

1. Leakage locations must be explicitly identified.
2. Emitter coefficients must be documented.
3. The pressure exponent must be justified.
4. Units must remain consistent.
5. Emitter discharge must be recorded separately from customer delivery.

### Important accounting rule

Hydraulic software may report junction demand that includes emitter discharge.

Therefore, customer-delivered demand must be reconstructed or obtained using a verified accounting method that separates customer demand from leakage.

Emitter flow must never be counted as water successfully delivered to customers.

---

## 6. Module 4 — PRV Control Model

### Purpose

Evaluate whether controlled downstream pressure can reduce modeled leakage without unacceptable deterioration in customer service.

### Proposed control device

A Pressure Reducing Valve (PRV) is considered at a suitable district inlet.

The PRV setting represents a downstream pressure target, expressed in the model's appropriate head units.

### Placement requirements

The proposed PRV location must be assessed against:

- Network topology.
- District boundaries.
- Upstream supply conditions.
- Downstream demand distribution.
- Alternative supply routes.
- Existing valves and control devices.

### Critical limitation

A PRV controls pressure only along hydraulic paths that it actually regulates.

If water can reach the intended district through bypasses or alternate feeds, a single PRV may not control the entire district.

The network must therefore be inspected before claiming district-wide pressure control.

### Operational checks

The PRV model should verify:

- Valve status.
- Flow direction.
- Upstream pressure.
- Downstream pressure.
- Pressure-setting response.
- Interaction with other hydraulic controls.

A successful valve smoke test alone does not prove that the selected location is suitable for the entire district.

---

## 7. Module 5 — Daily Schedule Generation

### Schedule structure

The proposed control strategy divides a day into four operating periods.

Each period has six candidate PRV settings.

The number of candidate schedules is:

\[
N_{\text{schedules}}=6^4=1,296
\]

### Schedule representation

A candidate schedule can be represented as:

\[
S=(s_1,s_2,s_3,s_4)
\]

Where each \(s_j\) is selected from the six candidate settings for period \(j\).

### Exhaustive search

The proposed algorithm generates every valid combination and evaluates it against the configured hydraulic model.

No machine-learning prediction or AI-based optimization is required.

### Important distinction

The 1,296 figure represents the number of possible combinations per scenario.

It does not represent 1,296 successful simulations, 1,296 improvements, or verified water savings.

---

## 8. Module 6 — Objective Calculation

Each candidate schedule is intended to be evaluated using two objectives.

### Objective A: Minimize simulated leakage

For a simulation horizon, calculate total modeled leakage using emitter discharge over time.

The integration or summation method must account for simulation time steps and flow units.

### Objective B: Protect service equity

For every demand junction, calculate:

\[
DSR_i=
\frac{D_{\text{customer},i}}
{D_{\text{required},i}}
\]

Where:

- \(D_{\text{customer},i}\) is delivered customer demand.
- \(D_{\text{required},i}\) is required customer demand.

The proposed equity indicator is:

\[
E=P_{10}(DSR_1,DSR_2,\ldots,DSR_n)
\]

The 10th percentile measures lower-tail demand satisfaction.

The implementation must define how zero-demand junctions and time-varying demand are handled.

### Minimum-pressure constraints

Designated critical junctions must satisfy their specified minimum-pressure requirements.

The thresholds must be selected and justified before optimization.

---

## 9. Module 7 — Pareto Analysis

PressureWise-Fair proposes a two-objective comparison:

- Minimize total simulated leakage.
- Maximize lower-tail demand satisfaction.

A schedule is Pareto-dominated if another feasible schedule is at least as good in both objectives and strictly better in at least one.

The non-dominated schedules form the Pareto set.

### Expected output

The proposed analysis may include:

- Candidate schedule identifier.
- Total simulated leakage.
- Lower-tail demand satisfaction.
- Critical-junction pressure checks.
- Feasibility status.
- Pareto membership.

No actual Pareto results should be published until the corresponding simulations have been completed and verified.

---

## 10. Simulation and Evaluation Pipeline

The proposed execution sequence is:

1. Load the configured network.
2. Validate network data and units.
3. Configure pressure-dependent demand.
4. Configure leakage emitters.
5. Run a baseline hydraulic simulation.
6. Check baseline simulation validity.
7. Configure the candidate PRV.
8. Generate the 1,296 schedules.
9. Apply each schedule to an appropriate model configuration.
10. Run hydraulic evaluation.
11. Reject failed or invalid simulations.
12. Separate customer demand from emitter discharge.
13. Calculate leakage and demand satisfaction.
14. Check minimum-pressure constraints.
15. Store valid candidate results.
16. Identify non-dominated schedules.
17. Produce reproducible analysis outputs.

### Simulation failure handling

A failed or non-convergent run must not be treated as a valid optimization result.

The system should record:

- Schedule identifier.
- Scenario identifier.
- Simulation status.
- Failure or warning details.
- Relevant configuration.

---

## 11. Proposed Software Organization

The following is a proposed future implementation structure:

```text
pressurewise-fair/
│
├── README.md
│
├── docs/
│   ├── PROJECT_OVERVIEW.md
│   ├── TECHNICAL_BLUEPRINT.md
│   ├── MATHEMATICAL_MODEL.md
│   ├── VALIDATION_PLAN.md
│   └── LIMITATIONS.md
│
├── model/
│   └── README.md
│
├── tests/
│   └── README.md
│
├── results/
│   └── README.md
│
└── requirements.txt
```

The directory structure is a proposed organization. It does not imply that the simulation modules or tests have already been implemented.

---

## 12. Reproducibility Requirements

Every future simulation result should be traceable to:

- Network input file.
- EPANET version.
- WNTR version.
- Python version.
- Model parameters.
- Demand patterns.
- Leakage assumptions.
- PRV placement and settings.
- Simulation duration and time steps.
- Schedule identifier.
- Simulation warnings and status.
- Post-processing method.

Results should be stored in a structured format such as CSV or JSON, with the configuration needed to reproduce them.

---

## 13. Validation Boundaries

The following statements must remain distinct:

| Evidence level | Meaning |
|---|---|
| Proposed | Included in the technical design |
| Implemented | Code or configuration exists |
| Tested | A defined test was executed |
| Validated | Test evidence supports the specified behavior |
| Field-validated | Evidence was obtained from a real operating network |

A successful simulation does not establish real-world performance.

A modeled reduction in leakage does not establish measured physical water savings.

A modeled improvement in demand satisfaction does not establish improved service for actual communities.

---

## 14. Technical Risks and Limitations

Potential risks include:

1. Incomplete or inaccurate network data.
2. Uncalibrated leakage parameters.
3. Incorrect PRV placement.
4. Unmodeled bypasses and alternate feeds.
5. Pressure-dependent demand parameter uncertainty.
6. Simulation convergence failures.
7. Incorrect customer-demand and leakage accounting.
8. Excessive computation time for larger scenario sets.
9. Differences between modeled and real network behavior.

These risks must be assessed before drawing conclusions.

---

## 15. Expected Technical Outcome

If implemented and validated, the proposed framework should produce a reproducible comparison of candidate pressure-control schedules.

Its intended output is not simply a single leakage-minimizing schedule.

It is a set of feasible alternatives that reveal the trade-offs between modeled water conservation and equitable customer service.

**PressureWise-Fair aims to make equity a measurable part of pressure optimization.**

---

*End of Technical Blueprint.*
