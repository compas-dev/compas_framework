# Contributing to COMPAS Framework

Contributions are welcome and very much appreciated!

## Code contributions

We accept code contributions through pull requests.
In short, this is how that works.

1. Fork [the repository](https://github.com/compas-dev/compas_framework) and clone the fork.
2. Install [uv](https://docs.astral.sh/uv/).
3. Synchronize the locked, tooling-only development environment:

   ```bash
   uv sync --frozen --only-group dev --no-install-project
   ```

4. Make sure all tests pass:

   ```bash
   uv run invoke test
   ```

5. Start making your changes on a feature branch based on **main**.
6. Make sure all tests still pass:

   ```bash
   uv run invoke test
   ```

7. Commit your changes and push your branch to GitHub.
8. Create a [pull request](https://help.github.com/articles/about-pull-requests/) through the GitHub website.

During development, use [pyinvoke](http://docs.pyinvoke.org/) tasks on the
command line to ease recurring operations:

* `uv run invoke check`: Run Ruff lint and format checks.
* `uv run invoke test`: Run the pure package tests.
* `uv run invoke typecheck`: Run Pyright over the coordination package and pure tests.
* `uv run invoke docs`: Build the MkDocs documentation strictly into temporary storage.
* `uv run invoke build`: Build wheel and source distributions into temporary storage.
* `uv run invoke --list`: Show available aliases.

## Bug reports

When [reporting a bug](https://github.com/compas-dev/compas_framework/issues) please include:

* Operating system name and version.
* Any details about your local setup that might be helpful in troubleshooting.
* Detailed steps to reproduce the bug.

## Feature requests

When [proposing a new feature](https://github.com/compas-dev/compas_framework/issues) please include:

* Explain in detail how it would work.
* Keep the scope as narrow as possible, to make it easier to implement.
