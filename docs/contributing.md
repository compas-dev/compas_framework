# Contributing

Install [uv](https://docs.astral.sh/uv/), clone the repository, and synchronize
the locked development group:

```bash
uv sync --frozen --only-group dev --no-install-project
```

This is intentionally a tooling-only environment. Although `uv.lock` records
the full framework dependency graph, `--only-group dev --no-install-project`
does not install the project or native backends. Use a package-specific native
environment for cross-package geometry integration work.

Run focused tests while developing, then run the repository aliases:

```bash
uv run invoke test
uv run invoke check
uv run invoke typecheck
uv run invoke docs
```

Integration tests and examples should use public APIs and span package
boundaries. Package-local fixes belong in the owning package repository.

The Invoke tasks are thin aliases for Ruff, Pyright, pytest, MkDocs, and
`uv build`. The direct commands used by CI remain visible in the
workflow files.
