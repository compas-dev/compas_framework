# ADR 017: Lazy Datastructure Element-Attribute Tables

## Status

Accepted.

## Context

Viewer can inspect a selected scene object's presentation attributes, but it
does not provide a scalable view of attributes stored on Mesh or Graph
elements. Building one widget per value would be slow for large structures,
while copying all sparse element dictionaries would increase startup cost and
could invent columns that have no declared domain meaning.

COMPAS datastructures already expose domain defaults such as
`default_vertex_attributes` and singular domain APIs for retrieving element
attributes. The initial table design can use those public contracts without a
new core abstraction.

## Options

1. Add Viewer-owned lazy table models for declared Mesh and Graph element
   domains.
2. Materialize every element attribute into ordinary table widgets.
3. Add a generic tabular-inspection API to core.
4. Scan sparse per-element dictionaries to infer every observed column.

## Recommendation

Choose option 1.

Viewer owns a lazy `QAbstractTableModel` for datastructure element attributes.
The initial supported types are Mesh and Graph. Domains are discovered from
their existing `default_*_attributes` mappings and corresponding singular
element APIs: Mesh vertex, edge, and face domains; Graph node and edge domains.
The default mapping's insertion order defines the initial column order.

The model stores element identifiers and reads effective cell values lazily
through the singular getter. It does not build one component per cell or copy
the complete attribute table. Sparse undeclared attributes found only in local
element dictionaries are omitted; the table does not scan the datastructure to
invent columns.

Viewer adds a tab only for a supported domain whose default-attribute mapping
declares at least one column. A declared domain with no elements may therefore
show a zero-row table with its declared columns. A domain with no declared
attribute columns is omitted.

This is a Viewer feature. It requires no changes to Mesh, Graph, or core
datastructure APIs and does not make Qt a core dependency.

## Consequences

- Large Mesh and Graph attribute sets can be inspected without eagerly
  constructing all cell widgets or values.
- The visible schema is stable and follows datastructure-declared defaults.
- Undeclared sparse attributes remain available through datastructure APIs but
  are not exposed by this initial table.
- Additional datastructure types or domains require evidence and a later
  amendment.

## Compatibility

The table is an additional Viewer sidebar surface. It does not change
datastructure serialization, element attribute semantics, object settings, or
the existing represented-item `ParameterForm`.

## Verification

- Discover the supported Mesh and Graph domains from default mappings and
  singular APIs.
- Preserve default mapping insertion order in columns.
- Verify data is read lazily and no per-cell component collection is created.
- Omit sparse undeclared attributes without scanning all local dictionaries.
- Create tabs only for domains with declared attribute columns, including a
  zero-row table when such a domain has no elements.
- Verify empty datastructures, large datastructures, and effective default
  values.
- Prove importing Viewer plugins remains graphics-free.

## Dependencies

- Uses the Viewer-owned sidebar boundary from ADR 006.
- Independent of ADRs 015–016; object settings and element tables edit
  different owners.
- Implementation must coordinate sidebar file ownership with ADRs 019–020 and
  other Viewer UI work.

## Decision

Approved on 2026-11-08. Viewer owns lazy Mesh and Graph element-attribute table
models whose domains and columns come from declared defaults and existing
singular datastructure APIs. The rationale is to keep large tables scalable and
their schema explicit without copying all values, scanning sparse dictionaries,
adding per-cell components, or introducing a new core abstraction.
