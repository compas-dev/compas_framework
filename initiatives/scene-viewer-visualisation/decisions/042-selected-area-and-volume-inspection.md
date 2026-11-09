# ADR 042: Selected Area and Volume Inspection

## Status

Accepted.

## Context

Viewer's Measure menu currently supports point-acquired distance inspection and
persistent distance dimensions. Area and volume are whole-object properties;
they do not require point snapping and should not be forced into the distance
tool state.

Core types expose area and volume through existing public APIs, but those APIs
are not syntactically uniform: some are methods and others are properties. A
selected scene object may also have inherited world transformations. Measuring
only its local item would disagree with displayed scale, while measuring its
render tessellation would silently replace exact public geometry behavior with
an approximation.

## Options

1. Add transient, selection-driven area and volume inspection using the
   represented item's public scalar and exact supported transformation rules.
2. Add click-to-acquire whole-object measurement tools.
3. Measure rendered tessellations for every object.
4. Add persistent area and volume annotations immediately.
5. Aggregate areas or volumes across the current selection.

## Recommendation

Choose option 1.

Add these commands to Measure:

1. Inspect Distance
2. Inspect Selected Area
3. Inspect Selected Volume
4. separator
5. Add Fixed Distance Dimension
6. Add Associative Distance Dimension
7. separator
8. Cancel Measurement

Use the public command and Viewer method identifiers
`viewer.inspect_selected_area` and `viewer.inspect_selected_volume`.

Each inspection requires exactly one selected spatial scene object. It first
cancels active and retained distance-inspection state, resolves the represented
item, and reads its public `area` or `volume` member structurally: call the
member when callable, otherwise use the property value. Missing members,
`NotImplementedError`, and `None` mean that the measurement is unsupported. An
open Mesh whose `volume()` returns `None` explicitly reports that it does not
enclose a measurable volume. Other implementation exceptions are reported as
operation failures rather than silently reclassified as unsupported.

Convert the result to a finite, nonnegative scalar. Reject booleans,
non-numeric values, non-finite values, and negative results. The public Viewer
method returns the world-space scalar or raises a clear error. Only the command
callback owns the read-only result or error dialog.

Use the complete inherited `SceneObject.worldtransformation`:

- For area, accept similarity transformations: rotation or reflection with a
  uniform scale. Multiply local area by the square of that scale. Reject
  non-uniform scale, shear, and projective transformations because a local
  scalar does not contain the orientation information needed for an exact
  transformed area.
- For volume, accept affine transformations and multiply local volume by the
  absolute determinant of the linear part. Reject projective transformations.

Similarity and affine classification may use COMPAS numerical tolerance
internally. Removing tolerance from Viewer UI in ADR 041 does not remove its
computational role. Never use rendered triangles as an implicit fallback.

Area meaning follows the represented item's public contract: for example,
planar enclosed area for planar regions and surface area for Mesh, Shape,
Polyhedron, and Brep values. Volume likewise follows the item's declared
contract.

Format the dialog using current Viewer precision. Append the declaration-only
unit with a squared or cubed exponent when present, such as `m²` or `m³`, and
perform no unit conversion. Retain no new measurement state. Do not mutate the
Scene, spatial or annotation selection, annotations, serialization, or
transformation history.

Do not aggregate multiple selections or add persistent area/volume
annotations, region acquisition, face snapping, a measurement registry, new
Core protocols, or an approximation mode.

## Consequences

- Users can inspect exact supported area and volume values from the existing
  selection model.
- The public Viewer methods remain UI-independent and reusable, while commands
  own dialogs.
- Displayed transforms affect results when a scalar can be transformed exactly.
- Unsupported APIs, open volumes, and transformations that cannot be resolved
  exactly fail explicitly instead of producing plausible but incorrect values.
- Persistent area and volume annotations and click-based region tools remain
  outside scope.

## Verification

- Verify zero, one, and multiple spatial selections.
- Verify method-valued and property-valued measurements.
- Verify Mesh area, closed Mesh volume, open Mesh volume rejection, analytic
  Shape, Polygon, Polyhedron, and available backend Brep behavior.
- Verify unsupported Group, Graph, BufferGeometry, and unresolved references.
- Verify parent and local rigid, reflected, and uniform-scale transformations.
- Verify area rejects non-uniform scale, shear, and projective transforms.
- Verify volume uses exact absolute affine-determinant scaling and rejects
  projective transforms.
- Verify boolean, non-numeric, negative, and non-finite results fail clearly.
- Verify precision and squared or cubed unit suffixes without conversion.
- Verify active and retained distance state is cancelled.
- Verify Scene content, both selections, annotations, serialization, and
  transformation history remain unchanged.
- Run focused Viewer tests, the full Viewer suite, Ruff, Pyright, strict
  MkDocs, package CI, and framework exact-source integration.

## Dependencies

- Uses Accepted ADR 003's ordered spatial selection.
- Uses Accepted ADR 004's world-transformation contract.
- Extends Accepted ADR 006's public Viewer facade.
- Defines a transient measurement outcome under Accepted ADR 024.
- Uses ADR 027's unit and precision semantics, as amended by ADR 041 if that
  proposal is accepted.
- Interacts with ADR 026 only by cancelling active distance state; it does not
  use point snapping.

## Decision

Approved on 2026-11-09. Measure gains transient Inspect Selected Area and
Inspect Selected Volume operations for exactly one spatial selection. They use
the represented item's public scalar, apply only the approved exact
world-transformation rules, format declaration-only squared or cubed units,
and present a read-only result without retaining state or mutating the Scene.
Unsupported data and transformations fail explicitly; tessellation fallback,
multi-selection aggregation, persistent annotations, and generic measurement
infrastructure are not authorized.
