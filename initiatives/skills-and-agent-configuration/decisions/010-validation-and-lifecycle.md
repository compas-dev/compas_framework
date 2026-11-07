# ADR 010: Behavioral Validation and Lifecycle

## Status

Accepted.

## Context

A syntactically valid `SKILL.md` can still route incorrectly, teach stale APIs,
or produce invalid code. Current skills have no shared behavioral evidence.

## Options

1. Validate routing, execution, artifacts, configuration, and references.
2. Validate frontmatter and Markdown only.
3. Rely on maintainer review without repeatable scenarios.

## Recommendation

Choose option 1. Blocking deterministic CI covers schemas and frontmatter,
scripts, configuration parsing, references, canonical tutorial artifacts,
Ruff, Pyright, relevant runtime checks, duplicate detection, and secret
scanning. Isolated user execution covers source, installed, and
version-mismatch scenarios.

Trigger, non-trigger, and independent realistic forward tests are release and
acceptance evidence; do not present model routing as perfectly deterministic
ordinary CI. Declare supported COMPAS version ranges and version the two
installable bundles independently from COMPAS package releases.

CI detects duplicated or diverged framework-wide skills and scans committed
configuration for secrets. Any future MCP adds schema, tool allowlist,
read/write classification, and permission tests.

## Consequences

- A skill is not considered complete merely because its Markdown parses.
- Validation has a maintenance cost proportional to public workflow promises.
- Routing and generated-code regressions become visible before distribution.
- Bundle releases need explicit compatibility metadata and behavioral
  evidence.

## Dependencies

ADRs 001–009.
