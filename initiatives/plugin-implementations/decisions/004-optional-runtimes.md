# ADR 004: Optional Runtime Selection and Failure Behavior

## Status

Accepted.

## Context

Native, GUI, notebook, Rhino, Grasshopper, and Blender implementations must be
discoverable without importing their runtimes. A requirement that checks only
the plugin package may not prove that the actual optional runtime is usable.

## Options

1. Use the current requirement mechanism with accurate runtime requirements.
2. Import optional runtimes during discovery.
3. Suppress failed imports and silently skip implementations.
4. Add a new dependency-resolution layer.

## Recommendation

Choose option 1. Use module-name requirements when `find_spec` is sufficient
and callable requirements only when presence does not establish availability.
Registration stays lightweight. Current selection, core defaults, and
`PluginNotInstalledError` remain authoritative; implementation failures
propagate after selection.

## Consequences

- Missing optional runtimes do not block unrelated discovery.
- Requirements identify the actual runtime.
- No silent failure or dependency framework is added.
- Host packages need host-runtime verification.

## Affected packages

Native, GUI, notebook, and host integration packages.

## Dependencies

- [ADR 001](001-authoritative-discovery.md)
- [ADR 002](002-registration-boundary.md)
