# Geometry Tessellation Implementation Plan

Status: complete at recorded implementation scope — Ready for handoff

Authority: the Accepted ADRs in `decisions/`. The earlier proposal is not an
implementation authority where it differs from those ADRs.

Release baseline: the user explicitly approved COMPAS 3.0 as the minimum for
the synchronized package set participating in this initiative. Package
dependency metadata and the supported-version matrix must express
`COMPAS >= 3.0` rather than carrying a pre-3.0 compatibility path.

Gates A–I are resolved and explicitly approved. Package implementation may
proceed through the ownership, dependency, testing, and review controls in this
plan. This plan does not authorize merge or publication.

## Readiness verdict

The Accepted ADRs establish the following intended baseline:

- `Tessellation` is the sole ephemeral, indexed-triangle result and public
  high-level plugin input.
- `PolygonalSurface` remains persistent lightweight polygon geometry, and
  `Mesh` remains the persistent editable half-edge datastructure.
- Polygonization and tessellation apply to continuous surface-like geometry;
  triangulation applies to discrete faces/domains and point sets.
- Strategies are declarative and serializable. Requested controls must not be
  presented as achieved or guaranteed approximation error.
- Trim-aware tessellation belongs to `BrepFace`/`Brep`, not standalone
  `NurbsSurface`.
- Plugins share core semantic contracts while retaining backend-local native
  dtype/layout conversion.
- Superseded APIs are removed in a coordinated breaking release rather than
  retained through compatibility aliases.

The dependency graph is acyclic. Gates A–I are closed by the explicitly
approved contracts recorded in the Accepted ADRs. The strategy applicability,
terminology and framed-planarity inconsistencies found by independent review
are resolved. Speculative capability discovery was removed by ADR 016.
Implementation is **ready** and must not
reintroduce ignored strategy dimensions, ambiguous operation terms, silent 3D
projection, or runtime capability-discovery APIs.

## Architecture gates

All gates are closed and retained below as the implementation baseline.

### Gate A — Tessellation strategy schemas (closed; amended by ADR 016)

Affected decisions: ADR 003, with ADR 016 superseding ADR 004's unused
capability and error schemas.

Resolution: explicitly approved and recorded in Accepted ADRs 003 and 016.

- `UVGrid(Data)` has positive integer `u` and `v`; it contains no domain
  restriction fields.
- `Deflection(Data)` has positive finite `linear` in model units and positive
  finite `angular` in public degrees, with `angular <= 180`.
- `Adaptive(Data)` has optional positive finite `max_deviation`, `max_angle`,
  and `max_edge_length`, requires at least one value, uses public degrees for
  `max_angle`, and exposes no recursion/depth control.
- Producers reject unsupported strategy parameters instead of ignoring them.
- Runtime capability discovery and reserved error records are not part of the
  API. Producers validate strategies directly and document their support.
- Requested targets are not presented as achieved or guaranteed error.
- No enriched `TessellationReport` API is authorized; closed Gate D explicitly
  defers all enriched result APIs.

The strategy schemas are implementation inputs for the coordinated public API.

### Gate B — Polygon and planar triangulation contracts (closed)

Affected decisions: ADR 007, ADR 011, and ADRs 017–020; depends on closed Gate
A where quality and error concepts overlap.

Resolution: explicitly approved and recorded in Accepted ADRs 007, 011, and
017–020. ADR 017 supersedes ADR 007's single-strategy collection-level policy.

- Face strategies inherit serializable `Data` through
  `TriangulationStrategy`.
- `DiagonalSplit(diagonal)` accepts `"shortest"`, `"02"`, or `"13"` and
  applies only to triangles/quads. Triangles pass through; shortest-diagonal
  ties deterministically choose `"02"`.
- `EarClipping` applies to planar polygonal faces, uses standard COMPAS
  tolerance, preserves input vertices, and inserts no Steiner points.
- `ProjectedEarClipping(max_deviation)` is an explicit opt-in policy for a
  near-planar polygon. It uses a documented best-fit plane, rejects excessive
  deviation and invalid projections, and returns indices into the original 3D
  vertices. Projection is never an implicit fallback.
- `MinimumAreaTriangulation` applies dynamic programming directly to an
  ordered 3D boundary without projection or vertex insertion. It minimizes
  total triangle area in cubic time and quadratic memory. The result is a
  combinatorial disk but is not guaranteed to be geometrically
  intersection-free.
- Collection-level operations require serializable
  `FaceTriangulation(quad=..., ngon=...)`. Triangles pass through, quads use
  the explicit quad policy, and faces with five or more vertices use the
  explicit n-gon policy. Projection and twisted-polygon policies are opt-in;
  there is no algorithm fallback.
