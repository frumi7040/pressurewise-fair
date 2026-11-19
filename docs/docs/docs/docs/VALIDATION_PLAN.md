# PressureWise-Fair — Validation Plan

**Document type:** Testing, Verification, and Validation Strategy  
**Project:** PressureWise-Fair  
**Version:** 1.0

> **Current status:** This document defines planned validation procedures. The tests below are not claimed to have been executed or passed.

---

## 1. Purpose

The purpose of this validation plan is to establish how PressureWise-Fair will be tested before any technical performance claims are made.

The project proposes to combine hydraulic simulation, pressure-driven leakage modeling, PRV-based pressure control, and equity-aware optimization.

Each component must be evaluated independently before its outputs are used in an overall optimization result.

The validation process is designed to prevent:

- Incorrect hydraulic model configurations.
- Leakage being counted as customer-delivered water.
- Incorrect PRV behavior or placement assumptions.
- Invalid optimization candidates.
- Misleading equity measurements.
- Unsupported water-saving claims.

---

## 2. Validation Principles

All validation activities must follow these principles:

1. **Reproducibility:** A test must be repeatable using documented inputs and parameters.
2. **Traceability:** Every result must be linked to its model configuration.
3. **Separation of evidence:** Proposed, implemented, tested, and validated components must be distinguished.
4. **Physical consistency:** Hydraulic outputs must be interpreted using appropriate engineering assumptions.
5. **Transparent failures:** Failed simulations and unsuccessful tests must be recorded.
6. **No fabricated results:** Missing evidence must be reported as missing, not estimated or invented.

---

## 3. Validation Architecture

The proposed validation sequence contains seven gates.

| Gate | Validation area |
|---|---|
| V1 | Network input and configuration |
| V2 | Baseline hydraulic simulation |
| V3 | Leakage model |
| V4 | Customer demand accounting |
| V5 | PRV operation and placement |
| V6 | Schedule generation and optimization |
| V7 | Pareto analysis and reproducibility |

A later gate should not be treated as validated if it depends on an earlier component that has not passed its required checks.

---

## 4. V1 — Network Input Validation

### Objective

Confirm that the selected network model is structurally consistent and uses valid inputs.

### Required checks

- Junction identifiers are unique.
- Pipe identifiers are unique.
- Pipe endpoints reference existing nodes.
- Pipe lengths and diameters are valid.
- Network units are documented.
- Supply sources and boundary conditions are defined.
- Demand patterns are correctly referenced.
- Leakage locations are explicitly identified.
- PRV candidate locations are valid network locations.

### Evidence to record

- Network input file.
- Model configuration.
- Input validation report.
- List of warnings or missing values.

### Pass criteria

All required input data are present and structurally consistent. Unresolved critical errors prevent the model from proceeding.

---

## 5. V2 — Baseline Hydraulic Simulation

### Objective

Establish a valid baseline simulation before pressure-control optimization.

### Proposed procedure

1. Load the configured network.
2. Confirm the hydraulic simulation settings.
3. Run the baseline using the selected EPANET 2.2 simulation workflow.
4. Check simulation completion.
5. Inspect pressure and flow outputs.
6. Check for non-convergence or invalid hydraulic conditions.
7. Preserve the simulation configuration and outputs.

### Evidence to record

- Baseline model file.
- Software versions.
- Simulation configuration.
- Simulation status.
- Hydraulic output files.
- Warnings and error logs.

### Pass criteria

The baseline simulation completes successfully, produces interpretable outputs, and has no unresolved critical modeling errors.

A successful run alone does not establish that the model accurately represents a real water distribution network.

---

## 6. V3 — Leakage Model Validation

### Objective

Verify that emitter-based leakage is represented consistently with the specified pressure relationship.

### Mathematical relationship

\[
Q_{\mathrm{leak}}=Cp^{N_1}
\]

### Proposed procedure

1. Create a controlled test configuration.
2. Specify a documented emitter coefficient.
3. Specify a documented pressure exponent.
4. Run the controlled hydraulic test at defined pressure conditions.
5. Record emitter discharge.
6. Compare the recorded discharge against the expected relationship.
7. Repeat at additional pressure conditions.
8. Investigate discrepancies.

### Pass criteria

The measured model output agrees with the expected emitter relationship within a predefined numerical tolerance.

The tolerance must be selected and documented before testing.

### Evidence to record

- Test network configuration.
- Emitter coefficient and exponent.
- Applied pressure conditions.
- Expected discharge calculations.
- Simulated discharge values.
- Error calculations.
- Test outcome.

This gate verifies the configured emitter relationship. It does not independently validate real-world leakage calibration.

---

## 7. V4 — Customer Demand and Leakage Accounting

### Objective

Ensure that customer-delivered water is not confused with modeled leakage.

### Required distinction

The model must distinguish:

- Required customer demand.
- Delivered customer demand.
- Emitter discharge.
- Total modeled junction outflow, where applicable.

### Proposed procedure

1. Identify demand junctions.
2. Identify emitter locations.
3. Retrieve the relevant hydraulic outputs.
4. Separate emitter discharge from customer-delivered demand.
5. Calculate demand satisfaction ratios.
6. Check the calculations against controlled test cases.
7. Document how zero-demand intervals and junctions are handled.

### Demand Satisfaction Ratio

