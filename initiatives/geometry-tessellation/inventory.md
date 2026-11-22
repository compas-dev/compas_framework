# Geometry Discretization, Tessellation, and Triangulation Inventory

Status: restarted reconnaissance complete (2026-11-01)

This inventory was rebuilt from fresh, read-only investigations after the
initiative objective was expanded. The earlier initiative documents were not
used as authoritative sources. The investigation covered `compas`,
`compas_occ`, `compas_cgal`, `compas_libigl`, `compas_gmsh`, and the visible
`compas_model` working tree. No package source was modified and no tests were
run during reconnaissance.

## Executive findings

1. Core already has three different mesh-like representations: ephemeral
   triangle buffers (`Tessellation`), persistent polygon buffers
   (`PolygonalSurface`), and rich mutable topology (`Mesh`). A new mesh class
   must justify overlap with all three.
2. Existing surface and shape tessellation is uniform and count-controlled.
   There is no `UVGrid`, adaptive/error-controlled strategy, common strategy
   base, or serialized tessellation configuration.
3. Trim-aware NURBS tessellation exists only at the OCC BRep level. A standalone
   `NurbsSurface` has no trim loops; sampling an underlying surface does not
   preserve face trims or holes.
4. Tessellation and triangulation are distinct in parts of the API, but naming,
   mutation behavior, diagonal choice, vertex insertion, and results vary.
5. CGAL and libigl predominantly consume raw `(vertices, faces)` triangle
   buffers. OCC instead converts a rich `Mesh`. No shared adapter or validation
   boundary spans these representations.
6. Core and CGAL constrained/conforming Delaunay signatures are incompatible,
   and CGAL lacks current plugin entry-point metadata. Direct CGAL tests miss
   both problems.
7. `Tessellation` carries normals, UVs, and boundary polylines, but not strategy,
   source-face/trim correspondence, error estimates, or validation status.
   Plugin-specific results already carry richer provenance.
8. Framework-level integration coverage is absent. Trimmed faces, periodic
   seams, approximation quality, plugin dispatch, native interoperability, and
   strategy serialization remain major gaps.

## Current representations

### `compas.geometry.Tessellation`

Source: `../compas/src/compas/geometry/tessellation.py`.

- Frozen, slotted, lightweight result with required `vertices` and indexed
  `triangles`.
- Optional same-index `vertex_normals` and `texture_coordinates`; independent
  `polylines` are intended for BRep edges.
- Retains buffers without copying. Tests require exact input-buffer identity.
- Same-index attributes deliberately require duplicate vertices at seams.
- Explicitly ephemeral and non-serializable; it does not inherit `Data`.
- Converts to independent `PolygonalSurface` and `Mesh` objects.
- Does not validate shape, arity, bounds, finiteness, winding, manifoldness, or
  attribute lengths.
- Carries no strategy, source geometry, source-face/trim mapping, error
  estimate, or provenance status.

This is already a compact triangle-buffer candidate, but it is not a persistent
mesh, serialized result, or validated native boundary.

### `compas.geometry.PolygonalSurface`

Source: `../compas/src/compas/geometry/polygonal_surface.py`.

- Persistent, serializable indexed polygon storage without half-edge topology.
- Supports arbitrary face arity and exposes closed/manifold/orientable/oriented
  queries.
- Its triangle view preserves triangles and Earcut-triangulates other faces
  without adding vertices.
- Cached tessellation shares its internal vertex list; tuple conversion copies.
- Basic vertex/index validation exists, but getters expose internal mutable
  lists, so in-place edits can bypass cache invalidation.

### `compas.datastructures.Mesh`

Source: `../compas/src/compas/datastructures/mesh/mesh.py`.

- Persistent, mutable half-edge topology with attributes and algorithms.
- `to_vertices_and_faces(triangulated=True)` is non-mutating: triangles pass
  through, quads split on `(a, c)`, and n-gons gain a centroid and fan.
