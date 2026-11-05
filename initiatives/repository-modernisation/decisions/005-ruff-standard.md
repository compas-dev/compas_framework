# ADR 005: Ruff as the Python Style Tool

**Status:** Accepted

## Context

The references already use Ruff, but `compas` retains Black configuration and
current shared lint tasks can mutate CI checkouts or omit repository Python
files.

## Options

1. Keep Black/isort/Flake8 beside Ruff.
2. Use Ruff only for linting and keep Black formatting.
3. Use Ruff for linting, import sorting, and formatting.

## Recommendation

Use Ruff alone. CI runs non-mutating `ruff check .` and
`ruff format --check .`. Local fix commands are separate. Adopt a conservative
common rule baseline and comment package-specific exclusions.

## Consequences

Overlapping dependencies/configuration are removed. Formatting may cause a
one-time mechanical diff. CI and local docs must distinguish checking from
fixing. Ruff and Pyright remain separate tools.

## Affected repositories

All core repositories.

## Dependencies

ADR 002, ADR 004.
