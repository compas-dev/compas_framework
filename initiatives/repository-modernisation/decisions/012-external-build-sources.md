# ADR 012: Reproducible External Native Build Sources

**Status:** Accepted

## Context

Native repositories may download third-party source during CMake builds.
`compas_libigl` currently tracks an upstream main branch, while CGAL also
downloads substantial native dependencies. An unpinned branch can produce
different artifacts from unchanged repository source.

## Options

1. Track upstream branches for immediate updates.
2. Vendor all native dependencies.
3. Pin reviewed immutable versions/hashes and update them through explicit PRs.

## Recommendation

Pin every fetched native source to an immutable reviewed tag/commit and verify
integrity where the tool supports hashes. Record versions visibly in repository
build configuration and update them through tested dependency PRs. Vendor only
when licensing, availability, patching, or offline-build requirements justify
the maintenance cost.

## Consequences

Native builds become reproducible and auditable. Updates are deliberate and
may lag upstream. Clean build tests must verify downloads and licenses. Build
documentation lists network and cached/offline behavior.

## Affected repositories

Native-wheel core repositories, initially `compas_cgal`, `compas_libigl`, and
`compas_shapeop` where applicable.

## Dependencies

ADR 001, ADR 010.
