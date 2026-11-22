# ADR 010: Workflow Security and External Action Policy

**Status:** Accepted

## Context

Current workflows include old actions, moving version tags, broad or implicit
permissions, token-based release paths, and inconsistent release environments.

## Options

1. Continue using moving major tags for convenience.
2. Pin only third-party actions deemed high risk.
3. Pin all external actions to reviewed commit SHAs and automate update PRs.

## Recommendation

Pin external actions immutably with readable version comments and automated
update PRs. Declare least-privilege permissions per workflow/job, use protected
environments and OIDC trusted publishing, add concurrency controls, and never
expose publish credentials to untrusted PR jobs.

## Consequences

Configuration is more verbose and needs an update bot. Pins and permissions
become reviewable/testable. Repository owners must configure environments and
trusted publishers; file changes alone cannot finish migration.

## Affected repositories

All core repositories and `compas-actions`.

## Dependencies

ADR 007.