- `quads_to_triangles()` mutates and splits on the opposite `(b, d)` diagonal
  while preserving face attributes.
- `is_trimesh()` and `is_quadmesh()` classify topology, but no dedicated
  `TriangleMesh` or `QuadMesh` runtime class exists.
- No general `triangulated()`, `triangulate()`, or `to_triangle_mesh()` method
  was found.

Core `MeshType` is only a tuple of coordinate and face-index sequences
(`../compas/src/compas/_typing.py`). It does not encode triangle arity,
topology, metadata, or rich objects.

## Continuous geometry

### Parametric surfaces

Source: `../compas/src/compas/geometry/surfaces/surface.py`.

- Stored U/V face-count defaults are 16 with minimum 1; per-call controls are
  `nu`, `nv`, and optional domain subsets `du`, `dv`.
- Uniform tensor-product sampling yields `(nu + 1) * (nv + 1)` vertices,
  `nu * nv` quads, and `2 * nu * nv` triangles.
- Tessellation splits cells on `(a, c)` and can add analytic normals and
  normalized grid UVs.
- Polygon/mesh conversions preserve quads; `to_triangles()` returns coordinate
  triples rather than indexed faces.
- Periodicity flags exist, but both endpoints are sampled and not welded.
- Singularities, coincident seams, reversed domains, watertightness,
  manifoldness, and approximation error have no common handling.
- No adaptive refinement, deviation control, error estimate, or guarantee
  exists.

Core `NurbsSurface` inherits this generic path and stores control points,
weights, knots, degrees, domains, and periodic flags
(`../compas/src/compas/geometry/surfaces/nurbs.py`). It stores no trim loops or
holes. Trimming belongs to a BRep face, which exposes its underlying surface,
ordered loops, and orientation (`../compas/src/compas/geometry/brep/face.py`).

### Analytical shapes and curves

`Shape` (`../compas/src/compas/geometry/shapes/shape.py`) uses stored U/V
resolution with minimum 3 and per-call names `u`/`v`. Concrete shapes may ignore
one or both dimensions. Tessellation passes triangles, splits quads on `(a, c)`,
rejects other faces, and omits normals, UVs, strategy, error, and provenance.

`Curve.to_points()` and `Curve.to_polyline()` uniformly sample parameter space
(`../compas/src/compas/geometry/curves/curve.py`). Counts have different
defaults/meanings and provide no arc-length or deviation guarantee.

## BRep and OCC tessellation

Core `brep_tessellate()`, misspelled `Brep.to_tesselation()`, and
`Brep.to_viewmesh()` return `(Mesh, list[Polyline])`. `Brep.to_meshes(u, v)`
forwards count-style keywords through a deflection-oriented plugin boundary.
See `../compas/src/compas/geometry/brep/operations.py` and `brep/brep.py`.

`OCCBrep.compute_tessellation()`
(`../compas_occ/src/compas_occ/brep/brep.py`):

- Calls OpenCASCADE incremental BRep meshing with linear/angular deflection on
  actual trimmed face topology.
- Extracts face-local vertices, fixes reversed-face winding, and extracts
  topological edge polylines with curve-sampling fallback.
- Returns core `Tessellation`; correctly spelled and legacy tuple-returning
  methods coexist.
- Does not attach UVs, normals, source-face IDs, trim-loop IDs, selected
  controls, or measured/guaranteed error.
- Uses truth-value defaults, so explicit `0.0` becomes the global default.
- Edge fallback sampling may use unrelated curve resolution.
- `to_meshes(u, v)` instead samples underlying NURBS surfaces and does not
  visibly apply trim loops.

Trim-aware NURBS tessellation is therefore a BRep operation, not a standalone
surface operation.

## Algorithms and semantics

### Local triangulation policies

- Surface/shape tessellation: fixed `(a, c)` diagonal.
- Non-mutating `Mesh` conversion: `(a, c)` for quads and centroid fans for
  n-gons, possibly adding vertices.
