# Title: How should operation concepts map to public conversion APIs?

## Status

Proposed.

## Context

The user-authored [`definitions.md`](../definitions.md) provides new evidence
that the accepted architecture made polygonization and tessellation too
symmetrical. In particular, ADRs 005, 006, and 014 allow every continuous
surface-like producer to expose both operations, and ADR 005 permits BReps to
polygonize when a backend can return polygons. That obscures three materially
different operations:

- structured discretization of a parameterized shape or surface;
- division of an existing discrete polygon, domain, or point set into
  triangles; and
- precision-controlled approximation of trimmed surfaces and BReps.

Typing-alignment ADRs 012 and 013 provide further accepted evidence. Numerical
backends need structural coordinate/index buffers rather than a compulsory
core representation, and named functions plus producer-owned controls are
clearer than nominal strategy objects.

This ADR reconciles those decisions before Typing ADR 015 fixes the exact
signatures. The user has selected representation-oriented public names:
continuous geometry converts with `to_polygonal_surface` and
`to_tessellation`, while the operation concepts remain polygonization and
tessellation. This ADR changes no package source while Proposed.

## Definitions

- **Discretization** is the broad process of representing continuous geometry
  with finite data.
- **Polygonization** discretizes a structured parametric `Shape` or untrimmed
  `Surface` into a `PolygonalSurface`. It preserves quadrilateral cells where
  the parameterization permits and uses triangles where the structure
  requires them, for example at a sphere pole. Resolution controls are cell
  counts, not geometric error bounds.
- **Triangulation** divides an existing polygon, collection of polygonal faces,
  planar region, or planar point/domain input into triangles. Every operation
  states whether it projects, inserts vertices, preserves source indices, and
  mutates its source.
- **Tessellation** is precision-controlled triangle approximation of trimmed
  surfaces, BRep faces, and BReps. Its controls are geometric approximation
  criteria such as linear and angular deflection, not parameter-grid counts.

The capitalized `Tessellation` remains a lightweight indexed-triangle
representation. A value of that type may be produced by either triangulation
or tessellation; the representation name does not redefine the operation that
created it.

## Options

1. **Use operation verbs as public methods.** Keep or refine `polygonize` and
   `tessellate`. This exposes the process but makes continuous geometry naming
   differ from established `to_mesh` and representation-conversion APIs.
2. **Expose only the primitive structured operation.** Shapes and untrimmed
   surfaces provide `to_polygonal_surface`; callers explicitly invoke
   `.triangulated()` afterward. This is minimal but removes the convenient
   direct conversion to the visualization-oriented `Tessellation`.
3. **Use representation-oriented conversion names with producer-specific
   availability.** Shapes and untrimmed surfaces expose both conversions;
   BReps expose only `to_tessellation`; discrete inputs keep triangulation
   verbs. The method documentation states whether polygonization or
   tessellation performs the conversion.

## Recommendation

Choose option 3.

### Shapes and untrimmed surfaces

`Shape` and untrimmed `Surface` types expose the structured polygonization
conversion:

```python
geometry.to_polygonal_surface(*, producer_specific_resolution) -> PolygonalSurface
```

Their resolution parameters are positive integer cell counts such as `nu` and
`nv`. They are supplied per operation, are not stored as defining geometry
state, and make no geometric-error guarantee.

For direct scene and transfer use, the same producers also expose:

```python
geometry.to_tessellation(*, producer_specific_resolution) -> Tessellation
```

This is not a precision-controlled tessellation operation or a second
approximation algorithm. Its vertices and triangle topology are exactly those
obtained through `to_polygonal_surface` with the same arguments and the
default no-insertion face triangulator.
Normals and texture coordinates may be attached only when one valid value
exists for every polygonized vertex in the same index order. The conversion
may not duplicate vertices or change connectivity; otherwise it omits the
attribute. Callers needing another diagonal or polygon algorithm use the
explicit two-step operation.

Standalone `NurbsSurface` remains untrimmed and follows this structured
contract over its rectangular parameter domain. Extracting it from a BRep face
continues to lose trimming information.

### BReps and trimmed faces

`Brep` and `BrepFace` expose only the precision-controlled tessellation
conversion:

