# Testing Strategy

Framework tests are organized by the contract they exercise:

- plugin discovery and dispatch through public COMPAS APIs;
- data roundtrips across serialization formats and package boundaries;
- end-to-end workflows combining geometry, algorithms, models, and viewing;
- performance baselines for representative cross-package operations; and
- packaging checks for the supported Python and operating-system matrix.

Use the `integration`, `roundtrip`, `performance`, `gui`, and `native_backend`
markers to select tests by capability. Tests needing a display or native
backend should skip with a precise reason when that capability is unavailable.

Geometry-tessellation integration tests run against the sibling repository
sources without installing them. From the framework repository, use:

```bash
PYTHONPATH=../compas/src:../compas_occ/src:../compas_cgal/src:../compas_libigl/src \
    pytest -m integration tests
```

Native-backend tests exercise installed plugin entry points while importing
the checked-out Python wrappers. A missing compiled extension is skipped with
its backend-specific reason; it is not treated as evidence that the contract
passed. The synchronized package matrix requires COMPAS 3.0 or newer.

Geometry-tessellation performance thresholds are deferred until the framework
has an environment-normalized benchmark runner. Wall-clock assertions in this
suite would primarily measure plugin discovery, native-library loading, and CI
machine variance rather than tessellation regressions. Functional integration
coverage therefore remains under `integration` and `native_backend`; future
benchmarks should use the existing `performance` marker with recorded input
sizes, warm-up policy, backend versions, and per-backend baselines.
