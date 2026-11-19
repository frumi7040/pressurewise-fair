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


## PRV fixture pressure and unit settings

The PRV fixture explicitly selects EPANET pressure-dependent analysis (PDA)
with illustrative values of 3.516 m minimum pressure, 21.097 m required
pressure, and a 0.5 pressure exponent. These values are software-test
parameters, not universal service standards.

WNTR stores hydraulic flow internally in m^3/s even when the source INP file
uses LPS. For example, an emitter coefficient of 0.05 L/s/sqrt(m) must be
passed to WNTR as 0.00005 m^3/s/sqrt(m). Pressure is expressed in metres.
