# ADR 005: Initial Learner Curriculum and Version Behavior

## Status

Proposed.

## Context

Existing tutorials and examples are uneven across packages. Creating many
topic skills immediately would multiply routing and maintenance before one
complete learner path is validated.

## Options

1. Pilot one progressive `compas-get-started` vertical slice.
2. Create one skill per package or API area immediately.
3. Copy a fixed tutorial into one skill.

## Recommendation

Choose option 1. Cover environment/version inspection, basic geometry, a mesh
using high-level accessors, transformation and serialization, optional
visualization, and one optional backend. Each stage creates and runs a small
artifact and offers a modification exercise.

Use checkout-matching docs during source development and release-matching docs
for installed packages. Report mismatches and ask before installing or
upgrading anything.

## Consequences

- The first learner outcome is end-to-end and testable.
- Viewer and backend stages can wait for their APIs to stabilize.
- The skill sequences authoritative material instead of copying it.

## Dependencies

ADRs 001, 002, and 004; documentation-coordination outputs.
