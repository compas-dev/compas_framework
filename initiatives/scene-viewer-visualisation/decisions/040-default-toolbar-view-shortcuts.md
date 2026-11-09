# ADR 040: Default Toolbar View Shortcuts

## Status

Accepted.

## Context

Viewer already exposes render-mode and current-view selection through the
View menu and System sidebar. Both surfaces use stable commands and shared
Viewer state, but the default toolbar is empty and hidden. Frequently changing
these presentation settings therefore requires opening a menu or sidebar.

Nine independent toolbar buttons would consume substantial space and require
new icons and active-button styling. Two labeled selectors can expose the same
choices while preserving one command and state path for every operation.

## Options

1. Add two state-bound toolbar selectors and show the default toolbar.
2. Add nine independent icon or text buttons.
3. Add the selectors but keep the default toolbar hidden.
4. Keep render-mode and view selection in the menu and sidebar only.

## Recommendation

Choose option 1.

Add one narrow toolbar item type, `select`, and populate the default toolbar
through `default_toolbar_items()`. The default controls, in order, are:

1. **Render Mode**
   - Shaded
   - Ghosted
   - Lighted
   - Wireframe
2. **View**
   - Perspective
   - Top
   - Front
   - Right
   - Ortho

The selectors reuse `viewer.change_rendermode` and `viewer.change_view` and
bind to `renderer.rendermode` and `renderer.view`. Toolbar, View menu, System
form, and public API updates synchronize through the existing Viewer-state
signal. State-driven selector updates block their own signals and do not invoke
the commands again.

Change the default `ui.toolbar.show` value to `True` so the shortcuts are
discoverable. An explicit configured value of `False` remains authoritative.
Existing custom `viewer.toolbar_items` remains the composition boundary.

Do not add renderer commands, a general toolbar-widget registry, an icon
system, or another state path.

## Consequences

- Render-mode and view shortcuts are visible by default and remain compact.
- Menu, sidebar, toolbar, and public API controls cannot drift because they
  observe the same state.
- Existing configurations that explicitly hide the toolbar remain unchanged.
- Applications that relied on the previous implicit hidden default gain one
  toolbar unless they set `ui.toolbar.show` to `False`.
- The supported toolbar schema gains one concrete state-bound selector type,
  not an arbitrary custom-widget mechanism.

## Verification

- Verify the exact selector labels, values, and ordering.
- Verify configured renderer state determines both initial selections.
- Verify each user selection invokes the existing command exactly once.
- Verify menu, System form, and public API changes update the toolbar without
  invoking a command again.
- Verify toolbar changes update the menu and System form through shared state.
- Verify explicit `ui.toolbar.show=False` remains effective and the unspecified
  default is visible.
- Verify invalid selector definitions and unsupported values fail clearly.
- Run focused offscreen Qt tests, the full Viewer suite, Ruff, Pyright, strict
  MkDocs, package CI, and framework integration.

## Dependencies

- Extends Accepted ADR 006's public Viewer UI facade.
- Amends Accepted ADR 020's default toolbar visibility without changing
  configuration ownership or schema.
- Coordinates with ADR 041 through the existing render-mode and view state
  paths but is independently implementable.

## Decision

Approved on 2026-11-09. The default toolbar gains visible, labeled Render Mode
and View selectors in that order. They reuse the existing commands and shared
renderer state, synchronize without recursive command invocation, and make the
toolbar visible by default while preserving an explicit
`ui.toolbar.show=False`. No button grid, new renderer command, general widget
registry, or icon system is authorized.
