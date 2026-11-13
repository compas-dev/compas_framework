# ADR 040: Default Toolbar View Shortcuts

## Status

Accepted baseline; amended on 2026-11-10 and locally verified. Direct use
confirms the standard-view buttons but rejects Render Mode popup focus. A
second amendment was approved on 2026-11-10, implemented, locally verified,
independently re-reviewed, and confirmed through user direct use. The grouped
viewport/measurement-menu amendment was accepted on 2026-11-11, implemented,
and locally verified.

## Context

Viewer already exposes render-mode and current-view selection through the
View menu and System sidebar. Both surfaces use stable commands and shared
Viewer state, but the default toolbar is empty and hidden. Frequently changing
these presentation settings therefore requires opening a menu or sidebar.

Nine independent toolbar buttons would consume substantial space and require
new icons and active-button styling. The original decision therefore used two
labeled selectors while preserving one command and state path for every
operation.

Direct use on native macOS later showed that view changes through the combo
popup could still leave viewport interaction without focus despite observing
the popup Hide lifecycle and requesting restoration. Standard views are
frequent, fixed actions and do not need a popup. Render mode remains a compact
multi-value choice and keeps its selector.

## Options

1. Add one state-bound Render Mode selector plus five exclusive, state-bound
   icon-only view buttons and show the default toolbar.
2. Keep two state-bound toolbar selectors.
3. Add nine independent icon or text buttons.
4. Keep render-mode and view selection in the menu and sidebar only.

## Recommendation

Choose option 1.

Keep the narrow `select` item for **Render Mode** and extend the existing
`button` item only with optional `state` and required `value` fields for
state-bound use. Populate the default toolbar through
`default_toolbar_items()`. The default controls, in order, are:

1. **Render Mode**
   - Shaded
   - Ghosted
   - Lighted
   - Wireframe
2. **Perspective** button with the existing palette-aware P icon
3. **Top** button with the existing palette-aware T icon
4. **Front** button with the existing palette-aware F icon
5. **Right** button with the existing palette-aware R icon
6. **Ortho** button with the matching palette-aware O icon

The Render Mode selector reuses `viewer.change_rendermode` and binds to
`renderer.rendermode`. Each view button reuses `viewer.change_view`, binds to
`renderer.view`, and declares the corresponding `value`. Buttons sharing that
state path form one exclusive group. A click invokes the existing command;
toolbar, View menu, System form, and public API updates then synchronize
through the existing Viewer-state signal. State-driven updates select the
matching control without invoking a command again.

An existing custom `type="button"` item without `state` keeps its unbound
callback behavior. The `state`/`value` fields define only this narrow
command-backed checked-state contract; they do not create a general toolbar
widget registry. `icon_only=True` hides button text while retaining `title` as
the tooltip and accessible name. Custom text-only and text-plus-icon buttons
remain unchanged.

Focus restoration is one event-driven pending operation shared by selector and
button activation. A `focusWindowChanged` signal and one queued readiness check
re-evaluate the request. Renderer focus is applied only after the main window
is both the focused window and active, and after any selector popup cycle has
finished. Do not use an arbitrary delay, polling retry, or fixed retry count.

Change the default `ui.toolbar.show` value to `True` so the shortcuts are
discoverable. An explicit configured value of `False` remains authoritative.
Existing custom `viewer.toolbar_items` remains the composition boundary.

Do not add renderer commands, a general toolbar-widget registry, an icon
system, or another state path.

## Consequences

- Render mode remains a compact dropdown, while the five standard views are
  one-click, popup-free, icon-only controls.
- Menu, sidebar, toolbar, and public API controls cannot drift because they
  observe the same state.
- Exactly one view button is checked for the current `renderer.view` value.
- Existing configurations that explicitly hide the toolbar remain unchanged.
- Applications that relied on the previous implicit hidden default gain one
  toolbar unless they set `ui.toolbar.show` to `False`.
- The supported toolbar schema keeps `select` and narrowly extends `button`
  with `state`, `value`, and optional `icon_only`; existing text-only,
  text-plus-icon, and unbound custom buttons remain valid.
- Semantic view titles remain available as tooltips and accessible names even
  though the default buttons display only P, T, F, R, and O icons.
- Focus restoration waits on observable Qt window and popup state without an
  arbitrary delay or retry loop.
- No arbitrary custom-widget mechanism is introduced.

## Verification

- Verify the Render Mode selector and five view-button icons, semantic titles,
  accessible names, tooltips, values, and ordering.
- Verify configured renderer state determines the initial selector value and
  exactly one checked view button.
- Verify each selector or button activation invokes the existing command
  exactly once and view-button activation restores viewport focus without a
  popup.
- Verify pending focus restoration does nothing while the main window is not
  focused and active or a popup cycle remains active, then completes exactly
  once after `focusWindowChanged` or the queued readiness check observes the
  ready state.
- Verify menu, System form, and public API changes update the toolbar without
  invoking a command again.
- Verify toolbar changes update the menu and System form through shared state.
- Verify state-bound buttons require a non-empty title, state path, command,
  and value; verify unsupported state values leave every button unchecked.
- Verify existing custom unbound buttons retain their callback behavior.
- Verify custom text-only and text-plus-icon buttons retain their presentation.
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

