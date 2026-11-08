# ADR 016: Contextual Editable-Attribute Overrides and Mutation

## Status

Accepted, amended on 2026-11-08.

## Context

ADR 015 makes `SceneStateField` and narrowly scoped
`__editable_attributes__` declarations the sources of one normalized editable
attribute mapping. A visualization context may still need to expose an
additional scene-object attribute, replace its data-side update callback, or
hide an otherwise editable attribute. This must operate on that normalized
mapping without reintroducing a second public field type or putting
presentation and rendering refresh instructions in core.

## Options

1. Let context plugins extend, replace, or remove entries in the resolved
   class declaration mapping.
2. Let context plugins return public form-field or widget objects.
3. Add refresh callbacks or context protocols to core declarations.
4. Keep context-specific hardcoded field inventories in Viewer components.

## Decision

Choose option 1.

Context plugins register graphics-free contributions under the exact key
`(context, stable SceneObject type, contribution ID)`. A contribution modifies
the normalized `attribute name -> optional update callback` mapping:

- a new attribute with an optional callback appends;
- an existing attribute's callback is replaced while retaining its position;
  and
- an explicit removal marker removes the attribute.

The removal marker is distinct from `None`, because `None` means the attribute
uses ordinary `setattr`.

Resolution starts with the base-to-derived class declarations from ADR 015 and
then applies applicable context contributions by stable scene-object MRO from
general to specific. At each MRO specificity, contributions are applied in
lexical contribution-ID order while preserving each contribution mapping's
insertion order. This makes the append order deterministic. Duplicate exact
registration keys are errors. Two contributions at the same specificity that
both edit or remove the same attribute are also errors; registration order
never silently resolves a conflict.

Class declarations and plugin discovery remain graphics-free. Contributions
and their resolved mappings are runtime-only and are never serialized.

Viewer introspects the final mapping and owns form construction. It determines
presentation from the current value, checks writability, and applies the
default assignment or synchronous data-side callback defined by ADR 015.
There is no public `FormField` object and the mapping contains no labels,
editors, arbitrary data, form metadata, or refresh instructions.

Mutation is atomic from the form's perspective. If assignment or the callback
raises, the owner remains unchanged under ADR 015's callback contract, the
control is restored to the previous value, the original failure is reported,
and no view refresh occurs. After a successful mutation, Viewer exclusively
decides which render-data rebuild, redraw, and UI refresh operations are
required. Context plugins only filter, extend, or replace normalized attribute
names and callbacks. Core declarations contain no refresh callback, refresh
category, or context protocol.

The initial scope is only stable `SceneObject` attributes in object settings.
Represented-item parameters continue to use the existing `ParameterForm` and
are not extended or overridden through this registry.

## Consequences

- Contexts customize the same authoritative attribute mapping instead of
  maintaining parallel form schemas.
- Conflict handling is deterministic and independent of plugin load order.
- Core remains unaware of rendering and UI refresh policy.
- Viewer may refresh conservatively first and optimize only with measured
  evidence.
- Arbitrary widgets, item parameters, dotted paths, asynchronous callbacks,
  and plugin-provided refresh hooks remain outside the mechanism.

## Compatibility

The current `FormField`-based context registry, represented-item targets, and
field-level `draw`/`geometry` refresh modes must be removed. Built-in object
settings migrate to class declarations; only genuinely contextual differences
remain plugin contributions. Existing `ParameterForm` behavior is preserved.

## Verification

- Compose class declarations and general-to-specific context contributions in
  lexical contribution-ID and mapping-insertion order, preserving positions
  for replacements and deterministically appending new attributes.
- Verify the explicit removal marker removes class-owned or inherited context
  attributes while `None` selects ordinary `setattr`.
- Reject duplicate exact registrations and same-specificity attribute
  conflicts with diagnostics naming context, scene-object type, and attribute.
- Verify two contexts may resolve different mappings for the same stable
  scene-object type.
- Verify failed assignment/callback leaves the owner unchanged, restores the
  control, and performs no render, redraw, or UI refresh.
- Verify successful mutation causes Viewer—not core metadata or context
  plugins—to select conservative render rebuild, redraw, and UI refresh.
- Prove plugin discovery imports no graphics or UI modules.
- Prove contributions and resolved mappings are absent from serialization.
- Verify represented-item parameters remain on the existing `ParameterForm`
  path.

## Dependencies

- Depends on Accepted ADR 015 for class-owned declarations and mutation.
- Reuses ADR 014's context/type registration principles without extending its
  public `draw`/`clear` operation surface.

## Amendment

Approved on 2026-11-08. This amendment supersedes the earlier accepted flat
`FormField` binding contract, including item targets and field-level refresh
semantics. The current implementation of that earlier design must be replaced.
