# Skills and Agent Configuration Proposal

## Summary

Create two separately routed skill families: learner skills for people writing
COMPAS code, and maintainer skills for contributors and coding agents working
on framework repositories. Author shared skills once as a portable bundle,
keep repository instructions compact, generalize the current custom agent
roles, and add no COMPAS MCP server until a concrete live-data or
controlled-action requirement exists.

## Responsibility boundaries

### Documentation

Versioned documentation, executable examples, public signatures, and package
configuration remain authoritative for factual behavior. Skills select,
sequence, exercise, and validate this material; they do not copy an API manual.

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

## Canonical bundle

Author framework-wide skills once in this coordination repository under
namespaced names such as:

- `compas-get-started`;
- `compas-update-docstrings`;
- `compas-update-docs`;
- `compas-update-type-hints`;
- `compas-verify-change`.

Package repositories keep only genuinely package-specific skills or thin
routing instructions. The authoring layout must remain portable so the bundle
can later be packaged as a public plugin or moved to a dedicated repository
without rewriting its skill bodies. The first wave will define one explicit
installation/bootstrap path; it will not copy editable forks into every
package.

## Initial learner curriculum

Pilot one `compas-get-started` skill against core COMPAS:

1. inspect the active Python environment and COMPAS version;
2. create and inspect basic geometry;
3. create and query a mesh using current high-level accessors;
4. transform and serialize data;
5. optionally visualize the result;
6. optionally use one computational backend and explain direct versus
   plugin-dispatched use.

Every stage produces a small runnable artifact, explains the expected result,
runs focused validation, and offers one modification exercise. It writes only
to a user-selected project or isolated temporary directory. It does not
install or upgrade packages without authorization. A version mismatch is
reported before work continues.

## Initial maintainer workflows

Normalize the three existing documentation and typing skills, then add one
verification skill. `compas-verify-change` selects the owning repository's
configured commands and reports evidence; it does not hard-code one test stack
for every package.

Additional geometry, plugin, release, or PR-handoff skills require a stable
approved contract and evidence of repeated use. They are not created
speculatively.

## Custom agent configuration

Retain explorer, architect, implementer, reviewer, and documenter, but make
their prompts apply across framework initiatives instead of geometry only.
Remove ineffective per-agent `sandbox_mode` claims, replace legacy configuration
keys with documented keys, and use supported capability controls where a role
should not receive a tool category. Parent-session permissions, MCP servers,
and approval policy remain authoritative.

No tutor-specific agent is proposed initially. The learner skill must work
with an ordinary agent.

## Validation

Every skill requires structural validation plus realistic trigger,
non-trigger, and forward-execution scenarios. Learner scenarios run in
isolated projects and check generated Python with Ruff, Pyright, and runtime
execution where applicable. The suite covers a source checkout, an installed
release, a missing optional dependency, and a version mismatch.

CI also checks referenced links and examples, parses agent configuration,
detects duplicate or diverged framework-wide skills, and scans committed
configuration for secrets. A later MCP addition would add schema, tool
allowlist, read/write classification, and permission tests.

## Rollout

1. Accept the independent ADRs.
2. Repair current skill references and custom-agent configuration.
3. Establish the canonical portable bundle and validation harness.
4. Migrate the three existing maintainer skills and add verification.
5. Pilot `compas-get-started` against core COMPAS.
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
- Learner behavior is explicitly version-aware.
- Portable skill bodies do not require Codex, MCP, or subagents for
  correctness; Codex configuration remains an optional adapter.
- No credentials or developer-specific absolute paths enter the bundle.

## Approval boundary

This proposal and ADRs 001–010 are Proposed. Approval authorizes only the
rollout above. It does not authorize publishing a plugin, adding an MCP server,
connecting external accounts, merging, or releasing.
