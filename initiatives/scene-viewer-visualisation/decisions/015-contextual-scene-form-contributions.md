# ADR 015: Editable Scene-Object Attributes

## Status

Accepted, amended on 2026-11-08.

## Context

Viewer's object-settings form currently infers editable controls from private
render-helper attributes. The first accepted correction introduced a separate
class-level editable-attribute declaration for every editable property. That
would duplicate durable semantic attribute names already declared by
`SceneStateField`, allowing persistence and editability declarations to drift.

Core needs one normalized answer to “which stable scene-object attributes are
editable?” without acquiring labels, editor choices, form layout, rendering
refresh policy, or other Viewer concerns.

## Options

1. Mark durable semantic fields editable on their existing `SceneStateField`
   and reserve a separate name-only declaration for editable attributes that
   are not scene state fields.
2. Duplicate every editable attribute in a separate class-level declaration.
3. Infer editable fields from annotations, constructors, or `hasattr` checks.
4. Put form descriptors or widget metadata on scene-object classes.

## Decision

Choose option 1.

`SceneStateField` gains only:

- `editable: bool = False`; and
- an optional synchronous atomic data-only `update(owner, value) -> None`
  callback.

A state field with `update` and `editable=False` is invalid. Without `update`,
an editable field uses `setattr(owner, name, value)`. The callback exists only
for a data-side update that cannot be expressed by direct assignment. It must
leave the owner unchanged if it raises. It is not a Viewer, form, rendering,
refresh, context, or asynchronous hook.

Durable semantic editable state uses its existing `SceneStateField` as the
single source of both persistence and editability. Subclasses do not repeat
those attribute names in a separate editable declaration.

`SceneObject.__editable_attributes__` remains a class-level mapping only for
genuinely editable attributes that are not `SceneStateField` entries. Its
initial core entries are `name` and `opacity`, matching the existing inspector.
Each mapping value is only an optional synchronous atomic data-only update
callback; `None` means ordinary `setattr`.

`SceneObject.editable_attributes()` composes both sources across the class MRO
and returns one normalized ordered mapping:

```text
attribute name -> optional update callback
```

MRO composition must not duplicate subclass names. A name resolves once in the
normalized result, with the most specific applicable definition governing its
callback while retaining deterministic order.

Core contains no label, editor, arbitrary metadata/data, form identifier,
refresh category, or context metadata. Viewer infers presentation from the
resolved object and owns every form and post-mutation refresh decision.

The initial scope contains only attributes owned by stable `SceneObject`
instances. Represented-item parameters remain on the existing `ParameterForm`
path.

## Consequences

- Durable semantic fields have one declaration rather than parallel state and
  editable inventories.
- Non-state editable attributes remain explicit and narrowly scoped.
- All consumers receive the same normalized name-to-callback mapping.
- Core remains free of form presentation and rendering refresh policy.
- Arbitrary widgets, item parameters, dotted paths, asynchronous callbacks,
  and refresh callbacks remain outside this contract.

## Compatibility

The uncommitted separate `EditableAttribute`/declaration design is superseded
before it becomes public. The current public `FormField` implementation and
parallel hardcoded Viewer field inventory must also be replaced. Existing
represented-item `ParameterForm` behavior remains separate and unchanged.

## Verification

- Compose editable `SceneStateField` entries and non-state
  `__editable_attributes__` entries across the MRO into one ordered mapping.
- Verify durable subclass fields are not duplicated in
  `__editable_attributes__` or the normalized result.
- Reject a `SceneStateField` with `update` and `editable=False`.
- Verify default mutation uses `setattr` and callbacks receive exactly
  `(owner, value)` synchronously and atomically.
- Verify the initial non-state entries are `name` and `opacity`.
- Prove core declarations and resolution contain no UI, form, context, or
  refresh metadata and import no graphics modules.
- Prove editability declarations and resolved mappings are absent from scene
  serialization.
- Verify represented-item parameters continue through `ParameterForm`.

## Dependencies

- Depends on Accepted ADR 013 for stable scene-object types and durable scene
  state.
- Respects ADR 014's restricted `draw`/`clear` operation surface.
- Context-specific normalized mapping changes are governed by Accepted ADR
  016.

## Amendment

Approved on 2026-11-08. This amendment supersedes both the earlier accepted
public `FormField`/item-target/refresh design and the first uncommitted
class-level design that separately redeclared durable editable attributes.
`SceneStateField` is now the single source for durable semantic editable state.
