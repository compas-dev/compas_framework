# ADR 050: Read-Only Data Item Inspection

## Status

Accepted on 2026-11-14. Implemented and locally verified in the uncommitted
Viewer working tree based on `0f263f1`.

## Context

Accepted ADR 048 makes Data a read-only, non-owning projection of items
referenced by the active Scene. Its Details dialog shows identity, status, and
references. A bound general `Data` item shows safe public constructor
parameters, while Mesh and Graph show lazy read-only component-attribute tables
instead of parameters.

Users need one coherent snapshot containing the available general parameters,
general datastructure attributes, and supported component-specific attributes.
This must not turn Data into an editing, ownership, resolution, or extension
registry boundary.

## Options

1. Expand Data Details with a fixed read-only composition using existing Core
   and Viewer contracts.
2. Make Data Details editable.
3. Add a generic per-Data-type inspection registry.
4. Keep the mutually exclusive parameter/table presentation.

## Recommendation

Choose option 1.

Keep the existing identity and references header. For one bound item, place one
read-only tab widget below it with sections in this order:

1. **Parameters** for safe available public constructor parameters;
2. **General Attributes** when the item is a Core `Datastructure`; and
3. the existing supported component-domain tabs in ADR 017 order.

The Parameters tab uses the existing public-attribute-first inspection path and
keeps serialized fallback disabled. It must never recursively inspect or dump
arbitrary `__data__`. An item with no exposed parameters has an empty table
rather than losing the section. The table columns remain **Parameter** and
**Value**.

General Attributes is supported only for verified Core `Datastructure`
instances. It reads the public `attributes` mapping, preserves mapping insertion
order, and displays one name/value row per entry. An empty mapping produces an
empty table. Its columns are **Attribute** and **Value**. Do not infer a general-
attributes contract from an arbitrary `attributes` attribute on other `Data`
subclasses.

Mesh and Graph retain the existing lazy read-only tables: Mesh vertex, edge,
and face domains; Graph node and edge domains. Preserve declared default-column
order, effective-value lookup, zero-row declared domains, and omission of
sparse undeclared attributes. Parameters and General Attributes appear
alongside these tabs rather than being replaced by them.

Parameter and general-attribute values use the existing Data Details display
convention: `str(value)`, or `<unavailable: ExceptionType>` if formatting
raises. Component tables retain ADR 017's key, scalar, and Boolean formatting;
a failed component read or format produces the same unavailable marker in that
cell. A failure does not prevent the remaining metadata, parameters,
attributes, or domains from opening. Inspection is a snapshot; it does not
track later mutation.

An unresolved row keeps the existing metadata-only Details view. It does not
invoke a resolver, synthesize parameters or attributes, or create a placeholder
item.

## Mutation and Ownership Boundary

This decision is read-only:

- no parameter, general-attribute, default-attribute, or element-attribute
  editing;
- no rename, delete, bind, load, or resolve operation;
- no Data, Scene, Session, or Viewer ownership change;
- no selection coupling, serialization, schema, render-buffer rebuild, redraw,
  or referrer refresh; and
- no generic inspector registration or arbitrary `Data` introspection.

The opt-in editable Scene Attributes component governed by ADR 018 remains a
separate Scene-object context. Editing from the deduplicated Data domain would
need a separate decision covering shared referrers, validation, atomicity,
refresh, reset/default semantics, and undo.

## Alternatives and Tradeoffs

Editable Data would satisfy a broader meaning of access but conflicts with ADR
048 and cannot safely refresh only one selected SceneObject when an item is
shared. It is deferred pending an explicit mutation design.

A generic inspection registry could support VolMesh, CellNetwork, or external
`Data` subclasses, but no current producer contract defines their sections,
columns, ordering, cost, or failure behavior. Adding that extension point now
would be speculative. Additional types require concrete evidence and a later
ADR.

Keeping the current mutually exclusive presentation is simplest in code but
does not satisfy the requirement to access general and component-specific
information together.

## Compatibility

The change is additive within the modal Data Details snapshot. Data inventory,
selection, identity, reference order, unresolved behavior, and public Core
contracts do not change. No migration, compatibility alias, or Core release is
required.

## Verification

- Show Parameters for bound general Data and for Mesh/Graph.
- Show General Attributes only for Core Datastructure values, preserving
  mapping insertion order for empty and populated mappings.
- Show Mesh/Graph lazy component tabs alongside Parameters and General
  Attributes in the exact approved order.
- Preserve declared column order, effective lazy lookup, zero-row declared
  domains, and omission of sparse undeclared attributes.
- Isolate parameter, mapping, and value-formatting failures to the affected
  entry.
- Keep unresolved rows metadata-only without resolution or synthesized data.
- Prove shared items remain one Data row and every reference remains listed.
- Prove opening Details performs no mutation, selection coupling,
  serialization, renderer rebuild, redraw, or Data projection refresh.
- Extend the Viewer tutorial to explain the read-only boundary and add a
  focused Mesh/Graph example with general attributes, declared defaults, local
  component overrides, and shared Scene references.

## Dependencies

- Amends the Details composition of Accepted ADR 048 without changing its
  read-only ownership boundary.
- Reuses the read-only part of Accepted ADR 017.
- Preserves ADR 018 editing as an opt-in Scene-context surface.
- Independent of Accepted ADR 051; either decision may be implemented and
  verified separately.

## Implementation Evidence

The Viewer implementation combines the ordered Parameters, General Attributes,
and supported component-domain tabs without adding a mutation or ownership
path. Focused Data-panel and datastructure-table tests pass 38 tests. The
complete Viewer suite passes 705 tests with two expected offscreen native
OpenGL skips. Viewer Ruff, formatting, package Pyright with zero errors, strict
MkDocs, and `git diff --check` pass. The framework direct-source gate passes 16
tests with one expected exact-revision skip and includes the ordered-tab,
general-attribute, default/override, and nonmutation contracts. Native visual
and interaction confirmation, refreshed hosted CI, and candidate-artifact
verification remain separate pending layers.

## Acceptance Scope

The user accepted the fixed read-only tabs, verified
`Datastructure.attributes` scope, and preserved exclusions on 2026-11-14.
Acceptance does not authorize Data editing, additional datastructure domains,
a generic inspection registry, or Core changes.
