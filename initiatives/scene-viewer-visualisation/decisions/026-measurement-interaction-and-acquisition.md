# ADR 026: Measurement Interaction and Acquisition

## Status

Proposed.

## Context

Accepted ADRs 005, 024, and 028 establish transient inspection, persistent
dimension outcomes, and fixed/associative anchor modes. Viewer has no
active-tool lifecycle or approved snapping path that turns pointer input into
an accurate world point and, when requested, a supported component reference.

## Options

1. Add one narrow snapping query used by inspection, Fixed dimension, and
   Associative dimension acquisition, with an explicit one-shot tool lifecycle.
2. Read rendered depth only and never expose associative dimensions.
3. Add a generalized snapping and sub-object editing framework before the
   first measurement tool.
4. Support only programmatic world-point input in the initial version.

## Recommendation

Choose option 1.

An explicit measurement mode activates one tool and cancels any previously
active tool. Left-button input reaches the active tool before ordinary
selection handling. The first valid click queries the approved snap targets.
Pointer movement over a valid snap updates a transient preview. The second
valid click completes the selected outcome:

- inspection mode displays a transient result without scene mutation; or
- Fixed dimension mode creates `PointAnchor` values from the snapped points; or
- Associative dimension mode creates `ComponentAnchor` values and accepts only
  snap results with supported component references.

Completing either dimension mode creates one root-level durable
`DistanceDimension`, selects it, clears preview state, and deactivates. The
data model permits mixed anchors; the UI must make each acquired anchor's mode
explicit if it exposes mixed construction.

Escape or explicit cancellation clears preview and result state and creates
nothing. A background or unsupported snap provides no anchor. Associative mode
never falls back to a fixed point. There is no construction-plane fallback,
general sub-object editing, repeating mode, or dimension editing in this phase.
Camera navigation remains available where its input does not conflict with the
active tool.

This ADR must still approve the initial supported snap targets and component
selectors. It should prefer the smallest set that can resolve stable component
references rather than promising a general snapping framework.

Whether transient inspection deactivates after one completed pair or remains
active for repeated live measurements must be approved as part of this ADR;
the recommendation is one-shot behavior for both modes in the first version.

## Consequences

- Measurement accuracy and association follow the explicitly supported snap
  targets; unsupported targets fail visibly.
- Input priority and background behavior are deterministic.
- Both outcomes share acquisition and preview without sharing persistence.
- A narrow one-shot lifecycle avoids a general tool framework promise.

## Compatibility

This is a new Viewer interaction. It does not change ordinary selection or
camera input when no measurement tool is active.

## Verification

- Verify activation, previous-tool cancellation, input priority, first anchor,
  preview, second anchor, and cleanup.
- Verify background clicks and pointer motion over background do not create or
  update anchors.
- Verify transient completion follows ADR 024 without scene mutation.
- Verify fixed, associative, and any exposed mixed acquisition follow ADR 028,
  including no silent fallback.
- Verify persistent completion creates and selects exactly one root-level
  dimension.
- Verify Escape and explicit cancellation create nothing in both modes.

## Dependencies

- Refines Accepted ADRs 005 and 024.
- Must implement Accepted ADR 028 anchor modes and unresolved behavior.
- Persistent results depend on proposed ADRs 021 and 022.
- Measurement labels and tolerance context depend on proposed ADR 027.
- Uses Accepted ADRs 003, 004, and 006 for selection, refresh/history
  boundaries, and the public Viewer facade.

