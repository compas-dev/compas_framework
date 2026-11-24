# ADR 012: Explicit Node-Backed Adapter State

## Status

Superseded by ADR 013 before acceptance.

## Context

ADR 009 correctly requires a closed base schema and explicit namespaced
extension declarations. Its implementation, however, uses
`SceneObject.__getattribute__` and `__setattr__` to scan declarations and
redirect attributes dynamically. Other durable fields use individual
node-or-local properties, and color uses a special descriptor. The result is
three different state-routing mechanisms whose behavior changes when an
adapter binds to a node.

The declarations should define persistence and validation, not invisibly
change normal Python attribute access.

## Options

1. Keep declarations as schema metadata and implement ordinary explicit
   node-backed adapter properties.
2. Replace interception with a general descriptor or state-proxy framework.
3. Store durable adapter state in a third state object.
4. Keep the current interception and add documentation.

## Recommendation

Choose option 1.

Keep `SceneStateField`-style declarations only for stable names, namespaces,
types, defaults, required fields, validation, and preservation of unknown
extension state. `Scene.add` validates declared keyword arguments and writes
them directly to `SceneNode.extensions`. Deserialization validates known state
without constructing adapters.

Adapters expose ordinary properties whose implementation visibly reads and
writes the node. A small typed `SceneNode.extension(namespace, field)` and
`set_extension(...)` helper may remove repetitive mapping access. Do not add a
general descriptor, proxy, reflection layer, or global attribute interception.
Property setters perform required invalidation explicitly.

Remove extension capture/apply operations, declaration-driven
`__getattribute__`/`__setattr__`, detached attribute validation, and all local
durable fallbacks. Base properties such as name, transformation, color,
opacity, and visibility are likewise direct node-backed properties on an
always-bound adapter.

## Consequences

- Durable state has one storage location and one visible access path.
- Persistence remains explicit and reviewable.
- Adapter classes contain some repetitive properties, which is preferable to
  hidden control flow.
- Unknown namespaced state remains serializable without importing its adapter.
- Constructor signatures no longer double as persistence or editor schemas.

## Verification

- Prove each declared property reads and writes its node extension.
- Prove setters trigger their documented cache invalidation.
- Reject unknown, missing, duplicate, and invalid declared fields precisely.
- Preserve unknown namespaces without adapter imports.
- Prove caches, selection, context handles, and construction commands are not
  durable.
- Assert no runtime adapter class uses persistence interception or capture.

## Dependencies

- Supersedes the runtime interception and capture mechanism introduced under
  Accepted [ADR 009](009-scene-state-fields.md), while retaining its closed
  schema and explicit declarations.
- Depends on Proposed [ADR 011](011-node-first-scene-adapters.md).
- Preserves Accepted [ADR 010](010-scene-description-and-item-bundling.md).

## Decision

Not accepted. Superseded on 2026-11-07 by Accepted ADR 013.
