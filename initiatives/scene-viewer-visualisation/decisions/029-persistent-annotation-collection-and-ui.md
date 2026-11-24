# ADR 029: Persistent Annotation Collection and UI

## Status

Accepted; amended 2026-11-10 and 2026-11-11. The independent
extension-line-width amendment is implemented and locally verified.

## Context

Persistent annotations are currently represented as ordinary root-level scene
objects. This makes them appear in the spatial scene tree and gives them the
same parent/child and transformation semantics as geometry, even though a
dimension instead references fixed world points or components of spatial scene
objects.

Persistence, spatial hierarchy, rendering, and user-interface placement are
independent concerns. An annotation can remain durable scene/session data
without becoming a transformable child in the ordinary object hierarchy.

## Options

1. Add one ordered, scene-scoped annotation collection outside the spatial
   hierarchy and expose it through a separate flat Annotations UI.
2. Add a reserved Annotations group inside the ordinary hierarchy and hide its
   special behavior behind UI filtering.
3. Move annotations to Session rather than Scene.
4. Keep annotations as ordinary root-level scene objects.

## Recommendation

Choose option 1.

Core Scene owns an ordered persistent annotation collection separate from its
spatial object tree. Annotation data remains independently serializable and is
referenced by stable identity; Scene records placement, ordering, and
presentation state without embedding independently owned data.

Semantic annotation data and presentation remain separate. A
`DistanceDimension` continues to own anchors, unit, precision, and label. Its
collection entry owns durable visibility and a narrow dimension style. The
initial style contains only color, line width, text size, arrow size, and label
offset. It is not a generalized styling or theme framework.

Collection entries have no parent, child, or inherited transformation. Fixed
dimension anchors are world-coordinate points. Associative anchors resolve
against the referenced scene objects and their world transformations. Ordinary
object transform, reparent, and hierarchy operations do not apply to
annotations.

Viewer presents the collection in a separate flat **Annotations** UI rather
than mixing it into the Scene tree. Initial operations are visibility,
selection, naming, removal, and editing the narrow supported style. Annotation
selection must not imply that the annotation can be transformed like a spatial
object.

Session does not own the collection. A future Session may aggregate the Scene,
its independently serialized data, settings, and history, but dimensions that
reference scene-object GUIDs remain scene-scoped.

## Consequences

- Spatial hierarchy again represents only transformable spatial composition.
- Persistent dimensions remain scene-scoped and serializable without living
  inside the ordinary tree.
- Viewer gains a clear location for annotation-specific controls without
  inventing hierarchy behavior.
- Dimension presentation can be changed without mutating its semantic
  measurement data.
- Scene serialization and the current annotation wrapper/storage model require
  an explicit schema migration.
- Existing annotation entries require a clean migration decision before
  implementation; no compatibility mechanism is implied by this proposal.

## Compatibility

This changes Scene's durable schema and the public location of persistent
annotations. Implementation must define the exact schema transition and update
Core, Viewer, framework gates, examples, and documentation together.

## Verification

- Round-trip spatial hierarchy and ordered annotations independently.
- Bind independently loaded annotation data by stable identity.
- Verify annotations have no node, parent, children, or inherited transform.
- Verify associative anchors resolve against spatial scene objects.
- Verify ordinary reparent and transform operations reject annotations.
- Verify the Scene tree excludes annotations and the flat Annotations UI shows
  them in collection order.
- Verify visibility, selection, naming, and removal do not mutate spatial
  hierarchy.
- Verify supported dimension-style values round-trip and refresh only the
  annotation render layer.
- Verify semantic anchors, unit, precision, and label are unchanged by style
  edits.
- Verify a future Session can aggregate the Scene without becoming annotation
  owner.

## Dependencies

- Amends Accepted ADRs 005, 013, and 021.
- Preserves ADR 010's independent-data binding boundary.
- Rendering is independent and governed by Accepted ADR 030.

## Decision

Approved on 2026-11-09. Core Scene owns one ordered annotation collection
outside the spatial hierarchy. Viewer presents it through a separate flat
Annotations UI. Semantic annotation data remains independent from durable
visibility and the narrow dimension style consisting of color, line width,
text size, arrow size, and label offset. Annotations have no hierarchy or
inherited-transform semantics, and Session remains only a possible future
aggregate rather than the annotation owner.

Amended on 2026-11-10: a newly constructed default `DimensionStyle` uses
`Color.magenta()` rather than `Color.white()` for its line and label. Explicit
colors remain authoritative, and deserialization preserves the stored color.
This changes no serialized field or schema version and does not rewrite
existing data. Magenta is a visible starting point, not a universal contrast
guarantee for every viewport background. No adaptive contrast, theme coupling,
outline, or automatic recoloring is added.

## Accepted extension-line-width amendment

Extend the durable narrow style with one independent positive finite width:

```python
DimensionStyle(
    line_width=3.0,
    extension_line_width=1.0,
    ...,
)
```

`line_width` continues to control the main dimension line and its arrowheads.
`extension_line_width` controls only the two lines from the measured anchors
to the displaced endpoints. Both are logical-pixel values. The Viewer form
labels them **Dimension Line Width** and **Extension Line Width**. Extension
lines retain the dimension color and selection behavior; no separate color,
dash pattern, opacity, or arrow style is added. A zero-offset dimension draws
no extension lines.

New styles keep the existing `line_width=3.0` default and use
`extension_line_width=1.0`. Preserve legacy appearance through a closed
schema transition: advance Scene schema 5 to 6, annotation-entry schema 2 to
3, and add `DimensionStyle.STYLE_SCHEMA_VERSION = 2`. Current versioned style
payloads require `extension_line_width`. A genuine unversioned schema-5 style
migrates with `extension_line_width=line_width`; a schema-6 scene rejects a
legacy or malformed style. Explicit current values round-trip unchanged.

Approved on 2026-11-11. The schema migration and Viewer behavior are implemented
and locally verified; native user retesting and hosted verification remain
pending.
