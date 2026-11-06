# Title: What are the exact triangulation and discretization APIs?

## Status

Accepted.

## Context

Accepted ADR 013 chose named algorithms and producer-specific keyword controls
over public strategy hierarchies. Accepted Geometry-tessellation ADR 022 was
introduced in response to the user-authored operation definitions and
distinguishes
structured polygonization, discrete triangulation, and precision-controlled
BRep tessellation.

This ADR supplies the exact signatures and invariants needed by WP7.4–WP7.7.
It depends on accepted Geometry ADRs 022–023 and Typing ADR 016. If any of
those decisions changes, this table must be reconciled before the affected
implementation changes.

Accepted Geometry ADR 024 makes one such amendment:
`Mesh.triangulated(...) -> Self` while the other aggregate return contracts
remain `Tessellation`. This ADR's shared aggregate return clause is superseded
for `Mesh` only; its other aggregate contracts remain unchanged.

## Polygon triangulation functions

### Default operation

```python
def triangulate_polygon(vertices: PointsLike) -> list[list[int]]: ...
```

The function:

- raises `ValueError` for fewer than three vertices;
- returns the input triangle topology unchanged for three vertices;
- splits a quadrilateral along its shortest diagonal;
- uses planar ear clipping for five or more vertices; and
- raises `ValueError` when a polygon with five or more vertices is non-planar.

### Named alternatives

```python
def triangulate_quadrilateral(
    vertices: PointsLike,
    *,
    diagonal: Literal["shortest", "02", "13"] = "shortest",
) -> list[list[int]]: ...

def triangulate_polygon_earclip(
    vertices: PointsLike,
) -> list[list[int]]: ...

def triangulate_polygon_projected(
    vertices: PointsLike,
    *,
    max_deviation: float,
) -> list[list[int]]: ...

def triangulate_polygon_minimum_area(
    vertices: PointsLike,
) -> list[list[int]]: ...
```

`triangulate_polygon_projected` projects to a best-fit plane only within the
explicit positive finite `max_deviation` bound.
`triangulate_polygon_minimum_area` accepts an ordered non-planar 3D polygon and
uses the O(n³) minimum-area triangulation. The ear-clipping function is the
explicit planar polygon operation. Delaunay processing of a concave boundary
uses the named constrained planar-domain operation below rather than an
implicit face-triangulation fallback.

### Polygon result invariants

For a valid polygon with `n` vertices, every polygon triangulator:

- does not mutate or reorder the source coordinates and introduces no new
  vertices;
- returns exactly `n - 2` triangles;
- returns three distinct integer indices in `[0, n)` for every triangle;
- references only source vertices; and
- produces triangles with nonzero area within `TOL`.

Invalid or degenerate input raises instead of returning partial topology.
Planar and projected triangulations wind triangles consistently with the
ordered boundary in the working plane. Reversing the boundary reverses that
winding. Minimum-area triangulation preserves cyclic source-index orientation,
but makes no global-normal promise for a non-planar polygon.

Ear clipping rejects non-simple polygons, repeated vertices, zero-length
edges, zero-area boundaries, and non-planarity. Projected triangulation applies
the same checks after projection within the deviation bound. Region
triangulation applies the corresponding checks to its exterior and holes. A
simple warped quadrilateral is supported, provided both triangles selected by
the requested diagonal are nondegenerate.

## Aggregate customization

### Options

1. Do not expose aggregate customization; always use `triangulate_polygon`.
2. Add a `Literal` method switch to every aggregate.
3. Add multiple aggregate methods for every named algorithm.
4. Retain the strategy hierarchy.
5. Accept a duck-typed triangulator callable.

### Recommendation

Choose option 5:

```python
Triangulator = Callable[[PointsLike], list[list[int]]]

def triangulated(
    self,
    triangulator: Triangulator | None = None,
) -> Tessellation: ...
```

`Polygon`, `PolygonalSurface`, `Polyhedron`, and `Mesh` expose this
`triangulated` contract. `Mesh` additionally exposes:

```python
def triangulate(
    self,
    triangulator: Triangulator | None = None,
) -> None: ...
```

An omitted selector and an explicit `None` both resolve to
`triangulate_polygon`. This keeps the normal aggregate call concise and lets
callers forward an optional selector without substituting the default
themselves. A provided callable remains the sole customization mechanism; the
removed nominal strategy classes are not accepted.

The callable keeps aggregate code independent of nominal strategy types and
allows algorithm-specific options to be bound transparently with
`functools.partial`. An aggregate stages all face results before mutating a
`Mesh`. Generated faces inherit source face attributes; vertex keys are
preserved, while generated face keys are not promised.

