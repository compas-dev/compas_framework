# Title: Where should tessellation metadata, provenance, and error information live?

## Status

Accepted

## Context

`Tessellation` currently contains triangle buffers, optional same-index normals
and UVs, and independent polylines. It deliberately remains lightweight and
non-serializable. OCC could expose face/trim correspondence, and CGAL already
has operation-specific intersection-edge, source-face, and skeleton mappings.
Carrying every possible field into `Tessellation` would couple unrelated
producers and simple conversions.

## Options

1. Add universal strategy, provenance, mapping, and error fields to
   `Tessellation`. This is discoverable but bloats a zero-copy interchange and
   creates unstable optional semantics.
2. Always return a universal `TessellationResult`. This is uniform but burdens
   simple callers and duplicates the existing container role.
3. Put metadata on persistent `Mesh`. This enables serialization but conflates
   generated approximation data with editable topology and attributes.
4. Keep `Tessellation` minimal and defer every enriched result API from the
   initial implementation. Require a separate future ADR and operation-specific
   result type when a concrete consumer and backend data source exist.

## Recommendation

Choose option 4. The initial stable operations remain exactly:

```python
geometry.tessellate(strategy) -> Tessellation
geometry.polygonize(strategy) -> PolygonalSurface
```

They do not accept detail/report flags and do not return unions. There is no
universal `TessellationReport` or `TessellationResult`, and no parallel
`tessellate_detailed()`-style method.

`Tessellation` retains representation data only: vertices, triangles, optional
aligned vertex normals, optional aligned UV coordinates, and optional relevant
boundary polylines. These fields describe the produced representation; they
are not provenance.

The initial implementation defers source-face and trim mappings, execution
reports, measured error, refinement histories, and backend diagnostics.
ADR 016 subsequently removes `TessellationCapability` and
`ApproximationError`: neither has a production consumer or operational backend
source. A future discovery or measured-error result requires its own ADR,
concrete consumer, and backend data rather than reusing a reserved schema.

Any future enriched operation requires all of the following:

- a separate ADR identifying a concrete consumer and backend data source;
- a separately named API, never a boolean result flag;
- an operation-specific stable result type, never a union return;
- no serializable references to source objects.

An envelope containing ephemeral `Tessellation` is itself ephemeral.
Independently stable metadata values may be serializable through `Data`.

## Consequences

- Simple conversion and plugin paths remain lightweight.
- The initial API surface has one stable result type per operation and no
  report-mode branching.
- Existing normals, UVs, and relevant boundary polylines remain representation
  fields and must not be documented as source provenance.
- OCC and native backends do not expose source mappings, histories, diagnostics,
  or measured error through the initial tessellation API.
- Capability discovery is available without implying that per-execution error
  or provenance was reported.
- Tests must assert the absence of result flags and union returns and preserve
  the ephemeral serialization boundary of `Tessellation`.
- Documentation must clearly label the deferred metadata categories and avoid
  promising a universal enriched result.

## Affected packages

`compas`, `compas_occ`, `compas_cgal`, `compas_libigl`, `compas_model`, and
`compas_framework`.

## Dependencies

- [002 — Mesh representations](002-mesh-representations.md)
- [003 — Strategy objects](003-strategy-objects.md)
- [004 — Error contracts](004-error-contracts.md)
- [009 — Trimmed surfaces](009-trimmed-surfaces.md)
