# Contributing to COMPAS Framework

Contributions are welcome and very much appreciated!

## Code contributions

We accept code contributions through pull requests.
In short, this is how that works.

1. Fork [the repository](https://github.com/compas-dev/compas_framework) and clone the fork.
2. Install Python 3.12–3.14 and [uv](https://docs.astral.sh/uv/).
3. From the repository root, synchronize the locked tooling environment:

   ```bash
   uv sync --locked --project .github/tooling
   ```

4. Start making changes on a branch based on `main`.
5. Run the ordinary checks:

   ```bash
   uv run --no-sync --project .github/tooling ruff check .
   uv run --no-sync --project .github/tooling ruff format --check .
   uv run --no-sync --project .github/tooling pyright
   uv run --no-sync --project .github/tooling pytest -p no:cacheprovider tests/test_package.py
   uv run --no-sync --project .github/tooling mkdocs build --strict
   ```

6. Commit, push, and open a pull request.

The tooling environment installs repository checks independently of the
framework and its native dependencies. Use an environment documented by the
owning package when running native or cross-package integration.

Use the canonical checkout for each repository. Keep one writer per repository
and record checkpoints in the initiative handoff or draft PR. Create an
additional worktree only when explicitly requested, with a visible path and
owner recorded in the handoff.

## Bug reports

When [reporting a bug](https://github.com/compas-dev/compas_framework/issues) please include:

* Operating system name and version.
* Any details about your local setup that might be helpful in troubleshooting.
* Detailed steps to reproduce the bug.

## Feature requests

When [proposing a new feature](https://github.com/compas-dev/compas_framework/issues) please include:

* Explain in detail how it would work.
* Keep the scope as narrow as possible, to make it easier to implement.
