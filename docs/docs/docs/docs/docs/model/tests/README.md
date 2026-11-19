# Testing Directory

## Purpose

This directory is reserved for automated and manual tests of PressureWise-Fair.

Tests will be used to verify mathematical calculations, hydraulic model behavior, leakage accounting, PRV operation, and optimization logic.

## Planned Test Areas

| Test area | Purpose |
|---|---|
| Input validation | Check network configuration and required data |
| Leakage calculations | Verify emitter relationship calculations |
| Demand accounting | Separate customer delivery from leakage |
| DSR calculations | Verify demand satisfaction ratios |
| Schedule generation | Confirm all 1,296 candidate combinations |
| PRV behavior | Check modeled pressure-control behavior |
| Pareto analysis | Verify objective comparisons and dominance |

## Testing Principles

- Tests must have defined expected behavior.
- Inputs and outputs must be reproducible.
- Failed tests must be recorded.
- Numerical tolerances must be specified.
- Tests must not be marked as passed without execution evidence.

## Current Status

This directory currently documents planned testing areas.

No completed test suite or passed validation result is claimed.
