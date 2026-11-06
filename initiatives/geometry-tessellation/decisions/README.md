# Geometry Tessellation Architecture Decisions

This directory decomposes the architecture proposal into independently
reviewable decisions. ADRs 001–023 are **Accepted**. ADR 024 is **Proposed**
and does not authorize implementation. ADRs 022–023 reconcile the earlier
architecture with the user-authored operation definitions. The target
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
| 22 | [022 — Operation concepts and conversion boundaries](022-operation-terminology-and-producer-boundaries.md) | Accepted | 001, 002, 009; Typing 012–013 | Representation-oriented `to_*` APIs backed by structured polygonization, discrete triangulation, or BRep tessellation as appropriate. |
| 23 | [023 — BRep conversion deflection defaults](023-brep-deflection-defaults.md) | Accepted | 022 | Deterministic core tolerance defaults versus mandatory values or backend-owned defaults. |
| 24 | [024 — Representation-preserving Mesh triangulation](024-representation-preserving-mesh-triangulation.md) | Proposed | 002, 007, 022; Typing 015 | Preserve `Mesh` type, topology, keys, and attributes versus a universal ephemeral result. |

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
024 <- 002, 007, 022, Typing 015
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
13. **Terminology reconciliation:** implement accepted ADR 022 before further
    triangulation/discretization integration. It supersedes the listed
    operation, strategy, and plugin-input clauses while preserving the
    unaffected representation, trim-ownership, bounds, and clean-break
    decisions.
14. **BRep defaults:** implement accepted ADR 023 after ADR 022; exact accepted
    Typing ADR 015 signatures depend on both.
15. **Mesh result correction:** ADR 024 is a proposed amendment based on new
    evidence. Do not implement the `Mesh.triangulated() -> Self` change until
    it is explicitly accepted.

## Highest-impact accepted decisions

- Retain `Tessellation` because its distinct name communicates an ephemeral
  operation result and avoids confusion with serializable `PolygonalSurface`
  and half-edge `Mesh`; reject additional `TriangleSurface`, `TriangleMesh`,
  `QuadMesh`, and universal `TessellationResult` containers (ADR 002).
- Public strategy hierarchies are removed. Shapes and untrimmed surfaces use
  producer-owned cell-count keywords; BReps use explicit linear/angular
  deflection keywords; numerical triangulation uses named functions and
  structural buffers (ADR 022 and Typing ADR 015, superseding affected clauses
  of ADR 003).
- Runtime capability discovery and its reserved error schemas are removed
  without replacement. Producers validate explicit strategies directly and
  document support; discovery or measured-error results return only for a
  concrete future consumer and backend source (ADR 016, superseding ADR 004).
- Shapes and untrimmed surfaces expose fresh, non-mutating
  `to_polygonal_surface(...)` and exact composed `to_tessellation(...)`
  conversions. BReps expose only precision-controlled `to_tessellation(...)`;
  public `polygonize` and `tessellate` verbs are removed (ADR 022, superseding
  affected clauses of ADRs 005–006).
- Discrete triangulation uses named functions and an optional duck-typed
  aggregate triangulator callable. Omitted and explicit `None` selectors use
  the default polygon triangulator. Nominal face-strategy objects are removed
  without aliases (Typing ADR 015, superseding affected clauses of ADR 007).
- Named strict/projected/minimum-area polygon functions retain the approved
  algorithms for planar, near-planar, and twisted ordered rings without the
  superseded nominal strategy classes (ADRs 017–019 and Typing ADR 015).
- Named Delaunay functions operate only on planar domains and return structural
  vertex/triangle buffers. The `Delaunay`, `ConstrainedDelaunay`, and
  `ConformingDelaunay` flag classes are removed (Typing ADR 015, superseding
  the naming choice in ADR 020).
- Shape and Surface conversions resolve producer-owned cell-count defaults;
  BRep/BRepFace conversions resolve omitted deflections from core tolerance
  before plugin dispatch (ADRs 022–023, superseding affected clauses of ADR
  021).
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
- Numerical plugins accept core-owned structural buffers and normalize once at
  native boundaries; `Tessellation` remains a useful representation but is not
  a mandatory algorithm gate (Typing ADRs 012 and 015–017, superseding affected
  clauses of Geometry ADRs 008 and 012).
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
