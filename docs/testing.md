# Testing Strategy

Framework tests are organized by the contract they exercise:

- plugin discovery and dispatch through public COMPAS APIs;
- data roundtrips across serialization formats and package boundaries;
- end-to-end workflows combining geometry, algorithms, models, and viewing;
- performance baselines for representative cross-package operations; and
- packaging checks for the supported Python and operating-system matrix.

## Pure repository checks

The ordinary pull-request matrix covers Python 3.12, 3.13, and 3.14 on Linux,
macOS, and Windows without installing the framework runtime dependencies:

```bash
uv sync --locked --only-group dev --no-install-project
uv run --no-sync ruff check .
uv run --no-sync ruff format --check .
uv run --no-sync pyright
uv run --no-sync pytest tests/test_package.py
```

CI also inspects the synchronized environment and fails if any framework
distribution, including OCC, CGAL, or libigl, was installed.

## Distribution artifacts

The package job builds one wheel and one source distribution into the runner's
temporary directory. The same files are checked for complete metadata and
expected runtime requirements, installed with `--no-deps` in an isolated
environment, and uploaded for review. This verifies the coordination package
without downloading its native runtime backends.

Documentation is built separately and strictly:

```bash
uv sync --frozen --only-group docs --no-install-project
uv run --no-sync mkdocs build --strict
```

CI supplies a temporary `--site-dir`; generated documentation never lands in
the repository checkout.

## Complete installation

The manual `framework-install.yml` workflow builds the metapackage from a
selected commit and installs it from scratch with its dependencies from PyPI.
It runs dependency checks on every target in the [package matrix](packages.md).
Run it after the matching upstream distributions are available. The runtime
and artifact gates supply separate evidence of cross-package behavior and
exact artifact provenance.

## Native integration

`native-candidate-integration.yml` is the authoritative Linux x86-64,
Python 3.12 candidate gate. A reviewed JSON manifest selects the exact COMPAS,
OCC, CGAL, and libigl wheels by owning workflow run, artifact, filename, and
SHA-256. Credentialed retrieval produces a verified offline bundle. A separate
secret-free job installs that bundle and the framework wheel with
`--no-index --no-deps`, then verifies installed distribution versions, plugin
discovery, CGAL-to-core-to-libigl data flow, OCC BRep construction, and the
external typing consumer.

The JUnit post-check rejects a failed, errored, skipped, or empty suite and
requires every named integration test. A skip is therefore useful diagnostic
information but never passing candidate evidence. The reviewed live manifest
is recorded, and the protected non-main integration ref plus read-only GitHub
App environment are configured. Protected run `42299118381` provides the
required hosted-positive evidence at `d0c9d4e`. Credentialed
retrieval, framework-wheel construction, and secret-free execution all pass;
the four required runtime tests report no skips, and installed-wheel Pyright
reports zero errors and warnings. Main remains untouched.

The selected `run_attempt` must be successful. GitHub reruns may retain outputs
from successful jobs in an earlier attempt and use them in dependent jobs of
the selected successful attempt. Candidate admission therefore binds the
artifact to its exact workflow-run ID, commit, repository, API digest, archive
digest, and wheel digest; it does not incorrectly require the retained
artifact's creation timestamp to fall after the selected attempt's start. An
artifact created after the selected successful attempt completed is rejected.

`candidate-contracts.yml` runs on ordinary pull requests without secrets. It
checks the schema, provenance rules, archive safety, wheel metadata, offline
revalidation, release-order fixtures, and focused negative cases proving that
a changed digest and a skipped backend are rejected.

The pending geometry fixtures live under `tests/integration/`. For local
diagnostics, explicitly select a file in that directory from `compas3`. The
fixtures require the Core, OCC, CGAL, and libigl sibling checkouts. Bare
`pytest` runs the pure suite and never loads those checkouts.

Geometry-tessellation performance thresholds are deferred until the framework
has an environment-normalized benchmark runner. Wall-clock assertions in this
suite would primarily measure plugin discovery, native-library loading, and CI
machine variance rather than tessellation regressions. Future benchmarks
should use the existing `performance`
marker with recorded input sizes, warm-up policy, backend versions, and
per-backend baselines.