Alternatives 1–4 are not recommended: no customization is unnecessarily
closed; a literal cannot express algorithm-specific options; multiple
aggregate methods duplicate APIs; and strategies preserve the abstraction
being removed.

## Planar region triangulation and conversion

`PlanarRegion` deliberately does not expose the aggregate triangulator
callable. Its exterior-and-holes contract has one no-insertion operation:

```python
def triangulated(self) -> Tessellation: ...
def to_polygonal_surface(self) -> PolygonalSurface: ...
def to_mesh(self) -> Mesh: ...
```

The latter two are representation conversions, not polygonization operations.
The tessellation vertex buffer is flattened deterministically: exterior
vertices first, followed by every hole in stored order. Every returned triangle
indexes that flattened buffer. The operation introduces no Steiner vertices.
Triangle winding agrees with `region.plane.normal` regardless of the winding
of individual hole rings. Both conversions delegate to `triangulated` so they
preserve the same vertex mapping and topology.

Users who need constrained or conforming refinement call the named planar
domain functions directly. Region triangulation rejects invalid, touching, or
intersecting rings rather than silently repairing them.

## Named planar Delaunay functions

```python
def delaunay_triangulation(
    points: PointsLike,
    *,
    frame: Frame | None = None,
) -> VerticesFaces: ...

def constrained_delaunay_triangulation(
    boundary: PointsLike,
    *,
    holes: PointGroupsLike = (),
    constraints: PointGroupsLike = (),
    points: PointsLike = (),
    frame: Frame | None = None,
) -> VerticesFaces: ...

def conforming_delaunay_triangulation(
    boundary: PointsLike,
    *,
    holes: PointGroupsLike = (),
    constraints: PointGroupsLike = (),
    points: PointsLike = (),
    max_edge_length: float | None = None,
    frame: Frame | None = None,
) -> VerticesFaces: ...
```

The matching private hooks are `_delaunay_triangulation`,
`_constrained_delaunay_triangulation`, and
`_conforming_delaunay_triangulation` with identical parameters and result
contracts.

Inputs are planar within `TOL`. With `frame=None`, the domain is interpreted in
world XY. An explicit frame defines the planar domain. The operations do not
project curved inputs, return raw structural vertex/triangle buffers, and
preserve accepted source coordinates. `max_edge_length`, when provided, is
positive and finite. No `min_angle` or `max_area` control is introduced.

The result is a concrete `(coordinates, triangles)` structural tuple, not a
`Tessellation`. Every triangle contains three distinct in-range integer
indices, has nonzero signed area in frame coordinates, and is counterclockwise
in frame XY. Its winding therefore agrees with the frame normal, or world +Z
when no frame is provided.

Every distinct accepted source location appears in the result with its
original 3D coordinate. Repeated shared endpoints coalesce. Conflicting 3D
coordinates at the same planar location are rejected. Result vertex order is
unspecified. Unconstrained Delaunay and valid nonintersecting constrained
Delaunay introduce no Steiner vertices. Conforming Delaunay may introduce
planar Steiner vertices.

Boundary and hole rings are simple and mutually disjoint. Constraints remain
inside the domain and may meet only at shared endpoints. Crossings and
unsupported touching configurations are rejected. No operation mutates Python
or NumPy source buffers.

## Structured shape and surface conversions

`Shape` and untrimmed `Surface` types expose `to_polygonal_surface` as the
conversion backed by structured polygonization:

| Producer | Exact signature | Validation and polygonal result |
|---|---|---|
| `Box` | `to_polygonal_surface()` | No controls; six quadrilateral faces. |
| `Cone`, `Cylinder` | `to_polygonal_surface(*, nu: int = 64)` | `nu >= 3`; structured side cells and required cap/pole triangles. |
| `Sphere` | `to_polygonal_surface(*, nu: int = 64, nv: int = 64)` | `nu >= 3`, `nv >= 3`; quads where regular and required pole triangles. |
| `Torus` | `to_polygonal_surface(*, nu: int = 64, nv: int = 64)` | `nu >= 3`, `nv >= 3`; a periodic quadrilateral grid. |
| `Capsule` | `to_polygonal_surface(*, nu: int = 64, nv: int = 64)` | `nu >= 3`; `nv >= 4` and even; quads where regular and required pole triangles. |
| untrimmed `Surface` | `to_polygonal_surface(*, nu: int = 64, nv: int = 64)` | Both counts `>= 1`; `(nu + 1) * (nv + 1)` vertices and `nu * nv` quads. |

Counts are cell resolution, not approximation-error targets. Booleans and
non-integral values raise `TypeError`; values below the stated minima raise
`ValueError`. No generic adaptive control is introduced.