- `DiagonalSplit` may explicitly define a piecewise-planar interpretation of a
  warped quad. `EarClipping` rejects non-planar quads and n-gons; no implicit
  projection or algorithm fallback occurs.
- Mutating `triangulate(strategy)` returns `None`, transfers source face
  attributes, does not guarantee face keys, and preserves vertex keys for the
  initial non-inserting strategies.
- Non-mutating `triangulated(strategy)` returns `Tessellation`.
- Planar-domain strategies are a separate serializable family: `Delaunay`,
  `ConstrainedDelaunay`, and `ConformingDelaunay(quality=None)`.
- `TriangulationQuality(Data)` has optional positive finite `min_angle` in
  public degrees below 60, `max_area` in model-units squared, and
  `max_edge_length` in model units, with at least one field required.
- Quality fields are triangulation targets, not `Adaptive` tessellation
  controls or approximation-error guarantees; unsupported fields raise.
- `triangulate_planar_points(points, *, strategy: Delaunay, frame=None)` and
  `triangulate_planar_domain(boundary, *, holes=(), constraints=(), points=(), strategy, frame=None)`
  are the canonical functions and return `Tessellation`. Their names expose
  the required planar contract; the standard Delaunay strategy names remain
  unchanged.
- `frame=None` means world XY. An explicit `Frame` projects into local XY and
  lifts result vertices back; implementations never silently discard Z.
- `Delaunay` preserves supplied points; constrained triangulation may insert
  vertices where constraints intersect; conforming triangulation may insert
  Steiner vertices to pursue quality targets.
- Self-intersecting planar arrangements, fill rules, and generated
  intersection vertices remain a separate domain-level operation. It is not
  exposed until an exact-intersection backend satisfies ADR 018. Arbitrary
  spatial loops remain outside polygon triangulation.

### Gate C — Topology-preserving polygonization API (closed)

Affected decisions: ADR 005 and ADR 006.

Resolution: explicitly approved and recorded in Accepted ADRs 005–006.

- Continuous surface-like geometry exposes fresh, non-mutating
  `polygonize(strategy) -> PolygonalSurface` for topology-preserving output.
- The result is independent, persistent, and serializable. It never returns
  `Mesh`; half-edge topology requires explicit `.to_mesh()` on the result.
- There is no cached property, scalar-control alternative, or topology flag.
- The operation applies to analytical `Shape`, parametric `Surface`, untrimmed
  `NurbsSurface`, and `BrepFace`/`Brep` where the backend supports polygonal
  output. Curves are excluded because their connected discrete result is a
  `Polyline`.
- `polygonize` and `tessellate` use the same tessellation strategies, but
  topology is a producer/strategy capability rather than a strategy flag.
- `UVGrid` on regular parametric surfaces guarantees quads; analytical shapes
  may produce mixed triangles/quads; `Deflection` and `Adaptive` provide no
  quad guarantee. Unsupported combinations raise.
- Direct `tessellate(strategy=None) -> Tessellation` remains the canonical
  triangle operation and need not call
  `polygonize(...).triangulated(...)`. For Shape and Surface only, `None`
  resolves to the deterministic defaults in ADR 021. BRep/BRepFace remain
  explicit.
- Direct and two-step paths for the same tessellation strategy must be
  geometrically consistent, but their connectivity may differ. Backends
  document seam and boundary behavior for both.
- Callers who require a specific face-triangulation policy use
  `polygonize(strategy).triangulated(FaceTriangulation(...))`.

### Gate D — Enriched result access (closed)

Affected decision: ADR 010; depends on Gates A and C where error and source
topology metadata are involved.

Resolution: explicitly approved and recorded in Accepted ADR 010.

- The initial stable operations remain
  `tessellate(strategy=None) -> Tessellation` for Shape and Surface,
  `tessellate(strategy) -> Tessellation` for BRep/BRepFace, and
  `polygonize(strategy) -> PolygonalSurface`.
- Initial APIs have no detail/report flags, union returns, universal report or
  result wrapper, or parallel detailed method.
- `Tessellation` retains representation fields only: vertices, triangles,
  optional aligned normals, optional aligned UVs, and optional relevant
  boundary polylines. These are not provenance.
- Source-face/trim mappings, execution reports, measured errors, refinement
  histories, and backend diagnostics are deferred.
- There is no support-discovery or reserved approximation-error schema. A
  future API requires a concrete consumer, backend source, and separate ADR.
- A future enriched API requires a separate ADR, concrete consumer/backend
  source, distinct method name, stable operation-specific result type, and no
  serializable source-object references.
- Any envelope containing ephemeral `Tessellation` is itself ephemeral.

### Gate E — Plugin-boundary editorial alignment (closed)

Affected decisions: ADR 008 and ADR 012.

