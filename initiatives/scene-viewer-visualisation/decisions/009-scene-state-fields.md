# ADR 009: Explicit Scene-State Serialization Fields

## Status

Proposed.

## Context

Current scene serialization depends on each runtime adapter's `settings`
property and reconstructs state by replaying that mapping as constructor
arguments. Subclasses can accidentally replace base settings, as demonstrated
by the lost transformation regression. Required subclass state can be omitted,
as demonstrated by lost ShapeObject resolution and face color. Conversely,
serializing `__dict__`, every property, annotations, or constructor parameters
would capture caches, renderer handles, item/scene backreferences, derived
values, and construction commands such as `add_elements`.

The durable node proposed by ADR 008 needs an explicit field policy that
supports inheritance without treating Python introspection as persistence.

## Options

1. Use a closed base node-state schema plus explicit MRO-composed extension
   field declarations.
2. Serialize every entry in `__dict__` except a growing denylist.
3. Serialize every public property, type annotation, or constructor parameter
   discovered through introspection.
4. Require every subclass to replace and manually merge a free-form
   `settings` dictionary.
5. Allow only the closed base schema and prohibit all adapter/domain extension
   state.

## Recommendation

Choose option 1.

Base node state is a closed value-object schema owned by core. A class that
owns additional durable scene state declares only its local fields through an
explicit class-level declaration. The serializer composes declarations across
the MRO from base to subclass, rejects duplicate or incompatible declarations,
and stores extension values under a stable owning namespace.

Declarations specify the serialized name, expected value contract, default or
required status, and whether omission is allowed. They do not execute arbitrary
getters during schema discovery. The implementation may use annotations,
constructor signatures, descriptors, and properties only to validate a
declaration or generate editor/documentation metadata; introspection never
decides that a field is persistent.

Unrestricted `__dict__`, public-property, constructor-parameter, or annotation
serialization is forbidden. Derived values, scene/item backreferences,
renderer/GPU handles, pick IDs, caches, selection, hover, tools, and command
history are not durable fields. `ModelObject.add_elements` and
`ElementObject.add_children` are construction commands, not state. Model render
caches are transient. Shape resolution and durable colors are serialized only
through explicit declarations.

Deserialization validates the closed base state and known declarations without
passing a free-form mapping to adapter constructors. Unknown namespaced
extension values remain inactive and round-trip unchanged under ADR 008.

## Consequences

- Base transformations and subclass fields cannot disappear because a
  subclass forgot `super().settings`.
- Persistence changes are visible in code review and independently testable.
- Runtime caches and constructor side effects are excluded by default.
- Subclasses must deliberately declare every durable field and migration.
- Editor tooling can reuse schema metadata without becoming the source of
  truth for persistence.
- A small schema/version and migration mechanism is required for renamed or
  removed fields; it remains data-focused rather than adapter-constructor
  compatibility code.

## Compatibility

Legacy `settings` mappings are accepted only by the legacy scene loader and
mapped into declared base/extension fields. Unknown unnamespaced legacy keys
cannot be assigned safely and must be reported; they are not passed to
constructors. Once migrated, only the explicit schema is written.

## Verification

- Assert MRO composition preserves base transformation plus declared subclass
  `u`, `v`, and face color.
- Assert duplicate field declarations, invalid values, missing required fields,
  and unknown base fields fail with precise paths.
- Prove caches, Viewer handles, pick IDs, selection, and construction commands
  are absent from serialized state.
- Prove unknown namespaced extension state round-trips byte-for-value without
  importing or constructing its adapter.
- Use introspection-based validation tests to detect a declaration that names a
  missing/incompatible attribute, without auto-serializing undeclared members.

## Affected packages

`compas`, `compas_viewer`, `compas_model`, and `compas_framework`.

## Dependencies

- [ADR 008](008-scene-nodes-and-runtime-adapters.md)
