# Typing Alignment Implementation Plan

## Status

ADRs 001–017 and Geometry ADRs 022–023 are Accepted. Remaining work may proceed
in dependency order, preserving duck typing through Python code and limiting
normalization to explicit hard boundaries. Acceptance authorizes the exact
geometry API, shared vocabulary, and native-binding alignment work; it does not
mark those source or verification slices complete.

Hosted draft-PR checks are green for the current pushed checkpoints: core PR
1539 at `4973c5fcfc53f0217a5fca20d0765e74b30459e2`, OCC PR 32 at
`5a4cf9701007266e517996181c8476488c4030d9`, CGAL PR 81 at
`a46eecab71de5dfea6df7380d2eafb7185cc789a`, and libigl PR 47 at
`86e3f1e0e02d6dc7cf9ad8049ac57c4c7d801877`. Those runs prove the
existing package, platform, and typed-wheel checkpoints only. WP7.4–WP7.7 and
WP8 are now authorized but remain unimplemented and unverified.

## Work packages

### WP0 — Baseline, tooling, and fixtures

**Ownership:** `compas_framework`; metadata/CI files in each package.

- Align Python, COMPAS, NumPy, and Pyright versions.
- Add authoritative `compas3` commands.
- Define typed consumer-fixture conventions.
- Add initial wheel-content checks.

**Depends on:** ADR 001.

**Gate:** identical supported baseline and reproducible Pyright invocation.

### WP1 — Core numeric and array vocabulary

**Ownership:** public `compas.typing`, datastructure type aliases, focused static and
runtime tests.

- Add approved real/integral, coordinate, collection, and index input aliases.
- Consolidate duplicate aliases.
- Add Python/NumPy scalar and array fixtures.
- Document static versus runtime guarantees.

**Depends on:** WP0; ADRs 002–003.

**Gate:** valid NumPy calls type-check; invalid runtime cases fail explicitly.

### WP2 — Core retained buffers and returns

**Ownership:** `Tessellation`, Mesh construction boundaries, selected scalar
return APIs.

- Expand retained buffer generic bounds without coercion.
- Align normals, UVs, and polylines.
- Preserve concrete buffer inference and ownership behavior.
- Normalize approved ordinary scalar returns.

**Depends on:** WP1; ADRs 004 and 008.

**Gate:** zero-copy/ownership tests and typed consumers pass.

### WP3 — Plugin contracts

**Ownership:** core pluggable modules and matching OCC/CGAL plugin modules.

- Separate public wrappers that enforce necessary documented invariants from
  narrow private pluggables where needed.
- Replace known generic forwarding with explicit signatures.
- Add signature and typed result conformance tests.

**Depends on:** WP1 and relevant parts of WP2; ADR 006.

**Parallelism:** independent plugin families may proceed in parallel after the
core signature for that family is fixed.

**BRep query rule:** curve, surface, and other BRep signatures and forwarding
tests may proceed independently. Implement the OCC BRep classification and
topology queries through independently failing contracts as approved in ADR
011; do not encode unsupported semantics as `False` or `[]`.

### WP4 — CGAL NumPy and native stubs

**Status:** current checkpoint hosted-verified on draft PR 81 at `a46eecab`,
with the deeper stub correction and 100% completeness contract scheduled in
accepted WP8.2. The branch is based on modernization commit `d31ec0f`.

**Ownership:** `compas_cgal` wrapper modules, `types.py`, native stubs, native
boundary tests, packaging.

- Standardize broad public inputs.
- Normalize exact `float64`/`int32` C-contiguous ABI buffers.
- Remove obsolete core-boundary ignores.
- Align result representations with core.
- Add stub export parity, typed smoke, and wheel checks.

**Depends on:** WP1–WP3; ADRs 003–006 and 009.

**Parallelism:** independent native module families may use separate owners.

**Known correctness limitation:** current `compas_cgal` skeletonisation results
are not correct. WP4 may align its Python/native signatures and distribution
artifacts, but must not mark skeletonisation behavior as verified. Functional
verification remains open pending a separate diagnosis and geometry regression
tests.

### WP5 — OCC core-contract alignment

**Status:** current pushed checkpoint hosted-verified on draft PR 32 at
`5a4cf970`; further work that depends on the accepted geometry/type vocabulary
remains pending with WP7–WP8.

**Ownership:** separate non-overlapping families:

