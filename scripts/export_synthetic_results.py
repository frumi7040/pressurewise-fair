"""Export the checked-in synthetic optimization JSON for a presentation demo.

Run from the repository root:
    python scripts/export_synthetic_results.py

Reads results/synthetic_optimization.json and writes CSV, SVG, and Markdown
summary files under build/pressurewise-demo/. It does not rerun the optimizer.
"""

from __future__ import annotations

import argparse
import csv
import html
import json
from pathlib import Path
from statistics import mean

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INPUT = ROOT / "results" / "synthetic_optimization.json"
DEFAULT_OUTPUT = ROOT / "build" / "pressurewise-demo"


def load_payload(path: Path) -> dict:
    payload = json.loads(path.read_text(encoding="utf-8"))
    required = {"scenario", "engine", "evaluated_schedule_count", "pareto_front", "results"}
    missing = required.difference(payload)
    if missing:
        raise ValueError(f"Results JSON is missing required fields: {', '.join(sorted(missing))}")
    if not isinstance(payload["results"], list) or not isinstance(payload["pareto_front"], list):
        raise ValueError("Results and pareto_front must be JSON arrays.")
    if len(payload["results"]) != payload["evaluated_schedule_count"]:
        raise ValueError("Schedule count does not match the number of result rows.")
    return payload


def write_csv(payload: dict, path: Path) -> None:
    pareto_keys = {tuple(item["schedule"]) for item in payload["pareto_front"]}
    fields = [
        "schedule",
        "period_1_setting_m",
        "period_2_setting_m",
        "period_3_setting_m",
        "period_4_setting_m",
        "leakage_volume_m3",
        "equity_10th_percentile_dsr",
        "minimum_pressure_m",
        "feasible",
        "pareto_candidate",
    ]
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in payload["results"]:
            schedule = row["schedule"]
            if len(schedule) != 4:
                raise ValueError("Expected four settings per 24-hour schedule.")
            writer.writerow({
                "schedule": "-".join(f"{float(value):g}" for value in schedule),
                "period_1_setting_m": schedule[0],
                "period_2_setting_m": schedule[1],
                "period_3_setting_m": schedule[2],
                "period_4_setting_m": schedule[3],
                "leakage_volume_m3": row["leakage_volume_m3"],
                "equity_10th_percentile_dsr": row["equity"],
                "minimum_pressure_m": row["minimum_pressure"],
                "feasible": row["feasible"],
                "pareto_candidate": tuple(schedule) in pareto_keys,
            })


def write_svg(payload: dict, path: Path) -> None:
    points = payload["pareto_front"]
    if not points:
        raise ValueError("Pareto front is empty; cannot create the plot.")

    width, height = 1000, 620
    left, right, top, bottom = 105, 55, 65, 100
    plot_w, plot_h = width - left - right, height - top - bottom
    xs = [float(p["leakage_volume_m3"]) for p in points]
    ys = [float(p["equity"]) for p in points]
    x_min, x_max = min(xs), max(xs)
    y_min, y_max = min(ys), max(ys)
    x_pad = max((x_max - x_min) * 0.06, 0.1)
    y_pad = max((y_max - y_min) * 0.08, 0.01)
    x_min -= x_pad
    x_max += x_pad
    y_min = max(0.0, y_min - y_pad)
    y_max += y_pad

    def sx(value: float) -> float:
        return left + (value - x_min) / (x_max - x_min) * plot_w

    def sy(value: float) -> float:
        return top + (y_max - value) / (y_max - y_min) * plot_h

    elements = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="#ffffff"/>',
        '<text x="500" y="32" text-anchor="middle" font-family="Arial" font-size="22" font-weight="bold">Synthetic Pareto candidates</text>',
    ]
    for i in range(5):
        x = left + i * plot_w / 4
        y = top + i * plot_h / 4
        x_value = x_min + i * (x_max - x_min) / 4
        y_value = y_max - i * (y_max - y_min) / 4
        elements.append(f'<line x1="{x:.1f}" y1="{top}" x2="{x:.1f}" y2="{top + plot_h}" stroke="#e5e7eb"/>')
        elements.append(f'<line x1="{left}" y1="{y:.1f}" x2="{left + plot_w}" y2="{y:.1f}" stroke="#e5e7eb"/>')
        elements.append(f'<text x="{x:.1f}" y="{top + plot_h + 25}" text-anchor="middle" font-family="Arial" font-size="13" fill="#374151">{x_value:.2f}</text>')
        elements.append(f'<text x="{left - 12}" y="{y + 5:.1f}" text-anchor="end" font-family="Arial" font-size="13" fill="#374151">{y_value:.3f}</text>')

    for point in points:
        x = sx(float(point["leakage_volume_m3"]))
        y = sy(float(point["equity"]))
        elements.append(f'<circle cx="{x:.2f}" cy="{y:.2f}" r="4.2" fill="#087e8b" fill-opacity="0.78"/>')

    elements.extend([
        f'<line x1="{left}" y1="{top + plot_h}" x2="{left + plot_w}" y2="{top + plot_h}" stroke="#111827" stroke-width="2"/>',
        f'<line x1="{left}" y1="{top}" x2="{left}" y2="{top + plot_h}" stroke="#111827" stroke-width="2"/>',
        f'<text x="{left + plot_w / 2:.1f}" y="{height - 35}" text-anchor="middle" font-family="Arial" font-size="17">Simulated leakage volume (m³)</text>',
        f'<text x="25" y="{top + plot_h / 2:.1f}" transform="rotate(-90 25 {top + plot_h / 2:.1f})" text-anchor="middle" font-family="Arial" font-size="17">10th-percentile DSR (equity indicator)</text>',
        f'<text x="500" y="{height - 8}" text-anchor="middle" font-family="Arial" font-size="11" fill="#6b7280">Synthetic software-validation network; not utility data</text>',
        '</svg>',
    ])
    path.write_text("\n".join(elements), encoding="utf-8")


