# Scene, Viewer, and Visualisation Implementation Plan

## Status

Architecture amendment required. ADRs 001–007 are Accepted, but verified
round-trip regressions block implementation. Proposed ADRs 008–009 must be
approved before Phase 1 or package source work begins.

## Dependency graph

```text
ADR 001 --> ADR 008 --> ADR 009
    |
    +--------> ADR 002
    +--------> ADR 003 --> ADR 004

ADRs 001–003 ----------> ADR 005
ADRs 001, 003–005 -----> ADR 006
ADRs 001–009 ----------> ADR 007 rollout gate
```

## Phase 0 — Scene ownership and serialization amendment

Governing ADRs: 001, 008, and 009.

Status: blocked on approval of ADRs 008–009.

1. Add the two verified round-trip regressions as failing tests without
   changing package behavior.
2. Audit Scene, SceneObject, Group, Viewer adapters, model adapters, and
   compatibility-only consumers against the proposed node/adapter split.
3. Implement the closed scene node/state schema, durable node GUIDs, separate
   item store, and two-phase deserialize/bind lifecycle.
4. Implement explicit MRO-composed extension field declarations and the legacy
   settings loader; preserve unknown namespaced extension state.
5. Migrate core, Viewer, and model adapters without serializing caches,
   selection, construction commands, or runtime handles.

Exit gate: both regressions pass; shared item identity and durable node identity
round-trip separately; scenes load without a visualization backend; model
adapters bind only after the complete hierarchy exists; local/package quality,
typing, docs, and artifact checks pass.

## Phase 1 — Boundaries and indexed geometry

Governing ADRs: 001, 002, 007, 008, and 009.

Status: paused until Phase 0 and its approval gate are complete.

1. Audit compatibility-only consumers for affected core scene contracts and
   stop for approval if a required core change would break them.
2. Implement indexed `BufferGeometry` and convenience constructors in Viewer.
3. Migrate Viewer adapters and buffer assembly without expanding indexed data.
4. Pass model render arrays to Viewer without intermediate Python-list
   expansion while retaining model-owned quality and cache policy.
5. Add performance-regression assertions based on buffer/object counts rather
   than unstable wall-clock thresholds.

Exit gate: package-local source, typing, artifact, rendering-semantic, and
large-indexed-input evidence passes at exact candidate heads.

## Phase 2 — State, selection, and transforms

Governing ADRs: 001, 003, 004, 007, 008, and 009.

1. Separate persistent Viewer configuration from transient Viewer state.
2. Implement the object-selection model and migrate viewport, rectangle, tree,
   commands, renderer settings, and model integration.
3. Remove `is_selected` as a second authority and update serialization/tests.
4. Add atomic multi-object transform transactions, categorized refresh, and
   the reversible transaction stack.
5. Add a minimal transform interaction only after command/programmatic
   semantics pass; visual gizmo design may be a follow-up if it requires new
   choices.

Exit gate: all selection paths share one model; transform/undo tests cover
parents, batches, failures, and buffer-update scope.

## Phase 3 — Annotations and overlays

Governing ADRs: 001–005 and 007.

1. Inspect current Tag/Arrow serialized behavior and document the exact
   migration.
2. Implement world text annotation and distance dimension scene items/adapters.
3. Implement measurement tool preview, cancel, and completion.
4. Implement scale and legend screen overlays through one Viewer overlay layer.
5. Remove concrete approved-type checks from the main render loop.

Exit gate: durable annotation round trips, transient overlays do not serialize,
and visual behavior passes offscreen and package artifact tests.

## Phase 4 — Public integration facade and model alignment

Governing ADRs: 001, 003–007.

1. Add public refresh, history, command/menu, dock, annotation, and overlay
   operations required by the approved features and model integration.
2. Migrate `ModelViewer` from direct renderer/sidebar access while preserving
   its hierarchy, projections, selection results, contacts, inspectors, units,
   quality, and cache behavior.
3. Add direct script examples for indexed buffers, selection, transforms,
   measurements, overlays, and one custom dock.
4. Update core, Viewer, and model documentation using repository skills and
   current MkDocs-compatible NumPy style.

Exit gate: model integration uses only public Viewer APIs and package-local
tests/docs/artifacts pass.

## Phase 5 — Framework integration and review

Governing ADR: 007.

1. Extend the existing coordinated model/viewer plugin lifecycle gate rather
   than duplicating it.
2. Install exact candidate revisions and exercise the approved cross-package
   runtime and typing contracts.
3. Run package and framework CI, candidate-artifact verification where
   applicable, and independent code/documentation review.
4. Resolve findings, update the handoff with evidence by layer, and request
   explicit merge approval.

Exit gate: all applicable verification layers pass at recorded exact heads;
required unavailable evidence remains an explicit blocker.

## Deferred work requiring new approval

- sub-object or domain-component selection;
- ancestor/descendant group-transform semantics and advanced gizmos;
- angular, radial, area, or snapping measurement systems;
- a general overlay/plugin registry;
- console, terminal, Python/shell execution, assistant services, credentials,
  or remote transports;
- `compas_session` reactive-state integration; and
- notebook, Rhino, Grasshopper, Blender, or other backend migrations.