1. curves;
2. surfaces and NURBS;
3. BRep components;
4. conversions and SWIG boundary helpers;
5. plugins;
6. serialization and tests.

For each family:

- fix stale core API use and override substitutability;
- centralize native downcasts/conversions;
- add intentional NumPy normalization only where approved;
- replace broad ignores with narrow documented boundary exceptions;
- add runtime and typed base-class consumer tests.

**Depends on:** WP1 and the relevant WP3 contract; ADRs 005–008.

**Parallelism:** families can proceed in parallel with explicit file ownership.

### WP6 — Typed distribution and integration

**Ownership:** package build configuration plus `compas_framework` integration
and independent review.

- Ship and verify `py.typed` in all wheels.
- Verify CGAL and libigl stubs in installed wheels and against native exports.
- Type-check an external installed-package consumer.
- Run lowest/latest NumPy runtime and typing matrices.
- Run native import/ABI tests, full feasible tests, Ruff, format, Pyright, and
  documentation builds.
- Independently review remaining ignores and runtime changes.

**Depends on:** WP0–WP5, WP7.7, and WP8.4; ADRs 009–010 and every Accepted
decision governing the integrated public/native surface.

### WP7 — Representation and numerical-boundary correction

**Status:** approved and in progress. ADRs 012–016 and Geometry ADRs 022–023
supply the exact API and structural vocabulary needed for WP7.4–WP7.7. Those
work packages are authorized in dependency order and remain incomplete.
Retained `Tessellation` representation semantics remain in scope.

#### Affected-API migration table

| Slice | Current public boundary | Approved destination | Principal dependents |
|---|---|---|---|
| Structural vocabulary | `Tessellation`, `TriangleMeshInput`, tuple-valued `MeshType`, or package-local `VerticesFaces` | One core `VerticesFaces` structural contract; exact concrete result aliases | Core typing fixtures; CGAL/libigl native boundaries |
| Mesh booleans | Public pluggables require and return `Tessellation` | Public raw-buffer dispatch plus private `_boolean_*` hooks; one backend conversion, minimal native-safety checks, native failure propagation, and shape-checked structural results | CGAL Boolean plugin/wrappers; `Polyhedron` Boolean methods |
| Intersection and slicing | `Tessellation` mesh inputs | Structural mesh inputs; existing polyline/hit results | CGAL intersection/slicer plugins and examples |
| Remeshing | `Tessellation` input/result | Structural mesh input/result | CGAL meshing plugin; Boolean documentation |
| Curvature, parameterization, geodesics, isolines, matrices | `Tessellation` mesh input | Structural mesh input; existing scalar/vector results | Each installed backend and core plugin fixtures |
| Planar Delaunay | `triangulate_planar_*` plus nominal strategy flags; `Tessellation` result | Named planar Delaunay/constrained/conforming operations and private hooks; structural result; no implicit curved-domain projection | CGAL triangulation; `Mesh.from_points` |
| Polygon triangulation | Public strategy hierarchy and nested `FaceTriangulation` | Named operations; aggregate triangulator callable where approved; distinct no-argument region conversion | `Polygon`, `PolygonalSurface`, `Polyhedron`, `Mesh`, `PlanarRegion` |
| Shape/surface conversion | `polygonize`/`tessellate` plus `Native`, `UGrid`, `UVGrid`, `Adaptive` | `to_polygonal_surface`/`to_tessellation` with producer-specific keyword-only resolution controls and one shared structured path | Shape/surface tests, examples, scene conversion |
| BRep conversion | `polygonize`/`tessellate` plus `Deflection` strategy | `to_tessellation` only, with explicit linear/angular deflection keywords and documented units | Core BRep, `compas_occ`, examples |
| Cleanup | `tessellation_pluggable`, strategy exports and serialization | Remove after all consumers migrate | Core exports, docs, installed-wheel consumers |

#### Dependency-ordered work packages

1. **WP7.1 — Structural triangle contract.** Add the authoritative buffer alias
   and static/runtime fixtures without changing algorithms.
2. **WP7.2 — Boolean pilot.** Prove public-wrapper/private-hook dispatch and
   direct CGAL raw-buffer use before migrating other families.
