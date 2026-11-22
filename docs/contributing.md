# Contributing

Install [uv](https://docs.astral.sh/uv/) and synchronize the tooling environment
from the repository root:

```bash
uv sync --locked --project .github/tooling
```

Run focused tests while developing, then run the repository checks:

```bash
uv run --no-sync --project .github/tooling ruff check .
uv run --no-sync --project .github/tooling ruff format --check .
uv run --no-sync --project .github/tooling pyright
uv run --no-sync --project .github/tooling pytest -p no:cacheprovider tests/test_package.py
uv run --no-sync --project .github/tooling mkdocs build --strict
```

Use the canonical checkout and keep checkpoints visible in the handoff or
draft PR. Install native dependencies separately using the owning package's
documented environment when working on cross-package integration.
