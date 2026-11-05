# ADR 001: Authoritative Discovery Mechanism

## Status

Proposed.

## Context

Current core discovers installed plugins through the `compas.plugins` package
entry-point group. It does not read `__all_plugins__`. Many ecosystem packages
still declare only the legacy list and are therefore undiscoverable. Restoring
scanning would create competing discovery paths and import side effects.

## Options

1. Use explicit package entry points only.
2. Support entry points and `__all_plugins__` concurrently.
3. Scan installed packages for plugin declarations.
4. Introduce a new centralized registry.

## Recommendation

Choose option 1. PEP 621 entry points are explicit, deterministic, installed
metadata that can be inspected without a global package scan. Remove legacy
lists only after contract inspection, compatible version requirements, and
replacement verification are complete.

## Consequences

- Core retains one discovery path.
- Legacy-only packages require deliberate migration.
- Metadata is not added to incompatible implementations merely to make them
  discoverable.
- No compatibility scanner or fallback list is introduced.

## Affected packages

Core and every package that provides COMPAS plugins.

## Dependencies

None.
