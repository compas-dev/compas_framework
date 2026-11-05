# `compas_shapeop` Modernisation Proposal

**Status:** Proposed; source implementation is blocked by ADRs 017–019

## Purpose

Apply the approved native-wheel repository profile to `compas_shapeop` without
changing its solver API. The migration must first resolve the repository's
Python/stable-ABI contradiction, make the native build reproducible and
portable, and establish installed-artifact evidence strong enough to make its
quality gates authoritative.

This package proposal refines the accepted framework-wide decisions. It does
not reopen the common uv, Ruff, MkDocs, workflow-security, or release-artifact
policies.

## Current evidence

The inspected `main` branch is clean at `9f57579` and currently has these
material inconsistencies:

- project metadata declares Python 3.9 and classifiers through 3.12, while
  scikit-build-core emits `cp312` stable-ABI wheels and nanobind's stable ABI
  requires Python 3.12 or newer;
- CMake asks for Python 3.8, the ordinary workflow tests only Python 3.10, and
  cibuildwheel excludes CPython 3.13;
- the extension is built with nanobind `STABLE_ABI`, but cibuildwheel does not
  explicitly build only the single CPython 3.12 wheel that is meant to cover
  later supported CPython versions;
- the Python package imports NumPy and COMPAS, but built-project metadata has
  no runtime dependencies;
- `requirements.txt` still declares COMPAS 2.x, while the current framework
  initiative targets COMPAS 3;
- Eigen 3.4.0 is downloaded without an integrity hash into an ignored
  source-tree directory;
- the static ShapeOp target receives the GCC/Clang-only `-fPIC` flag even on
  MSVC, and optional OpenMP probing contains host-specific Homebrew logic;
- tests contain one source-tree solver smoke test and do not test installed
  wheels, the sdist build path, stable-ABI compatibility, failure behavior, or
  typing metadata;
- an explicit import from outside the checkout with the required `compas3`
  interpreter fails because `compas_shapeop` is not installed there, so no
  local native baseline may be claimed from that environment;
- the wrapper license is MIT and bundled ShapeOp sources are MPL-2.0, but
  project metadata advertises BSD and does not declare both license files;
- documentation remains Sphinx/RST, Black and Ruff overlap, Pyright and a uv
  lock are absent, and build/release workflows rebuild equivalent artifacts
  independently.

The existing solver smoke test passes only when the extension and dependencies
are already available. It proves a basic numerical update but not the
distribution or platform contracts above.

## Recommended package contract

### Python and artifacts

- Require Python 3.12 or newer and advertise only versions with passing
  evidence.
- Retain nanobind's stable ABI with `cp312` as the baseline.
- Build one `cp312-abi3` wheel per supported OS/architecture, then install and
  test that exact wheel on every advertised CPython minor.
- Cover Linux x86_64, Windows AMD64, macOS arm64, and macOS x86_64. A target
  without a functioning runner remains explicitly unverified; it is not
  silently removed or reported as passing.
- Build and install an sdist in a clean environment to prove that all C++
  sources, license files, and build inputs are present.

ADR 017 records this decision.

### Native dependency and portability boundary

- Keep the bundled ShapeOp sources in the sdist and preserve their MPL-2.0
  notices. Wheels contain the compiled extension, both license files, and a
  third-party notice identifying the exact ShapeOp source revision and its
  corresponding-source location; wheels do not duplicate the C++ source tree.
- Fetch Eigen 3.4.0 from an immutable archive with a recorded SHA-256 hash into
  the CMake build tree, never into the checkout. Document that a clean sdist
  build needs network access for this verified download.
- Prefer target properties and imported CMake targets over compiler-specific
  global flags: use `POSITION_INDEPENDENT_CODE`, target-scoped include paths,
  and `Threads::Threads`/`OpenMP::OpenMP_CXX` where applicable.
- Keep OpenMP disabled by default. If explicitly enabled, require a toolchain
  where CMake can provide `OpenMP::OpenMP_CXX`; do not discover Homebrew or
  mutate compiler selection inside the project.
- Preserve C++20 and verify clean builds on every wheel platform.
- Correct distribution licensing to identify the MIT wrapper and bundled
  MPL-2.0 ShapeOp source, and include both `LICENSE` and `LICENSE.shapeop` in
  wheels and sdists.

ADR 018 records this decision.

### Python dependencies, verification, typing, and documentation

- Declare direct runtime requirements in `pyproject.toml`:
  `compas>=3,<4` and `numpy>=1.26`. Do not rely on transitive installation.
- Separate build, test, docs, and developer tools into PEP 735 groups and
  commit a frozen uv lock. CMake, Ninja, nanobind, scikit-build-core, and
  cibuildwheel are build/development tools, not runtime dependencies.
