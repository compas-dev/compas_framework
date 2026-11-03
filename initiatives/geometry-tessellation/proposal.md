# Geometry Discretization, Tessellation, and Triangulation Proposal

Status: historical proposal; superseded by the Accepted ADRs

ADR 016 removes the proposal's runtime capability-discovery and reserved
error-schema APIs. Producers validate explicit strategies directly. This file
is retained as design history and is not implementation authority where it
differs from the Accepted ADRs.

This proposal is based on the restarted objective and inventory. It changes no
package source and makes no claim that tests were run.

## Decision summary

Adopt an evolutionary architecture with stable representation roles:

1. Keep `Mesh` as the rich persistent topological datastructure,
   `PolygonalSurface` as the lightweight persistent polygon buffer, and
   `Tessellation` as the ephemeral indexed-triangle result.
2. Do not add persistent `TriangleMesh` or `QuadMesh` classes. Add explicit
   triangle/quad validation and conversion capabilities instead.
3. Do not add a synonymous `TessellationResult` as the default result. Add an
   optional, operation-specific metadata envelope only where provenance or
   measured error is actually requested or produced.
4. Standardize continuous geometry on fresh
   `compute_tessellation(strategy=...) -> Tessellation` plus cached
   `.tessellation` for the default strategy. Preserve polygon-topology
   conversion through existing `compute_mesh`/`to_polygonal_surface` APIs.
5. Keep output topology separate from sampling policy, but do not make one
   method return unrelated types. Triangle output is the canonical
   tessellation interchange; a quad/polygon grid is requested through an
   explicit polygonal conversion and can then be triangulated.
6. Add lightweight serializable strategy configuration objects. Initially
   support uniform parameter resolution and backend deflection. Define an
   adaptive/error request contract, but implement it only for producers that
   can state whether the requested threshold is estimated or guaranteed.
7. Add canonical non-mutating `triangulated(...)` and mutating
   `triangulate(...)` operations to polygonal/topological representations,
   following COMPAS naming conventions. Do not silently replace existing
   triangulation policies.
8. Add `to_triangle_mesh(...) -> Tessellation` as the common conversion for
   supported continuous and discrete geometry, backed by a central adapter for
   tuple, `Tessellation`, `PolygonalSurface`, and `Mesh` inputs.
9. Keep trim-aware NURBS tessellation owned by a trimmed face/BRep, not by a
   standalone `NurbsSurface`. The result may optionally record face/trim
   provenance.
10. Align plugin discovery, signatures, coercion, and validation before using
    the common interface in CGAL/libigl integration tests.

## Normative terminology

- **Sampling** evaluates points on continuous geometry. It makes no statement
  about connectivity.
- **Discretization** represents continuous geometry by finite samples such as
  points, polylines, or parameter grids.
- **Tessellation** approximates a continuous surface or trimmed boundary by
  connected polygonal cells. The canonical computational interchange in this
  proposal is triangular.
- **Triangulation** partitions an existing polygonal face/domain or point set
  into triangles. It must state whether it preserves input vertices, inserts
  vertices, projects to a plane, and mutates the source.
- **Refinement** increases resolution of an existing discretization while
  preserving its intended source relationship.
- **Remeshing** reconstructs or modifies an existing mesh discretization to
  satisfy quality goals.
- **Simplification** reduces mesh complexity.
- **Resolution** is a sample/cell count. It is not an error bound.
- **Deflection** is a kernel-specific distance or angular approximation
  control.
- **Quality constraint** is a requested mesh property such as maximum edge
  length, maximum area, or minimum angle.
- **Tolerance** is reserved for numerical comparison, cleanup, and validity;
  it is not a generic name for the preceding controls.
- **Estimated error** is measured or inferred after/between samples and may
  miss unsampled extrema.
- **Guaranteed bound** is a backend/algorithm contract that the produced
  approximation does not exceed a stated error under documented assumptions.

Documentation and types must never label a request as a guaranteed bound when
the backend only uses it as a heuristic target.

## Representation decisions

### Keep the three existing roles

