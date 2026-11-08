# Scene, Viewer, and Visualisation Implementation Plan

## Status

Architecture correction implemented and verified. ADRs 013–014 are Accepted
and supersede the adapter model. Accepted ADRs 015–016 govern
`SceneStateField`-backed editability, non-state editable declarations, and
contextual overrides; the superseded implementations were replaced and the
amended contract is independently approved and green in package and
exact-candidate integration CI. Accepted ADRs 017–020 are implemented, locally
verified, and independently approved in their required order: ADR 019, ADR 020,
ADR 017, then ADR 018. Their hosted verification passed. ADR 003 object
selection is now implemented, locally verified, independently approved, and
green in the hosted Viewer matrix and refreshed exact-candidate verification.
ADR 004 transformations, refresh, and undo is implemented, locally verified,
independently approved, and green in refreshed package and exact-candidate
verification. The current phase is Phase 3 annotation architecture approval.
ADRs 021–025 and 027–028 are Accepted; proposed ADR 026 blocks implementation.

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

Status: implemented and verified after the Accepted ADR 013–014 correction.

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

Status: ADR 003 object selection is implemented, locally verified, and
independently approved on the verified ADR 013–014 scene foundation. The hosted
Viewer matrix and exact-candidate verification passed. ADR 004 transformations,
refresh, and undo is implemented, locally verified, and independently approved;
hosted package and exact-candidate verification passed.

1. [Complete] Separate persistent Viewer configuration from transient Viewer
   state.
2. [Complete] Implement the object-selection model and migrate viewport,
   rectangle, tree, commands, renderer settings, and programmatic Viewer APIs.
3. [Complete] Remove scene-owned selection as a second authority and update
   serialization/tests. Keep only the read-only scene-object projection needed
   by rendering.
4. [Complete] Add atomic multi-object transform transactions, categorized
   refresh, and the Viewer-level reversible transaction stack.
5. [Complete] Add the transform-selected command and undo/redo menu operations
   after command/programmatic semantics passed. No transform-input UI was
   invented; visual gizmo design remains a follow-up if it requires new
   choices.

Exit gate: all selection paths share one model; transform/undo tests cover
parents, batches, failures, world/local conversion, cached descendant bounds,
history invalidation, and buffer-update scope. The local gate passed; hosted
package and exact-candidate verification passed.

## Contextual object-settings work

Governing ADRs: 013, 014, 015, and 016.

Status: implemented and independently verified under amended Accepted ADRs
015–016.

Implementation record:

1. Removed the public `FormField` API, item-target bindings, field refresh
   modes, the parallel built-in Viewer field inventory, and the first separate
   `EditableAttribute` implementation.
2. Added `editable` and the optional atomic data-only `update` callback to
   `SceneStateField`, rejecting `update` when the field is not editable.
3. Reserved `__editable_attributes__` for non-state fields, initially `name`
   and `opacity`, and composed both MRO sources through
   `SceneObject.editable_attributes()` without duplicate subclass names.
4. Added graphics-free context contributions that filter, extend, or replace
   entries through the same mapping with exact registry keys, deterministic
   lexical contribution ordering, and conflict errors.
5. Migrated object settings to infer presentation and writability from the
   normalized mapping and current values; represented-item parameters remain
   in `ParameterForm`.
6. Applied default assignment or the optional synchronous data-side callback
   atomically; Viewer conservatively rebuilds/redraws/refreshes after success
   only.
7. Verified source composition, removal, conflicts, rollback, graphics-free
   discovery, serialization exclusion, and multiple contexts.

Exit gate: passed. Durable semantic attributes use `SceneStateField` as their
single source; non-state names are declared once; context plugins only modify the
normalized mapping; Viewer exclusively owns form UI and post-mutation refresh;
core exposes no form or refresh protocol; all applicable core, Viewer, and
framework integration checks pass.

## Viewer identity and configuration lifecycle

Governing ADRs: 019 and 020.

Status: implemented, locally verified, independently approved, and passed in
hosted package and exact-candidate verification.

Implementation record: ADR 019 was completed first. ADR 020 followed because
its schema validation and startup application depend on the accepted identity
contract.

1. Applied validated startup configuration before Qt application/window
   construction and connected title, icon, dimensions, and fullscreen.
2. Retained dataclasses, added path-aware validation, and separated startup
   configuration from transient Viewer state.
3. Implemented the schema-2 field audit and migration/rejection behavior.
4. Verified identity, icons, fullscreen, status bar, every field disposition,
   setup-only mutation semantics, serialization, and typed subclass extension.

Local exit gate: passed. Startup identity and configuration are validated and
effective; removed fields are absent; transient state is not serialized.

## Datastructure attribute tables

Governing ADRs: 006, 017, and 018.

Status: implemented, locally verified, independently approved, and passed in
hosted package and exact-candidate verification after ADRs 019–020 established
configuration and sidebar ownership.

Implementation record:

1. Added lazy Mesh and Graph element-attribute table models using declared
   default mappings and singular domain APIs.
2. Added sidebar tabs only for domains with declared columns, preserved mapping
   insertion order, and omitted sparse undeclared attributes.
3. Added supported scalar delegates, singular setter/unset mutation, effective
   values, local selection, and conservative Viewer refresh.
4. Verified laziness, large/empty structures, value types, reset behavior,
   atomic failure, and excluded first-version features.

Local exit gate: passed. Tables are lazy, declared-domain-driven, Viewer-owned,
and verified without core API changes.

The implementation order was ADR 019, ADR 020, ADR 017, then ADR 018.
Configuration work established startup and sidebar visibility ownership before
the tables followed. The architectural watchpoint recorded in the proposal
remains active during integration verification; concrete contrary evidence
must be brought back without inventing a replacement model speculatively.

## Phase 3 — Annotations and overlays

Governing ADRs: 001–005, 007, and 021–028.

Status: existing `Tag` and `ArrowOverlay` behavior and serialization were
audited. ADR 023 approves a clean break with no aliases or legacy decoding.
ADR 024 approves distinct transient inspection and persistent dimension
outcomes. ADR 028 approves one dimension type with fixed and associative
anchors, snapping in both UI modes, no silent fallback, and explicit unresolved
references. ADRs 021–022 place narrow durable annotation data in `compas.scene`
and define persistent unit/precision snapshots without implicit conversion.
ADR 025 approves the ordered scale/legend overlay layer. Implementation waits
for approval of ADR 026 supported snap acquisition. ADR 027 approves nested
Viewer measurement presentation settings and the Units and Measurement UI.

1. [Complete] Inspect current `Tag`/`ArrowOverlay` serialized behavior and
   approve the clean-break migration in ADR 023.
2. [Complete] Separate transient measurement inspection from persistent
   dimension-annotation outcomes in ADR 024.
3. [Complete] Define fixed and associative persistent dimension anchors in ADR
   028.
4. [Complete] Approve core ownership/schema and persistent unit/precision
   snapshots in ADRs 021–022.
5. [Complete] Approve Viewer unit/precision presentation and read-only global
   tolerance UI in ADR 027.
6. Implement world text, arrow, and distance annotation scene items/adapters.
7. Implement transient inspection plus fixed/associative persistent dimension
   snapping, preview, cancel, and completion after ADR 026 is approved.
8. Implement the approved scale and legend screen overlays through one Viewer
   overlay layer.
9. Remove concrete approved-type checks from the main render loop.

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
