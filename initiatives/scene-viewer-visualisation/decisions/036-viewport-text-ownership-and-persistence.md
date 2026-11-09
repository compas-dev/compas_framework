# ADR 036: Viewport Text Ownership and Persistence

## Status

Accepted.

## Context

Text placed at a location in the view can mean either a world annotation whose
position is chosen through the viewport or text that remains fixed to the
screen while the camera changes. These have different ownership and
serialization contracts. Treating both as the existing world-space
`TextAnnotation` would hide that distinction.

Persistent screen text also belongs to a particular view rather than to the
spatial Scene. The current initiative has not yet approved Session or view-state
persistence for such content.

## Options

1. Add a screen-pinned Viewer overlay in normalized viewport coordinates and
   keep it out of Scene serialization for now.
2. Place an existing world-space text annotation by intersecting the viewport
   ray with geometry or a construction plane.
3. Store screen coordinates directly in Scene annotations.
4. Make screen-pinned text persistent immediately by first designing Session
   and view-state serialization.

## Recommendation

Choose option 1 for the requested view-screen text.

Add one concrete Viewer-owned `ScreenTextOverlay` rather than a generalized
overlay registry. It contains text, a normalized viewport position,
horizontal and vertical alignment, and color. If ADR 037 is separately
accepted, it also exposes the equivalent narrow optional background fields.

`(0, 0)` is the top-left and `(1, 1)` is the bottom-right of the viewport.
Resizing preserves the relative position. Camera changes do not move the text.
Drawing is clipped to the viewport. The overlay is not pickable, does not enter
the spatial Scene or annotation collection, and is absent from Scene
serialization.

This recommendation intentionally does not make the overlay survive save/load.
If immediate persistence is required, implementation is blocked until a
separate Session/view-state decision defines ownership, stable identity, and
serialization. Viewer configuration is not an alternative owner because it
describes application defaults rather than document content.

The narrow initial scope exposes construction through `viewer.add_overlay`
and removal through `viewer.remove_overlay`; it does not add a partial
interactive authoring UI. A user-facing click-to-place command also needs a
place to list, select, edit, and delete the resulting screen overlays. If that
workflow is required now, implementation is blocked until the same approval
defines that Viewer-side management surface, or Session/view-state ownership
if the result must persist.

World-space text selected through the viewport remains a different operation
using the existing `TextAnnotation`; it requires an explicit world-point
acquisition contract and is outside this decision.

## Consequences

- The meaning of screen text remains stable under camera movement and viewport
  resize.
- Scene stays limited to spatial content and durable scene annotations.
- The implementation remains one concrete overlay instead of a speculative
  text or overlay framework.
- Screen-text persistence is deferred unless the user explicitly requires it,
  in which case Session/view-state architecture must be approved first.
- World-space text placement remains available as a separately designed
  feature rather than an overloaded mode.

## Verification

- Verify normalized positions at viewport corners and interior locations.
- Verify viewport resize preserves relative placement and camera changes have
  no effect.
- Verify drawing clips to the viewport and respects insertion order.
- Verify screen text is unpickable and excluded from Scene and annotation
  serialization.
- Verify color, alignment, and optional background presentation update only
  the overlay layer.
- Verify no Session or configuration persistence is implied by the initial
  implementation.

## Dependencies

- Extends Accepted ADRs 005 and 025 with one concrete overlay type.
- Uses ADR 037's narrow background presentation if both are accepted.
- Persistent screen text is blocked on a future Session/view-state ADR.
- World-space text placement would require a separate acquisition decision.

## Decision

Approved on 2026-11-09. Initial viewport text is a screen-pinned Viewer overlay
using normalized viewport coordinates. It is created and removed through the
existing `viewer.add_overlay` and `viewer.remove_overlay` boundary. The initial
scope is programmatic only and does not add interactive placement, listing,
selection, editing, deletion, or persistence. Those capabilities require
separate approval, with durable screen-text ownership blocked on a future
Session/view-state decision.
