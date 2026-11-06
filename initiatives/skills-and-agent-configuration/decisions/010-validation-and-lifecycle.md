# ADR 010: Behavioral Validation and Lifecycle

## Status

Proposed.

## Context

A syntactically valid `SKILL.md` can still route incorrectly, teach stale APIs,
or produce invalid code. Current skills have no shared behavioral evidence.

## Options

1. Validate routing, execution, artifacts, configuration, and references.
2. Validate frontmatter and Markdown only.
3. Rely on maintainer review without repeatable scenarios.

## Recommendation

Choose option 1. Require structural validation; trigger and non-trigger cases;
independent realistic forward tests; isolated learner execution; Ruff,
Pyright, and relevant runtime checks; link and example checks; source,
installed, optional-dependency, and version-mismatch scenarios; and agent
configuration parsing.

CI detects duplicated or diverged framework-wide skills and scans committed
configuration for secrets. Any future MCP adds schema, tool allowlist,
read/write classification, and permission tests.

## Consequences

- A skill is not considered complete merely because its Markdown parses.
- Validation has a maintenance cost proportional to public workflow promises.
- Routing and generated-code regressions become visible before distribution.

## Dependencies

ADRs 001–009.
