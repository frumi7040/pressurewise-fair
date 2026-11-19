# PressureWise-Fair — Limitations and Assumptions

**Document type:** Engineering Scope, Assumptions, and Limitations  
**Project:** PressureWise-Fair  
**Version:** 1.0

> **Current status:** This document describes the limitations and assumptions of the proposed approach. It does not imply that the system has been fully implemented, simulated, or validated.

---

## 1. Purpose

PressureWise-Fair proposes an equity-aware approach to pressure management in water distribution networks.

Like any computational engineering approach, its reliability depends on the quality of its input data, mathematical assumptions, hydraulic model, and validation procedures.

This document identifies the current scope, assumptions, uncertainties, and limitations that must be considered before interpreting any future results.

---

## 2. Current Project Status

PressureWise-Fair is documented as a proposed technical concept and system architecture.

The repository currently contains design and specification documents.

The following achievements are not claimed:

- A completed hydraulic simulation.
- A calibrated leakage model.
- A validated PRV installation location.
- A completed 1,296-schedule optimization.
- Verified Pareto-frontier results.
- Measured water savings.
- Field validation.
- Deployment in a real water distribution network.

These activities require implementation and supporting evidence.

---

## 3. Network Data Limitations

The quality of hydraulic simulation depends heavily on the quality of network information.

Potential input limitations include:

- Inaccurate pipe lengths or diameters.
- Missing network connections.
- Incorrect elevation data.
- Uncertain pipe roughness.
- Incomplete valve information.
- Inaccurate demand patterns.
- Unknown operating conditions.
- Missing leakage-location information.

An incomplete network model may produce misleading pressure and flow estimates.

### Required response

Future implementations should document input sources, units, assumptions, missing information, and data-quality limitations.

---

## 4. Leakage Model Limitations

The proposed emitter-based relationship is:

\[
Q_{\mathrm{leak}}=Cp^{N_1}
\]

This relationship is a simplified representation of pressure-driven leakage.

Its reliability depends on:

- Emitter coefficient selection.
- Pressure exponent selection.
- Pressure units.
- Leakage-location assumptions.
- Calibration evidence.
- Consistency across scenarios.

A model using assumed emitter coefficients does not automatically represent actual physical leakage.

If the pressure exponent changes, the coefficient must also be reviewed because the resulting leakage relationship can change.

### Required response

Future implementations should clearly distinguish assumed parameters from measured or calibrated parameters.

---

## 5. Pressure-Dependent Demand Limitations

Pressure-dependent demand modeling estimates how customer delivery changes as available pressure changes.

However, actual customer water consumption can also depend on factors that are not represented by a simplified hydraulic model.

These may include:

- Household storage tanks.
- Local pumping systems.
- Intermittent supply.
- Customer-side plumbing.
- Behavioral changes.
- Local distribution arrangements.

Therefore, modeled demand satisfaction should not automatically be interpreted as measured household water access.

### Required response

The selected pressure-response function and parameters must be documented, justified, and tested for the intended network.

---

## 6. PRV Placement and Control Limitations

A Pressure Reducing Valve regulates pressure along the hydraulic paths it controls.

A single PRV may not regulate an entire district if alternative supply routes or bypasses exist.

Potential limitations include:

- Incorrect candidate placement.
- Multiple supply paths.
- Existing control valves.
- Variable upstream pressure.
- Interactions with pumps and tanks.
- Hydraulic changes over time.

### Required response

The proposed PRV location must undergo a network-topology and hydraulic suitability assessment.

A successful valve test alone does not establish district-wide pressure control.

---

## 7. Optimization Limitations

The proposed search evaluates:

\[
6^4=1,296
\]

possible schedules for four operating periods with six candidate settings per period.

This number represents candidate combinations, not guaranteed valid simulations.

The optimization is limited by:

- The selected candidate pressure settings.
- The number of operating periods.
- Hydraulic simulation runtime.
- Simulation convergence.
- Model accuracy.
- Parameter uncertainty.
- The chosen objective functions.

A different candidate setting range or schedule structure could produce different outcomes.

The proposed exhaustive search is intended for transparent evaluation of a defined candidate space, not proof of a globally optimal real-world operating policy.

---

## 8. Service Equity Measurement Limitations

