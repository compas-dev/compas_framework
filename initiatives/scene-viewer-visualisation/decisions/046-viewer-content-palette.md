# ADR 046: Viewer Scheme-Aware Content Palette

## Status

Accepted on 2026-11-11; implemented and locally verified.

## Context

Direct use requests an almost-white viewport with darker geometry in the light
scheme and the opposite hierarchy in the dark scheme. Core currently
materializes concrete colors and does not preserve whether a value was omitted
or explicitly selected. Heuristically recoloring matching values would
therefore overwrite legitimate user choices.

## Options

1. Resolve Viewer-owned defaults from the effective scheme at object creation.
2. Add durable automatic-versus-explicit color provenance to Core.
3. Recolor values heuristically whenever the scheme changes.
4. Keep one fixed viewport/content palette.

## Recommendation

Choose option 1 with these exact tokens:

| Role | Light | Dark |
|---|---:|---:|
| Viewport | `#FAFAFA` | `#10161B` |
| Surface and face | `#D8DEE4` | `#3A4650` |
| Line and edge | `#4B5563` | `#B8C2CC` |
| Point and vertex | `#111827` | `#F2F6F8` |

Advance Viewer configuration to schema 4 and change
`RendererConfig.backgroundcolor` to `Color | None`. `None` is the sole
automatic-viewport marker. A missing schema-4 value defaults to `None`; an
explicit color round-trips as a color. When loading schema 3, every concrete
background is preserved as explicit, including `#D8DDE2`; migration never
guesses that a color was automatic.

Viewer applies content tokens only through presentation arguments omitted at
the existing Viewer add boundary. Explicit and deserialized values remain
authoritative. Precedence is:

| Base color | Specialized channel | Result |
|---|---|---|
| Explicit | Explicit | Preserve the explicit specialized value. |
| Explicit | Omitted | Preserve current Core derivation of the specialized channel from the explicit base. |
| Omitted | Explicit | Preserve the explicit specialized value. |
| Omitted | Omitted | Apply the scheme token for that specialized role. |

Apply this matrix to the existing uniform presentation channels of Geometry,
Mesh, Graph, and VolMesh. Collections and buffer-backed objects preserve their
existing explicit/per-element semantics; they receive a token only where their
existing Viewer add API already exposes an omitted uniform channel. Do not add
unsupported roles, per-element inference, or new public presentation fields.
Core's global defaults and other visualization backends do not change.

An automatic (`None`) viewport follows the effective scheme. An explicit
background never does. Geometry defaults resolve when the Viewer object is
created and remain concrete thereafter. A live scheme switch therefore updates
chrome and the automatic viewport, but does not recolor existing geometry or
dimensions.

Option 2 is the correct basis for full live inversion, but it is a broad Core
API, schema, serialization, and cross-backend change with no present approval.
Reject option 3 because it cannot distinguish an explicit color from the same
materialized default. Option 4 no longer satisfies the requested dark-scheme
behavior.

## Consequences

- New Viewer content has a consistent hierarchy in both schemes.
- Viewer configuration advances from schema 3 to schema 4; schema-3 concrete
  backgrounds migrate as explicit values.
- Explicit and serialized presentation is never overwritten.
- Newly created objects can differ depending on the active scheme, and retain
  those resolved colors after a later switch.
- Core and non-Viewer backends keep their existing defaults.
- ADR 043 gains a narrow Viewer-content exception and ADR 045's fixed viewport
  default is superseded.

## Verification

- Verify every exact token in light and dark schemes.
- Verify schema-4 validation and round-trip for `None` and explicit colors;
  verify missing schema-4 background becomes `None`.
- Verify every schema-3 concrete background, including `#D8DDE2`, migrates as
  explicit and is never guessed to be automatic.
- Verify omitted and explicit base, point/vertex, line/edge, and surface/face
  presentation independently across Geometry, Mesh, Graph, and VolMesh using
  the precedence matrix.
- Verify collections and buffer-backed objects preserve existing explicit and
  per-element behavior and gain no unsupported role.
- Verify explicit and serialized colors survive construction and scheme
  changes unchanged.
- Verify the automatic viewport follows the scheme and an explicit background
  does not.
- Verify existing objects are not recolored on a scheme change.
- Verify Core construction and other backends retain their current defaults.
- Capture native light and dark results and run Viewer/Core tests, Ruff,
  Pyright, strict MkDocs, framework integration, and artifact checks as
  applicable.

## Dependencies

- Narrowly amends ADR 043's chrome-only ownership.
- Supersedes ADR 045's fixed Viewer viewport default if accepted.
- Coordinates with ADR 037's accepted Viewer-created dimension background.

## Decision

Approved on 2026-11-11 with the exact token table, Viewer configuration schema
4, `None` automatic-background marker, lossless schema-3 migration, channel
precedence, and creation-time resolution described above. Implementation and
local verification pass as recorded in the initiative handoff. Native direct
use confirms the scheme-aware viewport, geometry, and new-dimension defaults;
hosted verification remains pending.
