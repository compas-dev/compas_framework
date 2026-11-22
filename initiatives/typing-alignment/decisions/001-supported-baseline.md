# Title: What version and checker baseline should typing alignment use?

## Status

Accepted

## Context

Core and CGAL require Python 3.12+, while OCC still declares Python 3.9+ and an
unbounded COMPAS dependency. Pyright configuration and CI invocation differ by
repository. NumPy lower bounds do not reflect the supported Python baseline.

## Options

1. Preserve each package's current independent baseline. This avoids metadata
   changes but makes cross-package overrides and fixtures unreliable.
2. Align on Python 3.12+, COMPAS 3.x, NumPy 1.26+, and one pinned Pyright.
3. Target multiple historical baselines through conditional annotations. This
   adds compatibility complexity without a current requirement.

## Recommendation

Choose option 2. Require Python 3.12+, `compas>=3,<4` in integration packages,
NumPy 1.26+ where NumPy is declared, and pin Pyright 1.1.414 initially. Use
`compas3` for authoritative local checks and test both NumPy 1.26.x and current
2.x. Do not add mypy.

## Consequences

- Type syntax and override checks share one baseline.
- Unsupported Python/COMPAS combinations are removed from metadata and CI.
- CI, development dependencies, and contributor documentation change.
- Tests must exercise the lowest and latest supported NumPy lines.
- Future baseline changes require coordinated updates.

## Affected packages

`compas`, `compas_occ`, `compas_cgal`, and `compas_framework`.

## Dependencies

None.