def write_summary(payload: dict, path: Path) -> None:
    rows = payload["results"]
    pareto = payload["pareto_front"]
    feasible_count = sum(bool(row["feasible"]) for row in rows)
    min_pressure = min(float(row["minimum_pressure"]) for row in rows)
    max_pressure = max(float(row["minimum_pressure"]) for row in rows)
    min_leak = min(float(row["leakage_volume_m3"]) for row in rows)
    max_leak = max(float(row["leakage_volume_m3"]) for row in rows)
    min_equity = min(float(row["equity"]) for row in rows)
    max_equity = max(float(row["equity"]) for row in rows)

    content = f"""# PressureWise-Fair synthetic evaluation summary

> **Scope:** {payload['scenario']}. These are software-validation results from a synthetic network, not measured utility performance or field results.

- Hydraulic engine: {payload['engine']}
- Schedules evaluated: {len(rows):,}
- Feasible schedules: {feasible_count:,}
- Non-dominated Pareto candidates: {len(pareto):,}
- Minimum observed network pressure across evaluated schedules: {min_pressure:.3f} m
- Maximum observed network pressure across evaluated schedules: {max_pressure:.3f} m
- Simulated leakage-volume range: {min_leak:.3f}–{max_leak:.3f} m³
- 10th-percentile DSR range: {min_equity:.4f}–{max_equity:.4f}

## Files

- `synthetic_schedule_results.csv`: all evaluated schedules and metrics.
- `synthetic_pareto_front.svg`: scatter plot of the Pareto candidates.

## Interpretation

The Pareto candidates show trade-offs between simulated leakage volume and the 10th-percentile demand-satisfaction ratio. They do not establish real-world water savings, customer outcomes, or operational suitability.

The configured minimum-pressure constraint in the example is 3.516 m. The observed minimum pressure reported in the evaluated result rows is {min_pressure:.3f} m; do not confuse the configured threshold with the observed minimum pressure.

## Reproduction

From the repository root, first run:

```bash
python examples/run_synthetic_optimization.py
```

Then export the generated JSON:

```bash
python scripts/export_synthetic_results.py
```

The exporter reads the JSON and does not rerun the hydraulic model.
"""
    path.write_text(content, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()

    payload = load_payload(args.input)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    csv_path = args.output_dir / "synthetic_schedule_results.csv"
    svg_path = args.output_dir / "synthetic_pareto_front.svg"
    summary_path = args.output_dir / "SYNTHETIC_RESULTS_SUMMARY.md"

    write_csv(payload, csv_path)
    write_svg(payload, svg_path)
    write_summary(payload, summary_path)

    print(f"Schedules exported: {len(payload['results'])}")
    print(f"Pareto candidates plotted: {len(payload['pareto_front'])}")
    print(f"Feasible schedules: {sum(bool(row['feasible']) for row in payload['results'])}")
    print(f"Output directory: {args.output_dir}")


if __name__ == "__main__":
    main()