Amended on 2026-11-10 after native direct use showed that combo-popup teardown
could still disrupt viewport focus. The Render Mode dropdown remains. The View
selector is replaced by exclusive icon-only **Perspective**, **Top**,
**Front**, **Right**, and **Ortho** buttons bound to `renderer.view`. They use
the existing palette-aware P, T, F, and R assets plus a matching O asset; each
semantic title remains the tooltip and accessible name. The narrow toolbar
schema extends `type="button"` with `state`, `value`, and optional `icon_only`;
each button invokes the existing command and shared state keeps the checked
button, menu, System form, and public API synchronized without recursive
invocation. Custom text-only, text-plus-icon, and unbound buttons remain
supported. No general widget registry is authorized.

The earlier direct focus request is replaced by one pending event-driven
restoration. `focusWindowChanged` and a queued readiness check restore renderer
focus only after the main window is focused and active and the selector popup
cycle is complete. There is no arbitrary delay or retry loop. Actual-widget
tests and a native macOS probe cover the final revision. Earlier direct use
confirmed that button interaction had no focus problem before the icon-only
presentation was added. A subsequent direct-use retest confirmed the
standard-view buttons but found that Render Mode dropdown focus still fails.

## Implementation verification

The final toolbar/theme revision passes 47 focused tests, 61 initialization
smoke tests, five native macOS toolbar/Camera probes, and the full offscreen
Viewer suite with 587 passes plus one expected structured OpenGL skip. Ruff,
formatting, Pyright, strict MkDocs, diff checks, and independent review pass.
The framework direct-source gate passes 15 tests with one expected
exact-revision skip. Hosted package CI and candidate-artifact verification have
not been run for this tree.

## Second amendment after native retest

Native direct use confirms the five standard-view buttons, but the Render Mode
combo still fails to return viewport interaction focus reliably. The current
tests mask this path by forcing `hidePopup()` when synthetic interaction does
not close the popup. Native macOS can close it without delivering the watched
`Hide` event, leaving focus restoration pending indefinitely.

Remove the Render Mode combo from the default toolbar instead of adding more
popup-lifecycle machinery. Replace it with four exclusive state-bound buttons
using original semantic monochrome SVGs:

1. Shaded: filled cube.
2. Lighted: face-shaded cube.
3. Ghosted: translucent or dashed cube.
4. Wireframe: outline cube.

Move Perspective, Top, Front, Right, and Ortho from the default toolbar into a
private fixed list over the viewport. The approved interpretation of “view
selection” is this fixed standard-view set.
The control reuses `viewer.change_view` and `renderer.view`, remains synchronized
with the View menu, System form, and public API, and is private Viewer chrome.
It does not extend the mouse-transparent public overlay layer or create a
general viewport-widget registry.

Add three existing command-backed actions to the default toolbar:

- Zoom Selected, with a selection/magnifier icon;
- Zoom Extents, with a framing-corners icon; and
- Capture View, with a camera icon.

Reuse the palette-aware packaged-SVG path. Record asset origin and licensing;
retain semantic tooltips and accessible names; and verify high-DPI, light/dark,
checked, hover, focus, and disabled presentation. Preserve custom toolbar
composition and the narrow state-bound button contract.

Verification must exercise native activation followed immediately by viewport
orbit, pan, and zoom; command-once behavior; cancelled capture; and state
synchronization across toolbar, viewport control, menu, System form, and
public API. The proposal removes the failing popup from the default path rather
than claiming the current focus restoration is fixed.

This second amendment was approved on 2026-11-10. It authorizes the default
composition, private viewport control, assets, and verification described
above.

The corrected implementation passes the focused corrected-contract tests and
the full Viewer and direct-source framework gates recorded in the initiative
handoff, and the user confirms it works well through direct use. Hosted CI and
candidate artifacts remain pending. The accepted grouped-menu amendment is
implemented and locally verified.

## Accepted grouped viewport-menu amendment

Replace both the private fixed standard-view list and the four default toolbar
render-mode buttons with one private viewport menu button. Its menu has two
titled, exclusive groups:

1. **View** — Perspective, Top, Front, Right, Ortho.
2. **View Mode** — Shaded, Lighted, Ghosted, Wireframe.

Checked state and activation reuse the existing `renderer.view`,
`renderer.rendermode`, `viewer.change_view`, and
`viewer.change_rendermode` paths. Use a `QToolButton`/`QMenu`, not the native
combo box whose popup lifecycle failed direct use. Restore renderer focus from
the menu's deterministic triggered/hide lifecycle. Keep this private Viewer
chrome rather than adding a public interactive-overlay framework.

Remove the render-mode buttons from the default toolbar. Keep Zoom Selected,
Zoom Extents, and Capture View, and add one measurement menu button containing
only existing commands:

- Inspect Distance;
- Add Fixed Distance Dimension;
- Add Associative Distance Dimension; and
- Cancel Measurement.

This is a narrow default composition and menu-button presentation contract,
not a general toolbar-widget registry or new measurement behavior. The
amendment was approved on 2026-11-11. Implementation and local verification,
including popup and Escape lifecycle review, pass as recorded in the
initiative handoff. Native direct use confirms the grouped menu, focus,
alignment, non-overlap, and pressed-state behavior; hosted verification remains
pending.
