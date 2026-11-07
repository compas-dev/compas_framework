# ADR 010: Scene Description, Item Bindings, and Aggregation Boundary

## Status

Proposed.

## Context

ADRs 008–009 separate durable scene node state from runtime adapters and define
its serialization fields. They do not yet decide whether referenced domain
items must be embedded in a serialized scene.

A geometry or other `Data` object may need to be serialized independently for
later algorithmic processing while also being referenced by one or more scene
nodes. It must not be forced to live inside the scene or require extraction
from a scene file before ordinary data processing. Conversely, users sometimes
need an aggregate containing data, one or more scenes, settings, and history.

The current item table preserves shared identity inside one scene file, but
conflates a scene description, runtime bindings, and packaging.

## Options

1. Keep Scene reference-only and treat a redesigned Session as the likely
   optional aggregate under a separate decision and scope.
2. Always embed every referenced item in the scene serialization.
3. Add a dedicated `SceneBundle` containing one scene plus its items.
4. Introduce a general asset catalog with URIs, search paths, network loading,
   and resolver plugins.

## Recommendation

Choose option 1.

Define one Scene role, its runtime bindings, and one later aggregation boundary:

- `Scene` is the durable, backend-neutral visual description from ADRs 008–009.
  Its serialized node hierarchy contains stable item GUID references only.
  At runtime it may hold a nonserialized binding table from those GUIDs to
  already loaded `Data` objects. A binding is a reference, not ownership; the
  same object remains independently usable and serializable.
- A redesigned `compas_session.Session` is the likely optional aggregate for
  independently serialized data, one or more scene descriptions, settings,
  history, and their shared identity. Its exact schema, ownership, and loading
  behavior require a separate dependent decision and explicit scope approval.
  Do not add Session implementation to the current wave.

The intended runtime operations are conceptually:

```python
scene = Scene.from_json(...)
scene.bind(item)
scene.bind_many(items)
```

Exact method naming may follow established core conventions during
implementation. Scene serialization remains reference-only; it is not
controlled by an `include_items` boolean.

Loading a Scene succeeds when item references are unresolved. Hierarchy,
node state, and reference inspection remain available. Binding an item uses
its existing GUID. Binding the same instance again is idempotent; binding a
different object with the same GUID is rejected. All nodes referencing one
GUID resolve to the same bound object instance.

Drawing, adapter binding, or another operation that requires an
unresolved item raises a precise error containing the node GUID and item GUID.
The caller may bind the item later and retry. Serialization and inspection of
the reference-bearing description do not require bindings.

Do not add URIs, filesystem lookup, network loading, an asset registry, or a
resolver plugin. Callers load `Data` objects through existing serialization and
bind them explicitly. A concrete external-resource requirement would need a
separate decision.

## Refinement of ADR 008

ADR 008's separate item store is refined into a runtime binding table. Core
owns the Scene description and stable references, but it does not claim
exclusive ownership of bound `Data` objects. Aggregation belongs outside Scene;
a future Session design may package objects without making that aggregate their
only valid serialization path.

## Consequences

- Domain data remains independently serializable and directly available for
  algorithms.
- Scenes can be stored, compared, or transmitted without
  duplicating large items.
- A future self-contained aggregate can support multiple scenes, settings, and
  history without introducing a redundant one-scene bundle type now.
- Shared identity is deterministic within a runtime Scene and must remain so
  in any future approved Session aggregate.
- Unresolved references become a normal, inspectable state with precise
  failure at item-dependent operations.
- Cross-file discovery remains the caller's responsibility; no speculative
  asset system is introduced.

## Compatibility

The new Scene format is reference-only. Existing `Data` serialization remains
unchanged. A future Session aggregate and any legacy recovery tooling remain
outside Scene runtime serialization and require separate approval.

## Verification

- Serialize and load one `Data` object independently, bind it to a separately
  loaded Scene, and run an algorithm on the original/bound object
  without extraction or copying.
- Round-trip a reference-only Scene while items remain unresolved.
- Bind later and prove every node sharing one item GUID resolves to the same
  object instance.
- Reject a different object with a duplicate GUID atomically.
- Raise precise node/item errors for draw and adapter operations that
  require unresolved items.
- Prove description serialization needs no bound items and no URI/network
  resolver is invoked.
- In a separate future Session decision, verify data and multiple scenes share
  identity without requiring extraction from Scene.

## Affected packages

Initial implementation: `compas` and `compas_framework`.

Consumer: `compas_viewer`.

Separate later design/scope: `compas_session`, followed by `compas_model`,
notebook, and CAD-host integrations as applicable.

## Dependencies

- [ADR 008](008-scene-nodes-and-runtime-adapters.md)
- [ADR 009](009-scene-state-fields.md)
