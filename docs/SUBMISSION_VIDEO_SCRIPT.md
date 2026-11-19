# PressureWise-Fair — 3-minute narrated demo script

**Purpose:** Competition presentation and live software demonstration.  
**Target duration:** 2:50–3:00 at a steady speaking pace.  
**Recording format:** 16:9 landscape, narrated screen recording.  
**Evidence boundary:** All numerical results below come from the included synthetic test network. They are not utility measurements or field-validated outcomes.

## Recording preparation

- Open the repository on the `audit-and-fixes` branch.
- Have a terminal ready with the project installed and the synthetic optimization command available.
- Have the latest successful GitHub Actions run open, including its test and optimization steps.
- Do not show account settings, tokens, private email addresses, browser password managers, or unrelated private repositories.
- Keep the repository private. Do not switch its visibility to public for the recording.
- If the live command takes too long, show the successful CI run and its completed output; do not edit or fabricate result values.

## Narration and screen directions

### 0:00–0:25 — Problem

**Screen:** Title slide or README project heading.

**Narration:**

“Water utilities face a difficult trade-off. Reducing pressure can reduce leakage, but it can also reduce the water delivered to customers—especially communities already experiencing low pressure. PressureWise-Fair is a student research prototype that explores both outcomes together. Its central idea is simple: pressure management should be evaluated not only by water lost, but also by the service customers continue to receive.”

### 0:25–0:55 — Approach

**Screen:** README architecture and the technical blueprint.

**Narration:**

“The prototype uses the EPANET hydraulic engine through WNTR. Pressure-dependent demand represents how customer delivery changes with pressure. EPANET emitters represent pressure-driven leakage. A pressure-reducing valve is assigned a time-varying schedule, and the model evaluates customer demand satisfaction alongside total simulated leakage volume. The equity indicator is the tenth percentile of demand-satisfaction ratios across the selected customer junctions. The search is deterministic; it does not claim to use an AI optimizer.”

### 0:55–1:45 — Demonstration

**Screen:** Show the repository tree and open `examples/run_synthetic_optimization.py`. Then show the GitHub Actions run, the passing test summary, and the completed optimization step.

**Narration:**

“Here is the reproducible example and the synthetic network used for this demonstration. The search considers six candidate valve settings in each of four six-hour periods. That creates one thousand two hundred and ninety-six possible schedules. Each candidate is run through the hydraulic simulator; it is not merely counted as a generated combination.

“In the recorded automated run, all sixty-five tests passed. The full search completed all one thousand two hundred and ninety-six hydraulic schedule evaluations and identified one hundred and eighty-six non-dominated Pareto candidates. In this synthetic example, all candidates met the illustrative minimum-pressure constraint of three point five one six metres. The complete machine-readable output was saved as a workflow artifact.”

### 1:45–2:20 — Interpreting the result

**Screen:** Show the optimization output or workflow artifact metadata. If opening the JSON, show only a few representative fields and avoid exposing unrelated account information.

**Narration:**

“A Pareto candidate is a schedule for which no other feasible schedule in this evaluated set achieves both lower simulated leakage and a higher equity score. The Pareto set therefore presents trade-offs rather than pretending there is one universally best operating point. These results demonstrate that the software workflow runs end to end on the supplied test case. They do not demonstrate savings in a real water network.”

### 2:20–2:55 — Limitations and impact

**Screen:** README limitations section.

**Narration:**

“The current test network is synthetic. Its demands, leakage coefficient, pressure thresholds, and valve settings are illustrative. The evaluator currently assumes constant requested demand at each selected customer junction. The prototype has not been calibrated with utility data, field-validated, or deployed, and it makes no measured water-saving claim.

“Our next step is to test the approach against benchmark and utility networks, justify model parameters, and validate service and leakage estimates with field data. PressureWise-Fair is a reproducible starting point for exploring water conservation and equitable service together.”

## Final recording checklist

- [ ] The video contains spoken narration throughout the presentation; it is not music-only.
- [ ] The recording includes an actual screen demonstration of the repository and successful run evidence.
- [ ] The run shown is the successful GitHub Actions run that reports 65 passing tests and 1,296 completed schedule evaluations.
- [ ] The 186 Pareto candidates and illustrative 3.516 m pressure threshold are described as synthetic results.
- [ ] No real-world savings, utility calibration, deployment, or field validation are claimed.
- [ ] No passwords, access tokens, private keys, private email addresses, or unrelated personal information appear on screen.
- [ ] The final runtime is within the competition's three-minute limit.
- [ ] The submitted video link is accessible to competition judges without making the source-code repository public.
