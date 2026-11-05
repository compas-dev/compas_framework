# Title: What are the exact triangulation and discretization APIs?

## Status

Proposed.

## Context

Accepted ADR 013 chose named triangulation operations and producer-specific
keyword controls over public strategy hierarchies. It did not define the final
named polygon-operation table, aggregate customization contract, planar
Delaunay signatures, or exact producer defaults. WP7.4–WP7.7 cannot remove the
old strategy types without those public contracts.

This ADR refines ADR 013 rather than changing its direction. The new approval
choice is whether aggregate geometry methods accept a duck-typed triangulator
callable. All signatures and defaults below are proposed together so the
remaining migration can remove the old paths directly without compatibility
shims.

## Polygon triangulation functions

### Default operation

```python
def triangulate_polygon(vertices: CoordinatesInput) -> list[list[int]]: ...
```

The function:

- raises `ValueError` for fewer than three vertices;
- returns the input triangle topology unchanged for three vertices;
- splits a quadrilateral along its shortest diagonal;
- uses planar ear clipping for five or more vertices;
- raises `ValueError` when a polygon with five or more vertices is non-planar.

### Named alternatives

```python
def triangulate_quadrilateral(
    vertices: CoordinatesInput,
    *,
    diagonal: Literal["shortest", "02", "13"] = "shortest",
) -> list[list[int]]: ...

def triangulate_polygon_earclip(
    vertices: CoordinatesInput,
) -> list[list[int]]: ...

def triangulate_polygon_projected(
    vertices: CoordinatesInput,
    *,
    max_deviation: float,
) -> list[list[int]]: ...

def triangulate_polygon_minimum_area(
    vertices: CoordinatesInput,
) -> list[list[int]]: ...
```

`triangulate_polygon_projected` projects to a best-fit plane only within the
explicit `max_deviation` bound. `triangulate_polygon_minimum_area` accepts an
ordered non-planar 3D polygon and uses the O(n³) minimum-area triangulation.
The ear-clipping function is the explicit planar polygon operation.

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
Triangulator = Callable[[CoordinatesInput], list[list[int]]]

def triangulated(
    self,
    triangulator: Triangulator = triangulate_polygon,
) -> Tessellation: ...
```

`Polygon`, `PolygonalSurface`, `Polyhedron`, and `Mesh` expose this
`triangulated` contract. `Mesh` additionally exposes:

```python
def triangulate(
    self,
    triangulator: Triangulator = triangulate_polygon,
) -> None: ...
```

The callable keeps aggregate code independent of nominal strategy types and
allows options to be bound transparently with `functools.partial`, for example
a selected quadrilateral diagonal or projection bound.

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

The tessellation vertex buffer is flattened deterministically: exterior
vertices first, followed by every hole in stored order. Every returned triangle
indexes that flattened buffer. The operation introduces no Steiner vertices.
Triangle winding agrees with `region.plane.normal` regardless of the winding of
individual hole rings. Both conversion methods delegate to `triangulated` so
they preserve the same vertex mapping and topology.

Users who need constrained or conforming refinement call the named planar
domain functions directly with the region exterior and holes. Region
triangulation rejects invalid, touching, or intersecting rings rather than
silently repairing them.

## Planar Delaunay functions

```python
def delaunay_triangulation(
    points: CoordinatesInput,
    *,
    frame: Frame | None = None,
) -> TriangleMeshInput: ...

def constrained_delaunay_triangulation(
    boundary: CoordinatesInput,
    *,
    holes: CoordinatesCollectionInput = (),
    constraints: CoordinatesCollectionInput = (),
    points: CoordinatesInput = (),
    frame: Frame | None = None,
) -> TriangleMeshInput: ...

