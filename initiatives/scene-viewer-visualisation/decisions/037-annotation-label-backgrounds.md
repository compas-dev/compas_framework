# ADR 037: Optional Annotation Label Backgrounds

## Status

Proposed.

## Context

Text and distance labels can overlap geometry or a dimension line. Without a
background, their glyphs may become unreadable. This is durable presentation,
not semantic annotation data, and it does not justify a general typography,
theme, or label-style system.

## Options

1. Add two direct optional background fields to scene-annotation
   presentation.
2. Add a new public label-background class.
3. Duplicate background fields in dimension style and a new text style.
4. Make backgrounds a Viewer-global display preference.

## Recommendation

Choose option 1.

Add only these fields to the durable scene-annotation presentation:

```python
label_background: Color | None = None
label_background_padding: float = 2.0
```

`None` keeps the current transparent result. The color alpha controls
background opacity. Padding is a nonnegative distance in logical pixels around
the rendered glyph bounds. The fields apply only when the presented annotation
has a text label, initially `TextAnnotation` and `DistanceDimension`. They do
not add label semantics to arrows. A resolved arrow entry accepts only the
defaults (`None` and `2.0`); assigning a background color or non-default
padding raises `ValueError`. An unresolved entry is validated the same way
when it becomes bound.

Viewer draws the background immediately behind the label in the label's
existing render pass. For a distance dimension, the line is drawn first and
the label background covers the portion beneath the label. No border, corner
radius, shadow, font, theme, or generalized style object is introduced.

A Viewer-only screen-text overlay may expose equivalent direct fields, but it
does not use scene-annotation storage.

## Consequences

- Labels remain legible over geometry and dimension lines.
- The schema stays transparent and avoids a new public helper type for two
  values.
- Background presentation round-trips independently from semantic annotation
  data.
- Core scene-annotation serialization and Viewer label rendering require a
  coordinated clean update.
- More elaborate typography remains outside scope.

## Verification

- Round-trip `None`, opaque, translucent, and transparent colors.
- Accept zero and positive logical-pixel padding and reject negative padding.
- Verify default rendering is visually unchanged.
- Verify the background encloses padded glyph bounds and is drawn behind text
  but in front of an overlapping dimension line.
- Verify background edits refresh only the affected annotation render layer.
- Verify semantic text, anchors, units, values, and precision remain unchanged.
- Verify annotations without labels do not gain background rendering.
- Verify non-default background presentation is rejected for resolved and
  newly bound arrow annotations.

## Dependencies

- Extends Accepted ADRs 021 and 029's scene-presentation boundary.
- Preserves ADR 029's narrow `DimensionStyle` rather than mixing screen-pixel
  label background fields into line and arrow presentation.
- ADR 036 may expose equivalent Viewer-owned fields for screen text.

## Decision

Pending explicit approval.
