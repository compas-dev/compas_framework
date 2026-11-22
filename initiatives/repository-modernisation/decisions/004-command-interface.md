# ADR 004: Canonical Local and CI Commands

**Status:** Accepted

## Context

Current repositories mix direct tools, Invoke/`compas_invocations2`, Pixi
tasks, requirements installation, and workflow-specific commands. This creates
multiple definitions of the same operation.

## Options

1. Keep Invoke as a mandatory facade.
2. Create a new COMPAS command runner.
3. Document direct `uv run <tool>` commands and explicit native build commands.

## Recommendation

Make direct uv/tool commands authoritative and document them for local and CI
use. Workflows and convenience tasks execute the same underlying commands. Keep
thin repository-owned Invoke tasks for now, normally run as
`uv run invoke <task>`, when they provide useful command sequencing. Tasks must
not own environment creation, dependency resolution, system/native
provisioning, or hidden workflow policy. Do not create a wrapper framework.
Removing Invoke more broadly requires a separate coordinated team decision.

## Consequences

Commands remain transparent and reproducible even when contributors use a short
Invoke convenience. Native repositories document explicit provisioning and
build/rebuild steps outside the tasks. Contributor documentation lists both the
authoritative direct commands and retained conveniences without presenting
Invoke as a required environment or dependency-management layer. Shared actions
may call a thin task only when its bounded sequencing contract is explicit.

## Affected repositories

All core repositories and `compas-actions`.

## Dependencies

ADR 002, ADR 003, ADR 007.
