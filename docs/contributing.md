# Contributing

Install [uv](https://docs.astral.sh/uv/), clone the repository, and synchronize
the locked development group:

```bash
uv sync --locked --only-group dev --no-install-project
```

This is intentionally a tooling-only environment. Although `uv.lock` records
the full framework dependency graph, `--only-group dev --no-install-project`
does not install the project or native backends. Use a package-specific native
environment, such as `compas3`, for local native geometry integration work.

Run focused tests while developing, then run the repository aliases:

```bash
uv run --no-sync invoke check typecheck test docs
```

Integration tests and examples should use public APIs and span package
boundaries. Package-local fixes belong in the owning package repository.

The Invoke tasks are thin aliases for Ruff, Pyright, pytest, MkDocs, and
`uv build`. The direct commands used by CI remain visible in the
workflow files.

Use each repository's canonical checkout and make progress visible through the
initiative handoff and draft pull request. Keep one writer per repository at a
time. Read-only work and writes in different repositories can run in parallel.
Create an additional worktree only when explicitly requested and record its
visible path, branch, and owner in the handoff.

Changes to coordinated candidate infrastructure use the isolated locked group:

```bash
uv sync --frozen --only-group candidate --no-install-project
uv run --no-sync pytest .github/tests/test_candidate_artifacts.py
uv run --no-sync ruff check .github/scripts/candidate_artifacts.py .github/candidates .github/tests/test_candidate_artifacts.py
```

These checks use generated fixtures and need no GitHub credential. Trusted
cross-repository retrieval is a separately dispatched, protected workflow; do
not place App credentials in a local environment or pull-request workflow.
