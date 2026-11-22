# ADR 007: Shared Actions and Repository Workflow Boundary

**Status:** Accepted

## Context

Modern `compas-actions@v1` works well for `compas`, while OCC and CGAL still use
legacy actions and bespoke jobs. A universal remote workflow could hide native
toolchains and matrices.

## Options

1. Duplicate all mechanics in each repository.
2. Put complete CI/release workflows behind a parameterized shared workflow.
3. Share bounded actions while keeping orchestration and package commands
   visible in each repository.

## Recommendation

Use bounded shared actions for setup, release detection, PR checks, artifact
transfer/verification, GitHub releases, and docs deployment. Keep matrices,
commands, Conda provisioning, native builds, and artifact composition visible
in repository workflow YAML. Do not create a workflow generator.

## Consequences

Some YAML duplication remains intentionally. Shared actions need explicit
inputs/outputs, contract tests, versioning, and examples for all profiles.
Repository failures remain reproducible without reverse-engineering a remote
workflow.

## Affected repositories

All core repositories and `compas-actions`.

## Dependencies

ADR 001.