Resolution: ADR 012 is aligned with ADR 008. Core owns `Tessellation`
validation and buffer extraction, not a heterogeneous representation adapter.
Backend-local helpers own dtype, layout, range checks, native-safety checks,
and conversion to native inputs.

### Gate F — Strategy applicability to fixed and partially parameterized shapes (closed)

Affected decisions: ADR 003, ADR 005, and ADR 006.

Resolution: explicitly approved and recorded in Accepted ADRs 003 and 005.

- All tessellation strategies inherit `TessellationStrategy(Data)`.
- `Native()` requests fixed natural topology and is supported by `Box`.
- `UGrid(u)` has one positive integer dimension and is supported by `Cylinder`
  and `Cone`.
- `UVGrid(u, v)` has two positive integer dimensions and is supported by
  `Sphere`, `Capsule`, `Torus`, and general parametric surfaces.
- `Deflection` and `Adaptive` inherit the same common strategy base.
- Invalid geometry/strategy combinations raise. Producers never ignore extra
  dimensions to make a strategy appear supported.

### Gate G — Discretization, polygonization, and tessellation terminology (closed)

Affected decisions: ADR 001, ADR 005, and ADR 006.

Resolution: explicitly approved and recorded in Accepted ADRs 001, 005, and
006.

- Discretization is the broad category for finite samples or connected
  elements representing continuous geometry.
- Polygonization is the surface operation producing persistent connected
  polygonal faces through `polygonize(strategy) -> PolygonalSurface`.
- Tessellation is the canonical surface operation producing the ephemeral
  triangular result through `tessellate(strategy) -> Tessellation`.
- Triangulation partitions existing discrete faces, domains, or point sets.
- `polygonize` and `tessellate` are operations; `.to_mesh()` is the explicit
  representation conversion to half-edge `Mesh`.

### Gate H — Planarity and off-plane semantics for framed triangulation (closed)

Affected decision: ADR 011.

Resolution: explicitly approved and recorded in Accepted ADR 011.

- With `frame=None`, every input coordinate must lie in world XY within the
  standard COMPAS tolerance.
- With an explicit `Frame`, every input coordinate must lie on its plane within
  the standard COMPAS tolerance.
- Inputs beyond the applicable tolerance are rejected.
- Projection into local XY is internal only; implementations never silently
  discard Z.
- Existing input vertex coordinates are preserved exactly in the result.
- Generated intersection or Steiner vertices are lifted onto world XY or the
  explicit frame plane.

### Gate I — Strategy base type and direct validation (closed; amended by ADR 016)

Affected decisions: ADR 003, ADR 005, ADR 006, and ADR 016.

Resolution: explicitly approved and recorded in Accepted ADRs 003, 005, 006,
and 016.

- `TessellationStrategy(Data)` is the common base for `Native`, `UGrid`,
  `UVGrid`, `Deflection`, and `Adaptive`.
- Producers validate the supplied strategy directly and raise a precise
  `TypeError` or `ValueError` when unsupported.
- Supported strategies are documented by geometry type/backend. There is no
  runtime discovery method or parallel support predicate.

## Work permitted now

All implementation work packages below may proceed when their dependencies are
met and ownership is assigned. Work must remain within the accepted API:

1. Treat the completed core foundations and continuous/discrete APIs in
   WP1–WP3 as the implementation baseline.
2. Prepare repository-specific commits and release follow-ups only with the
   appropriate authorization.
3. Preserve the recorded tests and documentation artifacts during handoff.
4. Do not introduce ignored strategy dimensions, capability discovery or
   predicates, permissive off-plane projection, enriched result APIs,
   compatibility aliases, implicit triangulation fallbacks, or unapproved
   adaptive algorithms.
5. Preserve repository ownership boundaries and coordinate shared core export
   changes through the WP1 owner.

## Implementation progress and recorded evidence

WP0 is complete. WP1, WP2, WP3, and the WP3b follow-up are implemented and
their independent reviews concluded **Ready**. WP4–WP6 are independently
reviewed Ready, and WP7 completed with an assessment-only outcome. This plan
records the following evidence reported
by the implementing and reviewing agents; it does not claim that this planning
task reran those commands:

- WP1: 33 focused tests passed; Ruff, Pyright, and diff checks passed.
- WP2: 69 focused tests and 228 broader tests passed; the independent review
  ran 118 combined tests and reported Ready; Ruff, Pyright, and diff checks
  passed.
- WP3: 223 focused/subdivision tests passed; the independent review ran 37
  tests plus 5 doctests and reported Ready; Ruff, Pyright, and diff checks
  passed.
