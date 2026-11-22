# ADR 002: Python Project Configuration Source of Truth

**Status:** Accepted

## Context

The references already use `pyproject.toml`, but some duplicate Python
dependencies and tool configuration in requirements, environment, Pixi, and
legacy configuration files.

## Options

1. Keep tool-specific dependency files as equal authorities.
2. Generate multiple files from a new repository schema.
3. Make standards-based `pyproject.toml` authoritative and keep separate files
   only for system/native tools that cannot be represented there.

## Recommendation

Use PEP 621 project metadata, build-system tables, and PEP 735 dependency groups
in `pyproject.toml`. Configure pytest, Ruff, Pyright, cibuildwheel, and
versioning there when supported. Keep MkDocs, workflows, CMake, and minimal
system provisioning explicit in their native formats. Do not add a generator.

## Consequences

Duplicated Python requirements can be removed after consumer parity is proven.
Native/system dependencies remain visible. Package metadata and documentation
need consistency tests.

## Affected repositories

All core COMPAS repositories.

## Dependencies

ADR 001.
