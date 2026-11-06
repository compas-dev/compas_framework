# ADR 011: Initiative-First Framework Proposals

## Status

Accepted.

## Context

Framework-wide code PRs can embed architectural choices in a large
implementation diff before the objective, alternatives, package dependencies,
and approval boundary have been agreed. Review then tends to optimize the
submitted implementation instead of first deciding whether its contract is
right for the framework.

Requiring a full initiative for every edit would create unnecessary ceremony
for narrow fixes and mechanical maintenance.

## Options

1. Submit framework-wide architectural proposals as initiative PRs before
   opening their package implementation PRs.
2. Continue submitting architecture and implementation together as code PRs.
3. Require an initiative for every framework repository change.

## Recommendation

Choose option 1. A proposal that changes a public contract, shared engineering
policy, cross-package behavior, or more than one repository normally begins as
an initiative PR in the coordination repository. It provides an objective,
reconnaissance inventory, architecture proposal, independent Proposed ADRs,
dependencies, affected repositories, verification plan, and explicit approval
boundary. It does not include package implementation whose governing decisions
remain unresolved.

After explicit ADR acceptance, separate implementation PRs in the owning
repositories link to the initiative and contain only the approved work. Narrow
bug and security fixes, behavior-preserving maintenance, and genuinely
mechanical documentation or tooling changes may remain direct code PRs. A
direct change that exposes an unresolved public or cross-package design choice
stops expanding until that decision is handled through an initiative.

Existing PRs are not rewritten merely to adopt this policy. In the current
COMPAS 3 cycle, initiative PRs target the approved coordination base and do not
authorize changes to `main`.

## Consequences

- Architectural review happens before implementation creates anchoring and
  cross-package coupling.
- Package PRs have a smaller, explicit contract and approval boundary.
- Framework proposals gain consistent dependency and verification records.
- Maintainers must distinguish architectural work from narrow implementation
  work; borderline proposals may require a short initiative rather than a
  large code-first PR.
- Small fixes and mechanical maintenance retain a lightweight path.

## Dependencies

ADRs 002, 006, 007, and 010.

## Approval record

Accepted by the user on 2026-11-06. Acceptance establishes the hybrid
initiative-first review policy described above. It does not authorize package
implementation, merging, publishing, or changes to `main`.
