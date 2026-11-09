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
- an optional normalized component parameter.

The snap kinds in priority order are:

1. point, mesh vertex, or graph node;
2. standalone line or graph-edge location; and
3. face or surface location.

Snapping uses a screen-space radius so its acquisition footprint remains
usable across zoom levels. Within the highest available priority group, the
nearest screen-space candidate wins.

Fixed mode accepts every supported snap kind and stores only the resolved world
point in a `PointAnchor`.

Associative mode initially accepts:

- point objects;
- mesh vertices;
- graph nodes; and
- locations on standalone lines or graph edges, stored with a normalized
  parameter.

Face and surface hits are valid in Fixed mode but associative face/surface
anchors are deferred. An unsupported associative result is rejected visibly
and never converted silently to a fixed point.

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
anchors are distinct filled squares. Continuous snap visualization is
deferred. Palette points are guidance and are not independently
occlusion-tested. Only the distinct highlighted winner within the existing
screen-radius and depth acceptance rules is click-eligible.

Mesh edges do not produce measurement candidates. Standalone Line objects and
Graph edges remain eligible because their continuous geometry is the relevant
measurement target rather than a competing secondary target on a surface
mesh.

Winner visibility searches a small instance-depth footprint around the
projected point. Only pixels belonging to the hovered object and matching the
candidate depth within the existing precision epsilon qualify. This avoids a
steeply tilted Mesh edge overwriting the single center sample while neither
loosening the global epsilon nor admitting background, another object, or a
fully occluded component.

After the first winner is accepted, that anchor remains visible while the
palette follows the next hovered object. In Associative mode, a face or surface
winner remains fixed-only and produces the approved visible rejection. The
supported point palette remains visible at the same time so the user can move
to a valid point, vertex, or node.

Transient measurement graphics use the single Viewer overlay canvas recorded
in ADR 025's implementation note. Completed world annotations use an equal-depth
comparison so a dimension coincident with measured geometry remains visible,
while geometry closer to the camera still occludes it. These corrections do
not add a general snapping or widget framework.

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
- Verify screen-space radius, snap priority, nearest-candidate choice, and
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
- Verify Mesh edges do not produce candidates.
- Verify Fixed mode accepts point/vertex/node, standalone-line/graph-edge, and
  face/surface hits but stores only a `PointAnchor`.
- Verify Associative mode accepts point/vertex/node and parameterized
  standalone-line/graph-edge hits while rejecting face/surface association
  visibly.
- Verify a face/surface rejection can coexist with the supported point palette.
- Verify transient completion follows ADR 024 without scene mutation.
- Verify fixed, associative, and any exposed mixed acquisition follow ADR 028,
  including no silent fallback.
- Verify persistent completion creates and selects exactly one root-level
  dimension, remains visible at equal depth, and remains occluded by closer
  geometry.
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
scene-object GUID, snap kind, optional stable component reference, and optional
normalized parameter. Priority is point/vertex/node, then standalone
line/graph edge, then face/surface. Fixed mode accepts all available snap kinds
and stores points. Associative mode initially supports point/vertex/node and
parameterized standalone-line/graph-edge anchors; unsupported association is
rejected without fallback.
Active tools receive left-click input before selection, ignore background,
preview on pointer movement, cancel on Escape, retain non-conflicting camera
navigation, and complete as one-shot transient or persistent operations. The
rationale is precise, efficient initial snapping without a general snapping or
sub-object editing framework. Amended on 2026-11-09 to expose projected
Point/Mesh-vertex/Graph-node guidance for the hovered object, keep only the
distinct depth-qualified winner click-eligible, retain the first anchor while
the palette follows the next object, and keep completed dimensions visible at
equal depth. Refined through direct use on 2026-11-09 with larger bright square
markers, same-object point-footprint visibility, and Mesh-edge exclusion. The
rationale is direct, reliable, unambiguous feedback without widening the
accepted snapping contract or loosening occlusion rules.

