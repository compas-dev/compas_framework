# ADR 005: Annotations, Measurements, and Overlays

## Status

Accepted, amended by ADRs 024 and 028.

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
- Measurement preview state belongs to the active Viewer tool. Completing a
  transient inspection does not mutate Scene. Completing an explicitly
  persistent dimension-annotation mode creates a durable distance dimension;
  cancelling either mode creates nothing.
- Fixed and associative persistent dimension modes both use snapping. Fixed
  acquisition stores a point; associative acquisition stores a supported
  component reference and never silently falls back to a point.

Align current Tag/Arrow behavior with these paths. Use one Viewer overlay layer
for the approved screen types and ordinary scene adapter registration for
world annotations. Do not add a general overlay registry.

## Consequences

- Persistence follows user intent rather than rendering technique.
- World annotations participate in hierarchy and transformations.
- View-dependent overlays remain independent of scene files.
- Current concrete renderer checks can be consolidated behind the two paths.
- Dimension editing, angular dimensions, and arbitrary overlay plugins remain
  later requirements. Initial snap targets and acquisition behavior are
  governed by ADR 026.

## Compatibility

Accepted ADR 023 records the completed migration audit and chooses a clean
break. `Tag`, `ArrowOverlay`, their aliases, and their serialized dtype paths
are removed when the canonical types land. Old payloads are unsupported and no
compatibility decoder silently reinterprets them.

## Verification

- Test distance derivation, units, precision, label override, transformed
  parents, serialization, and reload.
- Test transient inspection and persistent dimension preview/cancel/complete
  state transitions, including their different scene-mutation behavior.
- Test fixed and associative snapping, mixed anchors, and explicit unresolved
  component references without silent fallback.
- Assert scale and legend overlays are absent from scene serialization.
- Verify renderer ordering, resize behavior, and no concrete type checks in
  the main render loop for approved types.

## Affected packages

`compas`, `compas_viewer`, and `compas_framework`.

## Dependencies

- [ADR 001](001-ownership-boundaries.md)
- [ADR 002](002-indexed-buffer-geometry.md)
- [ADR 003](003-viewer-state-and-selection.md)

## Amendment

Accepted ADR 024 refines measurement outcomes after the user identified two
distinct intents. Live inspection is transient and never creates scene
content. Persistent dimension-annotation mode may share acquisition and
preview infrastructure, but only its completion creates a durable
`DistanceDimension`.

Accepted ADR 028 adds explicit fixed and associative persistent dimension
anchors. Both modes use snapping, but only Associative mode stores a component
reference. Missing components become unresolved rather than silently falling
back or displaying stale coordinates.
