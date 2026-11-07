# ADR 005: Annotations, Measurements, and Overlays

## Status

Accepted.

## Context

Viewer has concrete `Tag` and `ArrowOverlay` rendering paths but no general
measurement, dimension, scale, or legend behavior. Treating every visual aid
as a scene item would serialize view-dependent UI; treating every annotation
as an overlay would lose world anchoring and durable intent.

## Options

1. Separate durable world annotations from transient screen overlays.
2. Make every annotation and overlay a core scene item.
3. Keep every visual aid as a renderer-special-cased Viewer class.
4. Add a framework-wide overlay plugin registry before adding features.

## Recommendation

Choose option 1.

- World text annotations and distance dimensions are serializable scene items
  with Viewer adapters. Distance dimensions store two anchors, unit,
  precision, and optional label override; distance is derived.
- Scale indicators and legends are transient screen-space Viewer overlays and
  are not serialized or picked initially.
- Measurement preview state belongs to the active Viewer tool. Completing the
  tool creates a durable distance dimension; cancelling creates nothing.

Align current Tag/Arrow behavior with these paths. Use one Viewer overlay layer
for the approved screen types and ordinary scene adapter registration for
world annotations. Do not add a general overlay registry.

## Consequences

- Persistence follows user intent rather than rendering technique.
- World annotations participate in hierarchy and transformations.
- View-dependent overlays remain independent of scene files.
- Current concrete renderer checks can be consolidated behind the two paths.
- Editing, snapping, angular dimensions, and arbitrary overlay plugins remain
  later requirements.

## Compatibility

Inspect existing serialized Tag/Arrow fixtures before choosing a migration.
Do not reinterpret ambiguous old data silently. Keep equivalent visible
behavior where the old type maps exactly; otherwise document removal and the
new construction path.

## Verification

- Test distance derivation, units, precision, label override, transformed
  parents, serialization, and reload.
- Test measurement preview/cancel/complete state transitions.
- Assert scale and legend overlays are absent from scene serialization.
- Verify renderer ordering, resize behavior, and no concrete type checks in
  the main render loop for approved types.

## Affected packages

`compas`, `compas_viewer`, and `compas_framework`.

## Dependencies

- [ADR 001](001-ownership-boundaries.md)
- [ADR 002](002-indexed-buffer-geometry.md)
- [ADR 003](003-viewer-state-and-selection.md)