- WP3b: complete; independent review reported Ready.
- WP3c (ADRs 018–020): complete. Strict and projected polygon policies,
  minimum-area twisted-polygon triangulation, and explicit planar Delaunay
  naming are implemented and independently reviewed Ready. Planar-arrangement
  dispatch remains intentionally unavailable pending a conforming exact-
  intersection backend, licensing resolution, and verification.
- WP4 OCC: 8 focused tests passed; independent review reported Ready; package
  metadata requires `compas>=3`.
- WP5 CGAL: 135 full-package and 35 focused tests passed; independent review
  reported Ready; package metadata requires `compas>=3,<4`.
- WP6 libigl: Python-boundary implementation is Ready; 18 stub tests passed
  and independent review reported Ready; package metadata requires
  `compas>=3`. Native-runtime verification is deferred to WP9/integration CI
  because the required extensions and `mapbox-earcut` were unavailable.
- WP7 Gmsh: assessment complete with no runtime change. Any future strategy
  adaptation requires a separate ADR and concrete consumer.

WP9 core/OCC/CGAL/libigl integration is implemented and independently reviewed
Ready: the implementation reported 18 passed and 1 skip; the reviewer reported
17 passed and 1 precise libigl-native skip, with Ruff and diff checks passing.
The performance baseline remains explicitly deferred until a normalized runner
and comparable baselines are available.

WP8 `compas_model` migration is implemented and independently reviewed Ready:
46 tests, Ruff, strict MkDocs, and diff checks were reported passing.

WP10 documentation/release artifacts are independently reviewed Ready. The
reported evidence includes strict documentation builds for core, framework,
and CGAL; an OCC non-strict build with pre-existing warnings; and terminology
corrections. A native libigl documentation build was unavailable. These are
reported results and were not rerun by this planning task.

All WP0–WP10 work packages are complete at their recorded scope. Independent
final review reported **Ready for handoff**, with no implementation blockers.
Final cross-package evidence included 90 OCC tests passing against the sibling
COMPAS checkout and 17 framework integration tests passing with 1 precise
libigl-native skip. These are reported results and were not rerun by this
planning task. The normalized performance infrastructure and native libigl
runtime/documentation verification remain explicit deferrals; WP7 remains a
completed no-runtime-change assessment.

## Implementation work packages

The following packages are executable in dependency order. Package owners must
not edit outside their assigned repository and file area. Exact new
filenames/modules remain implementation details and must follow each
repository's established organization.

### WP0 — Architecture closure (complete)

Owner: architect/coordinator.

Completed scope:

- Gates A–I are closed by the Accepted ADRs;
- the decision index and implementation plan reflect every accepted contract;
- the decision graph is coherent and acyclic;
- no blocking public contract remains for implementers to invent.

Exit: met. Implementation may start with WP1.

### WP1 — Core strategy and result foundations (implemented; review Ready)

Owner: one `compas` implementer for shared public types, serialization, typing,
and exports. Avoid concurrent edits to public export and data-registration
areas.

Depends on: completed WP0. The accepted Gates A–I contracts form the
implementation baseline.

Scope derived from ADRs 002–003, 010, and 016:

- retain `Tessellation` as ephemeral and non-serializable;
- preserve zero-copy buffer retention and same-index normal/UV semantics;
- implement `TessellationStrategy` and the approved serializable `Native`,
  `UGrid`, `UVGrid`, `Deflection`, and `Adaptive` strategies with exact
  validation;
- omit runtime capability discovery and reserved error records per ADR 016;
- do not add enriched result/report types; Gate D explicitly defers them;
- add core buffer extraction and validation required by ADR 008, without a
  public union adapter.

Tests delivered with the slice:

- strategy data roundtrip, equality, validation, common-base typing, and
  unsupported-strategy errors;
- `Tessellation` identity, arity, bounds, finiteness, and attribute alignment;
- explicit ephemeral/non-serialization behavior;
- absence of speculative capability/error-schema exports;
- absence of detail/report flags, union returns, and universal result wrappers.

Documentation:

- representation roles;
- strategy schemas, direct validation, and documented producer support;
- buffer ownership and seam duplication.

### WP2 — Core continuous geometry APIs (implemented; review Ready)

Owner: one `compas` implementer for surface, NURBS surface, shape, and curve
areas; coordinate shared exports with WP1's owner.

Depends on: WP1. Gates A and C are closed.

Scope derived from ADRs 001, 003–006, 009, and 021:

- implement `tessellate(strategy=None) -> Tessellation` on Shape and Surface;
  resolve `None` to `Native()` for Box, `UGrid(64)` for Cylinder/Cone,
  `UVGrid(64, 64)` for Sphere/Torus/Capsule, and `UVGrid(64, 64)` for every
  Surface;
