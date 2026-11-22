# ADR 017: ShapeOp Python and Stable-ABI Matrix

**Status:** Accepted

## Context

`compas_shapeop` currently declares Python 3.9+, asks CMake for Python 3.8,
tests Python 3.10, and configures scikit-build-core and nanobind to produce a
CPython 3.12 stable-ABI wheel. Those promises cannot all be true. The COMPAS 3
framework and the other native packages now use Python 3.12 as their minimum.

The present wheel configuration also builds an implicit set of interpreter
tags while intending one `cp312-abi3` artifact per platform. Without installing
that wheel on later CPython versions, the stable-ABI claim is configuration,
not evidence.

## Options

1. **Keep Python 3.9+ and publish interpreter-specific wheels.** This restores
   old-interpreter coverage but multiplies artifacts, abandons the current
   stable-ABI direction, and conflicts with the COMPAS 3 support floor.
2. **Keep Python 3.9+ but provide wheels only for Python 3.12+.** This creates a
   split support contract in which older users must build an undocumented
   native toolchain from source.
3. **Require Python 3.12+ and retain a CPython 3.12 stable-ABI baseline.** Build
   one `cp312-abi3` wheel per supported platform and test it on every advertised
   CPython minor.
4. **Require Python 3.12+ but publish one wheel per CPython minor.** This is
   simpler conceptually but needlessly duplicates native builds if the stable
   ABI works.

## Recommendation

Choose option 3.

- Set `requires-python` and CMake's Python discovery minimum to 3.12.
- Keep nanobind `STABLE_ABI` and scikit-build-core `wheel.py-api = "cp312"`.
- Configure cibuildwheel to build only the CPython 3.12 artifact for each
  supported OS/architecture, and assert that its tag is `cp312-abi3`.
- Advertise Python 3.12, 3.13, and 3.14 only after the exact wheel has been
  installed and tested on each version. Add future Python minors through the
  same evidence gate rather than an artificial upper bound.
- Preserve the intended platform set: Linux x86_64, Windows AMD64, macOS arm64,
  and macOS x86_64. Treat unavailable runners as explicit verification gaps,
  not successful or silently dropped targets.
- Build and install the sdist in a clean Python 3.12+ environment as a separate
  source-build contract.

## Consequences

The support promise becomes consistent with COMPAS 3 and the native artifact.
One wheel per platform serves the supported CPython minors, reducing build and
release duplication. The repository must maintain cross-version wheel smoke
tests because a successful CPython 3.12 build alone does not prove later
interpreter compatibility.

Python 3.9–3.11 support is removed. This is an intentional compatibility break
and must be stated in the changelog and installation documentation. A platform
cannot be reported as supported until its wheel and installed tests pass.

## Verification

- Assert consistency between `requires-python`, classifiers, Ruff target,
  CMake discovery, cibuildwheel, and documentation.
- Inspect every wheel filename and `WHEEL` metadata for the expected ABI tag.
- Install each exact wheel on CPython 3.12, 3.13, and 3.14 and run public solver
  smoke tests from outside the source tree.
- Build the sdist, build a wheel from it in a clean environment, and run the
  same smoke tests.

## Dependencies

ADRs 001, 002, 008, 009, 011, and 013.