| Representation | Role | Persistence | Face arity | Topology |
|---|---|---:|---|---|
| `Tessellation` | Computation/rendering interchange | Ephemeral | Triangles | Indexed buffers |
| `PolygonalSurface` | Lightweight polygon geometry | Serializable | Arbitrary | Derived queries |
| `Mesh` | Rich editable datastructure | Serializable | Arbitrary | Half-edge |

This division is useful rather than accidental. Native plugins need compact
buffers, persistent geometry needs serialization, and editing algorithms need
topology and attributes.

### `TriangleMesh` alternatives

**A. Persistent subclass/sibling of `Mesh`.** Face arity becomes explicit and
triangle-specific methods have an obvious home. The cost is a parallel mesh
hierarchy, duplicated serialization/topology behavior, conversion churn, and
unclear ownership of attributes and keys.

**B. New compact serializable buffer class.** This fits native plugins but
substantially overlaps `Tessellation` and `PolygonalSurface`; it also needs
buffer ownership, validation, attributes, and provenance decisions.

**C. Type/capability over existing representations (recommended).** Define an
accepted-input union/protocol plus validation and conversion. Triangle arity is
enforced at the adapter/operation boundary, while persistence remains an
orthogonal concern.

Decision: do not introduce `TriangleMesh` in this initiative. Reconsider only
if a later use case requires a persistent fixed-arity object with semantics
that cannot be expressed by `Mesh`, `PolygonalSurface`, or `Tessellation`.

### `QuadMesh` alternatives

A dedicated quad class makes arity explicit but does not represent mixed
triangle/quad shapes, trimmed domains, poles, or BRep output. `Mesh.is_quadmesh`
already classifies rich topology, and `PolygonalSurface` stores quad buffers.

Decision: do not add `QuadMesh`. Add quad validation/capabilities and explicit
polygonal conversion where useful.

### `TessellationResult` alternatives

**A. Replace `Tessellation`.** Rejected: the existing public class already has
the intended ephemeral role and tested zero-copy semantics.

**B. Always wrap every result.** Rejected: simple conversion callers would pay
an extra conceptual/container cost, and plugins would still need the triangle
buffers inside it.

**C. Optional metadata envelope (recommended).** Keep `Tessellation` as the
simple result. Operations that produce provenance/error data may return or
expose a named operation-specific result containing a `tessellation` plus
metadata. Do not add all possible metadata fields to `Tessellation`.

Illustrative, not final, shape:

```python
@dataclass(frozen=True, slots=True)
class SurfaceTessellationResult:
    tessellation: Tessellation
    strategy: TessellationStrategy
    provenance: TessellationProvenance | None = None
    error: ApproximationError | None = None
```

Such result objects should be serializable only if every contained field has a
stable data contract. Native buffer identity and source-object references must
not be serialized implicitly.

## Strategy model

### Principles

- Strategies are immutable, lightweight `Data` configurations.
- They describe requested policy, not executable geometry algorithms.
- Producers own the implementation and declare supported strategies.
- Unsupported strategies fail explicitly; they are never silently ignored or
  approximately mapped to a different quantity.
- Strategy equality/hashing supports complete cache keys.
- `None` selects the producer's documented default strategy.
- Passing both a strategy and legacy scalar controls is an error after initial
  compatibility normalization.

### Initial strategies

Names are provisional public API decisions:

```python
class TessellationStrategy(Data):
    pass


@dataclass(frozen=True)
class UVGrid(TessellationStrategy):
    nu: int
    nv: int
    domain_u: tuple[float, float] | None = None
    domain_v: tuple[float, float] | None = None


@dataclass(frozen=True)
class Deflection(TessellationStrategy):
    linear: float
    angular: float
    relative: bool = False


@dataclass(frozen=True)
class Adaptive(TessellationStrategy):
    max_deviation: float | None = None
    max_normal_angle: float | None = None
    max_edge_length: float | None = None
    max_depth: int | None = None
```

