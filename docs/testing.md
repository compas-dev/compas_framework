# Testing Strategy

Ordinary pull requests run a pure tooling check on Python 3.12–3.14 across
Linux, macOS, and Windows, plus a strict documentation build. The tooling check
does not install the framework or its runtime dependencies.

For a coordinated release, the manual `framework-install` workflow builds
one metapackage wheel and attempts a clean install of its required
dependencies from PyPI on each target in `framework-matrix.json`. Run it
after the intended upstream releases are available and record the result
alongside the runtime integration evidence.

Cross-package integration can cover:

- plugin discovery and dispatch through public COMPAS APIs;
- data roundtrips across serialization formats and package boundaries;
- end-to-end workflows combining geometry, algorithms, models, and viewing;
- performance baselines for representative cross-package operations; and
- installation checks for coordinated package releases.

Use the `integration`, `roundtrip`, `performance`, `gui`, and `native_backend`
markers to select tests by capability. Tests needing a display or native
backend should skip with a precise reason when that capability is unavailable.
