# Test Network Fixtures

## Purpose

This directory contains small, reproducible EPANET network models used to test PressureWise-Fair's hydraulic simulation functionality.

## Planned Fixture

The initial synthetic network should contain:

- One reservoir or other suitable water supply source
- A small network of pipes
- Multiple demand junctions
- At least one candidate location for a Pressure Reducing Valve (PRV)
- Clearly documented pipe dimensions and roughness values
- Defined customer demand patterns
- Explicit pressure and simulation settings

## Requirements

Each network fixture must:

1. Use a documented EPANET-compatible input format.
2. Have clearly defined units.
3. Include documented source and parameter assumptions.
4. Be small enough for repeatable automated testing.
5. Be checked for hydraulic connectivity and valid simulation behavior.
6. Be synthetic and clearly distinguished from real utility data.

## Validation

Before a fixture is used in automated tests, verify:

- The network file can be loaded.
- The hydraulic simulation completes.
- Junction pressures are available.
- Requested and delivered customer demand can be distinguished.
- The candidate PRV configuration is valid.

## Current Status

No synthetic EPANET network fixture is included yet.

This document describes the intended test fixture. It does not claim that a network has been created, simulated, or validated.
