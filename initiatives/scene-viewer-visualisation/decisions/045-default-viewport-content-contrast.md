# ADR 045: Default Viewport and Content Contrast

## Status

Accepted; implemented, locally verified, and confirmed through user direct
use. Accepted ADR 046 supersedes it for new Viewer behavior once implemented.

## Context

Direct use in the light Viewer scheme shows insufficient distinction between a
new default white surface and the default white viewport. Core currently
materializes white as the default scene-object color, while Viewer separately
defaults its renderer background to white.

Accepted ADR 043 owns Qt chrome only. It intentionally prevents `system`,
`light`, and `dark` appearance changes from mutating renderer or content
colors. The contrast correction must therefore be fixed presentation, not an
adaptive theme coupling.

## Options

1. Change Viewer's fixed default viewport background to an approved neutral.
2. Change Core's default scene-object/surface color to an approved neutral.
3. Adapt viewport or content colors to the effective light/dark scheme.
4. Add a Viewer default-surface-color configuration layer.

## Recommendation

Choose option 1.

Changing the Viewer background is the narrowest correction: it creates
contrast with existing white content, preserves explicit object colors, and
does not alter Core defaults for other visualization backends. The new value
must remain one fixed renderer default across `system`, `light`, and `dark`.
Explicit configured renderer backgrounds remain authoritative.

Option 2 more literally changes newly constructed surfaces, but it is a Core
scene-presentation change affecting every backend and potentially serialized
new content. Choose it only with explicit cross-backend compatibility approval.
Reject option 3 because it contradicts ADR 043 and makes content appearance
mode-dependent. Defer option 4 because Core currently materializes white, so
Viewer cannot distinguish inherited white from explicitly requested white
without a broader state-contract change.

The approved fixed neutral is `#D8DDE2`. It is not inferred from the Qt theme
token table because ADR 043 does not own the viewport.

## Consequences

- Default white surfaces remain visible against the default viewport.
- Explicit renderer and scene-object colors keep their existing ownership.
- Appearance switching does not recolor the viewport or content.
- Existing configurations that omit a renderer background receive the new
  Viewer default; configurations with an explicit value do not change.
- A Core default-color change remains a separate broader alternative, not a
  hidden consequence of this decision.

## Verification

- Verify `#D8DDE2` against white default surfaces and dimension/selection
  presentation.
- Verify default construction and configuration round-trip.
- Verify explicit renderer backgrounds remain unchanged.
- Verify `system`, `light`, and `dark` switching does not mutate renderer or
  content colors.
- Inspect native light and dark Viewer chrome around the fixed viewport on
  macOS, Windows, and Linux.
- Run focused configuration and Viewer tests, full Viewer tests, Ruff,
  formatting, Pyright, strict MkDocs, package CI, framework integration, and
  candidate-artifact verification as applicable.

## Dependencies

- Preserves ADR 043's Qt-chrome-only ownership.
- Coordinates with ADR 029's explicit dimension presentation and ADR 040's
  proposed toolbar/viewport controls without changing them.

## Decision

Approved on 2026-11-10. Viewer changes its fixed default renderer background to
`#D8DDE2`. Core's white scene-object and surface defaults remain unchanged.
The value does not adapt to `system`, `light`, or `dark`, and explicit renderer
background configuration remains authoritative.

## Implementation verification

Configuration tests, the full Viewer suite, quality checks, strict
documentation build, and direct-source framework gate pass as recorded in the
initiative handoff, and the user confirms the corrected Viewer works well
through direct use. Hosted verification remains pending. The accepted
superseding amendment is implemented and locally verified.

## Accepted superseding amendment

ADR 046 replaces the fixed `#D8DDE2` default with scheme-aware Viewer viewport
and omitted-presentation defaults. ADR 045 remains the
record of the earlier fixed-background decision but is superseded for new
Viewer behavior. Core defaults and explicit colors remain unchanged. During
schema-3 to schema-4 migration, `#D8DDE2` remains an explicit background; it is
never guessed to be the new automatic value.

Approved on 2026-11-11. ADR 046's replacement is implemented, locally verified,
and confirmed through native direct use; hosted verification remains pending.
