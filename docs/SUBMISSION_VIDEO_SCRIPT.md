# PressureWise-Fair — 3–4 minute narrated demo script

**Purpose:** Competition presentation and software demonstration.  
**Target duration:** Approximately 3:30.  
**Recording format:** 16:9 landscape, narrated screen recording.  
**Challenge area:** Water Quantity.  
**Evidence boundary:** All numerical results are from the supplied synthetic test network. They are not utility measurements or field-validated outcomes.

## Recording preparation

- Open the repository on the `audit-and-fixes` branch.
- Have a terminal ready with the project installed and the synthetic optimization command available.
- Have GitHub Actions run [#97](https://github.com/frumi7040/pressurewise-fair/actions/runs/44590378704) open, including its successful test and optimization steps.
- Prepare the project slides and show them where useful.
- Do not show account settings, tokens, private email addresses, browser password managers, or unrelated private repositories.
- Keep the repository private. Do not change its visibility for the recording.
- If the live command takes too long, show the successful CI run and its completed output; do not edit or fabricate result values.
- Replace the bracketed track placeholder with the category you are officially registered under: High School or University.

## Narration and screen directions

### 0:00–0:35 — Introduction and challenge

**Screen:** Title slide showing PressureWise-Fair, the presenter's name/team, and Water Quantity.

**Narration:**

“Hello, I’m [presenter name], and this is PressureWise-Fair. I’m presenting in the [High School or University] track, addressing the Water Quantity challenge. Water systems face pressure to meet growing demand while reducing losses. But pressure management creates a difficult trade-off: reducing pressure can limit leakage, while also reducing the water delivered to customers who may already receive inadequate service. PressureWise-Fair explores how to evaluate both outcomes together.”

### 0:35–1:10 — Technical approach

**Screen:** Show the project overview and a simple workflow diagram or the relevant README section.

**Narration:**

“The prototype uses the EPANET hydraulic engine through WNTR. Pressure-dependent demand represents how customer delivery changes with pressure. EPANET emitters represent pressure-driven leakage. A pressure-reducing valve is assigned a time-varying schedule. The model evaluates simulated leakage volume alongside customer demand satisfaction. To emphasize the lower-performing locations, it uses the tenth percentile of eligible junction demand-satisfaction ratios. The search is deterministic exhaustive enumeration; it does not claim to use an AI optimizer.”

### 1:10–2:20 — Demonstration

**Screen:** Show the repository structure, open `examples/run_synthetic_optimization.py`, then show GitHub Actions run #97 and the completed test and optimization steps.

**Narration:**

“Here is the runnable example and the synthetic network used for this software demonstration. The search considers six candidate valve settings in each of four six-hour periods, giving one thousand two hundred and ninety-six possible schedules. Each candidate schedule is evaluated through the hydraulic simulator.

“In this successful automated run, the test step passed and the complete search evaluated all one thousand two hundred and ninety-six schedules. The run identified one hundred and eighty-six non-dominated Pareto candidates. All one thousand two hundred and ninety-six schedules met the illustrative minimum-pressure threshold of three point five one six metres in this particular synthetic fixture. The complete machine-readable output was uploaded as a workflow artifact.”

### 2:20–2:55 — Interpreting the result

**Screen:** Show the JSON artifact or a few representative result fields, taking care not to expose unrelated account information.

**Narration:**

“A Pareto candidate is a feasible schedule for which no other evaluated feasible schedule achieves both lower simulated leakage and a higher equity score. The Pareto set therefore shows trade-offs rather than claiming one universally best operating point. These results demonstrate that the software workflow runs end to end on the supplied test case. They do not demonstrate savings in a real water network.”

### 2:55–3:30 — Limitations and next steps

**Screen:** Show the limitations section of the README.

**Narration:**

“The current network is synthetic. Its demands, leakage coefficient, pressure thresholds, and valve settings are illustrative. The schedule evaluator assumes constant requested demand at each eligible customer junction, and customer delivery is estimated using an emitter-accounting convention that needs further validation. The prototype has not been calibrated with utility data, field-validated, or deployed. No measured water-saving claim is made.

“Next, the approach needs testing on benchmark and utility networks, justified model parameters, topology and valve checks, and comparison with field data. PressureWise-Fair is a reproducible starting point for studying water conservation and equitable service together. Thank you.”

## Final recording checklist

- [ ] Runtime is between 3 and 4 minutes.
- [ ] The presenter introduces themselves and identifies the registered High School or University track.
- [ ] The Water Quantity challenge area is named.
- [ ] The video explains the problem, project approach, and includes a genuine screen demonstration.
- [ ] The displayed run is GitHub Actions run #97, with successful test and 1,296-schedule optimization steps.
- [ ] The 186 Pareto candidates and 3.516 m threshold are described as synthetic results.
- [ ] No real-world savings, utility calibration, deployment, or field validation are claimed.
- [ ] No passwords, access tokens, private keys, private email addresses, or unrelated personal information appear on screen.
- [ ] The final video link is accessible to competition judges without making the source-code repository public.
