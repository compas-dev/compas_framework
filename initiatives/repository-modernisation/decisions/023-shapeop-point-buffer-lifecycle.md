# ADR 023: ShapeOp Point-Buffer Reassignment Lifecycle

**Status:** Proposed

## Context

After `Solver.init()`, `Solver.points` is a writable NumPy view into the native
solver's Eigen point matrix. Constraints, forces, factorization state, and
that exported view are owned by or tied to the same native solver.

Replacing the native wrapper while an exported array still references its
matrix can leave that array pointing at released memory. The modernization
candidate avoids this by storing every prior native wrapper in
`_retired_solvers`. Repeated reassignment therefore retains every prior point
matrix, constraint set, force set, and solver allocation until the Python
`Solver` is destroyed.

No current requirement establishes repeated post-initialization reuse of one
solver object. Retaining an unbounded native history is not an acceptable
implicit ownership contract.

## Options

1. **Reject point reassignment after initialization.** Keep the initialized
   point array writable in place. Require a new `Solver` or `MeshSolver` for a
   different point set.
2. **Attach native ownership to each exported zero-copy array.** Rebuild the
   wrapper on reassignment and arrange for every old array view to keep exactly
   its originating native solver alive until the last dependent view is
   collected. This preserves reassignment without permanent history but
   requires a new native lifetime contract across NumPy base objects, slices,
   and nanobind/Eigen return handling.
3. **Return owned copies instead of a native view.** Rebuilding becomes safe,
   but in-place updates no longer affect the solver and an explicit
   synchronization API would be required.
4. **Retain every previous native solver.** This preserves old exported views
   but creates unbounded, invisible memory retention.

## Recommendation

Choose option 1.

A solver accepts point assignment while it is uninitialized. A
pre-initialization reassignment starts a fresh configuration and clears
constraints and forces associated with the replaced point set. Once `init()`
succeeds, assignment to `solver.points` raises `RuntimeError` before conversion
or native mutation.

The initialized array remains a live writable view. Updating coordinates
through `solver.points[...]` is supported and remains distinct from assigning a
new array to the property. The view is valid only while its owning `Solver`
remains alive; callers must copy it if the result must outlive the solver. A
caller that needs another point set creates a new solver instance.

`MeshSolver` additionally binds its point rows to the mesh vertex-key mapping
established during construction. Before initialization, reassignment is
allowed only with exactly the same number of point rows; it replaces
coordinates without replacing mesh topology or the key-to-row mapping. A
different mesh or vertex count requires a new `MeshSolver`.

Do not add a reset method, copied-buffer mode, ownership wrapper, or retained-
solver compatibility layer without a demonstrated use case and a separate
decision.

## Consequences

The `_retired_solvers` history is removed and each Python solver retains only
its current native solver. Merely retaining a NumPy view is not promised to
keep native storage alive; the existing copy-to-outlive rule remains part of
the public ownership contract.

Code that assigns a new point array after initialization receives a clear
failure instead of an implicit reset. Its migration is to instantiate a new
solver. Code that updates the current native positions in place continues to
work without copying.

`MeshSolver` follows the same post-initialization lifecycle and additionally
rejects a pre-initialization point count that differs from its bound mesh.

## Verification

- Initialize a solver, retain its point view, and verify that assigning another
  point array raises `RuntimeError` with guidance to create a new solver.
- Verify the failed assignment is atomic: initialization state, native points,
  constraints, forces, and the existing view remain unchanged.
- Verify in-place writes through the initialized point view still update the
  native state used by `solve()`.
- Verify pre-initialization reassignment uses the latest points and begins a
  fresh constraint/force configuration.
- Verify `MeshSolver` accepts pre-initialization coordinate replacement with
  the same row count, preserves the vertex-key mapping, and rejects a different
  row count atomically.
- Verify repeated rejected assignments do not retain native solvers or grow a
  history collection.
- Retain an initialized view, copy it, destroy the owning solver, and verify
  only the owned copy is documented and tested for use afterward.
- Update the public NumPy-style docstring, tutorial, examples, changelog, and
  installed-wheel typing consumer.
- Run focused solver tests, Ruff, Pyright, strict MkDocs, artifact checks, and
  memory/lifetime regression tests.

## Dependencies

ADR 019.
