# ADR 028: Fixed and Associative Dimension Anchors

## Status

Accepted.

## Context

Persistent dimensions may document either a position captured at creation or a
relationship to a component that should move as the referenced data changes.
Using only stored points makes every dimension stale after component edits.
Using only component references prevents intentionally fixed dimensions and
cannot represent every acquired location.

Separate dimension classes would duplicate formatting, rendering,
serialization, and editing behavior even though only anchor resolution differs.

## Options

1. Use one `DistanceDimension` whose two anchors are independently either a
   fixed `PointAnchor` or an associative `ComponentAnchor`.
2. Create separate fixed and associative dimension classes.
3. Store only points and update them opportunistically after component edits.
4. Store only component references and reject unassociated points.

## Recommendation

Choose option 1.

`DistanceDimension` stores two values of one anchor union:

- `PointAnchor` stores a fixed point captured at creation; and
- `ComponentAnchor` stores an explicit reference to a supported component and
  resolves its current point when the dimension is evaluated.

The data model permits two fixed anchors, two associative anchors, or one of
each. It does not infer an anchor kind from serialized fields.

Viewer exposes explicit **Fixed** and **Associative** dimension modes. Both use
the approved snapping path:

- Fixed mode snaps for accurate acquisition and stores the resulting point in
  a `PointAnchor`.
- Associative mode snaps to a supported component and stores a
  `ComponentAnchor`.

Viewer never silently falls back from associative to fixed. If a snap result
cannot produce a supported component reference, associative acquisition does
not accept that anchor and reports the reason through tool state.

Removing or invalidating a referenced component makes its
`ComponentAnchor` explicitly unresolved. The dimension retains the reference
and reports unresolved state; it never displays a cached point as if the
association were still valid. Rebinding or repairing the reference requires an
explicit later operation.

The exact supported component selectors and snap targets remain part of
proposed ADR 026. This ADR fixes anchor semantics and failure behavior without
inventing a general component-resolution registry.

## Consequences

- One dimension type covers fixed, associative, and mixed use cases.
- Persistence intent is explicit at acquisition and in serialized data.
- Fixed measurements remain stable after later model edits.
- Associative measurements follow supported components and fail visibly when
  their references cannot resolve.
- Snapping is required for both UI modes, but snapping does not imply
  association unless Associative mode is active.

## Compatibility

There is no existing `DistanceDimension` payload. This establishes the initial
anchor schema without a legacy representation.

## Verification

- Serialize and evaluate fixed, associative, and mixed anchor pairs.
- Verify Fixed mode stores the snapped point and does not retain a component
  reference.
- Verify Associative mode stores the component reference and follows supported
  component changes.
- Verify associative acquisition never falls back silently to `PointAnchor`.
- Verify removed or invalid components produce explicit unresolved state and
  never reuse a stale cached coordinate.
- Verify unresolved state survives serialization and reload.

## Dependencies

- Refines Accepted ADRs 005 and 024.
- Depends on proposed ADR 021 for canonical `DistanceDimension` ownership.
- Constrains proposed ADR 026 acquisition and snapping behavior.

## Decision

Approved on 2026-11-08. One `DistanceDimension` supports fixed
`PointAnchor` and associative `ComponentAnchor` values independently at both
ends. Viewer exposes explicit Fixed and Associative modes, uses snapping in
both, never silently falls back, and reports removed component references as
unresolved rather than displaying stale coordinates.

