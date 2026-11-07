# ADR 001: Ownership and State Boundaries

## Status

Accepted.

## Context

Core scene objects currently combine durable content with context-adapter
state, while Viewer selection, GPU identity, configuration, tool state, and UI
refresh paths are distributed across objects, renderer, commands, and widgets.
Moving everything into core would make Qt/rendering concerns framework
dependencies; leaving ownership implicit perpetuates coupling.

## Options

1. Keep core responsible for durable scene content and place renderer and
   interaction state in Viewer.
2. Add rendering, selection, and reactive application state to core Scene.
3. Keep all current ownership and coordinate behavior through conventions.
4. Move durable scene content into Viewer and reduce core Scene to adapters.

## Recommendation

Choose option 1.

- Core owns scene items, hierarchy, scene-object GUIDs, local transformations,
  visibility, durable appearance, and serialization.
- Viewer configuration owns persistent application preferences.
- Viewer session state owns selection, hover, tools, gestures, and transient
  results.
- Viewer rendering owns indexed buffers, pick IDs, GPU resources, and refresh.
- Domain packages own authoritative domain hierarchies and caches and project
  them into core scenes through public Viewer operations.

GUIDs connect durable scene objects to Viewer state. Pick IDs and transient
state are never serialized. Do not add Qt signals or GPU contracts to core.

## Consequences

- Core remains usable by notebook and host adapters without Viewer.
- Selection and tools stop leaking into serialized scene-object settings.
- Viewer must provide explicit public state and synchronization operations.
- Domain packages retain their own data authority rather than duplicating it
  in a generic application store.
- Existing Viewer code that reaches its singleton, renderer, or widgets must
  migrate gradually after the public boundary exists.

## Compatibility

Core serialized scene contracts remain authoritative. Removing transient
Viewer fields from scene-object settings may change Viewer-specific serialized
data and requires fixture inspection and migration documentation.

## Verification

- Round-trip core scenes without Viewer installed.
- Prove Viewer selection, hover, tools, and pick IDs are absent from scene
  serialization.
- Verify domain objects resolve through stable scene-object GUIDs after UI
  rebuilds.

## Affected packages

`compas`, `compas_viewer`, `compas_model`, and `compas_framework`.

## Dependencies

- Geometry-tessellation ADRs 022 and 024
- Plugin-implementations ADR 002
