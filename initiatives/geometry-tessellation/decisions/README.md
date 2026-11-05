# Geometry Tessellation Architecture Decisions

This directory decomposes the architecture proposal into independently
reviewable decisions. ADRs 001–021 are **Accepted**. ADRs 022–023 are
**Proposed** in response to the new user-authored operation definitions. The target
architecture prioritizes one clean, coherent API over backward compatibility;
breaking effects are recorded rather than mitigated through permanent aliases.

## Decision index

| Order | ADR | Status | Depends on | Consequential tradeoff |
|---:|---|---|---|---|
| 1 | [001 — Terminology](001-terminology.md) | Accepted | None | Consistency across packages versus preserving subsystem-specific vocabulary. |
| 2 | [002 — Mesh representations](002-mesh-representations.md) | Accepted | 001 | Retain distinctly ephemeral `Tessellation` versus adding mesh/surface containers that imply persistence or topology. |
| 3 | [003 — Strategy objects](003-strategy-objects.md) | Accepted | 001 | One serializable strategy hierarchy with explicit native, one-parameter, two-parameter, deflection, and adaptive policies. |
| 4 | [004 — Error contracts](004-error-contracts.md) | Superseded by 016 | 001, 003 | Historical capability/error design; removed after implementation showed no consumer or backend result source. |
| 5 | [005 — Output topology](005-output-topology.md) | Accepted | 001, 002, 003 | Fresh `polygonize(strategy) -> PolygonalSurface` preserves natural cells with explicit dimensional strategy support. |
| 6 | [006 — Tessellation API](006-tessellation-api.md) | Accepted | 002, 003, 005 | Symmetric `polygonize`/`tessellate` operations plus explicit polygonize-then-triangulate control, without cached/scalar/topology-flag alternatives. |
| 7 | [007 — Triangulation operations](007-triangulation-operations.md) | Accepted | 001, 002, 005 | Serializable diagonal/ear-clipping face strategies with explicit mutation, key, attribute, and vertex-insertion semantics. |
| 8 | [008 — Triangle interoperability](008-triangle-interoperability.md) | Accepted | 002, 005, 006, 007 | `Tessellation` as the sole plugin input versus a universal conversion facade or public input union. |
| 9 | [009 — Trimmed surfaces](009-trimmed-surfaces.md) | Accepted | 003, 004, 006 | BRep ownership of trims versus expanding standalone NURBS surface semantics. |
| 10 | [010 — Metadata and provenance](010-metadata-provenance.md) | Accepted | 002, 003, 004, 009 | Defer enriched results; keep stable simple returns and require a future ADR for operation-specific metadata APIs. |
| 11 | [011 — Planar triangulation contract](011-planar-triangulation-contract.md) | Accepted | 001, 003, 004, 007, 008 | Tolerance-checked planar APIs preserve input coordinates exactly and lift generated vertices onto the selected plane. |
| 12 | [012 — Plugin boundaries](012-plugin-boundaries.md) | Accepted | 008, 011 | Core `Tessellation` validation/extraction with backend-owned native coercion versus divergent direct package APIs. |
| 13 | [013 — Compatibility](013-compatibility.md) | Accepted | 006, 007, 009, 010, 011, 012 | COMPAS 3.0 synchronized breaking baseline versus staged aliases and mixed-version contracts. |
| 14 | [014 — Continuous geometry materialization](014-continuous-geometry-materialization.md) | Accepted | 003, 005, 006, 013 | Defining analytic state only, with explicit fresh operations and no stored resolution or derived caches. |
| 15 | [015 — Continuous bounds](015-continuous-bounds.md) | Accepted | 014 | Certified continuous enclosures versus sampled bounds; minimum-volume OBB semantics versus parameter-frame boxes. |
| 16 | [016 — Capability discovery](016-capability-discovery.md) | Accepted | 003, 004, 010, 013 | Remove unused runtime discovery and error schemas versus retaining speculative public contracts. |
| 17 | [017 — Mixed-face triangulation](017-mixed-face-triangulation.md) | Accepted | 003, 007, 013 | Composite quad/n-gon policy versus one algorithm, fallback lists, or arity maps. |
| 18 | [018 — Robust polygon triangulation](018-robust-polygon-triangulation.md) | Accepted | 003, 007, 011, 012, 017 | Tiered strict/projection/arrangement contracts versus one opaque universal strategy. |
| 19 | [019 — Twisted polygon triangulation](019-twisted-polygon-triangulation.md) | Accepted | 003, 007, 017 | Minimum-area 3D dynamic programming versus a misattributed or speculative multi-objective policy. |
| 20 | [020 — Planar Delaunay naming](020-planar-delaunay-naming.md) | Accepted | 003, 011, 012, 013 | Explicit planar operation names while retaining standard Delaunay strategy names. |
| 21 | [021 — Default tessellation strategy](021-default-tessellation-strategy.md) | Accepted | 003, 006, 014 | Deterministic Shape/Surface defaults versus mandatory policy or backend-chosen defaults. |
| 22 | [022 — Operation concepts and conversion boundaries](022-operation-terminology-and-producer-boundaries.md) | Proposed | 001, 002, 009; Typing 012–013 | Representation-oriented `to_*` APIs backed by structured polygonization, discrete triangulation, or BRep tessellation as appropriate. |
| 23 | [023 — BRep conversion deflection defaults](023-brep-deflection-defaults.md) | Proposed | 022 | Deterministic core tolerance defaults versus mandatory values or backend-owned defaults. |