Validation requires positive finite values and documented angular units.
`0.0` must never mean “use default.” `Adaptive` is a request vocabulary, not a
promise that core immediately implements a robust adaptive algorithm.

### Capability and guarantees

Each producer documents a support record conceptually equivalent to:

```python
TessellationCapability(
    strategy_type=Adaptive,
    supported_fields={"max_deviation", "max_normal_angle"},
    error_contract="estimated",  # "target", "estimated", or "guaranteed"
)
```

This need not be a public registry in the first implementation. A small helper
or documented class-level declaration is sufficient if it supports clear
errors and documentation generation.

- Core parametric surfaces initially support `UVGrid` with exact count
  semantics and no geometric error claim.
- Analytical shapes support `UVGrid`, documenting ignored/constrained axes.
- OCC BReps support `Deflection`, with guarantee wording matching OpenCASCADE's
  actual contract. Wrapper-side measured error must be reported separately.
- CGAL planar refinement supports only the quality fields actually wired to the
  native implementation.
- `Adaptive` implementation is a separate approved slice. Until implemented,
  a producer rejects it rather than falling back to `UVGrid`.

### Output topology is separate

Sampling/refinement policy and cell topology are conceptually independent, but
one method should not return different unrelated types. Therefore:

- `compute_tessellation(strategy=...)` and `to_triangle_mesh(...)` produce
  triangle `Tessellation`.
- An explicit polygonal conversion, provisionally
  `compute_polygonal_surface(strategy=...) -> PolygonalSurface`, preserves a
  producer's natural quad/mixed cells where supported.
- Triangle generation from polygonal cells accepts a separate triangulation
  strategy.

This preserves predictable return types. A future generic topology request can
be added only if one common result representation is approved.

## Public operation and conversion model

### Continuous geometry

Canonical lifecycle:

```python
surface.compute_tessellation(
    strategy: TessellationStrategy | None = None,
    *,
    triangulation: TriangulationStrategy | None = None,
    include_normals: bool = True,
    include_texture_coordinates: bool = True,
) -> Tessellation

surface.tessellation  # cached result for default strategy/options

surface.to_triangle_mesh(...) -> Tessellation
surface.compute_polygonal_surface(strategy=...) -> PolygonalSurface
surface.to_mesh(...) -> Mesh
```

`compute_tessellation` emphasizes a fresh approximation operation;
`to_triangle_mesh` emphasizes obtaining a representation and may internally
tessellate or triangulate. For continuous geometry they may share an
implementation, but both names have distinct user intent.

Avoid adding a third `tessellate()` spelling until COMPAS-wide naming policy is
settled. Existing `compute_tessellation` and cached `.tessellation` already have
tests and users.

### Discrete polygonal geometry

Recommended naming:

```python
mesh.triangulated(strategy=None) -> Mesh       # non-mutating
mesh.triangulate(strategy=None) -> None        # mutating
mesh.to_triangle_mesh(strategy=None) -> Tessellation

polygonal_surface.triangulated(strategy=None) -> PolygonalSurface
polygonal_surface.to_triangle_mesh(strategy=None) -> Tessellation
```

`triangulate`/`triangulated` follow the conventional mutating/non-mutating verb
pair. They must document preservation of keys, face attributes, source
vertices, and source-to-result mapping. Existing `quads_to_triangles()` remains
available during migration and retains its current diagonal/default behavior.

`to_triangle_mesh` is a conversion and must not mutate the source. It returns
the lightweight triangle interchange, not a rich half-edge object. Users who
need topology call `.to_mesh()` on the returned `Tessellation` or use
`triangulated()`.

### Triangulation strategies

Use serializable policy objects where a choice exists:

```python
class TriangulationStrategy(Data): ...


class FixedDiagonal(TriangulationStrategy):
    diagonal: Literal["ac", "bd", "shortest"] = "ac"


class Earcut(TriangulationStrategy):
    tolerance: float | None = None


class ConstrainedDelaunay(TriangulationStrategy):
    quality: TriangleQuality | None = None
```

Do not force Delaunay point-set/domain triangulation into the same method as
face triangulation if their inputs and guarantees differ. Shared strategy data
may be reused, but functions remain explicit.

