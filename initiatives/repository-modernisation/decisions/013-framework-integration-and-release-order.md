# ADR 013: Framework Integration and Coordinated Release Order

**Status:** Accepted

## Context

`compas_framework` depends on the core package set and verifies cross-package
behavior. Running every native dependency in its ordinary pure-Python job would
make that job slow and fragile, while independent package releases can publish
an incompatible combination.

## Options

1. Install all native packages in every framework check.
2. Test packages only within their own repositories.
3. Separate fast framework checks from a coordinated native integration job and
   make release order explicit.

## Recommendation

Use the pure uv profile for ordinary framework checks. Add a separate,
explicitly provisioned integration job that installs the exact candidate core
artifacts, exercises cross-package contracts, and records unavailable backends
as skips rather than passes. Define and verify a dependency-ordered release
plan before publishing coordinated changes.

## Consequences

Fast checks remain reliable while integration coverage is authoritative.
Candidate artifacts and versions must be passed explicitly. Coordinated release
automation cannot publish downstream packages before required upstream
artifacts exist and pass integration.

## Affected repositories

`compas_framework` and every core package participating in coordinated
contracts or releases.

## Dependencies

ADR 008, ADR 009, ADR 011, ADR 012.