- implement fresh, non-mutating
  `polygonize(strategy) -> PolygonalSurface` on the approved geometry scope;
- require an explicit strategy for `polygonize`; keep BRep/BRepFace
  tessellation explicit; remove stored `resolution_u`, `resolution_v`, and
  other resolution-backed derived state in accordance with ADR 014;
- ensure polygonal results are independent and serializable, exclude curves,
  and require explicit `.to_mesh()` for half-edge topology;
- enforce `Box`/`Native`, `Cylinder` and `Cone`/`UGrid`, and `Sphere`,
  `Capsule`, `Torus`, and general parametric surface/`UVGrid` support; reject
  invalid combinations without ignoring dimensions;
- validate supplied strategies directly with precise errors and expose no
  runtime capability-discovery method or parallel predicate;
- preserve standalone `NurbsSurface` as untrimmed rectangular-domain geometry;
- remove public cached/computed/conversion tessellation variants listed by
  ADR 013;
- do not add private discretization caches in the initial implementation.

Tests:

- exact resolution/count behavior and source non-mutation;
- periodic seam and same-index attribute behavior;
- singular-pole and reversed-domain behavior as documented;
- unsupported-strategy errors;
- precise strategy-type validation and absence of capability-discovery or
  convenience-predicate APIs;
- fixed-, one-, and two-parameter strategy applicability with explicit Box,
  Cylinder, Cone, Sphere, Capsule, Torus, and general-surface coverage and no
  ignored dimensions;
- absence of stored resolution properties and derived discretization caches;
- repeated explicit operations produce independent results without mutating
  the source geometry;
- omitted and explicit `None` tessellation are equivalent to the fixed ADR 021
  defaults, remain fresh, and do not mutate the source; explicit overrides
  remain effective;
- stable triangle versus polygonal result types;
- polygonal result independence, serialization, curve exclusion, explicit
  `.to_mesh()`, and natural quad/mixed-topology guarantees;
- direct versus two-step geometric consistency without requiring identical
  connectivity;
- removal of public cache-identity expectations.

Documentation/examples:

- uniform surface/shape tessellation with deterministic optional defaults and
  explicit strategy overrides;
- the intentional asymmetry between optional ephemeral Shape/Surface
  tessellation and explicit persistent polygonization/BRep deflection;
- removal of resolution-backed representation properties and derived caches;
- separate polygonized/quad output, explicit `.to_mesh()`, and subsequent
  strategy-controlled triangulation;
- explicit warning that standalone NURBS tessellation ignores BRep trims.

### WP3 — Core discrete triangulation and planar contracts (implemented; review Ready)

Owner: one `compas` implementer for `Mesh`, `PolygonalSurface`, polygon/region
triangulation, and planar pluggable declarations. Coordinate shared exports
with WP1's owner.

Depends on: WP1. Gates B and C are closed.

Scope derived from ADRs 005, 007, 008, 011, and 017–020:

- implement the approved mutating `triangulate(strategy)` contract on mutable
  topological types;
- implement `triangulated(strategy) -> Tessellation` on supported discrete
  polygonal types;
- implement `FaceTriangulation` as the required collection-level composite,
  with deterministic triangle/quad/n-gon dispatch and leaf strategies retained
  for low-level single-face use;
- implement strict `EarClipping`, explicit `ProjectedEarClipping`, and
  `MinimumAreaTriangulation` with the distinct validity, projection,
  complexity, and self-intersection contracts recorded in ADRs 018–019;
- implement `PolygonalSurface.to_mesh() -> Mesh` as the canonical explicit
  half-edge conversion and remove its cached `.mesh`/`compute_mesh()` forms;
- implement exact strategy applicability, planarity validation, internal
  projection, vertex-insertion, and source-index rules approved by Gates B and
  H;
- replace conversion flags and special-case triangulation methods listed in
  ADR 013;
- define the explicit `triangulate_planar_points` and
  `triangulate_planar_domain` keyword-only signatures and return `Tessellation`
  for plain, constrained, conforming, and refined operations;
- validate basic `Tessellation` structure before dispatch.

Tests:

- mutating versus non-mutating behavior and exact mutating return contract;
- source face-attribute transfer where required;
- mixed triangles/quads/concave n-gons, explicit quad diagonals, warped quads,
  nonplanar n-gons, and atomic failure, plus planar-domain holes, constraints,
  and points;
- projection deviation and invalid-projection rejection; deterministic
  minimum-area selection, twisted 3D boundaries, degeneracy rejection, and
  serialization of the new leaf strategies;
- input preservation versus Steiner insertion;
- winding, area/coverage, standard-tolerance acceptance/rejection in world XY
  and explicit frames, exact preservation of input coordinates, lifting of
  generated vertices, and unsupported quality fields;
