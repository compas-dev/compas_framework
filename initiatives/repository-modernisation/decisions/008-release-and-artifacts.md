# ADR 008: Release Governance and Artifact Promotion

**Status:** Accepted

## Context

The references mix release pull requests and tag-driven releases. CGAL
duplicates build logic; OCC lacks a complete modern publish path. Rebuilding at
publish time can release files different from those tested.

## Options

1. Preserve repository-specific tag releases.
2. Rebuild artifacts in each release stage.
3. Use release pull requests and promote one tested artifact set unchanged.

## Recommendation

Use a release PR as the version/changelog authority. On merge, run validation,
build artifacts once, inspect/install/test the exact files, publish them through
trusted publishing, attach them to the GitHub release, and deploy versioned
docs. Never rebuild for publication.

## Consequences

Maintainer workflow and branch protection may change. Artifact retention and
job dependencies must be explicit. Every PyPI project needs trusted-publisher
configuration before token workflows are removed. Dry runs must verify the
sequence without publishing.

## Affected repositories

All publishable core repositories and `compas-actions`.

## Dependencies

ADR 007, ADR 009, ADR 010, ADR 011.
