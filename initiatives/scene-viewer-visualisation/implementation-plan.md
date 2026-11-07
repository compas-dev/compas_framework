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

1. Add the verified Viewer round-trip regression and a minimal core adapter
   test covering the constructor-before-attachment failure. Keep the actual
   draft ModelViewer failure as evidence for its later redesign.
2. Audit Scene, SceneObject, Group, Viewer adapters, the draft model adapters,
   and compatibility-only consumers against the proposed node/adapter split.
3. Implement the closed scene node/state schema, durable node GUIDs, separate
   item store, and two-phase deserialize/bind lifecycle.
4. Implement explicit MRO-composed extension field declarations; preserve
   unknown namespaced extension state within the new schema.
5. Migrate core and Viewer adapters without serializing caches, selection,
   construction commands, or runtime handles. Use the draft ModelViewer failure
   as external regression evidence, not as behavior to preserve.

Exit gate: the Viewer and minimal-adapter regressions pass; shared item
identity and durable node identity round-trip separately; scenes load without
a visualization backend; runtime adapters bind only after the complete
hierarchy exists; local/package quality, typing, docs, and artifact checks
pass.

## Phase 1 — Boundaries and indexed geometry

Governing ADRs: 001, 002, 007, 008, and 009.

Status: paused until Phase 0 and its approval gate are complete.

1. Audit compatibility-only consumers for affected core scene contracts and
   stop for approval if a required core change would break them.
2. Implement indexed `BufferGeometry` and convenience constructors in Viewer.
3. Migrate Viewer adapters and buffer assembly without expanding indexed data.
4. Add performance-regression assertions based on buffer/object counts rather
   than unstable wall-clock thresholds.

Exit gate: package-local source, typing, artifact, rendering-semantic, and
large-indexed-input evidence passes at exact candidate heads.

## Phase 2 — State, selection, and transforms

Governing ADRs: 001, 003, 004, 007, 008, and 009.

1. Separate persistent Viewer configuration from transient Viewer state.
2. Implement the object-selection model and migrate viewport, rectangle, tree,
   commands, renderer settings, and programmatic Viewer APIs.
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

## Phase 4 — Public Viewer operations

Governing ADRs: 001, 003–007.

1. Add public refresh, history, command/menu, dock, annotation, and overlay
   operations required by approved Viewer-owned features.
2. Add direct script examples for indexed buffers, selection, transforms,
   measurements, overlays, and one custom dock.
3. Update core and Viewer documentation using repository skills and
   current MkDocs-compatible NumPy style.

Exit gate: Viewer-owned tools and components use public Viewer operations and
package-local tests/docs/artifacts pass.

## Later phase — compas_model redesign

The current `ModelViewer` is a draft and is not migrated as a compatibility
exercise. A later approved design may replace its controller, hierarchy
projections, selection, caching, and UI composition. It should consume proven
core Scene and Viewer contracts where they fit, and propose additions only for
new demonstrated requirements.

## Phase 5 — Framework integration and review

Governing ADR: 007.

1. Verify installed core Scene and Viewer behavior at exact candidates; keep
   the separate plugin initiative's model/viewer lifecycle gate independent.
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
