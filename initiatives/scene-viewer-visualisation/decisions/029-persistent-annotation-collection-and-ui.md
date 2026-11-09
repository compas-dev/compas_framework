# ADR 029: Persistent Annotation Collection and UI

## Status

Accepted.

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
