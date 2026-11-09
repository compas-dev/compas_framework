# ADR 021: Durable Annotation Ownership and Schema

## Status

Accepted.

## Context

Accepted ADR 005 separates durable world annotations from transient Viewer
overlays, but it does not assign the durable data types to a package. The
current `Tag` and `ArrowOverlay` types live in `compas_viewer`, so a scene that
references them cannot load without the visualization backend installed.
Core has no neutral text, arrow, or distance-annotation data types.

The durable schema must express annotation intent without storing Viewer
resources, editor state, or rendering implementation details.

## Options

1. Define neutral annotation data in `compas.scene`; Viewer provides only the
   rendering operations.
2. Keep serializable annotation data in `compas_viewer`.
3. Define annotation data in `compas.geometry`.

## Recommendation

Choose option 1.

Add three backend-neutral data types to `compas.scene`:

- `TextAnnotation` stores text, a local anchor, height, height mode, and
  horizontal and vertical alignment;
- `ArrowAnnotation` stores local start and end anchors; and
- `DistanceDimension` stores two anchors governed by Accepted ADR 028, plus
  unit, precision, and an optional label override.

Keep the first schemas narrow. Color, opacity, visibility, hierarchy, and
transformation remain scene-object state. Font files, background rendering,
padding, screen offsets, arrowhead styles, snapping metadata, editor state, and
Viewer configuration do not enter the neutral data schema.

Fixed annotation anchors use the annotation item's local coordinates. A
root-level fixed dimension initially stores `PointAnchor` values equal to
acquired world points. A fixed pair can derive its local-coordinate distance
directly; associative and mixed pairs require their `ComponentAnchor`
references to resolve and otherwise report unresolved state. Viewer derives
the displayed distance from resolved anchors after applying the owning scene
object's world transformation where applicable.

Viewer registers ordinary rendering operations for these stable core types.
Core loading, inspection, transformation, and serialization never import Qt,
OpenGL, font libraries, or `compas_viewer`.

## Consequences

- Durable scene intent loads without a visualization backend.
- One canonical data model serves Viewer and future visualization contexts.
- The initial annotation schema deliberately omits existing Viewer-specific
  typography and arrow styling.
- Adding later semantic fields requires evidence and a separate approved
  change rather than copying renderer options into core.

## Compatibility

ADR 023 governs removal of the current Viewer-owned `Tag` and `ArrowOverlay`
paths. This ADR defines their proposed canonical replacements but does not add
a compatibility loader.

## Verification

- Serialize and load every annotation type without `compas_viewer` installed.
- Verify local anchors, transformations, hierarchy, and independently bound
  item identity.
- Verify local distance derivation and transformed-world display distance.
- Verify core plugin discovery imports no Viewer, Qt, OpenGL, or font modules.
- Verify Viewer rendering uses registered scene operations rather than core
  renderer dependencies.

## Dependencies

- Refines Accepted ADR 005.
- Implements Accepted ADR 028's fixed and associative anchor model.
- Respects Accepted ADRs 010, 013, and 014 for item references, stable scene
  objects, and context-keyed rendering operations.

## Decision

Approved on 2026-11-08. Durable `TextAnnotation`, `ArrowAnnotation`, and
`DistanceDimension` data belong to `compas.scene`; Viewer provides rendering
operations only. The schemas remain narrow and backend-neutral, with
presentation, hierarchy, and transformation owned by scene objects. The
rationale is that durable scene intent must load and serialize without a
visualization backend or renderer-specific resources.

