# ADR 043: Built-in COMPAS Viewer Theme

## Status

Accepted.

## Context

Viewer currently exposes `system`, `light`, and `dark` appearances. They apply
a complete palette to the application-wide Qt instance. The implementation
also changes the renderer background whenever appearance changes, even though
background, selection, grid, object, annotation, measurement, and overlay
colors otherwise have separate configuration or data ownership.

The current palettes are generic. Component-local stylesheets provide a small
amount of additional presentation, and the pending System-section refinement
adds another local heading rule. There is no central theme module, public theme
contract, or authoritative COMPAS palette in the repositories inspected for
this decision.

The request is for a coherent COMPAS-styled Viewer, not for an arbitrary theme
framework. Exact colors must therefore be approved without presenting inferred
values as an organization-wide COMPAS brand standard.

## Options

1. Treat COMPAS as Viewer's one built-in theme and keep `system`, `light`, and
   `dark` as its color-scheme choices.
2. Add `compas` as a fourth appearance value.
3. Add independent public theme and color-scheme settings.
4. Allow custom stylesheets or theme plugins.
5. Coordinate Qt chrome and all viewport/content colors under one theme.

## Recommendation

Choose option 1.

COMPAS Viewer has one built-in theme with light and dark variants. Preserve the
existing public configuration and menu values:

```python
config.ui.appearance = "system"  # or "light" or "dark"
```

`system` follows the operating-system color scheme. `light` and `dark` force
the corresponding variant. Do not add a public theme field, another appearance
value, a theme registry, arbitrary stylesheet loading, or plugin hooks while
only one theme is required. Configuration remains schema 3.

Implement the theme privately in Viewer with semantic light and dark tokens,
complete `QPalette` construction, and at most one narrowly scoped application
stylesheet for states that palette roles cannot express. Cover application
surfaces, controls, inputs, alternate surfaces, primary and muted text,
disabled states, borders, accent states, selected text, links, errors,
keyboard focus, and tooltips. Do not introduce a public token, typography,
spacing, icon-theme, or component-theme abstraction.

The theme owns Qt application chrome only. It must not mutate renderer
background, selection, or grid colors; scene-object appearance; annotation or
dimension styles; measurement markers; legends; or overlays. Remove the
current appearance-driven renderer-background mutation. Explicit renderer and
content settings therefore remain unchanged when appearance switches. A dark
application surrounding a light viewport is valid.

Preserve the platform Qt UI font. Retain the packaged COMPAS application icon,
the configured `window.icon` override, and the existing monochrome UI icons.
Any new font or icon family requires a separate asset, licensing, fallback,
and accessibility decision. Reconcile the System-section heading refinement
with the private theme while keeping System layout behavior owned by
`SystemPanel`.

Exact tokens are an approval gate. Before implementation, approve either an
authoritative COMPAS brand source and an accessible token table derived from
it, or an explicitly Viewer-specific palette described as COMPAS Viewer
styling rather than an organization-wide standard. The approved table must
include contrast evidence for normal and selected text, links, disabled but
readable controls, and keyboard focus.

## Proposed Viewer-specific token table

The following table uses the blue hue visible in existing COMPAS-facing local
materials as visual direction only. It is proposed as the COMPAS Viewer
palette, not as an authoritative organization-wide brand standard.

| Token | Light | Dark | Purpose |
|---|---:|---:|---|
| `window` | `#F4F7F9` | `#18242C` | Application background |
| `surface` | `#FFFFFF` | `#10191F` | Panels and input base |
| `surface_raised` | `#E8EEF2` | `#24343E` | Buttons and raised controls |
| `surface_alternate` | `#ECF2F5` | `#1E2D36` | Alternate rows and secondary areas |
| `text` | `#17242D` | `#F2F6F8` | Primary text |
| `text_muted` | `#526674` | `#B8C5CC` | Secondary text |
| `text_disabled` | `#71818C` | `#87969E` | Disabled and placeholder text |
| `border` | `#AAB8C2` | `#52636D` | Borders and separators |
| `accent` | `#0077B6` | `#38BDF2` | Accent and focus |
| `accent_hover` | `#00689D` | `#159ED0` | Hovered accent control |
| `accent_pressed` | `#005985` | `#0777AD` | Pressed accent control |
| `selection` | `#0077B6` | `#0777AD` | Selection background |
| `selection_text` | `#FFFFFF` | `#FFFFFF` | Text over selection |
| `link` | `#00689D` | `#5CC8F2` | Underlined links |
| `error` | `#B42318` | `#FF8A80` | Error and destructive emphasis |
| `focus` | `#0077B6` | `#38BDF2` | Keyboard-focus outline |
| `tooltip_surface` | `#17242D` | `#24343E` | Tooltip background |
| `tooltip_text` | `#FFFFFF` | `#F2F6F8` | Tooltip text |

