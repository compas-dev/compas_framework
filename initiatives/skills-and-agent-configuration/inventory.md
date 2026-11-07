# Skills and Agent Configuration Inventory

Inventory date: 2026-11-06.

## Audited scope

The initial audit covered `compas_framework`, core `compas`, `compas_cgal`,
`compas_libigl`, `compas_occ`, `compas_model`, and `compas_viewer`. It inspected
repository instructions, local skills, custom agent configuration, MCP
configuration, and the available getting-started tutorials and examples.

## Repository instructions and skills

The framework workspace currently contains:

- `AGENTS.md` with framework-wide engineering policy and initiative workflow;
- `.agents/skills/update-docstrings`;
- `.agents/skills/update-type-hints`;
- an untracked `.agents/skills/update-docs` addition.

No audited repository contains a user tutorial skill. The current skills are
maintenance-only.

Sibling repositories contain copied or independently edited variants of some
of these skills. Their contents and hashes differ, and `compas_libigl` has no
equivalent repository-local skills. There is therefore no effective
framework-wide source of truth or synchronization contract.

The audited copies are not small packaging variations: every inspected
`update-docstrings` copy has a different content hash, as does every inspected
`update-type-hints` copy. `update-docs` currently exists only in the framework
and model workspaces.

Several current skill instructions refer to `AGENTS.md` section names that do
not exist anymore. For example, the framework type-hint skill names `Python and
Typing` and `Framework Integration Contracts`, while core variants refer to
other obsolete headings. A skill can therefore appear authoritative while
routing an agent to missing policy.

The root `AGENTS.md` describes a framework-wide coordinator, but its prescribed
reconnaissance remains geometry-specific. That mismatch should be repaired as
part of the developer configuration, not copied into the skills.

None of the inspected project skills has behavioral forward tests. Optional UI
metadata is also absent. Those are not defects by themselves, but the current
repositories do not verify that descriptions select the intended tasks, reject
unrelated tasks, or produce the required result.

Official Codex guidance confirms that repository workflows may be stored in
`.agents/skills`, that descriptions are the initial routing contract, and that
reusable skills distributed beyond one repository are better packaged rather
than copied between repositories:

- <https://learn.chatgpt.com/docs/build-skills>
- <https://developers.openai.com/blog/skills-agents-sdk>

## Custom agents and Codex configuration

The workspace has an untracked `.codex/config.toml` and custom definitions for
architect, documenter, explorer, implementer, and reviewer roles. The role
prompts are largely geometry-specific, so their stated scope is narrower than
the framework-wide modernisation work they are now asked to perform.

Two configuration problems are already visible:

1. explorer and reviewer files set `sandbox_mode = "read-only"`, but custom
   agents inherit parent permissions and cannot override `sandbox_mode`;
2. the root config uses the legacy `agents.max_threads` alias instead of the
   current `agents.max_concurrent_threads_per_session` field.

Read-only behavior can still be required by a role's instructions and its
supported capabilities can be reduced, but the configuration must not claim a
permission boundary it cannot enforce. Current behavior is documented at:

- <https://learn.chatgpt.com/docs/agent-configuration/subagents>

## MCP configuration

No MCP configuration, bundled MCP dependency, or COMPAS MCP server was found in
the audited repositories. That is a useful neutral baseline, not a missing
feature.

MCP is appropriate when the workflow needs live information, authentication,
or controlled actions. Static framework patterns already present in
`AGENTS.md`, skills, source, or documentation do not require a server. Any
future connection needs a named use case, least-privilege tool exposure,
explicit approval behavior, and credentials outside version control.

Official guidance distinguishes MCP tools from skills: the server supplies
live data and controlled actions, while the skill supplies the reusable
workflow around them:

- <https://developers.openai.com/plugins/concepts/skills>
- <https://learn.chatgpt.com/docs/extend/mcp>

## Learner material

The audited repositories contain substantial but uneven source material:

- core has a broad getting-started section and executable example assets;
- CGAL has many paired examples;
- libigl has extensive examples but a very short tutorial;
- OCC and model tutorials are skeletal;
- viewer has many examples but its tutorial is mostly a router.

These materials can support learner skills, but they do not yet form one
versioned progressive path. The documentation-coordination initiative must
remain responsible for their factual accuracy and organization. Learner skills
should select and sequence them, create exercises in a user project or
temporary directory, run focused validation, explain failures, and link back
to the matching documentation.

## Candidate learner journeys

The first curriculum should be a core-only vertical slice rather than a catalog
of every package:

1. verify an environment and create a first COMPAS script;
2. construct and inspect geometry and data structures;
3. transform and serialize the data;
4. modify the small program and validate the result.

Visualization through the supported viewer path and use of an optional
computational backend are later user journeys, gated on stable APIs and
matching documentation.

Advanced backend authoring, plugin implementation, native builds, host
integrations, and framework contribution belong in later learner or maintainer
workflows.

## Architecture decisions required

The proposal needs independent decisions for:

1. learner versus maintainer skill families;
2. source of truth and distribution;
3. the `AGENTS.md`, skill, script, CI, and documentation boundaries;
4. version-aware learner behavior and artifact ownership;
5. custom agent roles and enforceable capability boundaries;
6. the MCP admission, permission, and secret-management boundary;
7. behavioral validation and lifecycle/versioning;
8. the first learner curriculum;
9. Codex-first versus portable packaging and optional host adapters.

## Risks

1. Copied skills continue to drift and contradict framework policy.
2. Large always-loaded instruction files consume context and obscure the rules
   that matter for the current task.
3. Tutorial skills silently teach APIs from a different COMPAS version.
4. A skill becomes a second documentation system and goes stale.
5. Agent configuration suggests permission isolation that the host does not
   provide.
6. MCP is added without a live-data requirement, increasing installation,
   security, and maintenance cost without improving the workflow.
7. Credentials or developer-specific configuration enter version control.
8. Too many broad skills make automatic selection unreliable.
