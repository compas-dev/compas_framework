# ADR 001: Separate Learner and Maintainer Skill Families

## Status

Accepted.

## Context

People learning COMPAS and maintainers changing framework repositories have
different goals, authority, side effects, and validation needs.

## Options

1. Maintain separately named and installable user and developer skill
   families.
2. Create one universal COMPAS skill.
3. Provide repository maintainer skills only.

## Recommendation

Choose option 1. User tutorial skills create and validate code in user-owned or
temporary workspaces. Developer skills operate under repository policy and
framework architectural decisions. Do not route or install both audiences as
one catch-all surface.

## Consequences

- Routing descriptions can be precise.
- User workflows do not inherit developer mutation assumptions.
- Shared references may be reused, but workflow instructions remain separate.

## Dependencies

None.