def conforming_delaunay_triangulation(
    boundary: CoordinatesInput,
    *,
    holes: CoordinatesCollectionInput = (),
    constraints: CoordinatesCollectionInput = (),
    points: CoordinatesInput = (),
    max_edge_length: float | None = None,
    frame: Frame | None = None,
) -> TriangleMeshInput: ...
```

The matching private hooks are `_delaunay_triangulation`,
`_constrained_delaunay_triangulation`, and
`_conforming_delaunay_triangulation` with the same parameters and result
contract.

Inputs are planar within `TOL`. With `frame=None`, the domain is interpreted in
world XY. An explicit frame defines the planar domain. The operations do not
project curved inputs, return raw structural vertex/triangle buffers, and
preserve accepted source coordinates. `max_edge_length`, when provided, is
positive and finite. No `min_angle` or `max_area` control is introduced.

The result is a concrete `(coordinates, triangles)` structural tuple, not a
`Tessellation`. Every triangle contains three distinct in-range integer indices,
has nonzero signed area in frame coordinates, and is counterclockwise in frame
XY. Its winding therefore agrees with the frame normal, or world +Z when no
frame is provided.

Every distinct accepted source location appears in the result with its original
3D coordinate. Repeated shared endpoints coalesce. Conflicting 3D coordinates
at the same planar location are rejected. Result vertex order is unspecified.
Unconstrained Delaunay and valid nonintersecting constrained Delaunay introduce
no Steiner vertices. Conforming Delaunay may introduce planar Steiner vertices.

Boundary and hole rings are simple and mutually disjoint. Constraints remain
inside the domain and may meet only at shared endpoints. Crossings and
unsupported touching configurations are rejected. No operation mutates Python
or NumPy source buffers.

## Shape and surface discretization

Both `polygonize` and `tessellate` use the following keyword-only controls:

| Producer | Signature | Validation and result behavior |
|---|---|---|
| `Box` | `polygonize()` / `tessellate()` | No controls. |
| `Cone`, `Cylinder` | `(*, nu: int = 64)` | `nu >= 3`. |
| `Sphere`, `Torus` | `(*, nu: int = 64, nv: int = 64)` | `nu >= 3`, `nv >= 3`. |
| `Capsule` | `(*, nu: int = 64, nv: int = 64)` | `nu >= 3`; `nv >= 4` and even. |
| `Surface` | `(*, nu: int = 64, nv: int = 64)` | Both counts >= 1. `polygonize` returns quads; `tessellate` returns two triangles per grid cell with normals and UV coordinates. |

No generic `Adaptive` replacement is introduced. A no-argument call remains
available for generic visualization conversion through the documented
producer defaults.

For a `Surface` grid, vertices, normals, and UV coordinates each contain
`(nu + 1) * (nv + 1)` items. Buffers use lexicographic `(u, v)` order with `v`
varying fastest. UV coordinates are `[i / nu, j / nv]`; periodic seams retain
separate 0 and 1 endpoint samples. Each cell with corners `a, b, c, d` yields
triangles `[a, b, c]` and `[a, c, d]` in increasing parameter directions.
At regular samples, analytic normals and triangle winding agree with
`du × dv`.

Singular parameter cells may remain in the output. The implementation does not
silently delete or reindex them, so universal triangle nondegeneracy is not a
surface-grid guarantee. This limitation is documented rather than hidden by a
topology-changing cleanup.

## BRep discretization

Public `Brep` methods accept optional controls:

```python
def tessellate(
    *,
    linear_deflection: float | None = None,
    angular_deflection: float | None = None,
) -> Tessellation: ...

def polygonize(
    *,
    linear_deflection: float | None = None,
    angular_deflection: float | None = None,
) -> PolygonalSurface: ...
```

`BrepFace` exposes the same public signatures and delegates through `as_brep`.
Public methods resolve `None` before plugin dispatch: linear deflection uses
`TOL.lineardeflection`, and angular deflection uses the degree equivalent of
`TOL.angulardeflection`.

The plugin hooks receive the BRep positionally and concrete required keyword
arguments:

```python
def brep_tessellate(
    brep: Brep,
    *,
    linear_deflection: float,
    angular_deflection: float,
) -> Tessellation: ...

