# ADR 037: Optional Annotation Label Backgrounds

## Status

Accepted; implemented, locally verified, independently re-reviewed, and
confirmed through user direct use. The default-background amendment was
accepted on 2026-11-11; implemented and locally verified.

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

Approved on 2026-11-10. Durable annotation labels gain only the optional
`label_background` color and nonnegative logical-pixel
`label_background_padding` described above. Viewer renders the background
immediately behind label text, including over a dimension line. No border,
corner radius, shadow, font, theme, generalized style object, or arrow-label
semantics are authorized.

## Annotations-details amendment

Direct use confirms that the stored and rendered background has no editing
surface in the Annotations details panel. Add controls only for a selected
text-bearing annotation:

- **Enable Background**, mapping disabled to `label_background=None`;
- a background color control, used only while enabled; and
- nonnegative logical-pixel padding.

The existing transparent construction default remains unchanged. These
controls edit the existing fields atomically and refresh only the affected
annotation layer. Arrow annotations and unsupported selection states do not
show the controls. This amendment adds no field, schema version, generalized
style object, or theme dependency.

Verification must cover enable/disable, opaque/translucent color, zero and
positive padding, rejection of negative padding without partial mutation,
serialization, selection changes, Escape/cancel behavior, and immediate
render refresh.

This amendment was approved on 2026-11-10. It authorizes the controls and
verification described above without changing the accepted storage contract.

## Amendment implementation verification

The selected-annotation controls are implemented and covered by the focused
corrected-contract tests and full Viewer suite recorded in the initiative
handoff. The user confirms the corrected Viewer works well through direct use.
The accepted default-background amendment is implemented and locally verified.

## Accepted default-background amendment

New distance dimensions completed through Viewer's interactive measurement
tools should start with their label background enabled. Resolve the background
from the effective Viewer scheme at creation time:

- light: `#FAFAFAE6`;
- dark: `#10161BE6`;
- padding: `2.0` logical pixels.

This changes only Viewer-created persistent distance dimensions. Existing and
deserialized dimensions, explicit `None` or color values, text annotations,
and Core programmatic construction retain their current behavior. A later
appearance change does not recolor an already created dimension.

This amendment was approved on 2026-11-11 with the exact scheme colors and
creation-time semantics above. Implementation and local verification pass as
recorded in the initiative handoff; native direct use and hosted verification
remain pending.
