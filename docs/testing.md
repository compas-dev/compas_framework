# Testing Strategy

Framework tests are organized by the contract they exercise:

- plugin discovery and dispatch through public COMPAS APIs;
- data roundtrips across serialization formats and package boundaries;
- end-to-end workflows combining geometry, algorithms, models, and viewing;
- performance baselines for representative cross-package operations; and
- packaging checks for the supported Python and operating-system matrix.

## Pure repository checks

The ordinary pull-request matrix covers Python 3.12, 3.13, and 3.14 on Linux,
macOS, and Windows without installing the framework runtime dependencies:

```bash
uv sync --frozen --only-group dev --no-install-project
uv run --no-sync ruff check .
uv run --no-sync ruff format --check .
uv run --no-sync pyright
uv run --no-sync pytest tests/test_package.py
```

CI also inspects the synchronized environment and fails if any framework
distribution, including OCC, CGAL, or libigl, was installed.

## Distribution artifacts

The package job builds one wheel and one source distribution into the runner's
temporary directory. The same files are checked for complete metadata and
expected runtime requirements, installed with `--no-deps` in an isolated
environment, and uploaded for review. This verifies the coordination package
without downloading its native runtime backends.

Documentation is built separately and strictly:

```bash
uv sync --frozen --only-group docs --no-install-project
uv run --no-sync mkdocs build --strict
```

CI supplies a temporary `--site-dir`; generated documentation never lands in
the repository checkout.

## Native integration

`tests/test_native_geometry_backends.py` and
`tests/test_geometry_tessellation_integration.py` are pending geometry and
typing candidate-integration fixtures. The ordinary modernization checkpoint
deliberately excludes them from Ruff, Pyright, and runtime execution. They are
not authoritative proof of the accepted target contracts.

Their strategy-era source must not be hidden behind suppressions or presented
as current usage. Migration belongs to typing WP8.4 and modernization Phase 6,
after the `Mesh.triangulated()` amendment in ADR 024 and the cross-repository
candidate-artifact contract in ADR 021 are accepted and implemented. The final
candidate gate must then install the exact coordinated artifacts, run Ruff and
Pyright over the migrated fixtures, and execute the applicable integration and
native-backend cases.

When that gate exists, tests needing a display or native backend must skip with
a precise reason when the capability is unavailable. A skip is not passing
evidence. Mixing installed native extensions with unchecked sibling Python
wrappers is not an approved substitute for exact candidate artifacts.

Geometry-tessellation performance thresholds are deferred until the framework
has an environment-normalized benchmark runner. Wall-clock assertions in this
suite would primarily measure plugin discovery, native-library loading, and CI
machine variance rather than tessellation regressions. Functional integration
coverage will enter the final candidate gate under `integration` and
`native_backend`; future benchmarks should use the existing `performance`
marker with recorded input sizes, warm-up policy, backend versions, and
per-backend baselines.
