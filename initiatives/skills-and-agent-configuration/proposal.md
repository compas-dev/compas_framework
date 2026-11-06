# Skills and Agent Configuration Proposal

## Summary

Create two separately routed and installable skill families: user tutorial
skills for people writing COMPAS code, and developer tools for contributors and
coding agents working on framework repositories. Author both from one
canonical source, keep repository instructions compact, generalize the current
custom agent roles, and add no COMPAS MCP server until a concrete live-data or
controlled-action requirement exists.

## Responsibility boundaries

### Documentation

Accepted ADRs own intended architecture. Source, tests, version-matching
documentation, public signatures, and package configuration establish what is
actually available. Skills select, sequence, exercise, and validate this
material; they do not copy an API manual. A user tutorial must never teach an
accepted but unimplemented API.

### `AGENTS.md`

Repository instructions contain only durable, always-applicable policy,
repository commands, authorization boundaries, and concise rules that route a
matching task to a required skill.

### Skills

Each skill owns one recognizable workflow. Its description is a precise
routing contract. Conditional details live in references and deterministic,
repeated mechanics live in scripts. Learner and maintainer workflows are not
combined.

### Agent definitions

Custom agents define a reusable responsibility, ownership boundary, expected
evidence, and stopping condition. They do not duplicate framework policy or
claim permission isolation that the parent session does not enforce.

### MCP

MCP supplies live external information, authentication, or controlled actions.
It is not a storage mechanism for static COMPAS conventions. No new MCP server
is part of the baseline.

## Canonical source and bundles

Author framework-wide skills once in this coordination repository and expose
two independently installable portable skill bundles that can be packaged as
Agent Plugins:

- `compas-user-skills`, initially containing `compas-get-started`;
- `compas-developer-tools`, containing contributor workflow skills.

The same canonical source additionally maintains repo-scoped `.codex/` agent
and configuration adapters. Those adapters are installed and governed
separately; they are not presented as portable Agent Plugin contents.

Use namespaced skill names such as:

- `compas-get-started`;
- `compas-update-docstrings`;
- `compas-update-docs`;
- `compas-update-type-hints`;
- `compas-verify-change`.

Package repositories keep only genuinely package-specific skills or thin
routing instructions. Local and repository marketplace configuration supports
development and testing without copied skill bodies or machine-specific
symlinks. The authoring layout remains portable so either bundle can later move
to a dedicated repository without rewriting its skills. Public publication is
a separate approval boundary.

## Initial user tutorial curriculum

Pilot one guided `compas-get-started` skill against core COMPAS:

1. inspect the active Python environment and COMPAS version;
2. create and inspect basic geometry;
3. create and query a mesh using current high-level accessors;
4. transform and serialize data;
5. modify the program and inspect the changed result.

Every stage is an interactive lesson checkpoint: it produces a small runnable
artifact, explains the expected result, runs focused validation, and offers a
modification exercise. It writes only to a user-selected project or isolated
temporary directory. It does not install or upgrade packages without
authorization. A version mismatch is reported before work continues.

The tutorial includes user-facing `agents/openai.yaml` metadata and validates
both intended selection and non-selection. This metadata is an optional host
adapter; the portable skill remains complete without it.

Visualization and computational-backend lessons are later optional modules,
gated on stable public APIs and matching documentation. They are not required
for the first complete tutorial.

## Initial developer workflows

Normalize the three existing documentation and typing skills, then add one
verification skill. `compas-verify-change` selects the owning repository's
configured commands and reports evidence; it does not hard-code one test stack
for every package.

Additional geometry, plugin, release, or PR-handoff skills require a stable
approved contract and evidence of repeated use. They are not created
speculatively.

Every developer skill consults the owning repository instructions and accepted
initiative decisions, stops when a governing ADR is unresolved, and links to
the authoritative contract instead of becoming a second registry of framework
patterns. There is no universal "apply every COMPAS pattern" skill.

## Framework proposal intake

A framework-wide proposal that changes public contracts, shared engineering
policy, cross-package behavior, or more than one repository should normally
begin as an initiative PR in the coordination repository. That PR contains the
objective, reconnaissance inventory, architecture proposal, independent
Proposed ADRs, dependencies, affected repositories, verification plan, and
approval boundary. It should not bundle the package implementation whose
architecture is still under review.

