# ADR 025: Scale and Legend Overlay Contracts

## Status

Proposed.

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

## Consequences

- The scale bar has precise, testable meaning in both projection modes.
- Perspective display states its depth-dependent limitation rather than
  implying a global scale.
- Categorical legends cover a concrete initial need without speculative scalar
  normalization behavior.
- One narrow ordered layer replaces concrete main-loop checks without becoming
  a framework-wide extension registry.

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

## Dependencies

- Refines Accepted ADR 005.
- Uses Accepted ADR 006 for the public Viewer facade.
- Respects Accepted ADR 023's annotation/overlay vocabulary boundary.

