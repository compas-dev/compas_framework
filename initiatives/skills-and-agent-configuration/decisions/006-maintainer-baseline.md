# ADR 006: Initial Maintainer Workflow Baseline

## Status

Proposed.

## Context

Three related maintenance skills already exist in divergent forms. Framework
changes also need one consistent verification handoff.

## Options

1. Normalize the three existing workflows and add change verification.
2. Create skills for every current initiative immediately.
3. Keep independent package copies.

## Recommendation

Choose option 1. Start with `compas-update-docstrings`, `compas-update-docs`,
`compas-update-type-hints`, and `compas-verify-change`. Verification selects
the owning repository's configured commands and reports actual evidence rather
than hard-coding one framework-wide command list.

Add geometry, plugin, release, or PR-handoff skills only when an approved,
stable contract and repeated need justify them.

## Consequences

- Current drift is resolved first.
- The bundle remains small and discoverable.
- New skill proposals have an evidence threshold.

## Dependencies

ADRs 001–004.
