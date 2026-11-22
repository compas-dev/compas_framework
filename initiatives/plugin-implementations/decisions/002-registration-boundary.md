# ADR 002: Registration and Implementation Boundary

## Status

Accepted.

## Context

Core calls `entry_point.load()` during discovery. Entry points that target
implementation modules therefore import native, GUI, host, or adapter code
before any plugin is selected. CGAL, libigl, and OCC demonstrate that small
registration wrappers can avoid this cost.

## Options

1. Use lightweight category registration modules with function-local
   implementation imports.
2. Point entry points directly at implementation modules.
3. Use one monolithic registration module in every package.
4. Use one registration module per implementation or native extension.

## Recommendation

Choose option 1. Registration modules contain decorated wrappers, runtime
decorator imports, and type-only contract imports. They import implementations
inside wrapper bodies and otherwise have no discovery-time side effects.
Very small packages may use one lightweight module where clearer.

## Consequences

- Discovery remains independent of optional runtimes.
- Modules follow core plugin categories rather than build artifacts.
- Direct implementations become undecorated.
- Moving decorators may change diagnostic plugin IDs.

## Affected packages

All migrated implementation packages, beginning with reference, model, and
viewer packages.

## Dependencies

- [ADR 001](001-authoritative-discovery.md)
