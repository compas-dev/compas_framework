# Contributing to COMPAS Framework

Contributions are welcome and very much appreciated!

## Code contributions

We accept code contributions through pull requests.
In short, this is how that works.

1. Fork [the repository](https://github.com/compas-dev/compas_framework) and clone the fork.
2. Install [uv](https://docs.astral.sh/uv/).
3. Synchronize the locked, tooling-only development environment:

   ```bash
   uv sync --locked --only-group dev --no-install-project
   ```

4. Run the ordinary repository checks:

   ```bash
   uv run --no-sync invoke check typecheck test docs
   ```

5. Branch from `main` for ordinary changes. For COMPAS 3 upgrade work, use
   `c3-upgrade` or the base agreed for the initiative in the COMPAS Hub.
6. Repeat the ordinary checks and run any relevant integration checks:

   ```bash
   uv run --no-sync invoke check typecheck test docs
   ```

7. Commit your changes and push your branch to GitHub.
8. Create a [pull request](https://help.github.com/articles/about-pull-requests/) through the GitHub website.

During development, use [pyinvoke](http://docs.pyinvoke.org/) tasks on the
command line to ease recurring operations:

* `uv run --no-sync invoke check`: Run Ruff lint and format checks.
* `uv run --no-sync invoke test`: Run the pure package tests.
* `uv run --no-sync invoke typecheck`: Run Pyright over the metapackage and pure tests.
* `uv run --no-sync invoke docs`: Build the MkDocs documentation strictly into temporary storage.
* `uv run --no-sync invoke build`: Build wheel and source distributions into temporary storage.
* `uv run --no-sync invoke --list`: Show available aliases.

Use the canonical checkout for each repository and record progress and
verification in the pull request. Create an additional worktree only when
explicitly requested and record its visible path, branch, and owner.

## Bug reports

When [reporting a bug](https://github.com/compas-dev/compas_framework/issues) please include:

* Operating system name and version.
* Any details about your local setup that might be helpful in troubleshooting.
* Detailed steps to reproduce the bug.

## Feature requests

When [proposing a new feature](https://github.com/compas-dev/compas_framework/issues) please include:

* Explain in detail how it would work.
* Keep the scope as narrow as possible, to make it easier to implement.
