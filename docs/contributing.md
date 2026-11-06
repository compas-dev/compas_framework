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

Changes to coordinated candidate infrastructure use the isolated locked group:

```bash
uv sync --frozen --only-group candidate --no-install-project
uv run --no-sync pytest .github/tests/test_candidate_artifacts.py
uv run --no-sync ruff check .github/scripts/candidate_artifacts.py .github/candidates .github/tests/test_candidate_artifacts.py
```

These checks use generated fixtures and need no GitHub credential. Trusted
cross-repository retrieval is a separately dispatched, protected workflow; do
not place App credentials in a local environment or pull-request workflow.