- identical core/pluggable call binding;
- `PolygonalSurface.to_mesh()` result independence and topology preservation,
  plus absence of cached `.mesh` and `compute_mesh()` alternatives.

Documentation:

- local face triangulation versus planar domain triangulation;
- strategy applicability, projection, possible geometric self-intersection,
  complexity, and vertex insertion;
- canonical keyword-only planar API;
- explicit `PolygonalSurface.to_mesh()` representation conversion versus
  triangulation operations.

### WP4 — OCC trimmed tessellation (implemented; review Ready)

Owner: `compas_occ` implementer for BRep/BRepFace tessellation, plugin adapter,
tests, and OCC examples only.

Depends on: WP1 and WP2. Gates A and D are closed.

Scope derived from ADRs 003, 006, 009–010, 013, and 016:

- implement `tessellate(strategy) -> Tessellation` for BRep/BRepFace using
  actual trim topology and orientation;
- implement `polygonize(strategy) -> PolygonalSurface` for BRep/BRepFace only
  where the backend can provide a supported polygonal result, otherwise raise;
- validate BRep/BRepFace strategies through the active backend without a
  runtime capability-discovery facade;
- treat supported deflection values as requested targets, without a
  per-execution achieved-error claim or reserved error schema;
- preserve winding, holes, boundary polylines, and face-local seam needs;
- do not expose face/trim provenance, execution reports, measured errors,
  histories, or diagnostics in the initial public tessellation API;
- remove `to_tessellation`, `to_tesselation`, `to_viewmesh`, public cached
  tessellation, and unrelated scalar call forms;
- keep standalone NURBS surface behavior explicitly untrimmed.
- update `compas_occ` dependency metadata to require COMPAS 3.0 or newer as
  part of the synchronized package baseline.

Tests:

- holes, curved trims, reversed faces, boundaries, and face-local seam
  duplication; document that OCC output preserves geometric boundaries but is
  not guaranteed to have welded, topologically watertight indices;
- explicit strategy validation and no truth-value defaulting of zero;
- precise `Brep`/`BrepFace` strategy validation and absence of runtime
  capability-discovery methods;
- backend-appropriate refinement assertions without claiming a per-execution
  error report;
- representation fields remain limited to approved `Tessellation` data and are
  not documented as provenance;
- polygonal result independence, serialization, explicit `.to_mesh()`, and
  documented topology/seam/boundary behavior where polygonization is
  supported.

Documentation/example:

- trimmed face/BRep tessellation with explicit deflection strategy;
- loss of trim context when extracting an underlying NURBS surface.

### WP5 — CGAL planar and triangle-operation integration (implemented; review Ready)

Owner: `compas_cgal` implementer for entry points, high-level plugin functions,
native coercion helpers, annotations, tests, and CGAL docs only.

Depends on: WP1 and WP3. Gates A, B, and E are closed.

Scope derived from ADRs 008, 011–013:

- add current plugin entry-point metadata and register intended decorated
  modules;
- implement the exact core keyword-only planar signature and `Tessellation`
  result;
- accept only `Tessellation` at high-level triangle-operation boundaries;
- centralize package-local NumPy dtype/layout/range/native-safety coercion;
- align annotations with actual binding integer widths;
- reject unsupported quality fields rather than mapping them to other values;
- remove divergent high-level direct APIs, tuple inputs, and tuple/face-only
  result contracts; retain clearly internal native bindings as needed.
- update `compas_cgal` dependency metadata to require COMPAS 3.0 or newer as
  part of the synchronized package baseline.

Tests:

- installed entry-point discovery and dispatch through core;
- exact signature binding for boundary, holes, constraints, points, quality;
- dtype/layout/range and invalid-buffer failures before native calls;
- supported/unsupported quality controls;
- result winding, holes, and vertex insertion;
- optional-backend absence behavior.

Documentation:

- core-dispatched public use;
- backend constraints and supported operations without presenting a divergent
  high-level API.

### WP6 — libigl triangle-operation integration (Python boundary; review Ready)

Owner: `compas_libigl` implementer for high-level plugin functions, native
coercion, result annotations, tests, and docs only.

Depends on: WP1; Gate E is closed, and operation-specific work may depend on
WP3.

Scope derived from ADRs 008, 012, and 013:

- accept `Tessellation` at high-level triangle-operation boundaries;
- retain backend-local dtype/layout/native-safety coercion;
- align result types and annotations with accepted core contracts;
- do not expose operation-specific provenance/error envelopes in the initial
  high-level API;
- remove public raw tuple high-level inputs and divergent semantic contracts.
- update `compas_libigl` dependency metadata to require COMPAS 3.0 or newer as
  part of the synchronized package baseline.