- Mutating `Mesh.quads_to_triangles()`: `(b, d)` diagonal.
- `PolygonalSurface`: Earcut for non-triangular faces without adding vertices.

These differ in diagonal, allocation, vertex preservation, quality, and
mutation while using related terminology.

### Earcut and Delaunay

Core Earcut (`../compas/src/compas/geometry/triangulation_earclip.py`) supports
an exterior and holes, projects using the first usable exterior triple,
validates with Shapely, triangulates with Mapbox Earcut, and restores winding.
It preserves vertices but has no caller tolerance or coplanarity check. Its
documentation says best-fit plane although the implementation is not a
least-squares fit.

The visible `compas_model` tree has a separate tolerance-aware Earcut result
and algorithm with duplicate/collinear cleanup, Newell-normal projection,
coverage checks, and ring offsets, with different source-index semantics.

Core Delaunay (`../compas/src/compas/geometry/triangulation_delaunay.py`) uses
SciPy/XY for plain Delaunay and returns only faces. Constrained/conforming APIs
are plugin-only and return `(V, F)`; conforming controls are `angle` and `area`.

CGAL uses `boundary, points, holes, curves`, works in XY, and sets constrained
output Z to zero. Its conforming implementation does not accept core quality
arguments. Refined meshing exposes `maxlength`; native minimum-angle input is
unused, concave-hole seeds use arithmetic means, and optional Lloyd optimization
is iteration-limited.

### Refinement, remeshing, simplification

- Core subdivision returns new meshes through named schemes; this is topology
  refinement/smoothing, not a continuous-surface approximation strategy.
- Core also has a mutating heuristic triangle remesher, while geometry-level
  remeshing pluggables return tuples.
- CGAL adds backend-only feature-protection controls.
- libigl isoline remeshing returns face labels beyond the core annotated pair.
- No common refinement strategy or general mesh decimation API was found.

## Strategy and control inventory

No shared `UVGrid`, `Adaptive`, strategy base, serializable tessellation
configuration, or common error model exists. Current controls are backend- and
operation-specific:

- surface/shape U/V counts;
- OCC linear/angular deflection;
- CGAL planar maximum edge length and partially exposed angle/area concepts;
- Gmsh size and curvature options;
- remeshing targets and feature-protection flags.

No common API separates requested policy from backend algorithm, estimated
error from guaranteed bounds, output topology from sampling policy, or numeric
cleanup tolerance from approximation controls. New serializable strategies
must follow COMPAS `Data` conventions without implying equivalent backend
capabilities.

## Plugin and triangle-mesh interoperability

- COMPAS discovers plugins through the `compas.plugins` entry-point group
  (`../compas/src/compas/plugins.py`). OCC declares and tests current entries.
- CGAL retains legacy `__all_plugins__` but has no current entry-point table;
  the list also omits decorated skeletonization functions.
- Core validates calls against implementation signatures. Core/CGAL
  constrained and conforming Delaunay signatures are incompatible; positional
  calls can misbind and keyword calls can fail.
- CGAL direct tests do not exercise discovery or core dispatch.
- CGAL and libigl mainly use `(vertices, triangular_faces)` and repeat NumPy
  coercion. CGAL annotations say `int64` while wrappers usually use `int32`.
- CGAL geodesics is a useful precedent for accepting either `Mesh` or tuple via
  one conversion helper. OCC instead requires a rich `Mesh` and `is_trimesh()`.
- Native wrappers do not consistently validate arity, bounds, finiteness,
  orientation, closedness, or manifoldness. Required validation varies by
  operation.
- CGAL operation-specific results may include intersection edges, source-face
  mappings, or skeleton correspondence. A bare pair cannot represent all
  provenance, but simple conversions should not require it.

A shared interface must separate representation adaptation, backend dtype/
layout coercion, and operation-specific topology validation.

## Tests and documentation

Existing tests protect:

- `Tessellation` zero-copy identity, independent persistent conversions,
  same-index attributes, winding, optional attributes, per-call non-mutation,
  topology distinctions, and cache identity/invalidation;
- surface/shape counts, topology, placement, periodicity flags, finite domains,
  and resolution limits;
- Earcut/regions/polygonal geometry winding, holes, validity, area, and indices;
- mesh conversion counts, mutation, face attributes, and tri/quad classification;
- OCC NURBS serialization/generic tessellation and basic BRep box tessellation;
- CGAL native dtype/layout, remeshing behavior, Delaunay forms, and equivalent
  geodesic results from `Mesh` and tuple input;
- model rendering's distinction between fill triangles and source boundaries,
  plus intentionally different collision/contact/sectioning policies.

Major gaps:

- strategy serialization, adaptive control, deviation measurement, and
  guaranteed-error tests;
- trimmed/holed BRep tessellation behavior, trim orientation, and provenance;
- periodic seam topology, singularities, watertightness, and manifoldness;
- OCC deflection monotonicity, explicit-zero, global-tolerance cache behavior;
- CGAL discovery and dispatched signature compatibility;
- shared tuple/`Tessellation`/`PolygonalSurface`/`Mesh` adapter contracts;
- core/OCC-to-CGAL or libigl integration;
- any framework geometry coverage beyond the package version test.

Core has no narrative terminology/strategy/metadata guide. CGAL examples teach
raw tuples; OCC lacks a focused trimmed-surface tessellation example. No
migration guide reconciles cached/computed/converted tessellations, the legacy
misspelling, raw tuples, persistent meshes, and mutation semantics.

## Regression and compatibility constraints

1. Preserve `Tessellation` buffer identity and independent conversions.
2. Keep polygon-preserving conversion distinct from triangle conversion.
3. Do not weld equal seam positions when normals or UVs differ.
4. Do not silently serialize an intentionally ephemeral result.
5. Keep per-call controls non-mutating and cache keys policy-complete.
6. State mutation, vertex insertion, source-index, and topology behavior.
7. Keep trim-aware BRep tessellation distinct from untrimmed surface sampling.
8. Do not equate counts, deflection, edge length, area, angle, cleanup
   tolerance, estimates, or guaranteed bounds.
9. Preserve orientation, holes, source boundaries, attributes, and provenance.
10. Keep topological boundaries separate from generated internal diagonals.
11. Test native dtype/layout without imposing NumPy on core types.
12. Align plugin discovery and signatures before dispatch integration.
13. Reconcile the heavily modified `compas_model` worktree before editing it.

## Architectural questions

- Should existing `Tessellation` be the lightweight triangle interchange, or
  does a compact `TriangleMesh` justify another container?
- Should output topology be independent from a serializable tessellation
  strategy?
- Which strategies are portable configuration and which describe backend
  capability? How are unsupported guarantees reported?
- Does optional metadata belong in a result envelope, operation-specific
  result objects, or the mesh itself?
- How should trim-aware surface input be represented without pretending a
  standalone `NurbsSurface` owns BRep loops?
- What are the canonical mutating/non-mutating triangulation verbs?
- What validation belongs in a shared adapter versus each operation?
- How should tuple-returning and misspelled BRep APIs migrate?

## Affected packages

- `compas`: shared terminology, strategies/results/interfaces, surface/shape/
  mesh APIs, triangulation pluggables, validation, tests, and docs.
- `compas_occ`: trim-aware BRep tessellation, deflection, provenance, caching,
  compatibility APIs, tests, and examples.
- `compas_cgal`: discovery/signatures, native coercion, algorithms,
  provenance, tests, and docs.
- `compas_libigl`: shared triangle-buffer adoption and result alignment.
- `compas_gmsh`: comparison of existing sizing controls without false
  equivalence.
- `compas_model`: overlapping Earcut and regression-sensitive downstream uses.
- `compas_framework`: cross-package fixtures, integration, native-backend,
  roundtrip, and performance coverage.