Map Qt `Window`, `Base`, `AlternateBase`, `Button`, text, tooltip, link,
highlight, placeholder, and bright-text roles directly to the corresponding
semantic tokens. Use `text_disabled` for disabled text roles. Use fixed private
surface and border tokens for Qt light, midlight, mid, dark, and shadow roles;
do not derive colors dynamically. Active and inactive groups initially share
the same mapping, while disabled uses its explicit text mapping.

Limit the application stylesheet to a two-logical-pixel keyboard-focus
outline, accent hover and pressed states that Qt palette roles cannot express
reliably, underlined links, and the approved System-section heading hierarchy.

Calculated WCAG relative-luminance contrast is:

| Pair | Light | Dark | Target |
|---|---:|---:|---:|
| Primary text / window | `14.71:1` | `14.55:1` | `4.5:1` |
| Muted text / window | `5.56:1` | `8.96:1` | `4.5:1` |
| Disabled text / window | `3.74:1` | `5.19:1` | project target `3:1` |
| Selected text / selection | `4.87:1` | `4.94:1` | `4.5:1` |
| Link / primary background | `6.06:1` | at least `8.29:1` | `4.5:1` |
| Error / primary background | `6.57:1` | at least `6.93:1` | `4.5:1` |
| Focus / adjacent primary surface | `4.87:1` | at least `7.33:1` | `3:1` |

Links remain underlined so recognition does not depend on color. Focus uses a
persistent outline and does not depend on fill color. Native Qt captures may
justify small token corrections without reopening the structural decision only
when rendering or measured contrast fails. A hue-family, ownership, font, icon,
or public-configuration change requires an amendment.

## Consequences

- Viewer gains coherent branded chrome without expanding its public
  configuration or extension surface.
- Operating-system following and forced light/dark behavior remain intact.
- Appearance changes stop overwriting explicit viewport presentation.
- Existing configurations remain schema-compatible, but users who relied on
  appearance to change the viewport background must set that renderer value
  explicitly.
- The approved palette is Viewer-specific styling and is not presented as an
  organization-wide COMPAS brand standard.
- Core, Scene serialization, content appearance, and overlay contracts remain
  unchanged.

## Verification

- Verify the approved semantic tokens map to complete Qt palette roles for
  both variants.
- Verify `system` resolution, operating-system scheme changes, and runtime
  switching between all three existing appearance values.
- Verify appearance does not mutate renderer, grid, selection, object,
  annotation, measurement, legend, or overlay colors.
- Verify configuration round-trip remains schema 3 and configured window icons
  remain authoritative.
- Verify menus, toolbar, all three sidebar domains, trees, forms, dialogs,
  tooltips, disabled states, selection, and keyboard focus.
- Verify existing icons remain legible in both variants and at high DPI.
- Record contrast checks against the approved token table.
- Run focused offscreen Qt tests, the full Viewer suite, Ruff, formatting,
  Pyright, strict MkDocs, package CI, and framework exact-source integration.
- Capture native light and dark results on macOS, Windows, and Linux before
  claiming cross-platform visual completion.

## Dependencies

- Preserves ADR 019 configured identity and icon override.
- Preserves ADR 020 configuration lifecycle and schema ownership.
- Covers ADR 032's three sidebar domains without changing their structure.
- Covers ADR 040's toolbar controls without changing their command/state path.
- Preserves ADR 041's private System layout ownership.

## Decision

The structural contract was approved on 2026-11-10. COMPAS Viewer has one
built-in theme with system-following light and dark variants, the existing
appearance configuration remains unchanged, and theme ownership is limited to
Qt chrome. No public theme framework or renderer/content color coupling is
authorized.

The Viewer-specific token table in this ADR was approved on 2026-11-10. It is
the initial implementation contract and is not an organization-wide COMPAS
brand standard. Small token corrections remain limited to demonstrated native
rendering or measured-contrast failures as specified above.

## Accepted content-palette amendment

Direct use now requests coordinated light and dark viewport/content defaults.
This would amend the accepted chrome-only boundary only for omitted Viewer
presentation values, as specified by Accepted ADR 046. Explicit and serialized
colors remain authoritative. Core defaults do not change.

The accepted first version resolves defaults from the effective scheme when a
Viewer object or dimension is created. Switching appearance later changes
chrome and the automatic viewport background, but does not guess which already
materialized geometry colors were defaults. Live recoloring of existing
objects remains deferred until a separate design can preserve automatic versus
explicit color provenance.

Viewer configuration advances to schema 4. Only
`RendererConfig.backgroundcolor=None` means automatic; schema-3 concrete
backgrounds migrate as explicit. ADR 046 owns the exact migration and geometry
channel-precedence rules.

This amendment was approved on 2026-11-11 together with ADR 046's exact tokens,
schema, precedence, and creation-time semantics. Implementation and local
verification pass as recorded in the initiative handoff; native direct use and
hosted verification remain pending.