3. **WP7.3 — Remaining triangle operations.** Migrate independent
   intersection/slicing, remeshing, curvature, parameterization,
   geodesic/isoline, and matrix families with their actual backends.
   `compas_libigl` is included from `c3-upgrade` commit `70acf99`; repair its
   remesh-along-isoline registration before migrating its ray intersection,
   geodesic, isoline, mass-matrix, harmonic, and LSCM hooks. Curvature remains
   separate because the Rhino principal-curvature result contract conflicts
   with core. Accepted ADR 014 retains only verified core Gaussian angle defect
   and removes unsupported mean/principal core hooks after the verified libigl
   modernization checkpoint is integrated.
4. **WP7.4 — Named planar triangulation.** **Authorized by Accepted ADRs
   015–016.**
   Replace nominal Delaunay flags and
   migrate CGAL plus `Mesh.from_points` in one cross-package slice. Reject
   non-planar inputs outside tolerance and keep non-planar polygon
   triangulation on its separate path.
5. **WP7.5 — Polygon triangulation operations.** **Authorized by Accepted ADRs
   015–016.** Replace nested strategy objects using the approved named-operation
   and aggregate-callable table for `Polygon`, `PolygonalSurface`,
   `Polyhedron`, and `Mesh`. Omitted and explicit `None` aggregate selectors
   both resolve to the default `triangulate_polygon`; a provided callable is
   the only customization path. Migrate `PlanarRegion` separately to its
   no-argument `triangulated`, `to_polygonal_surface`, and `to_mesh` contract;
   it does not accept the aggregate triangulator callable.
   Accepted Geometry ADR 024 changes only `Mesh.triangulated(...)` from
   `Tessellation` to `Self`. Implement that representation-preserving Mesh
   slice and its coordinated consumers; the other aggregate return contracts
   remain unchanged.
6. **WP7.6 — Producer-specific controls.** **Authorized by Accepted Typing ADRs
   015–016 and Geometry ADRs 022–023.** Migrate shape/surface representation
   conversions, then core BRep and OCC together. Preserve documented
   no-argument generic conversions through deterministic defaults.
7. **WP7.7 — Export and integration cleanup.** **Authorized by Accepted ADRs
   015–017.** Remove obsolete decorators,
   strategy classes, exports, serialization fixtures, and documentation only
   after their dependents have migrated.

Every vertical slice must verify Python and NumPy inputs, C/Fortran/sliced/
read-only buffers, source non-mutation, semantic failures, exact native
normalization, signature parity, direct backend use, explicit representation
conversion, full feasible tests, Ruff, Pyright, documentation, and independent
review.

Core wrappers do not duplicate backend conversion or proactively recompute
mesh topology. Backend checks are limited to what its native implementation
needs for process safety, followed by native success/failure propagation and
result-shape verification. Geometric validity remains a documented algorithm
precondition unless an operation explicitly requires a different contract.

No additional architectural approval is required for WP7.1–WP7.7. Correct the
superseded alias vocabulary under accepted ADR 016 and execute the remaining
work packages in dependency order. Stop if a released
compatibility obligation, a result
requiring metadata beyond buffers, a backend incompatibility, a new
representation class, an implicit conversion, or a second public path becomes
necessary.

### WP8 — Shared vocabulary and native-binding truthfulness

**Status:** Accepted and authorized; source implementation and verification are
pending.

#### WP8.1 — Core vocabulary and constructor interoperability

**Ownership:** public `compas.typing`, removal of private `compas._typing`,
affected core constructors, static/runtime fixtures, and public documentation.

- replace `TriangleMeshInput` and tuple-valued `MeshType` with the sole neutral
  `VerticesFaces` structural alias;
- distinguish protocol, semantic accepted-input, structural interchange, and
  concrete result names according to ADR 016, using one rich indexed/sliced
  `CoordinateProtocol` and structurally identical `PointLike`/`VectorLike`
  unions for positional and directional roles;
- migrate quaternion and generic linear-algebra consumers to neutral
  `FloatSequenceLike` over `RealInput`, preserving existing direct arithmetic
  without new conversions, validation, casts, or ignores for typing;
- lock the static `RealInput`-to-`SupportsFloat` relationship with explicit
  union and concrete Python/NumPy scalar fixtures, including direct
  one-dimensional `PointLike`/`VectorLike` element assignment to representative
  `Point`/`Vector` component setters without conversion, cast, or ignore;
- make core `Point` and `Vector` explicitly conform to
  `CoordinateProtocol[float]`, preserve the runtime-checkable coordinate and
  point-collection membership used by equality, and use only unparameterized
  protocols in those runtime guards;
- inventory every indexed consumer and migrate it to a semantic alias or exact
  result type with accepted/error static fixtures and runtime duck fixtures;
