# ADR 005: Version and API Baseline

## Status

Accepted.

## Context

The active repositories do not all have the accepted COMPAS 3 geometry and
typing contracts implemented on their documentation branches. An example may
match its visible checkout while describing a different dependency version
than its published documentation.

## Options

1. Tie documentation to the branch package and declared dependency range.
2. Always document the newest candidate APIs.
3. Preserve old examples through compatibility aliases.

## Recommendation

Choose option 1. Coordinated unreleased examples use exact candidate pins.
Released documentation does not claim candidate-only APIs. Examples work with
the repository's declared minimum supported COMPAS version unless explicitly
labeled as candidate integration examples.

Migrations preserve semantics: explicit algorithms map to their equivalent
named callables, structural backend inputs remain direct, and producer controls
retain their meaning. No compatibility alias is introduced only to avoid an
example update.

## Consequences

- Version mismatch fails visibly rather than producing ambiguous guidance.
- `Mesh.triangulated()` examples use Accepted Geometry ADR 024 only on branches
  that contain its representation-preserving implementation.
- Candidate documentation and released documentation remain distinguishable.

## Dependencies

Stable contracts from typing, geometry, plugin, viewer, and model initiatives.
