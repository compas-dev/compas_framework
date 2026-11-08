# Scene, Viewer, and Visualisation Implementation Plan

## Status

Architecture correction implemented and verified. ADRs 013–014 are Accepted
and supersede the adapter model. Phase 2 may resume. Accepted ADRs 015–016 now
authorize `SceneStateField`-backed editability, non-state editable declarations,
and contextual overrides; superseded implementations must be replaced and
verified.

## Dependency graph

```text
ADR 001 --> ADR 008 --> ADR 009 --> ADR 010
    |
    +--------> ADR 002
    +--------> ADR 003 --> ADR 004

ADRs 001–003 ----------> ADR 005
ADRs 001, 003–005 -----> ADR 006
ADRs 001–010 ----------> ADR 007 rollout gate
```

## Phase 0 — Scene ownership and serialization amendment

Governing ADRs: 001, 008, 009, and 010.

Status: implemented, but subject to the Accepted ADR 013–014 correction before
Phase 2 proceeds.

1. Add the verified Viewer round-trip regression and a minimal core adapter
   test covering the constructor-before-attachment failure. Keep the actual
   draft ModelViewer failure as evidence for its later redesign.
2. Audit Scene, SceneObject, Group, Viewer adapters, the draft model adapters,
   and compatibility-only consumers against the proposed node/adapter split.
3. Implement the closed scene node/state schema, durable node GUIDs,
   reference-only descriptions, runtime item bindings, and two-phase
   deserialize/bind lifecycle.
4. Implement explicit MRO-composed extension field declarations; preserve
   unknown namespaced extension state within the new schema.
5. Migrate core and Viewer adapters without serializing caches, selection,
   construction commands, or runtime handles. Use the draft ModelViewer failure
   as external regression evidence, not as behavior to preserve.
6. Document the separate future Session aggregation boundary without adding a
   `SceneBundle`, URI resolver, asset registry, or Session implementation.

Exit gate: the Viewer and minimal-adapter regressions pass; shared item
identity and durable node identity round-trip separately; scenes load without
a visualization backend; runtime adapters bind only after the complete
hierarchy exists; independently loaded items bind without copying; unresolved
references follow ADR 010; local/package quality, typing, docs, and artifact
checks pass.

## Phase 1 — Boundaries and indexed geometry

Governing ADRs: 001, 002, 007, 008, 009, and 010.

Status: implemented and verified.

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

Status: ready on the implemented and verified ADR 013–014 scene foundation.

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

## Contextual object-settings work

Governing ADRs: 013, 014, 015, and 016.

Status: authorized by Accepted ADRs 015–016; implementation and verification
of the amended design pending.

1. Remove the public `FormField` API, item-target bindings, field refresh
   modes, the parallel built-in Viewer field inventory, and the first separate
   `EditableAttribute` implementation.
2. Add `editable` and the optional atomic data-only `update` callback to
   `SceneStateField`; reject `update` when the field is not editable.
3. Reserve `__editable_attributes__` for non-state fields, initially `name` and
   `opacity`, and compose both MRO sources through
   `SceneObject.editable_attributes()` without duplicate subclass names.
4. Add graphics-free context contributions that filter, extend, or replace
   entries through the same mapping with exact registry keys, deterministic
   lexical contribution ordering, and conflict errors.
5. Migrate object settings to infer presentation and writability from the
   normalized mapping and current values; keep represented-item parameters in
   `ParameterForm`.
6. Apply default assignment or the optional synchronous data-side callback
   atomically, then let Viewer conservatively rebuild/redraw/refresh after
   success only.
7. Verify source composition, removal, conflicts, rollback, graphics-free
   discovery, serialization exclusion, and multiple contexts.

Exit gate: durable semantic attributes use `SceneStateField` as their single
source; non-state names are declared once; context plugins only modify the
normalized mapping; Viewer exclusively owns form UI and post-mutation refresh;
core exposes no form or refresh protocol; all applicable core, Viewer, and
framework integration checks pass.

## Proposed datastructure attribute tables

Governing ADRs: 006, 017, and 018.

Status: blocked pending explicit approval of ADRs 017–018.

1. Add lazy Mesh and Graph element-attribute table models using declared
   default mappings and singular domain APIs.
2. Add sidebar tabs only for domains with declared columns; preserve mapping
   insertion order and omit sparse undeclared attributes.
3. Add supported scalar delegates, singular setter/unset mutation, effective
   values, local selection, and conservative Viewer refresh.
4. Verify laziness, large/empty structures, value types, reset behavior,
   atomic failure, and excluded first-version features.

Exit gate: tables are lazy, declared-domain-driven, Viewer-owned, and verified
without core API changes.

## Proposed Viewer identity and configuration lifecycle

Governing ADRs: 019 and 020.

Status: blocked pending explicit approval of ADRs 019–020.

ADR 019 is independently decidable. ADR 020 depends on its identity contract
for schema validation and startup application.

1. Apply validated startup configuration before Qt application/window
   construction; connect title, icon, dimensions, and fullscreen.
2. Retain dataclasses, add path-aware validation, and separate startup
   configuration from transient Viewer state.
3. Implement the schema-2 field audit and migration/rejection behavior.
4. Verify identity, icons, fullscreen, status bar, every field disposition,
   setup-only mutation semantics, serialization, and typed subclass extension.

Exit gate: startup identity and configuration are validated and effective;
removed fields are absent; transient state is not serialized.

Implementation of the two proposed sections must coordinate ownership of
sidebar and startup UI files. Neither proposal authorizes implementation before
its ADRs are accepted.

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
- `compas_session` aggregation of data, one or more scenes, settings, and
  history, including optional Viewer new/open/save conveniences;
- notebook, Rhino, Grasshopper, Blender, or other backend migrations.
