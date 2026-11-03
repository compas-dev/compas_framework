# Title: Should the unified architecture preserve legacy API compatibility?

## Status

Accepted

## Context

Public and downstream code already depends on scalar resolution controls,
tuple results, `.tessellation`, `compute_tessellation()`, OCC
`to_tessellation()`, misspelled `to_tesselation()`, `to_viewmesh()`,
`triangulated=True`, and direct native-package calls. Defaults also encode
specific diagonal, caching, seam, buffer identity, and serialization behavior.
The initiative now explicitly prioritizes the cleanest coherent target API
over backward compatibility. Retaining aliases and dual result forms would
make the new architecture harder to understand and test.

The coordinated baseline is COMPAS 3.0. Affected plugin packages cannot safely
advertise compatibility with COMPAS 2.x while implementing these contracts.

## Options

1. Make a coordinated breaking replacement across affected packages. This
   yields one coherent API but requires synchronized releases and caller edits.
2. Add new APIs indefinitely without deprecation. This is safe short-term but
   leaves permanent ambiguity.
3. Stage additions, aliases, adapters, warnings, and eventual removals. This
   reduces immediate breakage but temporarily or permanently doubles the API.
4. Change only documentation and preserve all behavior. This cannot resolve
   plugin signature and interoperability defects.

## Recommendation

Choose option 1. Implement the approved target contracts together and remove
superseded public forms rather than shipping aliases. This includes scalar
tessellation controls; cached `.tessellation`; `compute_tessellation()`;
`to_tessellation()`; misspelled `to_tesselation()`; `to_viewmesh()`;
`triangulated=True`; `quads_to_triangles()`; legacy planar keywords and
positional forms; face-only and tuple triangulation results; public raw tuple
plugin inputs; and divergent direct backend APIs. Coordinate package versions
so the breaking set is internally consistent. `Tessellation` itself remains
the canonical ephemeral result.

Release the core contract as COMPAS 3.0 and require affected plugin packages to
depend on `compas>=3.0.0`. Where a package already follows a major-version
upper-bound policy, advance that bound to `<4`; for example, CGAL uses
`compas>=3.0.0,<4`. This version floor is the synchronized breaking-release
baseline for the initiative.

## Consequences

- There is one target call form per operation; alias and normalization code is
  unnecessary.
- This is a broad source-breaking change for core, OCC, CGAL, libigl, model,
  examples, and downstream users.
- Geometry invariants that remain architecturally important—orientation,
  seams, polygon/source boundaries, and `Tessellation` buffer semantics—still
  require tests. Public cache identity and legacy connectivity defaults do not
  survive merely for compatibility.
- A concise migration guide maps removed names and result forms to the new API,
  but no deprecation period is required.
- A synchronized package version set and cross-package integration suite are
  prerequisites for release.
- Package metadata and supported-version tests must enforce COMPAS 3.0 as the
  minimum for affected plugins. Existing major upper-bound policies advance to
  `<4` rather than being removed implicitly.
- Mixed COMPAS 2.x/3.x package sets are unsupported for this initiative's API.
- Accepting this ADR authorizes the architectural break, not merging or
  publishing changes.

## Affected packages

`compas`, `compas_occ`, `compas_cgal`, `compas_libigl`, `compas_gmsh`,
`compas_model`, and `compas_framework`.

## Dependencies

- [006 — Tessellation API](006-tessellation-api.md)
- [007 — Triangulation operations](007-triangulation-operations.md)
- [009 — Trimmed surfaces](009-trimmed-surfaces.md)
- [010 — Metadata and provenance](010-metadata-provenance.md)
- [011 — Planar triangulation contract](011-planar-triangulation-contract.md)
- [012 — Plugin boundaries](012-plugin-boundaries.md)