Every strategy contract states projection/coplanarity behavior, whether it can
insert Steiner points, whether it preserves vertex indices, and winding/
boundary guarantees.

## Unified triangle-mesh interoperability

### Public input concept and adapter

Define a core accepted-input concept:

```python
TriangleMeshInput = Tessellation | PolygonalSurface | Mesh | tuple[CoordinatesType, Sequence[Sequence[int]]]


def to_triangle_mesh(
    geometry: TriangleMeshInput | SupportsTriangleMesh,
    *,
    strategy: TessellationStrategy | TriangulationStrategy | None = None,
    validate: bool = True,
) -> Tessellation: ...
```

Also expose instance `to_triangle_mesh()` on supported core classes for
discoverability. Both paths delegate to one implementation per type.

A supplemental protocol can support third-party objects:

```python
class SupportsTriangleMesh(Protocol):
    def to_triangle_mesh(self, **options) -> Tessellation: ...
```

The protocol is not the sole contract because raw tuples cannot implement it.

### Validation layers

Core conversion validates only representation-level invariants:

- three finite coordinates per vertex;
- exactly three integer indices per face;
- indices in range;
- optional attribute lengths match vertices;
- no mutation of source buffers.

Optional validators cover increasingly strong requirements:

- nondegenerate triangles;
- consistent orientation;
- manifoldness;
- closed/watertight topology.

Each operation requests only the level it requires. Volume/boolean operations
can demand closed oriented manifold input; slicing or rendering need not.

Native packages then own dtype/layout coercion:

```python
def _as_cgal_triangle_mesh(mesh, *, requirements=...):
    tessellation = to_triangle_mesh(mesh, validate=True)
    # float64 C-contiguous vertices, chosen integer dtype faces
```

Core must not require NumPy. CGAL/libigl annotations, actual integer widths,
and tests must agree. Conversion helpers state when a copy occurs and preserve
zero-copy paths for already-compatible arrays where safe.

## Trimmed NURBS and BRep responsibility

- `NurbsSurface` represents the underlying parametric surface only. It must not
  acquire hidden trim loops from an owning BRep face.
- A trimmed-face/BRep object owns loops, holes, face orientation, and trim-aware
  tessellation.
- `BrepFace.compute_tessellation(strategy=...)` is the natural face-level API;
  `Brep.compute_tessellation(strategy=...)` aggregates faces.
- Converting `BrepFace.nurbssurface` remains explicitly untrimmed.
- Face aggregation preserves orientation and permits seam/face-local vertex
  duplication. Watertight welding is a separate explicit operation and cannot
  discard normal/UV seams.
- Optional provenance can include triangle-to-face, vertex-to-UV, boundary
  polyline-to-edge/loop, strategy, and backend error data.
- A trim-aware generic strategy must operate on a trimmed face/domain input,
  not accept free-floating trim arrays on `NurbsSurface` without an ownership
  model.

## Metadata, provenance, and error

Keep simple `Tessellation` construction lightweight. Define optional immutable
metadata records for enriched operations:

```python
class TessellationProvenance(Data):
    triangle_sources: Sequence[int] | None
    vertex_parameters: Sequence[tuple[float, float]] | None
    boundary_sources: Sequence[BoundarySource] | None


class ApproximationError(Data):
    metric: str
    maximum: float | None
    rms: float | None
    contract: Literal["target", "estimated", "guaranteed"]
    method: str | None
```

Rules:

- Metadata is optional and requested/produced explicitly.
- Source IDs are stable scalar identifiers, not serialized object references.
- Error units and measurement method are mandatory when values are reported.
- A requested threshold is stored separately from a measured result.
- Backend-specific data remains in operation-specific records rather than an
  unbounded dictionary on the mesh.
- Conversion to `Mesh`/`PolygonalSurface` documents which metadata is dropped
  or mapped to attributes.

## Plugin architecture

### Discovery and signatures

Before interoperability work:

1. Add current `compas.plugins` entry points to CGAL and include all intended
   plugin modules.
