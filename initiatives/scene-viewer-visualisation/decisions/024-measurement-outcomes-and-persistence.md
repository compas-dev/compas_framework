# ADR 024: Measurement Outcomes and Persistence

## Status

Accepted.

## Context

A measurement interaction may serve two different intentions. A user may want
to inspect a value temporarily while working, or may want to create a durable
dimension annotation that remains part of the scene. Treating every completed
measurement as persistent would mutate the scene during ordinary inspection;
treating every result as transient would prevent intentional documentation.

The two workflows may share point acquisition and preview rendering, but their
results need different ownership and persistence.

## Options

1. Provide distinct transient inspection and persistent dimension-annotation
   modes that may share acquisition and preview infrastructure.
2. Make every completed measurement create a durable scene item.
3. Keep every measurement transient and require manual dimension construction.

## Recommendation

Choose option 1.

Transient inspection derives and displays the live measurement in Viewer tool
state. It does not add, remove, select, or serialize scene content. Completion
may retain the result only for the lifetime defined by the active inspection
tool; cancellation clears it.

Persistent dimension-annotation mode may use the same anchor acquisition and
preview path. Completing it creates exactly one durable `DistanceDimension` in
the scene using the explicit fixed or associative anchors governed by Accepted
ADR 028. Cancellation creates nothing. The exact acquisition, snapping,
repetition, activation, and post-completion lifecycles remain governed by
proposed ADR 026.

The mode is explicit before completion. Viewer never infers persistence from
the number of acquired points or silently promotes a transient result into a
scene item.

## Consequences

- Ordinary measurement does not pollute or mutate the scene.
- Users can intentionally preserve dimensions when they need documentation.
- Shared acquisition and preview code does not imply shared result ownership.
- Session history for transient inspections remains outside Scene and outside
  the Viewer transform-transaction stack.

## Compatibility

There is no existing measurement workflow. This decision establishes two
clear public outcomes without preserving an earlier behavior.

## Verification

- Verify transient inspection never mutates scene objects, hierarchy,
  selection, serialization, or transform history.
- Verify persistent completion creates exactly one durable dimension.
- Verify cancellation in either mode creates no durable content.
- Verify switching modes clears incompatible transient result state rather
  than reinterpreting it.

## Dependencies

- Refines Accepted ADR 005.
- Persistent results depend on proposed ADRs 021 and 022.
- Persistent anchor semantics are governed by Accepted ADR 028.
- Interaction details depend on proposed ADR 026.

## Decision

Approved on 2026-11-08. Viewer provides separate transient inspection and
persistent dimension-annotation outcomes. They may share acquisition and
preview infrastructure, but transient measurements never mutate or serialize
Scene, while persistent completion creates a durable `DistanceDimension`.

