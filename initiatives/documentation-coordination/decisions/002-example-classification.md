# ADR 002: Authoritative Example Classification

## Status

Accepted.

## Context

Example roots, exclusions, and runtime expectations currently differ by
repository. Directory names such as `__temp` can hide whether a file is a
published example, draft, or unsupported test case.

## Options

1. Declare roots and classify every example explicitly.
2. Treat every `.py` file under `docs` or `examples` identically.
3. Continue relying on ignores and directory naming.

## Recommendation

Choose option 1. Every Python file in a declared authoritative example root is
authoritative by default. Each root or subtree declares one default category:
static-and-smoke, static-only interactive, static-plus-optional-runtime, or
host-runtime. Record only files that are exceptions to that default. Imported
helper modules share their example's static gate. Draft and archive material
is not a category inside a published root: move it to an explicit
non-authoritative location and exclude it from published navigation, or
deliberately admit it.

Use `docs/examples/` by default. Core may retain `docs/assets/examples/` as an
approved exception. Other roots require recorded justification.

## Consequences

- Published scope and verification expectations are explicit.
- `__temp` and ignore rules stop functioning as undocumented policy.
- Each repository maintains declared roots, subtree defaults, and only the
  necessary per-file exceptions rather than a complete file-by-file manifest.

## Dependencies

ADR 001.
