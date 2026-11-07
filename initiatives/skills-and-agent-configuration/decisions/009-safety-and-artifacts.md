# ADR 009: Safety and Artifact Ownership

## Status

Accepted.

## Context

Learner and maintainer workflows can create files, install dependencies, or
interact with repositories and external systems. Their authority must be
explicit.

## Options

1. Define artifact ownership and authorization boundaries in every workflow.
2. Let each agent infer convenient side effects.
3. Make all skills read-only.

## Recommendation

Choose option 1. User tutorial output goes only to a user-selected project or
an isolated temporary directory, runs without network access by default, and
never overwrites an existing destination without explicit confirmation. Skills
never install, upgrade, publish, merge, push, or mutate external services
without relevant authorization. They keep credentials, tokens, OAuth secrets,
and machine-specific paths out of version control and report missing versions
or runtimes clearly.

## Consequences

- Useful implementation workflows remain possible.
- Side effects do not follow merely from skill selection.
- Optional dependencies and native runtimes must be stated.

## Dependencies

ADRs 001 and 002.
