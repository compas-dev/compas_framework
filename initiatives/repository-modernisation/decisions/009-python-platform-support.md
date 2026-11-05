# ADR 009: Python and Platform Support Matrices

**Status:** Accepted

## Context

Metadata, Ruff targets, and CI matrices currently disagree. OCC is constrained
by PythonOCC builds; CGAL distributes native artifacts across several systems.

## Options

1. Force one matrix across every repository.
2. Let workflow matrices drift independently from metadata.
3. Make project metadata authoritative and derive an explicit profile-specific
   test/artifact matrix from supported dependencies and user commitments.

## Recommendation

Keep `requires-python` and classifiers consistent and authoritative. Test the
minimum and latest supported Python, plus justified intermediates. OCC support
cannot exceed available PythonOCC packages. Native artifact matrices explicitly
list required OS/architecture targets and stable-ABI assumptions. Resolve
ShapeOp's current Python/ABI inconsistency and establish meaningful Gmsh test
coverage before accepting their matrices.

## Consequences

Some repositories support different matrices. Matrix changes require evidence
and metadata/docs updates. Tests should mechanically detect metadata/workflow
drift where feasible.

## Affected repositories

All core repositories, especially `compas_occ` and native packages.

## Dependencies

ADR 001, ADR 002.
