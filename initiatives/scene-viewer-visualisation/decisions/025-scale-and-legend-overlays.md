# ADR 025: Scale and Legend Overlay Contracts

## Status

Accepted.

## Context

Accepted ADR 005 assigns scale indicators and legends to a transient,
non-serialized Viewer overlay layer, but it does not define the meaning of the
scale or the initial legend content model. The first contract should be useful
without introducing a colormap framework or a general overlay registry.

## Options

1. Add a camera-target scale bar and an ordered categorical legend.
2. Limit scale display to orthographic view and add continuous numeric legends.
3. Add one generalized overlay and legend schema for every future use.

## Recommendation

Choose option 1.

Viewer owns one ordered overlay collection exposed through
`viewer.add_overlay()` and `viewer.remove_overlay()`. It accepts only the
approved concrete overlay types; it is not a plugin registry.

`ScaleBarOverlay` represents world distance at the camera-target plane. It is
globally exact in orthographic projection and explicitly local to that depth in
perspective projection. It selects a readable `1–2–5 × 10ⁿ` bar length near a
target pixel width.

`LegendOverlay` stores an optional title and ordered categorical
`(label, color)` entries. Continuous ranges, normalization, interpolation,
colormaps, and out-of-range behavior are deferred.

Both overlay types are Viewer-owned, screen-space, unpicked, and absent from
scene serialization.

## Implementation note: one widget overlay canvas

Recorded on 2026-11-09 after direct use of the measurement preview exposed
missing transient graphics and an intermittent `QPainter` failure on macOS.

Viewer renders scale, legend, and measurement feedback on one transparent,
mouse-transparent `QWidget` canvas stacked above the OpenGL renderer. The
renderer remains a pure OpenGL surface. `QPainter` is created, used, and ended
only during the overlay widget's ordinary `paintEvent`. A completed renderer
frame and a direct change to overlay or measurement state both schedule a
canvas repaint.

The canvas remains Viewer-owned, screen-space, unpicked, and absent from scene
serialization. This mechanism implements the already approved overlay
ownership and lifecycle; it does not introduce a general widget, snapping, or
plugin framework.

## Consequences

- The scale bar has precise, testable meaning in both projection modes.
- Perspective display states its depth-dependent limitation rather than
  implying a global scale.
- Categorical legends cover a concrete initial need without speculative scalar
  normalization behavior.
- One narrow ordered layer replaces concrete main-loop checks without becoming
  a framework-wide extension registry.
- One ordinary widget paint lifecycle keeps transient UI painting separate
  from the OpenGL renderer and its context lifecycle.

## Compatibility

These are new transient Viewer APIs. They do not preserve the obsolete durable
`ArrowOverlay` behavior removed by ADR 023.

## Verification

- Verify overlay insertion order, removal, resize behavior, and serialization
  exclusion.
- Verify orthographic scale and perspective target-depth scale, including the
  `1–2–5 × 10ⁿ` choice.
- Verify categorical legend order, title, and colors.
- Verify overlays do not participate in scene selection or instance picking.
- Verify the canvas is transparent to pointer input, is stacked above the
  renderer, and repaints after frame swaps and direct transient-state changes.
- Verify `QPainter` ownership begins and ends inside the canvas `paintEvent`.

## Dependencies

- Refines Accepted ADR 005.
- Uses Accepted ADR 006 for the public Viewer facade.
- Respects Accepted ADR 023's annotation/overlay vocabulary boundary.

## Decision

Approved on 2026-11-08. Viewer owns one ordered, concrete overlay layer with
public add/remove operations. The initial `ScaleBarOverlay` reports world scale
at the camera-target plane using readable `1–2–5 × 10ⁿ` lengths, with its
perspective depth limitation explicit. The initial `LegendOverlay` contains an
optional title and ordered categorical label/color entries. Both remain
screen-space, unpicked, and absent from Scene serialization. The rationale is a
small useful contract without a general overlay registry, continuous-colormap
semantics, or misleading global perspective scale.

