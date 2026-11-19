# Limitations

- The supplied networks are synthetic and are not based on measured utility assets.
- The example leakage coefficient, PDD pressure thresholds, PRV settings, and requested demands are illustrative.
- The prototype uses EPANET emitters with the standard square-root pressure exponent. It does not yet implement a generalized arbitrary-exponent leakage model inside the EPANET hydraulic engine.
- The current schedule evaluator expects constant requested demand per eligible junction. Time-varying customer-demand patterns need a time-series-aware requested-demand implementation.
- The optimizer enumerates candidate schedules and runs EPANET simulations; the number 1,296 is the candidate count for six settings over four periods, not a claim that every candidate has been evaluated unless the optimizer run completes and records all results.
- The Pareto front is only as meaningful as the input network, calibration, demand assumptions, emitter coefficients, and feasibility threshold.
- No utility calibration, field validation, deployment, measured water savings, or demonstrated real-world equity improvement has been completed.
- The prototype is not an operational controller and must not be connected to live infrastructure without engineering review, validation, and appropriate safeguards.
