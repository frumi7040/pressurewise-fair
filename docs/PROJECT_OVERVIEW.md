# PressureWise-Fair — Project Overview

**Project title:** PressureWise-Fair  
**Tagline:** Save Water. Protect Every Community.  
**Challenge area:** Water Quantity  
**Project type:** Software-based hydraulic modeling and optimization research prototype  
**Core tools:** EPANET 2.2, WNTR 1.5.0, Python  
**Optimization approach:** Deterministic exhaustive search; no AI/ML optimizer is used

## 1. Executive summary

PressureWise-Fair is a working research prototype for exploring equity-aware pressure management in water distribution networks. It evaluates modeled leakage together with customer demand satisfaction, with particular attention to the lower-performing portion of the modeled network.

Reducing excessive pressure can reduce pressure-driven leakage, but a pressure reduction can also reduce customer delivery at already disadvantaged locations. The prototype therefore evaluates two objectives together:

1. Minimize simulated leakage volume.
2. Protect lower-tail customer demand satisfaction.

The repository implements hydraulic simulation through EPANET/WNTR, emitter-based leakage accounting, time-varying pressure-reducing valve (PRV) schedules, candidate schedule evaluation, and Pareto comparison.

**Evidence boundary:** The implementation and automated workflow have been exercised using small synthetic test networks. These networks and their parameters are illustrative. The project has not been calibrated against utility data, field-validated, or deployed. No measured water savings or real-world service improvements are claimed.

## 2. Problem statement

A pressure-management strategy that minimizes total leakage alone may overlook the effect of pressure reduction on customers receiving inadequate service. PressureWise-Fair investigates how a modeled control strategy can be evaluated against both leakage and customer demand satisfaction, rather than treating leakage reduction as the only success criterion.

## 3. Implemented prototype workflow

1. Load an EPANET INP network through WNTR.
2. Use the pressure-dependent demand settings defined in the network input.
3. Assign EPANET emitters at selected junctions to represent pressure-driven leakage.
4. Apply time-varying PRV setpoints using WNTR time controls.
5. Run hydraulic simulations for candidate daily schedules.
6. Estimate customer-delivered demand by subtracting emitter discharge from EPANET-reported junction demand at emitter locations.
7. Calculate junction-level demand satisfaction ratios and their 10th percentile.
8. Integrate emitter discharge over time to estimate simulated leakage volume.
9. Filter schedules using the supplied minimum-pressure constraint and compare feasible schedules using Pareto analysis.

The optimizer is deterministic exhaustive enumeration. It is not an AI or machine-learning system.

## 4. Mathematical indicators

### Pressure-driven leakage

The generalized relationship is:

\[
Q_{leak}=C p^{N_1}
\]

The EPANET emitter implementation uses its configured emitter exponent. The current helper represents the standard square-root case:

\[
Q_{emitter}=C\sqrt{p}
\]

Flow and pressure units must remain consistent. WNTR uses flow in m^3/s and pressure head in metres.

### Customer-delivered demand and DSR

At an emitter junction, estimated customer delivery is calculated as:

\[
D_i^{del}(t)=D_i^{reported}(t)-Q_{emitter,i}(t)
\]

The demand satisfaction ratio is:

\[
DSR_i=\frac{\overline{D_i^{del}}}{D_i^{req}}
\]

The current schedule evaluator expects constant requested demand values per eligible junction. Demand-pattern-aware evaluation is not yet implemented in the schedule evaluator. The subtraction convention is an accounting assumption and requires independent validation before interpretation as actual customer delivery.

### Equity indicator

The lower-tail service indicator is the 10th percentile of eligible junction DSR values:

\[
E=P_{10}(DSR_1,DSR_2,\ldots,DSR_n)
\]

It is a modeled indicator, not a direct measure of household experience or a validated equity outcome.

### Leakage objective and feasibility

Emitter flow is integrated over the simulation horizon using the trapezoidal rule to estimate leakage volume in cubic metres. Candidate schedules are filtered against the configured minimum simulated pressure at eligible customer junctions. Pareto analysis minimizes leakage volume and maximizes the 10th-percentile DSR.

## 5. Synthetic evaluation evidence

The default schedule configuration uses four six-hour operating periods and six candidate PRV settings per period:

\[
6^4=1,296
\]

GitHub Actions run [#97](https://github.com/frumi7040/pressurewise-fair/actions/runs/44590378704) completed successfully. The automated test step passed, the optimization step evaluated all 1,296 schedules through EPANET 2.2, and the run identified 186 non-dominated Pareto candidates. All 1,296 schedules met the illustrative 3.516 m minimum-pressure threshold in the supplied synthetic fixture. The machine-readable JSON output was uploaded as a GitHub Actions artifact.

These numbers describe one synthetic software test scenario. The fixture, demand values, emitter coefficient, pressure thresholds, and PRV settings are illustrative and are not calibrated to a utility network. The results must not be presented as field performance, measured water savings, or a real-world service improvement.

## 6. Scope and limitations

### Included in the current prototype

- EPANET 2.2 hydraulic simulation through WNTR 1.5.0.
- Pressure-dependent demand settings supplied through EPANET network inputs.
- Emitter-based, square-root pressure leakage representation.
- Emitter-discharge accounting at selected junctions.
- Time-varying PRV setpoints.
- Four-period daily schedule generation and exhaustive evaluation.
- Junction-level DSR and a 10th-percentile equity indicator.
- Minimum-pressure feasibility filtering.
- Pareto comparison of leakage and lower-tail demand satisfaction.
- Automated tests and a repeatable synthetic optimization example.

### Not established

- Utility-specific calibration of network, demand, leakage, or valve parameters.
- Validation against field pressure, flow, leakage, or customer-delivery measurements.
- Suitability of a PRV location in a real network, including all bypasses and alternate supply paths.
- Generalized arbitrary-exponent leakage modeling inside the EPANET hydraulic engine.
- Demand-pattern-aware requested-demand evaluation in the schedule evaluator.
- Real-world water savings, service improvements, deployment, or operational readiness.

## 7. Validation roadmap

Further work should proceed through the following evidence gates:

| Gate | Evidence needed |
|---|---|
| Benchmark network | Reproducible baseline hydraulic behavior on a documented benchmark |
| Leakage model | Coefficient/exponent justification and comparison with appropriate reference data |
| Demand accounting | Independent verification that emitter flow is not misclassified as customer delivery |
| PRV suitability | Topology review, bypass/alternate-path analysis, and valve behavior verification |
| Demand variation | Evaluation using time-varying requested demand where applicable |
| External validation | Comparison with utility or field measurements, subject to data access and permission |
| Operational feasibility | Review by qualified water-network engineers and the relevant utility |

Passing the repository's automated tests is evidence of the tested software behaviors only. It does not complete these hydraulic, field, or operational validation gates.

## 8. Intended contribution

PressureWise-Fair provides a reproducible prototype for examining pressure-management trade-offs using two modeled perspectives: water lost through leakage and customer demand satisfaction, particularly in the lower tail of the network. Its intended contribution is to make those trade-offs explicit and inspectable before any future utility-specific validation.

**PressureWise-Fair — Save Water. Protect Every Community.**