```python
brep.to_tessellation(
    *,
    linear_deflection,
    angular_deflection,
) -> Tessellation
```

They do not expose `to_polygonal_surface`, `polygonize`, or `tessellate`. A
BRep has no single underlying uniform parameter-grid structure to preserve as
a `PolygonalSurface`. The public conversion performs the BRep tessellation
operation. Converting its triangle result to another representation afterward
is a separate representation conversion, not BRep polygonization.

Tessellation preserves face winding and relevant discretized boundary
polylines. Linear deflection is in model units and angular deflection has one
documented public angular unit. Whether those controls are required or have
deterministic public defaults is an independent decision in ADR 023. Exact
signatures, validation, and backend conversion belong to Typing ADR 015 after
that decision is accepted.

### Discrete geometry and planar domains

`Polygon`, `PolygonalSurface`, `Polyhedron`, and `Mesh` triangulate their
existing faces. `Mesh.triangulate` is mutating and returns `None`;
`triangulated` operations are non-mutating and return `Tessellation` where the
accepted representation contract requires it. Algorithm selection uses named
functions or a duck-typed callable, not strategy classes.

`PlanarRegion` uses its own exterior-and-holes triangulation contract. Point
and domain Delaunay operations remain explicitly planar and return structural
coordinate/triangle buffers. Projection, source-coordinate preservation, and
Steiner insertion are stated by each named operation rather than inferred from
the result type.

### Numerical and plugin boundaries

Numerical triangle-mesh operations accept one structural coordinate/index
contract. Suitable Python sequences and NumPy arrays are first-class inputs.
They do not require `Tessellation`, `PolygonalSurface`, or `Mesh`, and do not
implicitly convert among those representations. A backend normalizes once at
its native ABI boundary and performs only the minimal safety checks required
for native access plus result-shape validation.

Plugin wrappers and direct backend APIs implement the same semantic contract.
Lightweight registration modules may defer native imports, but discovery does
not change the operation terminology or input contract.

### Representations

Keep the three existing representation roles:

| Representation | Role |
|---|---|
| `Tessellation` | Ephemeral indexed-triangle result with optional same-index attributes and boundary polylines. |
| `PolygonalSurface` | Serializable lightweight polygonal geometry with arbitrary face arity. |
| `Mesh` | Serializable mutable half-edge topology with keys and attributes. |

Do not add `TriangleMesh`, `QuadMesh`, `TriangleSurface`, or a universal result
wrapper. Triangle and quad properties are structural/topological predicates,
not new nominal geometry classes.

## Resolution, deflection, and tolerance

- `nu` and `nv` are integer cell counts controlling structured polygonization.
- linear and angular deflection are approximation controls for BRep
  tessellation and state their units explicitly.
- `max_edge_length` is a triangulation refinement target only where a named
  operation supports it.
- `max_deviation` is an explicit projection acceptance bound for near-planar
  polygon triangulation.
- `TOL` is reserved for numerical predicates, degeneracy, and planarity
  comparisons. It is not a user-facing resolution or quality setting.

No control is silently mapped to a non-equivalent quantity.

## Superseded clauses if accepted

This ADR preserves useful parts of the existing decisions but supersedes the
following clauses:

