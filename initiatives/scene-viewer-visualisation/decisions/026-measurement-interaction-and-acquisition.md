# ADR 026: Measurement Interaction and Acquisition

## Status

Accepted.

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

### Snap result

One narrow snapping query returns a `SnapResult` containing:

- the resolved world point;
- the stable scene-object GUID;
- the snap kind;
- an optional stable component reference; and
- an explicit association error when a visible discrete component cannot be
  represented by a stable reference.

Interactive acquisition initially produces only discrete point kinds:

1. a Point object;
2. a Mesh vertex; or
3. a Graph node.

Snapping uses an 18-logical-pixel screen-space radius so its acquisition
footprint remains usable across zoom levels. The nearest eligible discrete
point wins.

Fixed mode copies the resolved world point into a `PointAnchor`.

Associative mode accepts the same displayed point, vertex, and node targets and
stores their stable component references. The two modes differ only in
persistence. Lines, edges, faces, and surfaces do not produce interactive
candidates until their eligible geometry has an explicit highlight overlay.

### Tool lifecycle

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
data model permits mixed anchors; the UI makes each acquired anchor's mode
explicit when constructing a mixed pair.

Escape or explicit cancellation clears preview and result state and creates
nothing. A background or unsupported snap provides no anchor. Associative mode
never falls back to a fixed point. There is no construction-plane fallback,
general sub-object editing, repeating mode, or dimension editing in this phase.
Camera navigation remains available where its input does not conflict with the
active tool. Transient inspection and persistent dimension tools are both
one-shot in the first version: the second valid anchor completes the operation
and deactivates the tool.

## Accepted amendment: visible discrete point acquisition

Accepted on 2026-11-09 after direct use showed that a distance label alone did
not communicate which object components were available, which result a click
would accept, or whether the first anchor had been retained.

While a measurement tool is active, hovering one object displays every
projected discrete point snap provided by that object:

- the point of a Point object;
- the vertices of a Mesh; and
- the nodes of a Graph.

The palette follows the hovered object and disappears when the pointer leaves
it. Guidance points are larger, bright hollow squares; the winner and retained
anchors are distinct filled squares. Palette points are guidance and are not
independently occlusion-tested. Only the distinct highlighted winner within
the existing screen-radius and depth acceptance rules is click-eligible.

No invisible candidate is eligible. Standalone Lines, Mesh and Graph edges,
faces, and surfaces do not produce candidates. Later support must first define
and implement a visible candidate overlay for the corresponding segment,
region, or surface.

Winner visibility searches a small instance-depth footprint around the
projected point. Only pixels belonging to the hovered object and matching the
candidate depth within the existing precision epsilon qualify. This avoids a
steeply tilted Mesh edge overwriting the single center sample while neither
loosening the global epsilon nor admitting background, another object, or a
fully occluded component.

After the first winner is accepted, that anchor remains visible while the
palette follows the next hovered object. A missed point or background click
creates no anchor. Fixed mode has no implicit construction-plane or camera-plane
fallback because a background screen position does not define a unique world
point.

Transient measurement graphics use the single Viewer overlay canvas recorded
in ADR 025's implementation note. Persistent dimension visibility follows ADR
030. These corrections do not add a general snapping or widget framework.

## Consequences

- Measurement accuracy and association follow the explicitly supported snap
  targets; unsupported targets fail visibly.
- Fixed and associative acquisition share one result contract without
  conflating a snapped coordinate with a durable association.
- Input priority and background behavior are deterministic.
- Both outcomes share acquisition and preview without sharing persistence.
- A narrow one-shot lifecycle avoids a general tool framework promise.
- Hover guidance makes the available discrete anchors, accepted winner, and
  retained first anchor visible without changing snap eligibility.

## Compatibility

This is a new Viewer interaction. It does not change ordinary selection or
camera input when no measurement tool is active.

## Verification

- Verify activation, previous-tool cancellation, input priority, first anchor,
  preview, second anchor, and cleanup.
- Verify background clicks and pointer motion over background do not create or
  update anchors.
- Verify the 18-logical-pixel screen-space radius, nearest-candidate choice, and
  every accepted `SnapResult` field.
- Verify hovering a Point, Mesh, or Graph shows all projected discrete point
  snaps for that one object and leaving it clears the palette.
- Verify palette points are guidance only, the distinct depth-qualified winner
  is the only click-eligible result, and the first anchor remains visible while
  the palette follows the next object.
- Verify guidance points are bright hollow squares and the winner and retained
  anchors are distinct filled squares.
- Verify point-footprint visibility accepts a visible receding vertex while
  rejecting background pixels, another object's pixels, depth-mismatched
  same-object pixels, and fully occluded vertices.
- Verify Lines, Mesh and Graph edges, faces, and surfaces do not produce
  interactive candidates.
- Verify Fixed mode stores an exact displayed point, vertex, or node coordinate
  in a `PointAnchor`.
- Verify Associative mode accepts the same target set and stores stable
  component references without fallback.
- Verify opposite vertices of the 4 × 3 example resolve to a distance of 5.
- Verify transient completion follows ADR 024 without scene mutation.
- Verify fixed, associative, and any exposed mixed acquisition follow ADR 028,
  including no silent fallback.
- Verify persistent completion creates and selects exactly one root-level
  dimension and uses ADR 030's always-visible pass.
- Verify Escape and explicit cancellation create nothing in both modes.

## Dependencies

- Refines Accepted ADRs 005 and 024.
- Must implement Accepted ADR 028 anchor modes and unresolved behavior.
- Persistent results implement Accepted ADRs 021 and 022.
- Measurement labels and tolerance context implement Accepted ADR 027.
- Uses Accepted ADRs 003, 004, and 006 for selection, refresh/history
  boundaries, and the public Viewer facade.

## Decision

Approved on 2026-11-08. One screen-space snapping query returns a world point,
scene-object GUID, snap kind, optional stable component reference, and explicit
association error for an unstable discrete component reference. Interactive
acquisition is restricted to Point objects, Mesh vertices, and Graph nodes with
visible guides. Fixed mode stores their resolved coordinates; Associative mode
stores their stable component references without fallback.
Active tools receive left-click input before selection, ignore background,
preview on pointer movement, cancel on Escape, retain non-conflicting camera
navigation, and complete as one-shot transient or persistent operations. The
rationale is precise, efficient initial snapping without a general snapping or
sub-object editing framework. Amended on 2026-11-09 to expose projected
Point/Mesh-vertex/Graph-node guidance for the hovered object, keep only the
distinct depth-qualified winner click-eligible, retain the first anchor while
the palette follows the next object, and keep transient graphics visible over
scene geometry. Refined through direct use on 2026-11-09 with larger bright
square markers, an 18-logical-pixel radius, same-object point-footprint
visibility, removal of every invisible line, edge, face, and surface candidate,
and ADR 030's always-visible final pass for persistent dimensions. The rationale
is direct, reliable, unambiguous feedback without loosening occlusion rules.
Continuous and regional targets can return only after their highlight overlays
are defined.

