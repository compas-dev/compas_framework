# ADR 001: Initial Scope and Initiative Ownership

## Status

Proposed.

## Context

The framework has documentation inconsistencies across core, backends,
integration packages, and the viewer. The complete ecosystem is much larger
and includes repositories without confirmed COMPAS 3 compatibility or modern
documentation infrastructure.

## Options

1. Coordinate the ten active repository-modernisation repositories.
2. Include the complete ecosystem immediately.
3. Coordinate core only.
4. Keep documentation inside repository modernisation.

## Recommendation

Choose option 1. Documentation coordination owns information architecture,
tutorial progression, example classification and source ownership, API
reference organization, terminology, and documentation-specific verification.
Modernisation owns the active-ten Ruff/Pyright wiring. Public API initiatives
own behavior and signatures.

## Consequences

- The first wave is bounded and matches repositories already receiving common
  tooling.
- Backend and viewer inconsistencies remain visible rather than being deferred
  outside core.
- Later packages require explicit admission under ADR 009.

## Affected repositories

`compas`, `compas_cgal`, `compas_framework`, `compas_gmsh`,
`compas_libigl`, `compas_model`, `compas_occ`, `compas_session`,
`compas_shapeop`, and `compas_viewer`.

## Dependencies

None.
