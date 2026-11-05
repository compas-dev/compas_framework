# Typing Alignment Implementation Plan

## Status

Approved. ADRs 001–011 are Accepted. Implementation may proceed in dependency
order, preserving duck typing through Python code and limiting normalization to
explicit hard boundaries. The `compas_cgal` branch `initiative/typing-alignment`
was created from modernization commit `d31ec0f`, and WP4 has started.

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

**Ownership:** `compas._typing`, datastructure type aliases, focused static and
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

**Status:** in progress on `initiative/typing-alignment`, based on modernization
commit `d31ec0f`.

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
- Verify CGAL stubs in installed wheels and against native exports.
- Type-check an external installed-package consumer.
- Run lowest/latest NumPy runtime and typing matrices.
- Run native import/ABI tests, full feasible tests, Ruff, format, Pyright, and
  documentation builds.
- Independently review remaining ignores and runtime changes.

**Depends on:** WP0–WP5; ADRs 009–010.

### WP7 — Representation and numerical-boundary correction

**Status:** partially approved. ADRs 012–014 are Accepted. ADR 015 is Proposed
and supplies the exact API table needed for WP7.4–WP7.7. Those work packages
remain blocked pending explicit approval of ADR 015. Retained `Tessellation`
representation semantics remain in scope.

#### Affected-API migration table

| Slice | Current public boundary | Approved destination | Principal dependents |
|---|---|---|---|
| Structural vocabulary | `Tessellation` or package-local `VerticesFaces` | One core `TriangleMeshInput` structural buffer contract; exact local NumPy result aliases | Core typing fixtures; CGAL native boundaries |
| Mesh booleans | Public pluggables require and return `Tessellation` | Public raw-buffer dispatch plus private `_boolean_*` hooks; one backend conversion, minimal native-safety checks, native failure propagation, and shape-checked structural results | CGAL Boolean plugin/wrappers; `Polyhedron` Boolean methods |
| Intersection and slicing | `Tessellation` mesh inputs | Structural mesh inputs; existing polyline/hit results | CGAL intersection/slicer plugins and examples |
| Remeshing | `Tessellation` input/result | Structural mesh input/result | CGAL meshing plugin; Boolean documentation |
| Curvature, parameterization, geodesics, isolines, matrices | `Tessellation` mesh input | Structural mesh input; existing scalar/vector results | Each installed backend and core plugin fixtures |
| Planar Delaunay | `triangulate_planar_*` plus nominal strategy flags; `Tessellation` result | Named planar Delaunay/constrained/conforming operations and private hooks; structural result; no implicit curved-domain projection | CGAL triangulation; `Mesh.from_points` |
| Polygon triangulation | Public strategy hierarchy and nested `FaceTriangulation` | Named operations; aggregate triangulator callable where approved; distinct no-argument region conversion | `Polygon`, `PolygonalSurface`, `Polyhedron`, `Mesh`, `PlanarRegion` |
| Shape/surface tessellation | `Native`, `UGrid`, `UVGrid`, `Adaptive` | Producer-specific keyword-only resolution or approximation controls | Shape/surface tests, examples, scene conversion |
| BRep tessellation | `Deflection` strategy | Explicit linear/angular deflection keywords with documented units | Core BRep, `compas_occ`, examples |
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
4. **WP7.4 — Named planar triangulation.** **Blocked by Proposed ADR 015.**
   Replace nominal Delaunay flags and
   migrate CGAL plus `Mesh.from_points` in one cross-package slice. Reject
   non-planar inputs outside tolerance and keep non-planar polygon
   triangulation on its separate path.
5. **WP7.5 — Polygon triangulation operations.** **Blocked by Proposed ADR
   015.** Replace nested strategy objects using the approved named-operation
   and aggregate-callable table for `Polygon`, `PolygonalSurface`,
   `Polyhedron`, and `Mesh`. Migrate `PlanarRegion` separately to its
   no-argument `triangulated`, `to_polygonal_surface`, and `to_mesh` contract;
   it does not accept the aggregate triangulator callable.
6. **WP7.6 — Producer-specific controls.** **Blocked by Proposed ADR 015.**
   Migrate shapes/surfaces, then core
   BRep and OCC together. Preserve no-argument generic tessellation.
7. **WP7.7 — Export and integration cleanup.** **Blocked by Proposed ADR
   015.** Remove obsolete decorators,
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

No additional architectural approval is required for completed WP7.1–WP7.3
work that follows ADRs 012–014. WP7.4–WP7.7 require approval of ADR 015 before
source migration. Stop if a released compatibility obligation, a result
requiring metadata beyond buffers, a backend incompatibility, a new
representation class, an implicit conversion, or a second public path becomes
necessary.

## Dependency graph

```text
WP0 -> WP1 -> WP2
          \-> WP3 -> WP4
                  \-> WP5
WP0 + WP2 + WP4 + WP5 -> WP6
WP1 -> WP7.1 -> WP7.2 -> WP7.3
          \-> WP7.4 -> WP7.5
WP7.0 -> WP7.6
ADR015 -> WP7.4, WP7.5, WP7.6, WP7.7
ADR014 -> WP7.3 -> WP7.7
WP7.2 + WP7.3 + WP7.4 + WP7.5 + WP7.6 -> WP7.7 -> WP6
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
- all three packages have zero Pyright errors in the approved scope;
- no broad/global suppressions or frozen error baseline exist;
- NumPy acceptance matches annotations and runtime tests;
- plugin implementations conform to core contracts;
- native ABI normalization and ownership are documented and tested;
- `py.typed` and CGAL stubs are present in built wheels;
- external installed-package consumers type-check;
- relevant/full feasible tests, Ruff, formatting, Pyright, docs, and independent
  review pass.

## Explicitly deferred

- universal tensor/shape typing;
- changing runtime behavior solely for checker convenience;
- typing optional ecosystem packages outside initial scope;
- automatic stub generation without evidence it improves contracts;
- speculative serialization schema hierarchies.
