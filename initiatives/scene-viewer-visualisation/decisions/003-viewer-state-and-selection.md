# ADR 003: Viewer State and Object Selection

## Status

Accepted.

## Context

Selection currently lives in mutable `ViewerSceneObject.is_selected` flags.
Viewport commands, tree widgets, shaders, and programmatic consumers mutate or
poll those flags and then trigger imperative refreshes. `ViewerState` observes
persistent configuration but not selection or tool state.

## Options

1. Add one Viewer-owned observable object-selection model and separate
   persistent configuration from transient state.
2. Keep scene-object flags and add selection-change signals around them.
3. Put selection into core Scene and serialize it.
4. Adopt a generic third-party reactive state store for all Viewer data.

## Recommendation

Choose option 1.

`Viewer.state.selection` stores ordered scene-object GUIDs and provides
replace, add, remove, toggle, clear, membership, and ordered-resolution
operations. It emits one batched change notification per operation. Viewport,
rectangle selection, scene tree, commands, shaders, and programmatic consumers use
this model exclusively.

Keep `Viewer.config` for persistent preferences. Keep hover, active tool,
gesture, and temporary tool values in small explicit Viewer state fields. Use a
Qt-neutral Python model with a Qt bridge. Remove `is_selected` rather than
retaining a second writable authority.

Initial selection is scene-object-level only. Do not invent a generic vertex,
edge, face, or domain-component token until an approved editing workflow
requires it.

## Consequences

- Tree, viewport, code, and renderer observe one mutation
  path.
- Selection no longer participates in scene serialization.
- Batch changes avoid repeated renderer/UI updates.
- Existing selection APIs and tests require a coordinated breaking migration.
- Sub-object selection remains explicitly unsupported in the initial wave.

## Compatibility

Remove Viewer `is_selected` constructor/settings behavior. Later integrations
may consume the selection model but do not define its contract.

## Verification

- Exercise replace/add/remove/toggle/clear from viewport, rectangle, tree, and
  programmatic paths.
- Assert one notification and one render/UI synchronization per batch.
- Verify stable ordering, removed-object cleanup, and serialization exclusion.

## Affected packages

`compas_viewer` and `compas_framework`. `compas_model` is a later redesign
consumer.

## Dependencies

- [ADR 001](001-ownership-boundaries.md)

## Refinement after acceptance

The current `compas_model.ModelViewer` is a draft and does not promise a
model-order selection contract that this ADR must preserve. The accepted
decision remains one Viewer-owned selection model; model-specific preservation
language has been removed by explicit user correction.