## Dependency graph

```text
001 <- none
002 <- 001
003 <- 001
004 <- 001, 003
005 <- 001, 002, 003
006 <- 002, 003, 005
007 <- 001, 002, 005
008 <- 002, 005, 006, 007
009 <- 003, 004, 006
010 <- 002, 003, 004, 009
011 <- 001, 003, 004, 007, 008
012 <- 008, 011
013 <- 006, 007, 009, 010, 011, 012
014 <- 003, 005, 006, 013
015 <- 014
016 <- 003, 004, 010, 013
017 <- 003, 007, 013
018 <- 003, 007, 011, 012, 017
019 <- 003, 007, 017
020 <- 003, 011, 012, 013
021 <- 003, 006, 014
022 <- 001, 002, 009, Typing 012, Typing 013
023 <- 022
```

## Recommended implementation and review sequence

Apply and independently review the ADRs in numeric dependency order:

1. **Conceptual foundation:** ADRs 001–004 establish vocabulary,
   representation roles, serializable policies, and honest error semantics.
2. **Public geometry API:** ADRs 005–008 decide topology, public methods,
   mutation conventions, and the common triangle boundary.
3. **Specialized geometry and metadata:** ADRs 009–010 decide trim ownership
   and whether enriched results are optional envelopes.
4. **Cross-package integration:** ADRs 011–012 resolve the incompatible planar
   contract and native plugin boundary.
5. **Breaking transition:** ADR 013 should be reviewed last because the exact
   removals depend on all approved public contracts.
6. **Continuous-state cleanup and bounds:** implement ADR 014 after the explicit
   strategy operations it depends on, then implement ADR 015 without restoring
   any implicit discretization dependency.
7. **Capability cleanup:** ADR 016 supersedes the discovery and error-schema
   portion of ADR 004; remove those speculative APIs after explicit operations
   and validation are in place.
8. **Mixed-face triangulation:** ADR 017 supersedes the collection-level policy
   portion of ADR 007 and introduces explicit quad/n-gon dispatch.
9. **Robust polygon triangulation:** ADR 018 authorizes strict and projected
   face policies before any exact-intersection planar-arrangement plugin.
10. **Twisted polygons:** ADR 019 authorizes an opt-in minimum-area 3D leaf
    strategy and renames the low-level polygon helper.
11. **Planar operation naming:** ADR 020 makes planarity explicit in Delaunay
    operation names while retaining standard strategy names.
12. **Default tessellation:** ADR 021 relaxes the mandatory-strategy rule only
    for ephemeral Shape and Surface tessellation.
13. **Terminology reconciliation:** review Proposed ADR 022 before further
    triangulation/discretization implementation. If accepted, it supersedes
    the listed operation, strategy, and plugin-input clauses while preserving
    the unaffected representation, trim-ownership, bounds, and clean-break
    decisions.
14. **BRep defaults:** review Proposed ADR 023 independently after ADR 022;
    exact Typing ADR 015 signatures depend on both.

## Highest-impact accepted decisions

- Retain `Tessellation` because its distinct name communicates an ephemeral
  operation result and avoids confusion with serializable `PolygonalSurface`
  and half-edge `Mesh`; reject additional `TriangleSurface`, `TriangleMesh`,
  `QuadMesh`, and universal `TessellationResult` containers (ADR 002).
