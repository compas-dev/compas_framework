# ADR 008: Serializable Scene Nodes and Runtime Adapters

## Status

Accepted.

## Context

ADR 001 correctly separates durable scene content from Viewer interaction and
renderer state, but it still treats `SceneObject` as both durable node and
context-specific runtime adapter. Current serialization stores an item's GUID
plus `sceneobject.settings`, then calls `Scene.add(..., **settings)` during
load. Factory dispatch chooses a runtime subclass and executes its constructor
before that object is attached to the reconstructed hierarchy.

Two verified regressions expose the consequences:

1. A Viewer Box/ShapeObject with local translation `[2, 0, 0]` reloads with
   `transformation is None` because `ViewerSceneObject.settings` replaces
   rather than extends core settings. In a headless ShapeObject case, `u=7`,
   `v=9`, and a face color reload as the defaults `16`, `16`, and the default
   face color.
2. A `ModelViewer` scene cannot reload. The controller originally creates
   `ModelObject(add_elements=False)` and `ElementObject(add_children=False)`,
   but those construction controls are absent from serialized settings.
   Reload dispatches `ModelObject` with `add_elements=True`; its constructor
   calls `self.add(...)` before attachment and raises `RuntimeError: A detached
   scene object cannot own child objects.` Render caches are transient and
   should not be serialized, but hierarchy reconstruction must not depend on
   them or on constructor side effects.

The shared item store already preserves identity when multiple nodes reference
one item GUID. Scene-object/node GUIDs are not preserved across round trips.
Context also determines which runtime subclass is constructed, even though a
serialized scene should remain loadable without that backend.

## Options

1. Separate a serializable scene-owned node/state value from context-specific
   runtime adapters and reconstruct them in two phases.
2. Keep `SceneObject` as both node and adapter and expand every subclass's
   `settings` property until current tests pass.
3. Serialize complete runtime adapter objects, including their concrete class
   and context.
4. Serialize only items and hierarchy and discard all per-node appearance and
   transformations.

## Recommendation

Choose option 1.

`Scene` owns a serializable node/state record for every hierarchy entry. The
closed base record contains:

- a durable node GUID;
- node kind (`item` or `group`);
- optional item GUID;
- name;
- local transformation;
- visibility, opacity, and base appearance; and
- explicitly declared extension state governed by ADR 009.

Items remain separate and keyed by item GUID, preserving shared item identity.
Accepted ADR 010 requires a serialized scene description to reference those
items without embedding them. Node GUIDs are serialized
and restored so selection references, domain indexes, and external scene
references have durable identity. Runtime adapter instances are not durable
identities.

Deserialize in two phases:

1. validate and create nodes, state, GUIDs, and the complete hierarchy without
   requiring item bindings, context dispatch, or adapter constructors;
2. bind adapters for an explicitly requested or detected runtime context only
   after the scene is structurally complete, either eagerly for drawing or
   lazily on first use.

`SceneObject` becomes the runtime adapter bound to a scene, node, and optional
item. Its constructor must not populate hierarchy or own serialized state.
Application/domain projection creates nodes explicitly through an owning
controller; adapter binding never recreates children. The current draft
`ModelViewer` is evidence of why constructor-driven hierarchy creation fails,
not a controller contract to preserve.

Scene context is runtime binding configuration, not authoritative serialized
content. A scene may record a non-binding context hint for user experience,
but loading must not require that context or silently select a different one.
Drawing without a usable context raises a precise runtime error after the
backend-neutral scene has loaded.

Known extension fields are activated only by a compatible adapter. Unknown
extension namespaces and fields are preserved losslessly as inactive node
state and written back unchanged. Unknown required base schema versions fail
validation; unknown adapter state is not passed blindly to constructors.

## Refinement of ADR 001

This ADR preserves ADR 001's package boundaries but refines these clauses:

- "Core owns scene items, hierarchy, scene-object GUIDs..." becomes: core
  owns durable node/state GUIDs and stable item references; runtime adapter
  identity is not serialized. Accepted ADR 010 defines the non-owning runtime
  binding boundary for items.
- "GUIDs connect durable scene objects to Viewer state" becomes: durable node
  GUIDs connect scene content to Viewer state and domain indexes.
- Core still owns transformations, visibility, durable appearance, and
  serialization, but those values live on node state rather than being
  discovered from a runtime adapter's constructor/settings implementation.

ADR 001's durable identity and serialization boundary is amended by this
Accepted decision and ADR 009. Accepted ADR 010 defines item ownership and
packaging.

## Consequences

- Scenes load without Viewer, model adapters, or another visualization backend.
- Runtime constructors no longer execute hierarchy-building side effects during
  deserialization.
- Switching or omitting runtime contexts does not destroy durable node state.
- Shared item identity and durable node identity have separate, explicit GUIDs.
- Core Scene/SceneObject APIs require a coordinated redesign and compatibility
  review; this is larger than patching two `settings` properties.
- Adapter binding and lifecycle need focused tests, but no universal renderer
  abstraction or event bus is introduced.

## Compatibility

The new node schema replaces the existing serialized scene shape. The initial
implementation does not include a compatibility loader because current files
omit required state and cannot be migrated reliably without guessing. If
concrete legacy files later require recovery, migration tooling needs separate
evidence, scope, and approval.

Existing public code may continue to receive a `SceneObject` adapter from
`Scene.add`, but code that treats adapter identity or constructor side effects
as durable must migrate. Exact compatibility is part of the Phase 1 audit.

## Verification

- Reproduce the Viewer regression as a focused test and retain the draft
  ModelViewer failure as evidence.
- Round-trip local transformations, `u=7`, `v=9`, face color, shared items,
  node GUIDs, groups, and hierarchy without a visualization backend installed.
- Use a minimal test adapter with constructor-side-effect behavior to prove
  hierarchy deserialization never invokes runtime construction; redesign and
  test the actual ModelViewer later.
- Load and re-save unknown extension state without loss or constructor use.
- Verify missing/unknown context permits load but produces a precise binding or
  draw error.
- Verify duplicate item or node GUIDs and unsupported base schema versions fail
  atomically.

## Affected packages

Initial implementation: `compas`, `compas_viewer`, and `compas_framework`.

Later redesign/regression consumer: `compas_model`.

Compatibility review only: `compas_session`, `compas_notebook`, and CAD-host
scene adapters.

## Dependencies

- [ADR 001](001-ownership-boundaries.md), refined by this decision

ADR 009 supplies the serialization field policy required to implement this
decision. ADR 010 separately decides that referenced items remain external to
Scene and defines the boundary for later Session aggregation.

## Decision

Accepted on 2026-11-07. The user additionally required a separate decision
ensuring that independently serializable `Data` objects are not forced to live
inside a scene. Accepted ADR 010 records that packaging refinement without
changing this decision's accepted node/adapter separation.