2. Add discovery tests that resolve functions through core COMPAS.
3. Align core and implementation signatures exactly.

Canonical planar triangulation vocabulary should be explicit:

- `boundary`: exterior closed ring;
- `holes`: closed interior rings;
- `constraints`: open constrained polylines;
- `points`: optional unconstrained interior points;
- `quality`: supported quality request.

Deprecate positional parameters after `boundary`; keyword-only calls prevent
silent reinterpretation. Do not map maximum area to maximum edge length or
advertise native minimum angle until implemented.

### CGAL and libigl

- Adopt the core triangle-mesh adapter at every triangle input boundary.
- Centralize each package's NumPy coercion and native safety checks.
- Preserve operation-specific result metadata through named results or
  compatibility adapters.
- Retain raw low-level tuple APIs where performance/users require them, but
  make high-level APIs accept the common input concept.
- Align pluggable return annotations with actual result shapes, including
  libigl face labels.

### OCC

- Map `Deflection` only to BRep/kernel tessellation.
- Expose trim-aware face and aggregate BRep results through the common triangle
  representation.
- Define cache keys from effective strategy plus output options rather than
  mutable global tolerance alone.
- Preserve compatibility tuple methods while downstream callers migrate.

### Gmsh

Treat Gmsh sizing options as a backend-specific meshing policy. Reuse common
names only where semantics match; do not claim that curvature sizing or element
size is the same as parametric UV resolution or OCC deflection.

## Compatibility plan

### Compatible additions

- Serializable strategy types and capability errors.
- `to_triangle_mesh` function/methods.
- Core triangle input adapter and validators.
- Non-mutating `triangulated()` methods.
- Optional enriched result/provenance records.
- Trim-aware face-level tessellation where supported.

### Behavior-preserving migration

- Legacy `nu`/`nv`, `u`/`v`, and deflection arguments normalize into strategy
  objects during a documented transition.
- Existing default connectivity and diagonal choices remain unchanged at first.
- Existing `Tessellation` identity, seam, and independent-conversion behavior
  remains unchanged.
- Existing polygon-preserving conversions remain distinct.
- Raw tuple inputs and outputs remain supported through adapters initially.

### Deprecation candidates

Only after replacements and downstream migration:

- misspelled `to_tesselation`;
- `to_viewmesh` where it is only a tessellation alias;
- positional constrained/conforming arguments after `boundary`;
- mismatched planar keyword names;
- `quads_to_triangles` only if `triangulate(FixedDiagonal(...))` fully preserves
  its behavior and metadata.

Do not deprecate `Mesh`, `PolygonalSurface`, `Tessellation`, polygon-preserving
conversion, or raw native buffers in this initiative.

## Alternatives rejected

### One universal executable strategy object

An `apply(geometry)` strategy would enable injection but creates double
dispatch, unclear backend ownership, and a plugin system inside the existing
plugin system. Configuration-only strategies keep algorithms with producers.

### One broad method with all controls

A signature containing U/V counts, tolerance, deflection, angle, area, and edge
length conflates units/guarantees and encourages ignored arguments. Explicit
strategy types allow clear rejection.

### One method whose return type depends on topology

Returning `PolygonalSurface`, `Tessellation`, or `Mesh` based on a topology
flag harms typing and predictability. Use explicit conversions with stable
return types.

### Immediate adaptive implementation in core

The current code has no error estimator or singularity/trim model. Defining a
portable request contract is useful; claiming robust adaptive behavior before
algorithm/quality validation is not.

## Tests

Tests ship with each implementation slice.

### Core unit contracts

- Strategy validation, equality, hashing, `Data` JSON roundtrip, and rejection
  of unsupported fields/strategies.
- Legacy scalar normalization and conflicting-form rejection.
- `to_triangle_mesh` equivalence for tuple, `Tessellation`,
  `PolygonalSurface`, and `Mesh`, including copy/identity behavior.
- Validation of arity, indices, finiteness, degeneracy, orientation,
  manifoldness, and closedness at the appropriate layers.