\[
DSR_i=
\frac{D_i^{\mathrm{del}}}
{D_i^{\mathrm{req}}}
\]

### Pass criteria

The accounting procedure correctly distinguishes customer delivery from leakage and produces consistent demand satisfaction calculations for the defined test cases.

### Evidence to record

- Junction classification.
- Raw simulation outputs.
- Emitter discharge records.
- Customer-demand accounting calculations.
- DSR calculation checks.

---

## 8. V5 — PRV Operation and Placement Validation

### Objective

Confirm that the proposed PRV model operates as intended and that its location is suitable for the modeled control objective.

### Part A — PRV behavior

Check:

- Valve configuration.
- Upstream pressure.
- Downstream pressure.
- Flow direction.
- Valve status.
- Response to different downstream pressure settings.

### Part B — Network placement

Check:

- Supply paths into the intended district.
- Alternative supply routes.
- Bypasses.
- Existing control valves.
- Critical downstream junctions.
- Hydraulic suitability of the proposed location.

### Pass criteria

The PRV behavior is consistent with its configured operating conditions, and the selected location is supported by a documented network-topology assessment.

A successful PRV behavior test alone does not establish district-wide control.

### Evidence to record

- PRV configuration.
- Network topology.
- Upstream and downstream outputs.
- Valve status.
- Flow-path assessment.
- Critical-junction pressure results.

---

## 9. V6 — Schedule Generation and Optimization Validation

### Objective

Verify that the proposed deterministic search evaluates the intended candidate schedules correctly.

### Schedule definition

Four operating periods and six candidate settings per period:

\[
6^4=1,296
\]

### Proposed procedure

1. Define the four operating periods.
2. Define the six candidate settings.
3. Generate all combinations.
4. Confirm the number of unique schedules.
5. Check for duplicate schedules.
6. Verify that every schedule has four settings.
7. Apply schedules to the hydraulic model.
8. Record successful and failed simulations separately.
9. Calculate objectives only for valid results.
10. Check critical-pressure constraints.

### Pass criteria

The schedule generator produces exactly 1,296 unique combinations for the defined four-period, six-setting configuration.

Every candidate has the correct structure, and failed simulations are not treated as valid optimization outcomes.

### Evidence to record

- Candidate setting definitions.
- Generated schedule list.
- Unique schedule count.
- Schedule identifiers.
- Simulation status for each candidate.
- Objective calculation records.

The number of generated schedules must not be confused with the number of successful simulations.

---

## 10. V7 — Pareto Analysis and Reproducibility

### Objective

Verify that objective calculations and Pareto comparisons are mathematically consistent.

### Proposed procedure

1. Select the feasible candidate records.
2. Confirm leakage values and units.
3. Confirm the lower-tail equity calculation.
4. Apply the defined dominance rule.
5. Identify non-dominated candidates.
6. Independently check selected dominance comparisons.
7. Reproduce the analysis using the saved input records.

### Pareto objectives

Minimize:

\[
V_{\mathrm{leak}}
\]

Maximize:

\[
E=P_{10}(DSR)
\]

### Pass criteria

The Pareto procedure correctly identifies non-dominated candidates from the verified feasible dataset and can be reproduced using saved inputs and documented calculations.

### Evidence to record

- Feasible candidate dataset.
- Objective values.
- Dominance-check records.
- Pareto candidate identifiers.
- Reproducibility instructions.

No Pareto result should be presented as an actual project finding until the supporting simulations and calculations exist.

---

## 11. Overall Validation Status

The project should maintain a validation register.

| Gate | Description | Current status |
|---|---|---|
| V1 | Network input validation | Planned |
| V2 | Baseline simulation | Planned |
| V3 | Leakage verification | Planned |
| V4 | Demand and leakage accounting | Planned |
| V5 | PRV validation | Planned |
| V6 | Schedule and optimization verification | Planned |
| V7 | Pareto and reproducibility verification | Planned |

A gate may be marked **Passed** only after its procedure has been executed and supporting evidence has been recorded.

---

## 12. Failure Handling

If a validation test fails:

1. Record the failure.
2. Preserve the relevant inputs and outputs.
3. Identify the affected module.
4. Investigate the cause.
5. Correct the configuration or implementation.
6. Repeat the affected test.
7. Record the new outcome.

Failed tests must not be silently removed from the evidence record.

---

## 13. Evidence Management

Every completed validation test should include:

- Test identifier.
- Date of execution.
- Software versions.
- Input configuration.
- Procedure.
- Expected behavior.
- Actual output.
- Pass/fail decision.
- Explanation of discrepancies.
- Supporting files or logs.

Results should be stored in the repository with clear filenames and links to the corresponding test.

---

## 14. Limitations of Validation

Even if all planned computational tests pass, this does not automatically establish:

- Accuracy for every real water distribution network.
- Calibration against field leakage measurements.
- Actual physical water savings.
- Improved real-world customer service.
- Suitability for operational utility deployment.

These claims require additional evidence appropriate to the claim being made.

---

## 15. Final Validation Principle

PressureWise-Fair must demonstrate its technical behavior through documented and reproducible tests.

The project will not treat a proposed method as a completed result, a successful simulation as field validation, or a modeled improvement as measured real-world impact.

**Credible engineering requires evidence, not assumptions.**

---

*End of Validation Plan.*