- forbid runtime protocols as general input-validation gates;
- migrate every core and integration consumer without aliases or shims;
- make copying core constructors accept the approved NumPy coordinate/index
  values and align corresponding setters that use the same normalization path;
  and
- correct `PolygonalSurface`/`Polyhedron` NumPy integral index handling during
  their existing ownership copy, without a separate validation pass.

**Depends on:** accepted ADR 016; WP1–WP2 and WP7.1–WP7.3 evidence.

#### WP8.2 — CGAL stub and wrapper correction

**Ownership:** `compas_cgal` native `.pyi`, `types.py`, wrappers, exports,
runtime ABI tests, typed consumers, and package verification.

- import the core broad vocabulary instead of redefining it;
- correct every measured native-stub/runtime mismatch;
- type every supported public wrapper and make exports explicit;
- retain exact concrete array and heterogeneous result aliases only where they
  describe actual CGAL results; and
- reach 100% known public type completeness and verify installed stubs.

**Depends on:** WP8.1 and accepted ADR 017.

#### WP8.3 — Libigl native stubs and public completion

**Ownership:** `compas_libigl` 13 private extension stubs, 21 public wrappers,
plugins, imports, consumers, and package verification.

- add one accurate `.pyi` for every compiled extension and remove broad import
  ignores;
- type dense arrays, sparse matrices, Python containers, and mixed results as
  actually returned;
- replace casts and old structural aliases with the core vocabulary; and
- reach 100% known public type completeness and verify every installed stub.

**Depends on:** WP8.1 and accepted ADR 017. WP8.2 and WP8.3 may proceed in
parallel with separate repository ownership.

#### WP8.4 — Cross-package installed integration

**Ownership:** `compas_framework` integration fixtures and independent review.

- install exact candidate wheels outside their checkouts;
- type-check every supported CGAL/libigl public family;
- pass applicable backend results directly into core constructors;
- verify no removed aliases, `.tolist()` workarounds, broad ignores, or casts
  mask the shared contract; and
- rerun the complete runtime, Pyright, Ruff, documentation, wheel, and native
  matrix after review.

**Depends on:** WP8.1–WP8.3; ADRs 016–017.

## Dependency graph

```text
WP0 -> WP1 -> WP2
          \-> WP3 -> WP4
                  \-> WP5
WP0 + WP2 + WP4 + WP5 + WP7.7 + WP8.4 -> WP6
WP1 -> WP7.1 -> WP7.2 -> WP7.3
          \-> WP7.4 -> WP7.5
WP7.3 -> WP7.6
Geometry ADR022 -> Geometry ADR023
Typing ADR016 -> WP8.1 -> WP8.2 -> WP8.4
Typing ADR016 -> WP8.1 -> WP8.3 -> WP8.4
Typing ADR015 + Typing ADR016 -> WP7.4, WP7.5
Typing ADR015 + Typing ADR016 + Geometry ADR022 + Geometry ADR023 -> WP7.6
Typing ADR015 + Typing ADR016 + Typing ADR017 -> WP7.7
ADR014 -> WP7.3 -> WP7.7
WP7.2 + WP7.3 + WP7.4 + WP7.5 + WP7.6 -> WP7.7
```

## Verification requirements per work package

- smallest relevant runtime tests first;
- typed consumer fixtures for changed public contracts;
- Ruff check and format verification;
- Pyright through `compas3` with zero new errors;
- `git diff --check`;
- documentation updated with each public contract;
- exact commands/results recorded in initiative status.

## Final exit criteria

- all ADRs governing implemented work are Accepted;
- core, OCC, CGAL, and libigl have zero Pyright errors in the approved scope;
- no broad/global suppressions or frozen error baseline exist;
- NumPy acceptance matches annotations and runtime tests;
- plugin implementations conform to core contracts;
- native ABI normalization and ownership are documented and tested;
- `py.typed` and all CGAL/libigl native stubs are present in built wheels;
- CGAL and libigl reach 100% known types for their intentionally exported
  public surfaces;
- external installed-package consumers type-check;
- relevant/full feasible tests, Ruff, formatting, Pyright, docs, and independent
  review pass.

## Explicitly deferred

- universal tensor/shape typing;
- changing runtime behavior solely for checker convenience;
- typing optional ecosystem packages outside initial scope;
- automatic stub generation without evidence it improves contracts;
- speculative serialization schema hierarchies.
