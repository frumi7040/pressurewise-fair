# Demonstrating the synthetic evaluation results

This guide creates presentation-friendly evidence from the actual
`results/synthetic_optimization.json` produced by the project workflow.

## 1. Run the optimizer

From the repository root, with the project dependencies installed:

```bash
python examples/run_synthetic_optimization.py
```

This runs the 24-hour synthetic-network evaluation using EPANET 2.2 through
WNTR 1.5.0 and writes `results/synthetic_optimization.json`.

## 2. Export the results

```bash
python scripts/export_synthetic_results.py
```

The exporter reads the JSON; it does not rerun the hydraulic simulation. It
writes these files under `build/pressurewise-demo/`:

- `synthetic_schedule_results.csv`: one row per evaluated schedule.
- `synthetic_pareto_front.svg`: plot of the returned Pareto candidates.
- `SYNTHETIC_RESULTS_SUMMARY.md`: concise, qualified summary.

The output directory is covered by the existing `build/` ignore rule and
should not be committed as generated output.

## 3. What the evidence supports

For the supplied workflow artifact:

- 1,296 schedules were evaluated.
- 186 non-dominated Pareto candidates were returned.
- 1,296 of 1,296 result rows are marked feasible.
- The configured minimum-pressure constraint in the runner is 3.516 m.
- The lowest observed minimum-pressure value in the result rows is about
  9.992 m (not 3.516 m).

The 65/65 automated test result is reported separately by the GitHub Actions
test step. It is not a metric from the optimization JSON.

## 4. How to record a short, genuine demo

1. Open the GitHub Actions run and show its completed test step and optimizer
   output, keeping private account details out of frame.
2. If running locally, show the two commands above in a terminal.
3. Open the generated SVG and CSV/summary to show the actual exported outputs.
4. Keep the on-screen qualification visible:

   **Synthetic software-validation network; not utility data. No field
   validation or measured real-world water savings are claimed.**

Do not present the SVG as a live utility dashboard. It is a static plot
generated from the saved synthetic evaluation results.
