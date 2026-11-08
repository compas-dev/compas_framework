# ADR 015: Editable Scene-Object Attribute Declarations

## Status

Accepted, amended on 2026-11-08.

## Context

Viewer's object-settings form currently decides which controls to show through
hardcoded attribute checks on private render helpers. An initial implementation
of this ADR added public `FormField` values and a parallel Viewer-owned field
inventory. That duplicates knowledge already owned by stable `SceneObject`
classes and lets the form description drift from the object API.

Editable attributes are part of the stable scene-object contract. Viewer
exclusively owns form layout, widgets, and post-mutation render and UI refresh.
The design must preserve that boundary without adding UI state to serialized
objects or mixing editable declarations with `SceneStateField` persistence
declarations.

## Options

1. Let stable `SceneObject` classes declare their editable attributes and
   compose those declarations through the class MRO.
2. Maintain public `FormField` objects in a parallel Viewer registry.
3. Infer fields from annotations, constructor parameters, or `hasattr` checks.
4. Store form state or widget metadata on scene-object instances.

## Decision

Choose option 1.

Every stable `SceneObject` class may provide one class-level mapping of editable
attribute names to neutral declaration data. A declaration identifies the
attribute and may contain only neutral metadata/data needed to describe it. It
may also provide one optional synchronous data-side update callback with the
contract:

```text
(owner, value) -> None
```

Without a callback, mutation uses `setattr(owner, attribute, value)`. A
callback exists only for a data-side update that cannot be expressed by direct
assignment. It is not a Viewer, rendering, refresh, context, or asynchronous
hook. The callback must be atomic: if it raises, it leaves the owner unchanged.

Declarations compose from base class to derived class:

- a derived declaration for an existing attribute replaces its data while
  retaining the attribute's existing position;
- a newly declared attribute appends after inherited attributes; and
- a value of `None` removes an inherited attribute.

Viewer introspects the resolved attribute value, editor, writability, default
label, and order. There is no public `FormField` object and no parallel
hardcoded Viewer inventory of built-in editable fields. Viewer owns control
construction and layout, but the stable class remains the source of truth for
which of its attributes are editable.

Editable declarations are runtime class metadata. They are graphics-free,
contain no Qt or OpenGL objects, and are never serialized with a scene object.
They are separate from `SceneStateField`: declaring an attribute editable does
not make it durable, and declaring a state field does not make it editable.

The initial scope contains only attributes owned by stable `SceneObject`
instances. Represented-item parameters remain available through the existing
`ParameterForm`; they are not part of this declaration mechanism.

## Consequences

- Stable scene-object classes own one authoritative editable-attribute
  inventory.
- Viewer no longer infers editing capabilities from renderer aliases or a
  parallel list.
- Neutral class declarations remain usable by more than one UI context without
  putting form or render behavior in core.
- Arbitrary widgets, represented-item parameters, nested paths, asynchronous
  updates, and refresh callbacks are outside this contract.

## Compatibility

The current public `FormField` implementation and hardcoded Viewer field
inventory must be replaced. This is an approved correction before that API is
treated as stable. Existing represented-item `ParameterForm` behavior remains
separate and unchanged.

## Verification

- Compose declarations base-to-derived with position-preserving overrides,
  appended new attributes, and `None` removal.
- Verify Viewer derives the value, editor, writability, default label, and
  order without a built-in field inventory.
- Verify a default declaration uses `setattr` and a declared callback receives
  exactly `(owner, value)` synchronously and leaves the owner unchanged when it
  raises.
- Prove declaration resolution imports no graphics or UI modules.
- Prove declarations and resolved editor state are absent from scene-object
  serialization.
- Verify `SceneStateField` and editable declarations remain independent.
- Verify represented-item parameters continue through `ParameterForm` rather
  than this mechanism.

## Dependencies

- Depends on Accepted ADR 013 for stable scene-object types.
- Respects ADR 014's restricted `draw`/`clear` operation surface.
- Context-specific declaration changes are governed by Accepted ADR 016.

## Amendment

Approved on 2026-11-08. This amendment supersedes the earlier accepted design
in which Viewer providers returned public `FormField` values for scene-object
and represented-item targets with explicit field refresh modes. The current
implementation of that design must be replaced by the class-owned declaration
model above.
