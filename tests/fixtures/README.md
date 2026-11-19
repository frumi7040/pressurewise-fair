# Test Network Fixtures

## Purpose

This directory contains small, synthetic EPANET input files used by the
PressureWise-Fair automated tests. They are software test fixtures, not
calibrated representations of a real water distribution system.

## Included fixtures

- `synthetic_network.inp`: a small baseline network with one reservoir,
  three demand junctions, and connecting pipes.
- `synthetic_network_prv.inp`: a small network with a candidate pressure
  reducing valve between junctions J1 and J2.

Both fixtures use LPS flow units and the Hazen-Williams headloss model.
Their dimensions, demands, elevations, and valve settings are illustrative
test inputs, not utility measurements.

## Intended use

The fixtures support repeatable checks of network loading, hydraulic
simulation, emitter assignment, and related software behavior.

Passing an automated test with a fixture does not establish that:
- the network represents real operating conditions;
- the PRV arrangement is suitable for a real distribution system;
- customer-delivered demand has been independently validated;
- leakage estimates are calibrated; or
- any water-saving or equity improvement has been achieved.

## Validation status

The files are included in the repository and are used by automated tests.
Hydraulic behavior and demand-accounting assumptions must be examined
separately before interpreting simulation outputs as customer service or
research results.
