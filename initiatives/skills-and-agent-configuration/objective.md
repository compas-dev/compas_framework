# Skills and Agent Configuration Initiative

## Objective

Establish a simple, maintainable way for two audiences to work with the COMPAS
framework:

1. users who want guided, executable help while learning to write COMPAS code;
2. maintainers and coding agents who must apply approved framework-wide
   engineering patterns consistently across repositories.

The initiative will define the responsibilities and distribution of tutorial
skills, maintainer workflow skills, `AGENTS.md`, custom agent roles,
deterministic scripts and CI checks, and optional MCP connections. It will not
duplicate the API documentation in prompts or introduce an MCP server for
static knowledge that can be shipped as versioned documentation or skill
resources.

## Questions to resolve

1. Which learner journeys should the first tutorial skills support?
2. How should a tutorial skill select documentation and examples that match the
   user's installed COMPAS version?
3. Which framework-wide maintainer workflows deserve reusable skills, and
   which rules must remain in `AGENTS.md`?
4. Where is the authoritative source for shared skills, and how are they made
   available without copied, drifting forks in every repository?
5. Which custom agent roles are useful across the framework, and which
   capabilities can their configuration actually constrain?
6. What live information or controlled actions, if any, justify MCP
   connections?
7. How are credentials, permissions, tool availability, and local developer
   configuration kept outside version-controlled defaults?
8. How will skill routing, tutorial results, workflow compliance, links, and
   configuration be tested?
9. Which parts should be portable Agent Skills and which, if any, should be
   Codex-specific adapters or configuration?
10. When should a new framework proposal arrive as an initiative PR before any
    package implementation PRs are opened?

## Design principles

- Keep learner skills and maintainer workflow skills separate.
- Treat versioned COMPAS documentation, executable examples, public APIs, and
  repository configuration as the factual sources of truth.
- Use skills to orchestrate a recognizable task, not to copy an API manual.
- Keep `AGENTS.md` small and limited to durable, always-applicable policy and
  skill-routing triggers.
- Put deterministic repeated mechanics in scripts or CI.
- Add MCP only for a named live-data or controlled-action requirement.
- Keep secrets and personal connections outside version control.
- Prefer one maintained framework-wide workflow over repository copies that
  can diverge.
- Start with a small end-to-end curriculum and validate it before expanding.
- Review framework-wide architecture as an initiative before implementation,
  while allowing narrow fixes and mechanical maintenance to remain direct code
  changes.

## Deliverables

1. A cross-repository inventory of skills, agent instructions, configuration,
   tutorials, examples, and MCP use.
2. An approved architecture and independent ADRs.
3. A minimal user tutorial curriculum and at least one validated tutorial
   skill.
4. A coherent set of developer workflow skills with one source of truth.
5. Compact repository instructions that route work into the appropriate
   skills.
6. General-purpose custom agent roles whose documented constraints match the
   actual configuration system.
7. A documented MCP boundary, admission checklist, and secure local
   configuration pattern; an MCP server is not a required deliverable unless
   an approved use case needs one.
8. Scenario-based validation for skill selection, non-selection, behavior,
   generated artifacts, links, and configuration.

## Non-goals

- Replacing the COMPAS documentation or tutorials.
- Encoding every framework API in skill instructions.
- Giving learners or agents permission to install packages, publish artifacts,
  access accounts, or mutate external systems without authorization.
- Committing credentials, tokens, OAuth secrets, or developer-specific paths.
- Creating a catch-all COMPAS skill or a speculative COMPAS MCP server.
- Standardizing every editor and agent host in the first implementation wave.

## Dependencies

The documentation-coordination initiative owns the quality and organization of
the factual tutorials and examples used by learner skills. Repository
modernisation owns the package commands and CI surfaces invoked by maintainer
skills. Typing, geometry, and plugin initiatives own their architectural
contracts; this initiative may teach or verify those contracts but must not
redefine them.

## Current status

Phase 1 reconnaissance and Phase 2 architecture are complete. ADRs 001–011
are Accepted and the approved rollout is implementation-ready. ADR 011 makes
initiative-first review the default for future framework-wide architectural
proposals while preserving direct PRs for narrow fixes and mechanical
maintenance. Public Agent Plugin publication, MCP server creation, external
account connections, merging, and releasing remain separately
approval-gated.
