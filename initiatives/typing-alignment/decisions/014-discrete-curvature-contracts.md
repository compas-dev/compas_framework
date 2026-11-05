# Title: Which discrete triangle-mesh curvature operations belong in core?

## Status

Accepted

## Context

The three remaining `tessellation_pluggable` consumers are Gaussian, mean, and
principal triangle-mesh curvature. Their contracts are not interchangeable:

- Core Gaussian curvature has a tested angle-defect implementation. Boundary
  vertices use $\pi-\sum\theta$ and interior vertices use
  $2\pi-\sum\theta$.
- Core mean curvature has no implementation and does not define whether its
  result is an integrated measure or a pointwise density.
- Core principal curvature documents direction pairs, while the only
  registered Rhino implementation returns maximum/minimum scalar values.
- Rhino Gaussian uses a different boundary convention. Its source is not in a
  managed Git checkout or importable in the initiative environment.
- The direct libigl API returns both principal directions and values from a
  neighborhood-fitting estimator, and deliberately is not registered as a
  core plugin.

Truthful annotations cannot make these mathematically different operations
substitutable.

## Options

1. Preserve principal direction pairs and discard the incompatible Rhino
   registration.
2. Redefine principal curvature as maximum/minimum scalar-value lists and
   separately define an integrated mean-curvature convention.
3. Return principal directions and values together, following libigl.
4. Keep only the verified core Gaussian angle-defect operation; remove the
   unsupported core mean/principal plugin APIs until a concrete cross-backend
   requirement and implementation exist.

## Recommendation

Choose option 4.

Migrate `trimesh_gaussian_curvature` to a direct function accepting
`TriangleMeshInput`. It retains its documented, tested boundary-aware
angle-defect semantics and is not replaceable by plugins with different
boundary conventions.

Remove core `trimesh_mean_curvature` and `trimesh_principal_curvature` rather
than retaining public operations without a verified conforming backend.
Package-owned Rhino and libigl curvature functions remain direct backend APIs.
If scalar principal values, direction fields, or an integrated mean-curvature
measure become a concrete cross-package requirement, introduce separately
specified operations with explicit normalization, units, estimator, and
boundary behavior.

After this correction, delete `_tessellation_plugin.py`, its imports, and its
decorator-specific tests.

## Decision

Approved on 2026-11-05. Core retains only the verified boundary-aware Gaussian
angle-defect operation. Unsupported core mean and principal curvature plugin
APIs are removed. Backend-specific curvature estimators remain package-owned;
future cross-package operations require explicit mathematical contracts rather
than compatibility adapters.

## Consequences

- Core exposes one verified curvature quantity with unambiguous semantics.
- No backend-specific estimator is presented as universally substitutable.
- Two existing but unsupported core public names are removed on the unreleased
  C3 initiative branch.
- Direct libigl curvature remains available without lossy adaptation.
- No new result classes, compatibility aliases, or plugin shims are added.

## Verification

- Python and NumPy raw mesh inputs for core Gaussian curvature.
- Boundary and interior angle-defect regression values.
- Source non-mutation and no implicit representation conversion.
- Removed symbols absent from exports, documentation, and typed consumers.
- No remaining `tessellation_pluggable` references.
- Ruff, Pyright, strict MkDocs, full feasible tests, and independent review.

## Dependencies

- [012 — Structural triangle-mesh boundaries](012-structural-triangle-mesh-boundaries.md)
