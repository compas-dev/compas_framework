# ADR 035: Distance-Dimension Spatial Layout

## Status

Accepted on 2026-11-11; implemented, locally verified, and independently reviewed. Native direct use and hosted verification are pending.
The extension-line-width amendment coordinated with ADR 029 is implemented and
locally verified.

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

### Proposed initial editing surface

For exactly one selected, bound distance dimension, the Annotations details
panel adds a **Spatial Layout** group with:

- **Offset**, a required finite signed world-space number;
- **Plane Normal X**, **Plane Normal Y**, and **Plane Normal Z**;
- **Status**, a read-only derived result; and
- **Reset Layout**, which restores `offset=0.0` and `plane_normal=None`.

All three normal fields blank represents `None`. All three populated fields
represent one finite world-space vector. A partially blank normal, a
non-numeric value, or any non-finite component is invalid. The stored vector
is not normalized: its magnitude is immaterial to rendering, and its exact
components round-trip.

Editing Offset or a normal component updates only a local draft. Tabbing among
the four fields preserves partial drafts, including an incomplete normal.
**Apply Layout** is the explicit commit boundary: it parses the complete form
and creates one replacement `DistanceDimensionLayout`. Assignment is atomic;
components are never mutated individually. Invalid Apply restores every editor
from the durable layout, performs no mutation, and triggers no refresh. Escape
has the same rollback behavior and preserves annotation selection. **Reset
Layout** immediately assigns `offset=0.0` and `plane_normal=None`. A successful
changed Apply or Reset calls exactly one annotation-only refresh for the
selected entry, rebuilding its dimension geometry and bounds without touching
spatial geometry buffers.

Status uses this exact precedence:

1. When `offset == 0`, report `Resolved — no displacement` regardless of the
   normal or anchor layout inputs.
2. For a nonzero offset, report `Unresolved — dimension anchor is unresolved`
   when either anchor cannot resolve.
3. Otherwise report `Unresolved — anchors coincide` when the anchors coincide.
4. Otherwise report `Unresolved — plane normal is missing` when no normal is
   stored.
5. Otherwise report `Unresolved — plane normal is zero` for a zero vector.
6. Otherwise report `Unresolved — plane normal is parallel to dimension` when
   the cross product has zero length.
7. Otherwise report `Resolved`.

Status is derived Viewer presentation and is not serialized. When both anchors
resolve but the nonzero layout direction is missing, zero, or parallel, Viewer
draws the current zero-offset line while reporting the reason and does not
substitute a camera-dependent direction. If either anchor is unresolved,
ADR 028 remains authoritative: Viewer draws no cached, stale, or synthesized
dimension line.

The group is hidden for multiple selection, text and arrow annotations, and
unresolved data bindings. A bound dimension whose associative geometry is
currently unresolved still exposes the group, consistent with format editing.
Acquisition does not capture camera or construction-plane state.

`DistanceDimensionLayout` is a validated immutable-value-style data object:
`offset` and every supplied normal component must be finite. Scene
serialization advances from schema 4 to schema 5, and
`SceneAnnotation.ENTRY_SCHEMA_VERSION` advances to 2. COMPAS `DataDecoder`
decodes each nested `SceneAnnotation` before `Scene.__from_data__` can inspect
the parent Scene version. The entry payload must therefore carry its own
version rather than relying on the parent to select entry migration.

Every current/versioned entry (`version=2`) requires the `layout` field and
rejects missing fields or unsupported entry versions. Only a legacy
unversioned entry may omit `layout`; this is the narrow bottom-up JSON migration
path for a schema-4 Scene. Such an unresolved entry retains `layout=None`
because its item type is not yet known. When binding later determines that it
is a distance annotation, `None` normalizes to `DistanceDimensionLayout()`;
text and arrow annotations retain `None` and reject any non-`None` layout.
Schema 5 round-trips signed offsets and optional normals through versioned
entries.

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
- Verify real schema-4 JSON migration through an unversioned nested entry and
  later distance/text/arrow binding behavior.
- Verify versioned entry schema 2 requires `layout`, rejects unsupported
  versions, and schema-5 round-trips signed offsets and exact optional normal
  components.
- Verify tabbing preserves partial drafts, Apply is the only draft commit,
  invalid Apply and Escape restore durable values without refresh, and changed
  Apply or immediate Reset produces exactly one annotation-only refresh.
- Verify the exact status precedence, including zero offset overriding every
  normal/anchor layout condition, then anchor, coincidence, missing-normal,
  zero-normal, and parallel-normal order for nonzero offsets.
- Verify zero-offset rendering fallback only for missing, zero, or parallel
  layout direction when both anchors resolve.
- Verify an unresolved anchor preserves ADR 028 behavior with no cached,
  stale, synthesized, or fallback dimension line.
- Verify the Spatial Layout group visibility for supported and unsupported
  selection and binding states.

## Excluded from the initial version

- Viewport drag handles or clicking to place the dimension line.
- Automatic camera-facing offset directions.
- Reusable or live construction planes.
- Multi-dimension layout editing.
- Automatic label or dimension collision avoidance.

## Dependencies

- Extends Accepted ADRs 021, 028, 029, and 030.
- Preserves ADR 022's informational unit semantics.
- Does not approve a reusable Viewer construction-plane feature.

## Accepted UI amendment

The initial editing surface described above was identified as the preferred
first UI path on 2026-11-11 and was approved with the complete amended ADR.

## Decision

Approved on 2026-11-11. Core gains the validated durable layout and Scene
schema 5 migration described above. Viewer gains deterministic displaced
dimension rendering, extension lines, derived resolution status, displaced
bounds, and the atomic single-selection Spatial Layout form. The excluded
interactive and automatic-layout features remain outside this decision.

## Implementation verification

The completed Core tree passes 2,306 tests. The completed Viewer tree passes
652 tests with two expected offscreen native-OpenGL skips. Core and Viewer Ruff and
formatting, Viewer Pyright, focused Core source Pyright, strict Core and Viewer
MkDocs, framework direct-source integration with 15 passes and one expected
exact-VCS-metadata skip, independent review, and diff checks pass.

Full Core Pyright remains blocked by two unrelated existing documentation
example errors (`Tag` import and a VolMesh call). The Markdown doctest remains
blocked by a pre-existing `scene.add(box)` output mismatch. Native direct use,
hosted CI, and candidate-artifact verification remain pending.

## Accepted extension-line rendering amendment

The displaced main dimension line continues to use
`DimensionStyle.line_width`, whose default is already `3.0`. Both extension
lines use the proposed `DimensionStyle.extension_line_width`, default `1.0`
for newly constructed styles. Style-only edits refresh the selected annotation
once and do not mutate spatial buffers. Layout resolution, measured value,
bounds, label positioning, final no-depth rendering, and unresolved-anchor
behavior remain unchanged.

Legacy schema-5 scenes migrate the new width from their stored `line_width`,
preserving the exact appearance that previously used one width for all three
lines. The coordinated schema and UI contract is specified by ADR 029's
accepted amendment. It was approved on 2026-11-11, implemented, and locally
verified. Native user retesting and hosted verification remain pending.
