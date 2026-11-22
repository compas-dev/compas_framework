# ADR 018: ShapeOp Native Dependencies and Build Portability

**Status:** Accepted

## Context

`compas_shapeop` bundles MPL-2.0 ShapeOp source and downloads Eigen 3.4.0 into
an ignored directory under the checkout. The Eigen URL has no integrity hash.
The build also applies `-fPIC` unconditionally to a static target, uses global
compiler flags, and contains host-specific Homebrew discovery for optional
OpenMP. These choices make clean and cross-platform builds difficult to audit
and reproduce.

The package itself is MIT-licensed, but its metadata currently advertises BSD
and does not describe the bundled MPL-2.0 source accurately.

## Options

### Eigen provisioning

1. Use only a system Eigen package.
2. Vendor Eigen in the repository.
3. Fetch an immutable Eigen archive with integrity verification into the CMake
   build tree.

### Compiler and OpenMP behavior

1. Preserve compiler-specific global flags and host package-manager probing.
2. Use CMake target properties and imported targets; keep OpenMP opt-in and
   fail clearly when an explicitly requested toolchain feature is unavailable.

## Recommendation

Choose Eigen option 3 and compiler option 2.

- Fetch Eigen 3.4.0 from an immutable archive and record its SHA-256 digest in
  CMake. Place downloaded and extracted content below the build directory, not
  the source checkout. Document the verified network download required by a
  clean build.
- Do not vendor Eigen without a demonstrated offline, patching, licensing, or
  availability requirement.
- Keep the current bundled ShapeOp sources and their notices in the source
  distribution. Binary wheels contain the compiled extension, `LICENSE`,
  `LICENSE.shapeop`, and a third-party notice identifying the exact bundled
  ShapeOp source revision and its corresponding-source location; they do not
  duplicate the C++ source tree.
- Use `POSITION_INDEPENDENT_CODE` instead of an unconditional `-fPIC`; use
  target-scoped include directories, definitions, and compile options; link
  imported CMake targets such as `Threads::Threads` and
  `OpenMP::OpenMP_CXX`.
- Keep OpenMP disabled by default. If a caller enables it, use CMake's normal
  `find_package(OpenMP)` contract and fail clearly when the requested feature
  is unavailable. Do not execute Homebrew or choose a compiler from project
  CMake.
- Preserve C++20 and verify the same CMake path on every wheel platform and
  from the sdist.
- Correct packaging metadata and documentation to distinguish the MIT wrapper
  from bundled MPL-2.0 ShapeOp source. Include both `LICENSE` and
  `LICENSE.shapeop` in wheels and sdists and remove the incorrect BSD
  classifier.

## Consequences

Clean builds remain network-dependent for Eigen but become deterministic and
integrity-checked. The build no longer writes ignored dependencies into the
checkout. Compiler behavior is expressed through portable CMake mechanisms,
so MSVC does not receive GCC flags and optional OpenMP does not depend on a
developer's package manager.

The distribution exposes its mixed licensing accurately. Updating Eigen or
the bundled ShapeOp source requires an explicit dependency update, license
review, and clean platform builds.

## Verification

- Configure from a clean source tree and confirm no generated or downloaded
  file appears in the checkout.
- Verify the recorded Eigen digest and exercise both a cold download and a
  cache-backed build.
- Build with GCC/Clang, Apple Clang, and MSVC through the supported wheel jobs.
- Test the default OpenMP-off configuration everywhere; test OpenMP-on only in
  an explicitly provisioned job and assert a clear failure when requested but
  unavailable.
- Inspect wheels for both license files and the third-party source notice.
  Inspect the sdist for those files and every bundled ShapeOp source needed
  for an offline ShapeOp compile (apart from the separately fetched,
  hash-verified Eigen archive).

## Dependencies

ADRs 001, 002, 008, 010, 011, 012, and 017.