For a `Surface` grid, vertices use lexicographic `(u, v)` order with `v`
varying fastest. Periodic seams retain separate endpoint samples. Cell corners
`a, b, c, d` follow increasing parameter directions. Analytic normals follow
`du × dv`; arbitrary coarse chord faces do not have a universal orientation
guarantee relative to those normals on curved or folded cells.

Singular cells may remain. The conversion does not silently delete or reindex
them, so universal face nondegeneracy is not guaranteed at parameter
singularities. This limitation is documented rather than hidden by a
topology-changing cleanup.

## Shape and surface triangle conversion

The same producers expose `to_tessellation` for visualization and transfer,
with signatures identical to their `to_polygonal_surface` calls:

```python
shape.to_tessellation(*, same_resolution_keywords) -> Tessellation
surface.to_tessellation(*, nu: int = 64, nv: int = 64) -> Tessellation
```

This is an exact composition, not an independent approximation algorithm:

```python
geometry.to_tessellation(**options)
# has the same vertices and triangles as
geometry.to_polygonal_surface(**options).triangulated()
```

Every polygonal face uses the default `triangulate_polygon` policy. The
conversion inserts no vertices beyond the structured polygonization and may
not choose a backend-specific alternative. A caller needing another policy
uses `to_polygonal_surface(...).triangulated(custom_callable)`.

For `Surface`, the result may additionally carry analytic vertex normals and UV
coordinates sampled in the same vertex order. UV coordinates are
`[i / nu, j / nv]`. Analytic normals follow `du × dv`; no universal agreement
between those normals and coarse chord-triangle winding is promised for an
arbitrary curved or folded surface. Attributes are attached only when one
valid same-index value exists per polygonized vertex. The conversion never
duplicates vertices to manufacture seam or crease attributes.

## BRep tessellation conversion

`Brep` and `BrepFace` do not expose a polygonal-surface conversion. They expose
only the representation-oriented method backed by BRep tessellation:

```python
def to_tessellation(
    self,
    *,
    linear_deflection: float | None = None,
    angular_deflection: float | None = None,
) -> Tessellation: ...
```

`BrepFace.to_tessellation` delegates through `as_brep`. Public methods resolve
`None` before plugin dispatch: linear deflection uses
`TOL.lineardeflection`, and angular deflection uses the degree equivalent of
`TOL.angulardeflection`.

The plugin hook receives the BRep positionally and concrete required keyword
arguments:

```python
def brep_to_tessellation(
    brep: Brep,
    *,
    linear_deflection: float,
    angular_deflection: float,
) -> Tessellation: ...
```

The hook does not accept or resolve `None`. Linear deflection is in model
units; angular deflection is in degrees. Public resolution and explicit values
use the same validation: booleans and non-real values raise `TypeError`;
non-finite or non-positive values raise `ValueError`; angular values greater
than 180 raise `ValueError`. OCC converts degrees to radians exactly once at
the native boundary. Tessellation preserves face winding and relevant boundary
polylines.

There is no `Brep.to_polygonal_surface` or
`BrepFace.to_polygonal_surface`. The old `brep_tessellate` and
`brep_polygonize` hooks are removed; `brep_to_tessellation` is the sole BRep
conversion hook. Converting its result to a `PolygonalSurface` afterward is a
separate representation conversion and does not claim structured BRep
polygonization.

## Numerical triangle-mesh boundaries

Numerical mesh operations use the structural contract accepted in ADR 012:

```python
VerticesFaces = tuple[PointsLike, IndexGroupsLike]
```

They accept suitable Python sequences and NumPy buffers directly and return
shape-checked structural buffers. They do not require or implicitly convert
`Tessellation`, `PolygonalSurface`, or `Mesh`. Backend normalization occurs
once at the native ABI boundary with only the minimal safety checks required
for native access and operation-specific result validation.

## Direct removal and migration

Remove the following without aliases, adapters, deprecation shims, or duplicate
public paths:

- `TriangulationStrategy`, `FaceTriangulation`, `DiagonalSplit`,
  `EarClipping`, `ProjectedEarClipping`, and `MinimumAreaTriangulation`;
- `_PlanarTriangulationStrategy`, `Delaunay`, `ConstrainedDelaunay`,
  `ConformingDelaunay`, and `TriangulationQuality`;
- strategy-selected `triangulate_planar_*` functions and private hooks;
- `TessellationStrategy`, `Native`, `UGrid`, `UVGrid`, `Adaptive`, and
  `Deflection`;
