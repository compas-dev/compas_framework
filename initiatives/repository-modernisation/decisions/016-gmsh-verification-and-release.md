# ADR 016: Gmsh Verification, Typing, and Artifact Release

**Status:** Proposed

## Context

The current `compas_gmsh` test only imports the wrapper and prints a version.
It does not prove that the native Gmsh SDK loads, initializes, meshes geometry,
or finalizes correctly. Pyright has measured source errors, installed typing is
not advertised, strict docs have real warnings, and `Model.from_brep` leaves a
generated file and descriptor behind. Legacy workflows rebuild across a
matrix, use moving actions, and publish with a token.

## Options

1. **Keep import tests and mock Gmsh.** Fast, but cannot verify the external
   runtime, native loader, API compatibility, or artifact installation.
2. **Run broad examples as integration tests.** Exercises more behavior, but is
   slow, fragile, and obscures the minimum supported contract.
3. **Define compact real-runtime gates plus focused unit tests.** Exercise a
   small deterministic meshing contract on every supported target, while using
   unit tests only for pure logic and exceptional cleanup paths.

## Recommendation

Choose option 3. A supported environment must:

1. initialize and finalize named models repeatedly without leaking global
   state;
2. generate and retrieve a nonempty two-dimensional mesh;
3. generate nonempty tetrahedral output for one simple OCC solid;
4. complete one boolean operation with the expected entity dimension;
5. open one committed read-only STEP fixture;
6. preserve `Model.from_brep(Brep)`, serialize through `Brep.to_step` into a
   scoped temporary file, and release that file and descriptor on success and
   failure; and
7. round-trip representative public mesh options.

All generated test files use `tmp_path` or `tmp_path_factory`. Runtime
intermediates use scoped temporary directories and deterministic cleanup.
Mocks may cover failure paths but never replace native initialization and mesh
generation in the blocking matrix.

Keep OCC out of the ordinary Gmsh matrix. A separate Linux integration job
installs `compas_occ` and verifies the real
`COMPAS Brep backed by compas_occ -> Brep.to_step -> Model.from_brep` path.
Unit tests may use a small duck-typed exporter for exceptional cleanup paths.
Native BREP serialization would require a separate input-protocol ADR; it is
not implied by the existing method name.

Make Ruff check/format, Pyright, tests, and strict MkDocs blocking. Add
`py.typed`, type all exported wrapper APIs, and verify those types from the
installed wheel. A narrow Pyright exception for the external generated `gmsh`
module is allowed; broad source exclusions or a repository-owned full Gmsh
stub package are not. Apply the repository-local `update-docstrings` skill
whenever docstrings, rendered signatures, or examples change.

Build one pure-Python wheel and one sdist in a runner temporary directory.
Inspect their Python, dependency, and license metadata and require `py.typed`.
Install the exact wheel with dependencies into a clean environment outside the
checkout, then run the runtime smoke and strict typing consumer. Promote those
unchanged files through OIDC trusted publishing and the GitHub release, then
deploy documentation from the same verified release revision, only after
protected environments/trusted publishers exist and publication is explicitly
approved. Never rebuild for publication.

## Consequences

CI becomes slower than an import-only job but provides evidence for the actual
package purpose. The real-runtime contract is deliberately small and
headless. Existing lifecycle, temp-file, typing, and documentation debt must be
resolved before modernization can be declared complete. Release artifacts are
traceable to the files tested on supported runtimes.

## Affected files

Source annotations and BRep temporary-file handling, tests and fixtures,
`py.typed`, `pyproject.toml`, `uv.lock`, MkDocs pages/configuration, `tasks.py`,
and all repository workflows.

## Dependencies

ADRs 004, 005, 006, 007, 008, 009, 010, 011, 014, and 015.