- Mutating/non-mutating triangulation, key/attribute preservation, source
  immutability, diagonal choice, vertex insertion, and mappings.
- Periodic seam fixture with duplicate positions and distinct attributes.
- Singular poles, reversed domains, and nonplanar polygons.
- Existing default counts/connectivity and cache behavior remain unchanged.

### OCC

- Trimmed/holed face tessellation excludes holes and preserves orientation.
- Boundary polylines map to loops/edges when provenance is requested.
- Face aggregation and face-local seam behavior.
- Deflection validation, explicit-zero rejection, cache identity, and monotonic
  refinement without requiring exact connectivity.
- Document/test whether deflection is a target, estimate, or guarantee.

### CGAL/libigl

- Real entry-point discovery and core-dispatched keyword calls.
- Equivalent tuple, `Mesh`, `PolygonalSurface`, and `Tessellation` inputs.
- Exact dtype/layout and zero-copy/copy behavior.
- Unsafe arity/index/topology failures occur before native calls.
- Holes, constraints, points, and quality parameters bind correctly.
- Unsupported quality fields fail rather than being ignored.
- Rich result provenance and libigl label outputs remain available.

### Framework integration

- Core shape/surface -> `Tessellation` -> CGAL and libigl operation.
- OCC trimmed face/BRep -> triangle interchange -> native consumer.
- Discovery and canonical keyword dispatch through installed packages.
- Cross-representation equivalence and source immutability.
- Strategy serialization and package-boundary roundtrip.
- Count/deflection/quality monotonic refinement with backend-appropriate
  assertions.
- Persistent mesh serialization versus ephemeral tessellation behavior.
- Native backend absence/skip behavior and focused performance baselines.

## Documentation and examples

Create a core terminology and migration guide explaining:

- operation versus conversion;
- sampling/discretization/tessellation/triangulation/refinement/remeshing;
- resolution, deflection, quality, cleanup tolerance, estimate, and guarantee;
- stable representation roles and buffer ownership;
- topology-preserving versus triangle conversion;
- seams, trims, singularities, orientation, and validation assumptions;
- legacy-to-new API mapping and deprecation timing.

Examples:

1. Parametric surface with `UVGrid`, normals/UVs, and a separate polygonal
   quad conversion.
2. The same polygonal surface triangulated with two diagonal strategies.
3. Trimmed OCC face with `Deflection`, boundary polylines, and provenance.
4. A `Tessellation` passed unchanged to CGAL/libigl high-level APIs.
5. Polygon with holes using Earcut versus constrained Delaunay, explicitly
   comparing vertex insertion and guarantees.
6. Adaptive request showing a supported backend and an explicit unsupported
   strategy error elsewhere.

## Affected packages and ownership

- **`compas`:** terminology, strategy and metadata data types, adapters,
  validators, conversion methods, triangulation naming, public exports, tests,
  and core docs.
- **`compas_occ`:** trimmed face/BRep strategy mapping, provenance extraction,
  cache semantics, compatibility wrappers, tests, and examples.
- **`compas_cgal`:** entry points, exact plugin signatures, common-input
  adoption, native coercion/validation, result metadata, tests, and docs.
- **`compas_libigl`:** common-input adoption, result-shape alignment, tests,
  and docs.
- **`compas_gmsh`:** capability comparison and optional strategy adaptation
  where semantics genuinely align.
- **`compas_model`:** downstream migration and preservation of distinct
  rendering/collision/contact/sectioning policies; no edits until its dirty
  worktree is reconciled.
- **`compas_framework`:** cross-package fixtures, integration/native-backend/
  roundtrip/performance tests, and initiative records.

## Dependency-aware implementation plan

No task is authorized until proposal approval.

### Phase 0: finalize public decisions (serial)

Coordinator/architect, no package implementation:

1. Approve representation decisions and stable return types.
2. Confirm strategy, metadata, adapter, and method names/modules.
3. Confirm whether `Adaptive` is contract-only initially or includes a first
   implementation.
