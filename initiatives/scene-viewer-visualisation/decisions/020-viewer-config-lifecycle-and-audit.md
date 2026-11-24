# ADR 020: Viewer Configuration Lifecycle and Field Audit

## Status

Accepted.

## Context

Viewer uses nested dataclasses for configuration, but deserialization currently
performs limited structural migration rather than explicit validation. Several
fields are inert, duplicate transient runtime state, or retain residues of
earlier sidebar and display designs. The cleanup needs a complete disposition
without replacing the simple dataclass model with another framework.

## Options

1. Retain typed dataclasses, add explicit path-aware validation, and remove or
   connect fields according to demonstrated ownership.
2. Replace configuration with Pydantic models.
3. Store arbitrary plugin dictionaries and validate them inside consumers.
4. Turn all configuration into a live reactive state store.

## Recommendation

Choose option 1.

Retain the nested configuration dataclasses and add explicit `validate()`
behavior that reports the complete field path for every invalid value. Validate
after construction/deserialization and before Viewer creates `QApplication`.

Separate startup configuration from transient state:

- startup configuration includes window identity and geometry, appearance,
  UI component visibility, renderer/camera defaults, and `vectorsize`;
- transient selection, hover, active tools, live view interaction, and other
  session values remain outside serialized configuration.

Apply this field audit for schema version 2:

- connect `window.fullscreen` to startup behavior;
- connect `ui.statusbar.show` to status-bar visibility;
- remove `window.about`;
- remove obsolete sidebar residues `show_widgets` and `sceneform`;
- remove `renderer.opacity` because effective renderer opacity is derived from
  render mode;
- remove the root `display` group and its duplicated scene-object defaults;
- remove root `unit` until a unit-aware workflow has an approved owner and
  lifecycle;
- add `ortho` to the accepted renderer view values; and
- keep root `vectorsize` as an active render default.

Unknown or invalid schema fields fail with their full path; migration must not
silently preserve removed fields as runtime attributes. Schema version 2 also
implements ADR 019's identity and icon contract.

Typed Viewer subclasses may extend configuration with typed dataclass fields
and validation. Do not add untyped plugin dictionaries, automatic plugin
configuration merging, Pydantic, or a promise that configuration is reactive.

Direct dataclass mutation is supported only while assembling configuration
before Viewer construction. Post-construction mutation has no reactive
guarantee, and replacing `viewer.config` is unsupported. Existing dotted-path
`ViewerState` access is transitional internal wiring, not a configuration or
extension target.

## Consequences

- Configuration remains simple Python data with explicit validation.
- Removed fields stop suggesting unsupported behavior.
- Startup and transient ownership become testable.
- Typed subclass extensions remain possible without a generic plugin schema.
- Schema version 2 is an intentional compatibility boundary.

## Compatibility

Serialized schema version 2 removes `about`, sidebar residues, renderer
`opacity`, the `display` group, and root `unit`. Loading schema 1 drops known
retired fields and preserves every retained value. Unknown schema-1 fields are
rejected. Schema 2 rejects retired fields when they are supplied explicitly,
rather than silently accepting or storing them.

## Verification

- Validate nested types, literals, ranges, icon paths, and unknown fields with
  complete configuration paths.
- Apply configuration before `QApplication` and window construction.
- Verify fullscreen and status-bar fields affect startup UI.
- Verify every removed field is absent from schema-2 serialization and rejected
  when explicitly supplied in schema 2.
- Verify schema-1 migration drops known retired fields, preserves retained
  values, and rejects unknown fields.
- Verify renderer view accepts `ortho` and rejects other unknown modes.
- Verify `vectorsize` remains active.
- Verify transient state changes do not mutate serialized startup
  configuration.
- Verify setup-time direct mutation is honored, post-construction mutation has
  no reactive contract, replacing `viewer.config` is unsupported, and
  dotted-path `ViewerState` access is not presented as an extension API.
- Verify a typed subclass can add and validate typed dataclass fields without
  untyped plugin dictionaries.

## Dependencies

- Depends on Accepted ADR 019 for the identity fields that schema 2 validates
  and applies at startup.
- Independent of ADRs 015–018, but sidebar implementation must coordinate file
  ownership with ADRs 017–018.

## Decision

Approved on 2026-11-08. Viewer retains typed nested dataclasses, adds explicit
path-aware validation, separates startup configuration from transient state,
and applies the complete schema-version-2 field audit and migration contract.
The rationale is to keep configuration simple and truthful without Pydantic,
untyped plugin dictionaries, reactive-state promises, or silent preservation
of removed and unknown fields.