def brep_polygonize(
    brep: Brep,
    *,
    linear_deflection: float,
    angular_deflection: float,
) -> PolygonalSurface: ...
```

Plugin hooks do not accept or resolve `None`. Linear deflection is in model
units; angular deflection is in degrees. Public resolution and explicit values
use the same validation: booleans and non-real values raise `TypeError`;
non-finite or non-positive values raise `ValueError`; angular values greater
than 180 raise `ValueError`. OCC converts degrees to radians exactly once at
the native boundary. Core and OCC wrappers keep these exact shapes.
`polygonize` uses the same tessellation controls and retains the established
boundary-polyline behavior.

## Direct removal and migration

The following are removed directly, without aliases, adapters, deprecation
shims, or duplicate public paths:

- `TriangulationStrategy`, `FaceTriangulation`, `DiagonalSplit`,
  `EarClipping`, `ProjectedEarClipping`, and `MinimumAreaTriangulation`;
- `_PlanarTriangulationStrategy`, `Delaunay`, `ConstrainedDelaunay`,
  `ConformingDelaunay`, and `TriangulationQuality`;
- strategy-selected `triangulate_planar_*` functions and private hooks;
- `TessellationStrategy`, `Native`, `UGrid`, `UVGrid`, `Adaptive`, and
  `Deflection`;
- strategy serialization, exports, documentation, and examples;
- generic `Shape` strategy handling and `_tessellation_strategy`.

| Removed path | Replacement |
|---|---|
| Polygon strategy object | Named polygon function or aggregate callable. |
| Delaunay strategy flag | Matching named Delaunay function. |
| `TriangulationQuality` | `max_edge_length` on conforming Delaunay only. |
| Shape/surface tessellation strategy | Producer-owned `nu`/`nv` keywords. |
| BRep `Deflection` | Linear and angular deflection keywords. |
| Strategy serialization and exports | No replacement; the public strategy types are removed. |

## Verification

- Assert exact public and plugin signatures, defaults, and keyword-only
  controls.
- Cover Python and NumPy coordinate inputs and source non-mutation.
- Verify polygon triangle counts, index bounds and distinctness, source-only
  references, nonzero areas, winding, reversed boundaries, warped quads,
  degeneracy rejection, and minimum-area cyclic orientation.
- Verify aggregate face-to-triangle mapping and preservation of attributes.
- Verify callable customization, including `functools.partial` for
  algorithm-specific options.
- Verify no-argument `PlanarRegion` triangulation, either hole winding,
  exterior-then-holes flattening, region-normal winding, no Steiner vertices,
  invalid/touching/intersecting ring rejection, and conversion delegation.
- Verify Delaunay result shape and bounds, signed nonzero frame area,
  counterclockwise winding, reversed boundaries, rotated frames, shared-point
  coalescing, conflicting-coordinate rejection, source-coordinate retention,
  no Steiner vertices for unconstrained/constrained operations, permitted
  Steiner vertices for conforming operations, crossing rejection, and Python
  and NumPy source non-mutation.
- Verify producer triangle/quad counts, minimum resolutions, generic
  no-argument conversion, surface buffer lengths and ordering, UV endpoints,
  two-triangle cell indices, analytic-normal/winding agreement, and the
  documented singular-cell behavior.
- Inspect exact public BRep, `BrepFace`, and plugin-hook signatures. Verify
  hooks reject `None`; explicit and tolerance-derived validation rejects
  `NaN`, infinity, booleans, zero, negative values, and angles above 180;
  verify `TOL.temporary` defaults, degrees-to-radians conversion exactly once,
  `BrepFace` delegation, plugin parity, and retained boundary polylines.
- Assert removed symbols are absent from source exports, serialization,
  examples, documentation, typed fixtures, and built packages.
- Run focused and full feasible tests, Ruff, formatting, Pyright, strict docs,
  distribution checks, and cross-package integration.

## Consequences

- Users select algorithms by calling them rather than constructing nominal
  flags.
- Aggregate customization follows Python duck typing through a callable.
- Each producer exposes only controls it can implement truthfully.
- Delaunay remains planar and returns structural buffers.
- Angular BRep controls have one public unit: degrees.
- The C3 branch makes a clean break; migration is direct and no compatibility
  layer remains.

## Affected packages

`compas`, `compas_cgal`, `compas_occ`, `compas_framework`, documentation,
examples, serialization fixtures, plugin fixtures, and installed consumers.

## Dependencies

- [012 — Structural triangle-mesh boundaries](012-structural-triangle-mesh-boundaries.md)
- [013 — Explicit algorithms and discretization controls](013-explicit-algorithms-and-discretization-controls.md)

## Approval boundary

All signatures, defaults, validation rules, removals, and the aggregate
triangulator callable remain **Proposed**. WP7.4–WP7.7 implementation is
blocked until the user explicitly approves this exact table. In particular,
the callable aggregate contract is a new choice not settled by ADR 013.