- Keep the compiled `_shapeop` module private. Preserve the existing public
  import paths `compas_shapeop.shapeop.Solver` and
  `compas_shapeop.meshsolver.MeshSolver`; do not introduce package-root
  re-exports. Test behavior through those Python wrappers, while also proving
  that the installed extension resolves from the wheel rather than the
  checkout.
- Add numerical contract tests for accepted input shape, finite output,
  constraint effects, `fix_vertex` target proximity within its documented
  finite-weight tolerance, and repeatable results within documented
  tolerances. Preserve and test only invalid-input failures already exposed by
  the wrappers or binding; do not add broad runtime validation or new
  exception promises. Generated files and build products must use pytest
  temporary paths or runner temporary directories.
- Add `py.typed` and a private `_shapeop.pyi` binding contract so strict
  Pyright can validate the Python wrapper without making `_shapeop` public.
  Verify the marker, stub, and representative public calls from an installed
  wheel in a clean consumer environment.
- Convert Sphinx/RST to strict MkDocs/mkdocstrings Markdown. Apply the
  repository-local `update-docstrings` skill to every touched public docstring;
  documentation work must not change solver behavior.
- Record the primary ShapeOp methodology and backend sources in a top-level
  `REFERENCES.md`. Scope numerical and performance claims to behavior actually
  verified by the wrapper, and include both license texts from the docs license
  page.
- Build artifacts once in the release workflow, test those exact files, and
  promote them unchanged under the accepted trusted-publishing policy. The
  migration may validate this sequence but may not publish without separate
  approval.

ADR 019 records this decision.

## Alternatives and tradeoffs

### Build one wheel for every CPython minor

This avoids relying on the stable ABI but multiplies build and release
artifacts. It also discards a stable-ABI design already shared by the native
COMPAS packages. Prefer retaining `cp312-abi3`, with installation tests that
make the compatibility claim observable.

### Keep Python 3.9–3.11 through source builds

This would split the support promise: old interpreters could build only from
source while published wheels start at 3.12. It also conflicts with the COMPAS
3 framework floor. Prefer one honest Python 3.12+ contract.

### Use a system Eigen package

System Eigen can avoid downloads but creates platform- and distribution-
specific provisioning and makes PyPI sdist builds harder to reproduce. A
verified immutable archive is the smallest consistent cross-platform path.

### Vendor Eigen in the repository

Vendoring supports offline builds but adds a large third-party source tree and
an update burden. No current offline requirement justifies it. Vendoring can be
reconsidered only if availability, patching, or licensing evidence requires it.

### Test only the Python wrapper from the checkout

This is fast but cannot prove wheel tags, packaged native binaries, licenses,
typing metadata, or source-distribution completeness. Source tests remain
useful, but installed-artifact tests are required for completion.

## Implementation sequence after approval

1. Accept ADRs 017–019 and create the ShapeOp modernization branch from the
   recorded clean baseline.
2. Align Python metadata, stable-ABI settings, CMake Python discovery, and the
   cibuildwheel matrix.
3. Replace the unverified Eigen download and non-portable CMake flags; verify
   clean native builds before changing workflows.
4. Consolidate dependencies/groups, create `uv.lock`, and add Ruff, Pyright,
   source tests, and installed-artifact tests.
5. Migrate docs with the `update-docs` and `update-docstrings` instructions.
6. Modernize visible workflows with immutable action pins, least privilege,
   temporary artifact directories, and one tested release artifact set.
7. Run an independent review and the full platform matrix. Record unavailable
   targets as unverified.
8. Push an initiative branch and open a draft PR only when authorized. Do not
   merge or publish.

## Completion evidence

The repository is not modernized until all applicable checks pass:

- frozen uv sync and lock validation;
- Ruff check and format check;
- strict Pyright over source, tests, and the private binding stub;
- source tests on the minimum and latest supported Python;
- strict MkDocs build and focused doctests;
- one `cp312-abi3` wheel for every supported OS/architecture;
- clean installation and public solver smoke tests on Python 3.12, 3.13, and
  3.14 for each produced platform artifact;
- clean sdist build and installed smoke tests;
- artifact inspection for runtime metadata, wheel tags, native module,
  `py.typed`, `_shapeop.pyi`, `LICENSE`, and `LICENSE.shapeop`; wheels also
  contain the third-party source notice, while the sdist contains the complete
  bundled ShapeOp source tree required for its build;
- workflow policy checks for immutable pins, permissions, artifact reuse, and
  temporary output locations;
- independent code and documentation review.

## Approval requested

Approval of this proposal means accepting ADRs 017–019 and authorizing the
bounded ShapeOp implementation described above. It does not authorize merging,
publishing, repository-setting changes, or removal of a currently advertised
platform without evidence and explicit follow-up approval.
