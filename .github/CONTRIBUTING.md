# Contributing to COMPAS Framework

Contributions are welcome and very much appreciated!

## Code contributions

We accept code contributions through pull requests.
In short, this is how that works.

1. Fork [the repository](https://github.com/compas-dev/compas_framework) and clone the fork.
2. Create a virtual environment using your tool of choice (e.g. `virtualenv`, `conda`, etc).
3. Install development dependencies:

   ```bash
   python -m pip install -e ".[dev,docs]"
   ```

4. Make sure all tests pass:

   ```bash
   invoke test
   ```

5. Start making your changes on a feature branch based on **main**.
6. Make sure all tests still pass:

   ```bash
   invoke test
   ```

7. Commit your changes and push your branch to GitHub.
8. Create a [pull request](https://help.github.com/articles/about-pull-requests/) through the GitHub website.

During development, use [pyinvoke](http://docs.pyinvoke.org/) tasks on the
command line to ease recurring operations:

* `invoke clean`: Clean all generated artifacts.
* `invoke check`: Run various code and documentation style checks.
* `invoke test`: Run all tests and checks in one swift command.
* `invoke typecheck`: Run Pyright over integration code and tests.
* `invoke docs`: Build the MkDocs documentation.
* `invoke`: Show available tasks.

## Bug reports

When [reporting a bug](https://github.com/compas-dev/compas_framework/issues) please include:

* Operating system name and version.
* Any details about your local setup that might be helpful in troubleshooting.
* Detailed steps to reproduce the bug.

## Feature requests

When [proposing a new feature](https://github.com/compas-dev/compas_framework/issues) please include:

* Explain in detail how it would work.
* Keep the scope as narrow as possible, to make it easier to implement.
