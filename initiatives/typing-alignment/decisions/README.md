# Typing Alignment Architecture Decisions

Decisions 001–017 are **Accepted** and implemented for the approved initiative
scope. Their source, distribution, package-hosted, and exact installed-candidate
verification gates pass on the recorded initiative heads.

## Decision index

| Order | ADR | Status | Depends on | Main tradeoff |
|---:|---|---|---|---|
| 1 | [001 — Supported baseline](001-supported-baseline.md) | Accepted | None | One truthful modern baseline versus historical package combinations. |
| 2 | [002 — Numeric and array inputs](002-numeric-array-inputs.md) | Accepted | 001 | Explicit Python/NumPy unions versus sequence-only or overly broad ArrayLike. |
| 3 | [003 — Array guarantees](003-array-guarantees.md) | Accepted | 001, 002 | Static dtype plus runtime shape/layout versus speculative shape typing. |
| 4 | [004 — Tessellation buffers](004-tessellation-buffers.md) | Accepted | 002, 003 | Preserve zero-copy concrete buffers versus normalized containers. |
| 5 | [005 — Native normalization](005-native-normalization.md) | Accepted | 002, 003, 004 | Broad public input with exact private ABI buffers versus exposing native requirements. |
| 6 | [006 — Plugin conformance](006-plugin-conformance.md) | Accepted | 002, 005 | Core-owned validated signatures versus generic backend forwarding. |
| 7 | [007 — Backend substitutability](007-backend-substitutability.md) | Accepted | 001, 005, 006 | Core-compatible OCC APIs versus backend-specialized incompatible overrides. |
| 8 | [008 — Return normalization](008-return-normalization.md) | Accepted | 002, 004, 005, 006, 007 | Python/core defaults with explicit NumPy exceptions versus one universal representation. |
| 9 | [009 — Typed distribution](009-typed-distribution.md) | Accepted | 001, 005, 006, 007, 008 | Verified PEP 561 packages and maintained stubs versus development-only typing. |
| 10 | [010 — Verification ratchet](010-verification-ratchet.md) | Accepted | 001–009 | Full consumer/native/wheel verification versus source-only checks or suppression baselines. |
| 11 | [011 — BRep query truthfulness](011-brep-query-truthfulness.md) | Accepted | 006–008 | Explicit independent failure for unsupported semantics versus false or empty placeholders. |
| 12 | [012 — Structural triangle-mesh boundaries](012-structural-triangle-mesh-boundaries.md) | Accepted | 002–006 | Raw structural buffers versus mandatory `Tessellation` objects at numerical boundaries. |
| 13 | [013 — Explicit algorithms and discretization controls](013-explicit-algorithms-and-discretization-controls.md) | Accepted | 012 | Named operations and producer-specific keywords versus public strategy-object hierarchies. |
| 14 | [014 — Discrete curvature contracts](014-discrete-curvature-contracts.md) | Accepted | 012 | Keep only verified core Gaussian curvature versus preserving unsupported or incompatible plugin contracts. |
| 15 | [015 — Exact triangulation and discretization APIs](015-exact-triangulation-and-discretization-apis.md) | Accepted | 012–013, 016, Geometry 022–023 | Duck-typed triangulation plus exact representation-oriented structured/BRep conversion signatures versus inventing the API during implementation. |
| 16 | [016 — Core structural type vocabulary](016-core-structural-type-vocabulary.md) | Accepted | 002–005, 008, 012 | One layered coordinate protocol with semantic NumPy-aware `PointLike`/`VectorLike` aliases and one neutral `VerticesFaces` vocabulary versus overlapping names. |
| 17 | [017 — Native binding stubs and public contracts](017-native-binding-stubs-and-public-contracts.md) | Accepted | 005–006, 008–010, 016 | Exact private native stubs plus coordinated complete wrappers versus package-specific stubs and ignores. |

## Dependency graph

```text
001 <- none
002 <- 001
003 <- 001, 002
004 <- 002, 003
005 <- 002, 003, 004
006 <- 002, 005
007 <- 001, 005, 006
008 <- 002, 004, 005, 006, 007
009 <- 001, 005, 006, 007, 008
010 <- 001, 002, 003, 004, 005, 006, 007, 008, 009
011 <- 006, 007, 008
012 <- 002, 003, 004, 005, 006
013 <- 012
014 <- 012
016 <- 002, 003, 004, 005, 008, 012
015 <- 012, 013, 016, Geometry 022, Geometry 023
017 <- 005, 006, 008, 009, 010, 016
```

## Recommended review order

1. Approve the baseline and public numeric/array vocabulary (001–003).
2. Decide zero-copy and native boundaries (004–005).
3. Decide cross-package API conformance (006–008).
4. Decide distribution and verification commitments (009–010).
5. Decide how partially supported OCC BRep queries fail (011).
6. Reconsider triangle-mesh algorithm boundaries and public strategy objects
   in light of direct NumPy use and namespace clarity (012–013).
7. Resolve the shared structural vocabulary and core constructor contract
   (016), then approve the exact polygon, Delaunay, shape/surface, and BRep
   migration table, especially the aggregate triangulator callable (015).
8. Approve the common CGAL/libigl native-stub, public-wrapper, completeness,
   and artifact-verification policy (017).

## Highest-impact approvals

- NumPy arrays/scalars become first-class inputs only where tested runtime
  support is intentional.
- `Tessellation` remains a zero-copy retained-buffer exception.
- Public coercible inputs and exact native buffers are separate contracts.
- OCC aligns to core signatures rather than preserving incompatible override
  annotations.
- Ordinary APIs return Python/core values; NumPy outputs remain explicit.
- Core, OCC, CGAL, and libigl become verified PEP 561 typed distributions.
- Core owns one `VerticesFaces` structural type; `TriangleMeshInput` and the
  tuple-valued `MeshType` are removed without aliases.
- CGAL and libigl native modules ship accurate stubs, and supported public
  surfaces reach 100% known type completeness.