| Earlier ADR | Superseded clause |
|---|---|
| 001 | Public operation verbs on continuous geometry. Polygonization and tessellation remain documented process concepts, while public continuous-geometry methods use representation-oriented `to_*` names. |
| 003 | The public `TessellationStrategy`, `Native`, `UGrid`, `UVGrid`, `Deflection`, and `Adaptive` hierarchy. Producer keywords and named operations replace it, consistent with accepted Typing ADR 013. |
| 005 | Public `polygonize`, `Brep`/`BrepFace` polygonal conversion, shared polygonization/tessellation strategies, and backend-dependent polygonization of unstructured BReps. Structured producers use `to_polygonal_surface`. |
| 006 | Public `polygonize`/`tessellate` verbs and independent shape/surface triangle connectivity. Structured producers expose both `to_*` conversions with exactly composed geometry/topology; BReps expose only `to_tessellation`. |
| 007, 017–019 | Nominal face strategy classes and their composite strategy. Their algorithmic, mutation, insertion, winding, and failure semantics remain, but selection moves to named functions and a callable aggregate boundary. |
| 008 | `Tessellation` as the compulsory input to numerical plugins. Accepted Typing ADR 012's structural buffers become authoritative. |
| 009 | Generic `NurbsSurface.tessellate(strategy)` as an independent rectangular-domain algorithm. It becomes `NurbsSurface.to_tessellation`, exactly composed from its structured `to_polygonal_surface` conversion; BRep ownership of trims remains unchanged. |
| 011, 020 | Delaunay strategy objects and `Tessellation`-only results. Named planar algorithms returning structural buffers become authoritative; planarity and insertion guarantees remain. |
| 012 | Core `Tessellation` extraction as the plugin boundary. Structural wrapper/hook parity and backend-local normalization replace it; lightweight discovery refinements remain. |
| 014 | Public operation verbs and two independent materialization paths for every continuous producer. Shape/surface conversions share one structured path; BRep `to_tessellation` directly performs tessellation. The no-cache decision remains. |
| 021 | Strategy-object defaults. Producer-owned `nu`/`nv` defaults replace Shape/Surface strategy defaults. BRep default policy is separated into ADR 023. |

ADR 002's representation decision remains unchanged. ADR 009's BRep ownership
of trims, ADR 013's clean-break policy, ADR 015's continuous bounds, and ADR
016's removal of speculative capability discovery also remain unchanged.

## Compatibility implications

- Remove public `polygonize` and `tessellate` methods rather than retaining
  aliases. Structured producers expose `to_polygonal_surface` and
  `to_tessellation`; BReps expose only `to_tessellation`.
- Remove `Brep.polygonize`, `BrepFace.polygonize`, and both old BRep operation
  hooks. The sole replacement hook is `brep_to_tessellation`.
- Remove public strategy classes, serialization, and exports without shims.
- Replace shape/surface `polygonize`/`tessellate` with the two `to_*`
  conversions under the exact shared-path contract above; `to_tessellation`
  may not select unrelated sampling or triangulation.
- Preserve `Tessellation` as a representation, but do not use it as a nominal
  gate for numerical backends.
- Coordinate the breaking change across core, OCC, CGAL, libigl, model,
  viewer, framework tests, examples, and documentation.

## Verification

- Assert exact conversion availability by producer family: both `to_*`
  conversions for shapes/untrimmed surfaces, only `to_tessellation` for
  BReps/BRepFaces, and triangulation verbs for discrete inputs/domains.
- Compare every shape/surface `to_tessellation` result with
  `to_polygonal_surface(...).triangulated()` for identical vertices and
  triangles.
- Verify sampled normals/UVs use the same vertex order without changing
  connectivity, and are omitted where seams or creases require vertex
  duplication.
- Assert that BRep polygonal conversion and old operation hooks are absent;
  `brep_to_tessellation` respects documented deflection units and boundary
  winding.
- Exercise Python and NumPy structural buffers directly through core dispatch
  and backend APIs without constructing core geometry objects.
- Assert removed strategy classes and compatibility aliases are absent from
  source exports, serialization, documentation, examples, and built packages.
- Run focused and full tests, Ruff, Pyright, strict documentation, distribution
  checks, and cross-package integration before completion is claimed.

## Affected packages

`compas`, `compas_occ`, `compas_cgal`, `compas_libigl`, `compas_model`,
`compas_viewer`, and `compas_framework`.

## Dependencies

- [001 — Terminology](001-terminology.md), revisited by new evidence
- [002 — Mesh representations](002-mesh-representations.md)
- [009 — Trimmed surfaces](009-trimmed-surfaces.md)
- Typing-alignment ADR 012 — structural triangle-mesh boundaries
- Typing-alignment ADR 013 — explicit algorithms and producer controls

## Approval boundary

This decision is **Proposed**. The representation-oriented naming choice is
recorded, but the exact conversions, BRep-only restriction, removal of public
operation verbs, and supersession of the listed strategy/input clauses still
require approval as one coherent contract. No source implementation may
proceed before then.
