# ADR 039: Scene-Owned Add Menu

## Status

Proposed.

## Context

Viewer currently exposes geometry presets in a separate top-level **Add** menu.
Every geometry item created by these commands enters the current spatial Scene,
alongside the Scene menu's clear, load, and save operations. Keeping Add at the
top level obscures that ownership.

Other creation workflows have different meanings. Measurement commands are
interactive acquisition tools even when they produce a durable dimension.
Transient overlays and system configuration do not enter the Scene.

## Options

1. Move the existing geometry hierarchy to **Scene > Add**.
2. Keep **Add** as a top-level menu.
3. Move every command that can eventually create durable data under Scene.
4. Expand Add with speculative datastructure, group, annotation, and text
   commands during the move.

## Recommendation

Choose option 1.

Move only the existing geometry hierarchy beneath **Scene > Add**:

- Primitives;
- Curves;
- Surfaces; and
- Shapes.

Preserve the existing command identifiers, callbacks, preset parameters, and
resulting Scene insertion behavior. This is a menu-ownership change, not a new
creation API.

Keep measurement acquisition under **Measure**, including fixed and
associative dimension commands. Keep Scene load as a separate Scene operation.
Do not add datastructure, group, general annotation, or text creation commands
as part of this change. Transient overlays and System settings remain outside
Scene > Add.

The old top-level Add path is removed without a compatibility alias. Extension
code should not receive a new arbitrary nested-menu registration API merely to
preserve the former path; any future menu-extension contract requires its own
evidence and decision.

## Consequences

- Menu placement communicates that added geometry belongs to the current
  Scene.
- Existing creation behavior and command identities remain stable.
- Measurement remains organized by authoring workflow rather than by the
  persistence of its result.
- The top-level menu becomes less crowded without introducing new commands or
  extension abstractions.
- Code or tests that locate the former top-level Add menu must use the new
  nested location.

## Verification

- Verify the top-level Add menu is absent and **Scene > Add** contains the four
  existing geometry categories in their current order.
- Verify every existing geometry command retains its identifier, callback,
  preset parameters, and resulting Scene object.
- Verify Measure still owns transient inspection and fixed and associative
  dimension acquisition.
- Verify Scene load, save, and clear remain separate operations.
- Verify no datastructure, group, general annotation, text, overlay, or System
  creation command is added.
- Update user and developer documentation that names the old Add menu path.

## Dependencies

- Consistent with Accepted ADRs 001 and 013's Scene ownership.
- Preserves Accepted ADRs 024 and 026's measurement-tool lifecycle.
- Requires no Core, Scene schema, or serialization change.

## Decision

Pending explicit approval.