The proposed equity indicator is:

\[
E=P_{10}(DSR)
\]

This lower-tail percentile helps identify poor demand satisfaction among modeled demand junctions.

However, it has limitations:

- A junction is not necessarily equivalent to a household or person.
- Junctions may represent different numbers of customers.
- The 10th percentile can hide individual extreme cases.
- Results depend on how junctions are selected.
- Time aggregation can change the interpretation.
- A higher percentile does not guarantee that every customer receives adequate service.

### Required response

Future analyses should document junction selection, demand weighting decisions, time aggregation, and the handling of zero-demand locations.

Where appropriate, additional indicators may be considered to investigate individual critical locations.

---

## 9. Pareto Analysis Limitations

Pareto analysis identifies non-dominated alternatives under the selected objectives and constraints.

It does not independently decide which alternative is socially, economically, or operationally best.

The final selection may require additional considerations such as:

- Utility operating priorities.
- Customer service requirements.
- Infrastructure constraints.
- Cost.
- Reliability.
- Local policy.
- Risk tolerance.

The Pareto frontier will only be meaningful when based on valid and comparable simulation results.

---

## 10. Simulation Limitations

Hydraulic simulation is a mathematical representation of a physical system.

Its outputs depend on the accuracy of the network model, parameter choices, boundary conditions, and numerical methods.

Potential issues include:

- Non-convergence.
- Invalid hydraulic configurations.
- Incorrect control logic.
- Uncertain demand conditions.
- Numerical tolerances.
- Incomplete representation of real operating conditions.

A successful simulation is evidence that a model run completed. It is not proof that the model accurately represents a real network.

---

## 11. Real-World Deployment Limitations

The current proposed scope is software-based.

It does not include verified:

- Physical PRV installation.
- Live network control.
- Real-time monitoring.
- Utility-system integration.
- Field leakage measurements.
- Customer-level service measurements.

Operational deployment would require additional engineering review, safety procedures, utility authorization, field evidence, and appropriate operational safeguards.

No automated pressure adjustment should be applied to a real network based solely on unvalidated model outputs.

---

## 12. Assumptions Register

The following assumptions must be explicitly documented for every future scenario.

| Assumption | Required treatment |
|---|---|
| Network topology | Verify against available network information |
| Pipe characteristics | Record values, units, and sources |
| Customer demand | Document demand patterns and assumptions |
| Pressure response | Justify selected PDD parameters |
| Leakage behavior | Document emitter coefficients and exponent |
| PRV placement | Assess all relevant supply paths |
| Candidate settings | Record all six pressure settings |
| Operating periods | Define duration and transitions |
| Critical pressures | Specify junction-specific limits |
| Equity calculation | Document percentile and time aggregation |

Assumptions must not be presented as measured facts.

---

## 13. Future Improvements

Potential future development areas include:

1. Network-specific calibration using field measurements.
2. Sensitivity analysis for uncertain leakage parameters.
3. Evaluation of multiple PRV locations.
4. Investigation of alternate supply routes.
5. Additional service-equity indicators.
6. Scenario analysis for changing demand patterns.
7. Computational improvements for larger schedule spaces.
8. Independent engineering review.
9. Controlled comparison with operational data, where available.

These are possible future directions, not completed features.

---

## 14. Responsible Reporting Rules

All future reports and presentations should distinguish among:

- **Assumed:** A value or condition selected for modeling.
- **Simulated:** A result generated by a computational model.
- **Tested:** A defined test has been executed.
- **Validated:** Evidence supports the specified behavior within the defined scope.
- **Field-measured:** Evidence was collected from a real operating system.

A simulated improvement must not be described as a measured real-world improvement.

A proposed system must not be described as a deployed solution.

A completed document must not be described as a completed hydraulic implementation.

---

## 15. Conclusion

PressureWise-Fair addresses an important engineering trade-off: reducing water loss while protecting equitable customer service.

Its proposed framework provides a structured way to investigate this challenge, but the reliability of any future conclusion will depend on accurate modeling, justified assumptions, successful validation, and transparent reporting.

**The project's credibility depends not only on what it aims to achieve, but also on clearly documenting what it has and has not demonstrated.**

---

*End of Limitations and Assumptions.*