- strategy serialization, exports, documentation, and examples;
- generic `Shape` strategy handling and `_tessellation_strategy`; and
- public `polygonize`/`tessellate` methods, BRep/BRepFace polygonal-surface
  conversion, and the old `brep_polygonize`/`brep_tessellate` hooks.

| Removed path | Replacement |
|---|---|
| Polygon strategy object | Named polygon function or aggregate callable. |
| Delaunay strategy flag | Matching named planar Delaunay function. |
| `TriangulationQuality` | `max_edge_length` on conforming Delaunay only. |
| Shape/surface policy strategy | Producer-owned `to_polygonal_surface` and `to_tessellation` `nu`/`nv` keywords. |
| BRep `Deflection` | Linear and angular `to_tessellation` keywords. |
| Shape/surface `polygonize`/`tessellate` | Representation-oriented `to_polygonal_surface`/`to_tessellation`. |
| BRep polygonization | No direct conversion; explicitly convert the resulting `Tessellation` if needed. |
| `brep_polygonize`/`brep_tessellate` | Sole `brep_to_tessellation` hook. |
| Strategy serialization and exports | No replacement. |

## Verification

- Assert exact public and plugin signatures, defaults, keyword-only controls,
  and producer-family operation availability.
- Cover Python and NumPy coordinate inputs and source non-mutation.
- Verify polygon triangle counts, index bounds and distinctness, source-only
  references, nonzero areas, winding, reversed boundaries, warped quads,
  degeneracy rejection, and minimum-area cyclic orientation.
- Verify aggregate face mapping, atomic mutation, attribute transfer, omitted
  and explicit-`None` default equivalence, and callable customization including
  `functools.partial`.
- Verify no-argument `PlanarRegion` triangulation, either hole winding,
  exterior-then-holes flattening, region-normal winding, no Steiner vertices,
  invalid ring rejection, and conversion delegation.
- Verify Delaunay result shapes, signed frame area, winding, rotated frames,
  source-coordinate retention, coalescing/rejection rules, allowed Steiner
  insertion, crossing rejection, and input non-mutation.
- Verify polygonal cell counts and order for every producer. Compare direct
  shape/surface `to_tessellation` against
  `to_polygonal_surface(...).triangulated()` for identical vertices and
  triangles, including singular-cell behavior.
- Verify Surface normals and UVs use the same vertex order without affecting
  topology, document that chord-triangle orientation may differ from analytic
  normals on folded/coarsely sampled cells, and omit attributes that require
  vertex duplication.
- Assert BRep polygonal conversion and old operation hooks are absent. Verify
  exact `brep_to_tessellation` parity, BRep deflection defaults, validation,
  degree-to-radian conversion exactly once, face delegation, winding, and
  boundary polylines.
- Exercise structural numerical operations directly with Python and NumPy
  buffers without core geometry-object construction.
- Assert removed symbols are absent from exports, serialization, examples,
  documentation, typed fixtures, and built packages.
- Run focused and full feasible tests, Ruff, formatting, Pyright, strict docs,
  distribution checks, and cross-package integration.

## Consequences

- Operation names follow the geometry being processed rather than the desired
  face arity alone.
- Structured producers have one primary discretization path and one exact
  triangle representation conversion.
- BRep `to_tessellation` has a precision-controlled tessellation contract and
  no misleading polygonal-surface twin.
- Aggregate customization follows Python duck typing.
- Delaunay remains planar and structural at numerical boundaries.
- The C3 branch makes a direct clean break without compatibility layers.

## Affected packages

`compas`, `compas_cgal`, `compas_occ`, `compas_model`, `compas_viewer`,
`compas_framework`, documentation, examples, serialization fixtures, plugin
fixtures, and installed consumers.

## Dependencies

- [012 — Structural triangle-mesh boundaries](012-structural-triangle-mesh-boundaries.md)
- [013 — Explicit algorithms and discretization controls](013-explicit-algorithms-and-discretization-controls.md)
- [016 — Core structural type vocabulary](016-core-structural-type-vocabulary.md)
- Geometry-tessellation ADR 022 — operation terminology and producer boundaries
- Geometry-tessellation ADR 023 — BRep deflection defaults

## Decision

Approved on 2026-11-05 together with Geometry ADRs 022–023 and Typing ADRs
016–017. The accepted contract uses named planar algorithms, duck-typed
aggregate triangulators, producer-specific conversion controls, raw structural
numerical boundaries, and one BRep tessellation hook. The rationale is to keep
the public API explicit and composable without nominal strategy objects or
mandatory core representation wrappers.

On 2026-11-06, the aggregate selector contract was clarified by explicit user
direction: omitted and explicit `None` selectors both mean the default
`triangulate_polygon` operation. This does not restore the removed strategy
hierarchy or add a second customization path.
