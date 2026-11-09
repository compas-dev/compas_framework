# ADR 035: Distance-Dimension Spatial Layout

## Status

Proposed.

## Context

Persistent distance dimensions currently draw their dimension line between the
two measured anchors. This keeps the measured value correct, but it does not
allow the line and label to be moved away from the geometry for legibility.

The measured anchors and value are semantic dimension data. The location of
the displayed dimension line is scene-specific presentation. A Viewer
construction plane can help an author choose an offset direction, but the
resulting dimension must not depend on mutable Viewer state or on the current
camera.

## Options

1. Store a signed world-space offset and captured plane normal as durable
   dimension layout on the scene annotation.
2. Store a complete construction plane on the semantic distance dimension.
3. Choose the offset direction from the current camera whenever the annotation
   is rendered.
4. Add the spatial offset to the existing screen-space dimension style.

## Recommendation

Choose option 1.

Add a narrow durable `layout` field to the scene annotation that presents a
distance dimension:

```python
DistanceDimensionLayout(
    offset: float = 0.0,
    plane_normal: Vector | None = None,
)
```

`SceneAnnotation.layout` has type `DistanceDimensionLayout | None`. A resolved
distance-dimension entry normalizes `None` to `DistanceDimensionLayout()`.
Supplying a layout for a resolved text or arrow annotation raises `ValueError`.
An unresolved entry may carry the layout until binding, when the same
annotation-type validation is applied.

`offset` is a signed distance in world coordinate units. The informational
unit stored by the distance dimension does not convert it. `plane_normal` is
captured in world coordinates. For resolved anchors `start` and `end`, the
positive offset direction is

```text
unit(plane_normal × (end - start))
```

The displaced endpoints define the dimension line. Extension lines connect
the measured anchors to those endpoints. The measured value continues to come
only from the original anchors. The existing logical-pixel label offset applies
relative to the displaced dimension line.

An offset of zero preserves current rendering and does not require a normal. A
nonzero offset is explicitly layout-unresolved when the normal is missing or
zero, the anchors coincide, or the normal is parallel to the measured segment.
Viewer does not substitute a camera-dependent direction.

A complete durable construction plane is not part of this decision. Its origin
does not affect the resolved layout. A future Viewer construction-plane tool
may copy its normal into the durable layout, but the dimension does not retain
a live reference to that authoring context.

## Consequences

- Dimensions can be placed away from measured geometry without changing their
  value or anchors.
- Fixed and associative dimensions use the same deterministic world-space
  layout.
- The same independently serialized dimension data can have different layouts
  in different scenes.
- The scene-annotation schema and Viewer dimension rendering require a
  coordinated clean update.
- A general construction-plane feature remains a separate future decision.

## Verification

- Round-trip zero and signed nonzero layout values with scene annotations.
- Verify default normalization and rejection on text and arrow annotations,
  including validation when an unresolved entry becomes bound.
- Verify the measured value is unchanged by layout offset.
- Verify positive and negative offsets and extension-line geometry.
- Verify associative-anchor updates recompute the displaced endpoints from the
  stored normal and current resolved anchors.
- Verify missing, zero, coincident, and parallel inputs produce an explicit
  layout-unresolved state with no camera fallback.
- Verify the existing logical-pixel label offset is relative to the displaced
  line and persistent dimensions remain in the final no-depth render pass.
- Verify annotation bounds include both anchors and displaced endpoints.

## Dependencies

- Extends Accepted ADRs 021, 028, 029, and 030.
- Preserves ADR 022's informational unit semantics.
- Does not approve a reusable Viewer construction-plane feature.

## Decision

Pending explicit approval.