- All policies share `TessellationStrategy(Data)`: `Native` for fixed topology,
  `UGrid` for one-parameter shapes, `UVGrid` for two-parameter geometry, plus
  `Deflection` and `Adaptive`. `Capsule`, `Sphere`, and `Torus` use both
  `UVGrid` dimensions. Invalid type/dimension combinations error and dimensions
  are never ignored (ADR 003).
- Runtime capability discovery and its reserved error schemas are removed
  without replacement. Producers validate explicit strategies directly and
  document support; discovery or measured-error results return only for a
  concrete future consumer and backend source (ADR 016, superseding ADR 004).
- Discretization is the broad umbrella; continuous surface-like geometry uses
  fresh, non-mutating `polygonize(strategy) -> PolygonalSurface` for
  independent serializable natural-cell topology; curves remain `Polyline`,
  and `Mesh` requires an explicit `.to_mesh()` conversion (ADR 005).
- Direct `tessellate(strategy) -> Tessellation` remains canonical for triangles;
  callers who care about face triangulation use
  `polygonize(strategy).triangulated(triangulation_strategy)`. Connectivity may
  differ when geometry and documented seam/boundary behavior remain consistent
  (ADR 006).
- Discrete triangulation uses serializable `DiagonalSplit` and `EarClipping`
  strategies with deterministic diagonals, standard tolerance, explicit
  mutation/attribute/key behavior, and no initial vertex insertion (ADR 007).
- Mixed collections use `FaceTriangulation` for explicit arity dispatch.
  `ProjectedEarClipping` is an explicit bounded-deviation interpretation of
  near-planar rings, while `MinimumAreaTriangulation` handles twisted ordered
  3D boundaries without projection and documents that its combinatorial disk
  may geometrically self-intersect (ADRs 017–019).
- Planar Delaunay operations are named `triangulate_planar_points` and
  `triangulate_planar_domain`; the conventional `Delaunay`,
  `ConstrainedDelaunay`, and `ConformingDelaunay` strategy names remain concise
  (ADR 020).
- Ephemeral Shape and Surface tessellation accepts an omitted strategy and
  resolves it deterministically to `Native()`, `UGrid(64)`, or
  `UVGrid(64, 64)` according to geometry arity. Persistent polygonization and
  deflection-based BRep/BRepFace tessellation remain explicit (ADR 021).
- Trims remain owned by BRep faces/BReps instead of changing standalone
  `NurbsSurface` (ADR 009).
- Enriched tessellation results are deferred: initial APIs have no report flag,
  union return, universal report/result wrapper, or parallel detailed method.
  Any future enriched operation requires its own ADR, concrete consumer/backend
  source, named API, and operation-specific stable result type (ADR 010).
- Planar triangulation uses separate serializable Delaunay strategies,
  validated model-unit/degree quality targets, tolerance-checked world/frame
  planes, exact input-coordinate preservation, and on-plane generated Steiner
  vertices (ADR 011).
- Plugins accept only `Tessellation` through one core-dispatched API; core owns
  validation/buffer extraction while backend helpers own native coercion, with
  raw tuples and divergent direct APIs relegated to internals (ADRs 008, 012).
- All superseded APIs are removed in the coordinated COMPAS 3.0 breaking
  release without compatibility aliases or a deprecation period. Affected
  plugins require `compas>=3.0.0`; existing major upper bounds advance to `<4`
  where used (ADR 013).
- Continuous geometry retains no stored resolution or derived discretization
  caches. Materialization occurs only through explicit fresh operations; exact
  shape-specific finite data such as `Box.points` remains available (ADR 014).

- Continuous bounds use exact parameter-derived AABBs for analytic shapes and
  full-domain analytic surfaces, certified-only NURBS bounds, and retain
  minimum-volume `obb` semantics with unsupported cases instead of sampled or
  parameter-frame fallbacks (ADR 015).
- Runtime tessellation capability discovery and unused error schemas are
  removed without replacement; explicit operations validate their strategies
  directly (ADR 016, superseding ADR 004).

## Status policy

- **Proposed:** recommended but not explicitly approved.
- **Accepted:** explicitly approved and authoritative for implementation.
- **Superseded:** historically accepted, but no longer implementation authority
  where a later Accepted ADR replaces it.
- **Rejected:** the architectural decision itself was explicitly rejected;
  rejected alternatives inside an ADR do not change its status.

The Accepted ADRs define the implementation architecture. Implementation,
review, merge, and publication remain subject to the ownership, testing, and
coordination rules in `AGENTS.md`.
