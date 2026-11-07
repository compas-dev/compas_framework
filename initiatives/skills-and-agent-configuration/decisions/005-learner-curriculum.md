# ADR 005: Initial Learner Curriculum and Version Behavior

## Status

Accepted.

## Context

Existing tutorials and examples are uneven across packages. Creating many
topic skills immediately would multiply routing and maintenance before one
complete learner path is validated.

## Options

1. Pilot one progressive `compas-get-started` vertical slice.
2. Create one skill per package or API area immediately.
3. Copy a fixed tutorial into one skill.

## Recommendation

Choose option 1. The mandatory first slice is core-only: environment/version
inspection, basic geometry, a mesh using high-level accessors, transformation,
serialization, and a modification exercise. Each stage is a guided checkpoint
that creates and runs a small artifact, explains the result, and asks the user
to change it. Visualization and computational backends are later optional
modules gated on stable APIs and matching documentation.

Use checkout-matching docs during source development and release-matching docs
for installed packages. Teach only implemented matching APIs. Report
mismatches and ask before installing or upgrading anything. Provide
user-facing `agents/openai.yaml` metadata for hosts that support it, without
making that adapter necessary for the portable workflow.

## Consequences

- The first learner outcome is end-to-end and testable.
- Viewer and backend stages can wait for their APIs to stabilize.
- The skill sequences authoritative material instead of copying it.

## Dependencies

ADRs 001, 002, and 004; documentation-coordination outputs.
