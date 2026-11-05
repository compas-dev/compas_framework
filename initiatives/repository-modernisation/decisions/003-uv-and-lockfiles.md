# ADR 003: uv and Development Lock Files

**Status:** Accepted

## Context

`compas` uses uv in CI without a lock, `compas_occ` needs Conda, and
`compas_cgal` has a stale uv lock alongside a stronger Pixi environment. A
library's published dependency bounds and its reproducible development
environment are different contracts.

## Options

1. Use uv without committed locks.
2. Commit a uv development lock and keep project metadata as the installation
   compatibility contract.
3. Use Conda or Pixi universally.

## Recommendation

Use uv as the canonical Python dependency runner and commit a current
`uv.lock` for each migrated repository. CI ordinarily uses frozen sync. Keep
Conda only where it supplies unavailable runtime dependencies and keep native
toolchain provisioning explicit. Validate declared lower/upper compatibility
separately from the locked development environment.

## Consequences

Local and CI environments are reproducible. Lock update policy and automated
update PRs are required. OCC retains a minimal Conda layer; CGAL retains system
build prerequisites. Stale locks become blocking configuration defects.

## Affected repositories

All core repositories; special handling for Conda/native profiles.

## Dependencies

ADR 001, ADR 002.
