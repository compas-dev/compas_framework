# ADR 001: Separate Learner and Maintainer Skill Families

## Status

Proposed.

## Context

People learning COMPAS and maintainers changing framework repositories have
different goals, authority, side effects, and validation needs.

## Options

1. Maintain separately named learner and maintainer skill families.
2. Create one universal COMPAS skill.
3. Provide repository maintainer skills only.

## Recommendation

Choose option 1. Learner skills create and validate code in user-owned or
temporary workspaces. Maintainer skills operate under repository policy and
framework architectural decisions. Do not route both audiences through a
catch-all skill.

## Consequences

- Routing descriptions can be precise.
- Learner workflows do not inherit maintainer mutation assumptions.
- Shared references may be reused, but workflow instructions remain separate.

## Dependencies

None.