4. Confirm compatibility/deprecation version policy and supported package
   matrix.

All implementation depends on these decisions.

### Phase 1: core foundations (coordinated ownership)

One core implementer owns shared strategy/metadata types, typing modules, and
public exports to avoid concurrent conflicts.

1. Add strategies, capability errors, serialization, and tests.
2. Add `to_triangle_mesh` adapter and layered validators with tests.
3. Add conversion/triangulation methods without changing defaults.
4. Clarify `Tessellation` docs while preserving its implementation contract.
5. Add terminology/migration docs in parallel once names stabilize.

Adapter work and strategy work can be developed in parallel if public exports
are integrated by the same owner.

### Phase 2: producer and discrete-operation slices (parallel)

After core contracts are available:

- Core surface/shape owner maps legacy counts to `UVGrid` and adds seam/
  singularity tests.
- Core mesh/polygon owner adds triangulation strategies and mutating/
  non-mutating operations.
- Core triangulation owner aligns planar vocabulary and legacy adapters.
- OCC owner implements trimmed face/BRep strategy mapping, provenance, caching,
  and tests.
- CGAL owner fixes discovery/signatures and adopts the native adapter.
- libigl owner adopts the adapter and aligns result annotations.
- Documenter owns examples/narrative files only.

Avoid concurrent edits to core public exports, shared typing, plugin
configuration, or the same geometry modules.

### Phase 3: optional advanced strategy slice

Only if separately approved after the base contracts:

- implement and validate a first `Adaptive` backend;
- define an error measurement harness and fixtures;
- document singularity/trim limitations and target/estimate/guarantee status.

This phase must not block basic interface and interoperability improvements.

### Phase 4: integration and independent review

Framework owner adds cross-package tests after compatible package versions are
available. Reviewer independently checks API consistency, compatibility,
native safety, geometry guarantees, docs, and executed test evidence. Findings
return to repository owners. Merge/publication require separate approval.

## Parallel work graph

```text
approved public decisions
          |
          v
 core strategies + adapter + exports
      |          |          |
      |          |          +--> core mesh/triangulation APIs
      |          +-------------> OCC trimmed BRep adaptation
      +------------------------> CGAL and libigl native adaptation
                                   |
 docs/examples -------------------+  (after names stabilize)
                                   v
                       framework integration tests
                                   |
                                   v
                         independent review

 optional Adaptive implementation starts only after the base contract
```

## Open decisions requiring approval

1. Approve retaining `Tessellation`, `PolygonalSurface`, and `Mesh` roles and
   deferring dedicated `TriangleMesh`/`QuadMesh` classes.
2. Approve optional operation-specific result envelopes instead of a universal
   `TessellationResult`.
3. Approve `UVGrid`, `Deflection`, and `Adaptive` as serializable configuration
   names, with `Adaptive` rejected by unsupported producers.
4. Decide whether the first implementation includes an adaptive algorithm or
   only its interoperable contract. Recommendation: contract first; algorithm
   as a separately validated slice.
5. Approve stable triangle return types and separate explicit polygonal
   conversion instead of a topology-dependent union return.
6. Approve `compute_tessellation`, cached `.tessellation`, and
   `to_triangle_mesh`, without introducing `tessellate()` yet.
7. Approve `triangulate()`/`triangulated()` as the canonical mutating/
   non-mutating pair.
8. Approve BRep/BRepFace ownership of trimmed-surface tessellation and keep
   standalone `NurbsSurface` explicitly untrimmed.
9. Approve canonical planar terms `boundary`, `holes`, `constraints`, `points`,
   and `quality`, with keyword-only migration.
10. Approve the stated deprecation intent; exact release versions remain a
    repository release decision.

## Approval scope

Approval authorizes implementation planning and the phased source/test/docs
work described above, with explicit repository/file ownership and preservation
of user changes. It does not authorize merging, publishing, deleting legacy
APIs, implementing an unapproved adaptive algorithm, consolidating the dirty
`compas_model` tree, or unrelated geometry behavior changes.

Until approval is given, the initiative stops at this proposal.
