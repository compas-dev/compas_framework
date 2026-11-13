# ADR 048: Referenced Data Domain

## Status

Accepted on 2026-11-11. Implemented, locally verified, and independently
reviewed.

## Context

Scene objects and annotation entries refer to domain `Data` by GUID, but the
default Viewer exposes only the spatial hierarchy and annotation list. The
represented item is available through the existing runtime binding table, yet
there is no flat UI for finding shared or unresolved items independently from
scene-object placement.

Core `Scene` is deliberately reference-only. Its `item_store` is a non-owning,
non-serialized runtime binding map, and unrelated unattached data belongs to a
future Session aggregate. Viewer must not introduce another owning store or
silently broaden Scene into that aggregate.

## Recommendation

Add a fourth top-level Viewer sidebar domain named **Data**. The final order is
**Scene**, **Data**, **Annotations**, **System**. Data is a Viewer-owned flat
projection of items referenced by the current Scene, not an owning data store.

Build one row per distinct item GUID in deterministic first-reference order:

1. spatial scene objects in hierarchy order;
2. annotation entries in durable annotation order.

Deduplicate shared items and show **Name**, **Type**, **Status** (Bound or
Unresolved), and **References**. An unresolved row retains its GUID and
reference inventory without invoking a resolver. A bound shared item appears
once and resolves to the existing instance in `Scene.item_store`.

Data-list selection is local transient UI state. It does not mutate spatial,
annotation, viewport, or element-table selection and does not serialize.
Preserve the selected GUID across refresh when it remains referenced.

For one row, expose a main-window-owned, read-only modal **Data Details**
dialog. Its header shows name, concrete type, GUID, binding status, and every
referring scene object and annotation. General bound `Data` shows the same safe
inspected public parameters used by Object Details; do not recursively dump or
eagerly materialize arbitrary `__data__`.

For Mesh and Graph, reuse ADR 017's lazy domain-table models in read-only mode.
Preserve declared-column order, retrieve values lazily, and omit sparse
undeclared attributes. Unresolved rows show only their GUID and references.

Refresh after scene replacement, spatial-object add/remove, annotation
add/remove, item binding, and Data-domain activation. Rebuilding the projection
must not mutate data, resolve items implicitly, or rebuild render buffers.

## Consequences

- Represented items become discoverable independently from spatial placement.
- Shared identity and unresolved references remain explicit.
- Data selection remains independent and transient.
- No Core API, Scene schema, or ownership change is required.
- “Data” names a UI projection; it does not create an owning store.

## Exclusions

- unattached item storage or Session aggregation;
- files, URIs, catalogs, resolvers, loading, or binding;
- deleting, renaming, or editing data or element attributes;
- viewport linkage, batch operations, search, or filtering;
- persisted Data selection; and
- modeless or pinned inspectors.

The initial projection intentionally uses only references in the active
`Scene`. A separately approved future Session design may replace or extend
that source with an aggregate spanning unattached data and multiple scenes.
That evolution must preserve the ownership boundary: Session, not Viewer,
would own the aggregate, and Viewer would remain a read-only consumer.

## Verification

- Deduplicate an item shared by multiple scene objects.
- Include annotation-only items and preserve first-reference order.
- Show bound and unresolved rows without implicit resolution.
- List every reference in Data Details.
- Keep spatial, annotation, Data, viewport, and element selections independent.
- Keep Mesh and Graph tables lazy, declared-column-driven, and read-only.
- Avoid recursive item serialization during generic inspection.
- Refresh after add, remove, bind, activation, and scene replacement.
- Prove no Scene serialization, Core ownership, identity, or buffer changes.

## Dependencies

- Preserves ADRs 001, 010, and 013.
- Reuses the read-only part of ADR 017.
- Extends ADR 032's closed sidebar domains.
- Keeps ADR 018 editing outside this initial scope.

## Decision

Approved on 2026-11-11 as the narrow first step described above. This approval
does not include Session aggregation, unattached data, multiple-scene
inventory, or Viewer ownership of data. Evolving the inventory source to a
Session aggregate requires a separate ADR and explicit approval.

## Implementation Note

Implementation and independent review pass. Direct `add_object` and
`add_reference` operations trigger exactly one immediate Data refresh without
a renderer refresh, and a still-referenced selected GUID remains selected.
Generic shared-item inspection uses safe public parameters and never reads
arbitrary `__data__`; one failing inspected attribute is isolated rather than
preventing the remaining details from opening.

Final review adds removal, clearing, and batched-deletion regressions and
confirms exactly one Data refresh without extra renderer work. The Viewer suite
passes 672 tests with two expected offscreen OpenGL skips. Ruff, formatting,
Pyright, strict MkDocs, and diff checks pass. The framework direct-source gate
passes 16 tests with one expected exact-VCS skip. Native user direct-use,
refreshed hosted CI, and candidate-artifact verification remain pending.