After the relevant ADRs are explicitly accepted, separate implementation PRs
apply the approved decisions in their owning repositories and link back to the
initiative records. Narrow bug fixes, security fixes, behavior-preserving
maintenance, and genuinely mechanical documentation or tooling changes may
remain direct code PRs. If such a change exposes an unresolved public or
cross-package design choice, that choice moves into an initiative before the
implementation expands.

This is a review default, not mandatory ceremony for every edit. Existing PRs
do not need to be rewritten solely to adopt the intake model. During the
current COMPAS 3 cycle, initiative PRs target the approved coordination base;
they do not imply a merge to `main`.

## Custom agent configuration

Retain explorer, architect, implementer, reviewer, and documenter, but make
their prompts apply across framework initiatives instead of geometry only.
Remove ineffective per-agent `sandbox_mode` claims, replace legacy configuration
keys with documented keys, and use supported capability controls where a role
should not receive a tool category. Parent-session permissions, MCP servers,
and approval policy remain authoritative.

No tutor-specific agent is proposed initially. The user tutorial skill must
work with an ordinary agent. Portable skill behavior must not depend on custom
agents, MCP, or subagents.

## MCP configuration deliverable

The baseline adds no COMPAS MCP server, but it does provide an admission and
configuration template. Every proposed connection names the live use case,
tool inventory, read/write classification, authorization points, credential
ownership, and verification. MCP configuration belongs to the parent session;
custom agent files cannot override it. Examples contain no credentials or
developer-specific paths.

## Validation

Blocking deterministic validation covers schemas and frontmatter, scripts,
configuration parsing, references, canonical tutorial artifacts, Ruff,
Pyright, relevant runtime execution, duplicate detection, and secret scanning.
User scenarios run without network access by default in isolated projects and
cover a source checkout, an installed release, and a version mismatch.

Trigger, non-trigger, and independent forward-execution scenarios are release
and acceptance evidence rather than a claim that model routing is perfectly
deterministic CI. Each bundle declares its supported COMPAS versions and is
versioned independently from COMPAS package releases.

CI also checks referenced links and examples, parses agent configuration,
detects duplicate or diverged framework-wide skills, and scans committed
configuration for secrets. A later MCP addition would add schema, tool
allowlist, read/write classification, and permission tests.

## Rollout

1. Record the accepted independent ADRs.
2. Repair current skill references and custom-agent configuration.
3. Establish the canonical source, two installable bundles, and validation
   harness.
4. Migrate the three existing developer skills and add verification.
5. Pilot the core-only `compas-get-started` tutorial.
6. Add viewer and optional-backend lessons only after their APIs stabilize.
7. Consider plugin distribution or an MCP connection only after demonstrated
   demand and a new approval.

## Alternatives

### One universal COMPAS skill

Rejected. It combines different audiences, side effects, authorities, and
release cadences, making routing imprecise and instructions large.

### Copy every shared skill into every repository

Rejected. Existing copies have already drifted and package coverage is
inconsistent.

### Put shared skills in core COMPAS

Rejected. Framework contributor workflows should not be coupled to the Python
package's runtime release.

### Create a dedicated skills repository immediately

Deferred. It adds governance and release machinery before the bundle is
proven. The initial structure will keep that move possible.

### Build a COMPAS documentation MCP server now

Rejected for the baseline. Static local source, docs, examples, and skill
references already cover the identified need. A live use case can justify a
later, independently approved server.

## Compatibility implications

- Namespaced skill names avoid collisions with generic user skills.
- Existing copied skills will be migrated deliberately rather than silently
  replaced.
- User installations do not implicitly include contributor mutation
  workflows or custom agent configuration.
- User tutorial behavior is explicitly version-aware.
- Portable skill bodies do not require Codex, MCP, or subagents for
  correctness; Codex configuration remains an optional adapter.
- No credentials or developer-specific absolute paths enter the bundle.

## Approval boundary

This proposal and ADRs 001–010 are Accepted. ADR 011 is Proposed and is not yet
part of the implementation authorization. Existing approval authorizes only
the rollout above. It does not authorize publicly publishing either Agent
Plugin bundle, adding an MCP server, connecting external accounts, merging, or
releasing.