Tests/documentation mirror WP5 for libigl-supported operations and the absence
of unapproved enriched high-level results.

### WP7 — Gmsh strategy alignment assessment (complete; no runtime change)

Owner: `compas_gmsh` implementer/investigator; initially read-only.

Depends on: WP1; Gate A is closed.

Scope derived from ADRs 003, 013, and 016:

- map Gmsh controls only where their semantics exactly match an approved
  strategy;
- explicitly document unmatched size/curvature controls rather than forcing a
  false equivalence;
- implement adaptation only after a concrete consumer and separate decision
  establish its semantics.

Exit may legitimately be documentation of non-alignment with no runtime
change.

Recorded outcome: no runtime change. A future
`Adaptive.max_edge_length` mapping requires a separate ADR before
implementation.

### WP8 — compas_model consumer migration (implemented; review Ready)

Owner: `compas_model` implementer. The previously dirty worktree is now clean
and the task branch has been created.

Depends on: WP2–WP6 as applicable.

Scope derived from ADRs 001–002, 005–010, and 013:

- migrate rendering, collision, contact, and sectioning call sites to the
  accepted operations/results;
- preserve their intentionally different policies;
- keep source/topological boundaries distinct from generated fill diagonals;
- decide no new Earcut consolidation beyond what Gate B and ADR 011 authorize.

Tests:

- rendering fill versus visible boundary;
- collision/contact/sectioning policy preservation;
- BRep boundary representation consumption without source-provenance claims.

### WP9 — Framework integration and performance (implemented; review Ready)

Owner: `compas_framework` implementer for tests/fixtures and integration docs
only.

Depends on: WP1–WP7 for core/OCC/CGAL/libigl/Gmsh scenarios. Only
model-specific integration scenarios depend on optional WP8.

Scope derived from all Accepted ADRs:

- exercise real plugin discovery and canonical dispatch;
- verify core surface/shape -> `Tessellation` -> CGAL/libigl workflows;
- verify OCC trimmed BRep -> `Tessellation` -> native consumer;
- test strategy serialization across package boundaries;
- compare backend-appropriate refinement behavior without requiring identical
  connectivity;
- verify ephemeral `Tessellation` versus persistent geometry serialization;
- defer focused conversion/validation/native-coercion performance baselines
  until a normalized runner and comparable baselines are available;
- verify optional-backend skip/absence behavior.
- run model-specific integration scenarios only when WP8 is complete and its
  user-owned worktree has been reconciled.

Tests use the existing framework markers for integration, roundtrip,
performance, and native backends as appropriate.

### WP10 — Documentation and breaking release preparation (complete; review Ready)

Owner: documenter for narrative docs/examples; coordinator for version matrix
and release checklist.

Depends on: stable implemented APIs from WP1–WP7. Model-specific documentation
depends on optional WP8, but core release documentation does not.

Scope derived from ADRs 001, 006–013:

- publish the normative terminology and representation guide;
- document strategies, direct validation, requested-control semantics, seams, trims,
  singularities, validation, and native constraints;
- replace examples with the one accepted call form per operation;
- produce a concise breaking-change guide mapping removed forms to new forms;
- document the synchronized supported package-version set, with COMPAS 3.0 as
  the explicit minimum baseline for participating integration packages;
- do not publish compatibility aliases or a deprecation timeline.

## Dependency and parallelization graph

```text
WP0 architecture closure (complete)
          |
          v
WP1 core foundations (complete)
   |          |             |
   v          v             v
WP2 core      WP3 core      WP7 Gmsh assessment (complete)
continuous    triangulation
(complete)    (complete)
   |          | \
   v          |  +--------> WP5 CGAL (complete)
WP4 OCC       +-----------> WP6 libigl
(complete)                  (Python boundary Ready)
   \          |               /
    +---------+--------------+
              |
              v
        WP9 core integration (complete/Ready)
              |
              v
        WP10 docs/release (complete/Ready)
              |
              v
       independent review

WP2-WP6 -----> WP8 model migration (complete/Ready)
                    |
                    v
              WP9 model scenarios
```

WP0–WP10 are complete at their recorded validation levels; WP7's assessment
completed with no runtime change. WP9 retains precise optional native skips
where the libigl extensions are unavailable, and its performance baseline is
deferred pending a normalized runner and baselines. WP10 likewise records the
unavailable native libigl documentation build rather than claiming it passed.
Independent final review found no implementation blockers and reported Ready
for handoff.

## Coordinated removals required by ADR 013

The breaking release removes, rather than aliases, the superseded public forms
after their accepted replacements are implemented and tested:

- scalar tessellation call controls superseded by explicit strategy objects;
- public cached `.tessellation`;
- `compute_tessellation`, `to_tessellation`, misspelled `to_tesselation`, and
  `to_viewmesh`;
- `to_triangle_mesh` as a redundant universal facade;
- `triangulated=True` conversion flags, `.triangles` as an operation facade,
  and `quads_to_triangles` where superseded by accepted triangulation methods;
- `PolygonalSurface.mesh` and `PolygonalSurface.compute_mesh()` in favor of the
  sole explicit `PolygonalSurface.to_mesh()` conversion;
- legacy planar keywords and positional arguments after `boundary`;
- face-only and `(vertices, faces)` high-level triangulation results;
- raw tuple inputs to high-level plugin operations;
- divergent direct backend high-level contracts.

Removal tasks happen in the owning package work package, not as an isolated
search-and-delete pass. Each removal requires updated tests, examples, and
downstream callers in the synchronized version set.

ADR 014 supersedes the earlier exclusion of `resolution_u`, `resolution_v`,
and resolution-backed derived caches. Continuous geometry retains only its
defining analytic state. Stored resolution properties, cached derived
vertices/edges/faces and related sampled views, `Shape.to_vertices_and_faces`,
and `Mesh.from_shape` are coordinated removals. Public materialization uses
explicit `polygonize(strategy)` and fresh `tessellate(strategy=None)`
operations. Only Shape and Surface resolve `None` to the fixed ADR 021
defaults; BRep/BRepFace remain explicit. Half-edge conversion is
`shape.polygonize(strategy).to_mesh()`.

ADR 015 authorizes continuous-bounds implementation. Exact parameter-derived
AABBs should replace sampled shape bounds; analytic surfaces and certified
NURBS enclosures follow the guarantees and phasing in that ADR. Minimum-volume
`obb` remains unsupported where a correct continuous result is unavailable.
No implementation may preserve old sampled bounds through a hidden default
tessellation.

## Verification plan

This planning task did not rerun verification. The progress ledger above
records evidence reported for WP1–WP3. Implementers must continue to record
the exact commands and results for the remaining repositories.

### Per-work-package verification

1. Run the smallest relevant unit-test module after each focused change.
2. Run the affected repository's full non-GUI test suite before handoff.
3. Run static/type checks configured by that repository for changed public
   annotations.
4. Build or render changed documentation/examples using repository tooling.
5. For native packages, run both supported-backend tests and absence/skip
   behavior where the environment permits.

Representative test categories, with exact repository commands confirmed by
each owner before execution:

- core geometry/tessellation, surface, shape, mesh, polygon/region, plugin, and
  serialization tests;
- OCC surface/BRep/plugin/data tests;
- CGAL/libigl triangulation, meshing, geodesic, boolean, slicing, dtype/layout,
  and discovery tests as affected;
- model rendering/collision/contact/sectioning tests;
- framework `integration`, `roundtrip`, `native_backend`, and focused
  `performance` markers.

### Final cross-package exit criteria

Implementation is complete only when:

- Gates A–I have Accepted resolutions or recorded editorial alignment as
  applicable;
- every work package has recorded passing unit and repository-level evidence;
- core/plugin signatures bind through installed entry points;
- all high-level triangle consumers accept `Tessellation` and no public raw
  tuple alternative remains in the approved scope;
- trimmed BRep tests cover holes, orientation, and boundaries;
- strategy serialization and error-strength semantics are verified;
- removal searches find no superseded public examples or internal callers in
  the synchronized package set;
- cross-package integration and optional-backend behavior pass;
- the synchronized package-version matrix and WP4/WP5/WP6 dependency metadata
  consistently require COMPAS 3.0 or newer, with no pre-3.0 compatibility
  claim;
- documentation is verified against actual signatures;
- an independent reviewer resolves all implementation findings.

### Remaining release follow-ups

Completion at the recorded implementation scope does not authorize or imply a
commit, merge, or publication. Release preparation still requires:

- native libigl wheel CI to exercise the deferred runtime and documentation
  paths;
- a core version bump to the approved 3.x line before publication;
- repository-specific commit preparation and review;
- excluding workspace-only `AGENTS.md` and `.codex` content from commits unless
  their inclusion is separately intentional; and
- separate explicit authorization for merge and publication.

## Plan status transitions

- **Architecture-gated:** completed; retained as the historical pre-WP0 state.
- **Ready:** completed architecture state; all gates are closed and
  architecture review found no blockers.
- **In progress:** completed implementation state preceding integration.
- **Integration / final review:** completed; WP0–WP10 reached their recorded
  scope and underwent independent final review.
- **Review complete:** completed; the reviewer reported Ready for handoff with
  no implementation blockers.
- **Complete:** current state at the recorded implementation scope. Nothing has
  been committed, merged, or published by this status update; the release
  follow-ups above remain.
