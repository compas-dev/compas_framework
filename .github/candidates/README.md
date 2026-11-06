# Native candidate manifest

`native-linux-py312.json` is the sole authority for the coordinated COMPAS,
OCC, CGAL, and libigl candidate set on Ubuntu 24.04, x86-64, and Python 3.12.
[`schema-v1.json`](schema-v1.json) documents its machine-readable structure;
the verifier additionally enforces normalized identities, graph constraints,
wheel metadata, and the exact live package/repository set.

The live manifest is intentionally absent until all four owning workflows have
produced successful, unexpired artifacts. Run IDs, artifact IDs, filenames,
and hashes must not be fabricated or represented by placeholders. The schema,
unit tests, and negative security contracts use generated temporary fixtures,
not a pretend live manifest.

To create or update the manifest:

1. obtain a successful protected workflow run from each owning repository;
2. record the exact commit, workflow path, run attempt, pull request and base;
3. download the selected one-wheel artifact and compute the archive and wheel
   SHA-256 digests;
4. run `python .github/scripts/candidate_artifacts.py validate-manifest
   .github/candidates/native-linux-py312.json --live`;
5. request review of the manifest and producer runs; and
6. dispatch the trusted native candidate workflow only after the
   `candidate-artifact-retrieval` environment is configured.

The manifest must contain only candidate packages. Third-party runtime pins
live in `runtime-linux-py312.txt` and
`environment-native-linux-py312.yml`; the Python set is complete enough to be
installed with `--no-deps` and therefore performs no implicit resolution.
The Conda file fixes the Python patch and OCC/OCCT API versions; Conda build
identifiers and their transitive system libraries remain solver-selected and
are recorded by the hosted job rather than claimed as bit-reproducible inputs.

## Trusted retrieval

Organization owners configure a GitHub App with read-only Actions access to
only `compas`, `compas_occ`, `compas_cgal`, and `compas_libigl`. Store its App
ID and private key as `CANDIDATE_ARTIFACT_APP_ID` and
`CANDIDATE_ARTIFACT_PRIVATE_KEY` in the protected
`candidate-artifact-retrieval` environment. Ordinary pull requests never use
that environment or those secrets. The trusted workflow also refuses to run
outside `compas-dev/compas_framework` or from an unprotected ref.

The retrieval job checks the owning non-fork pull request, workflow run,
artifact ID, GitHub archive digest, safe one-wheel archive layout, wheel hash,
metadata, target tags, and declared candidate dependencies. It emits a
one-day, credential-free bundle. A separate job with no repository permission,
checkout, or secret revalidates the bundle, installs every selected wheel in
dependency order with `--no-index --no-deps`, and runs installed plugin,
runtime, and typing contracts.

The workflow fails closed for missing or expired artifacts, unsuccessful or
fork-origin runs, changed digests, extra archive members, incompatible tags,
dependency drift, any skipped/failed/errored native test, an empty test suite,
or a missing required test ID.

The read-only Actions API does not expose repository branch-protection rules.
Manifest review must therefore confirm that every recorded PR base is
protected and that `.github/workflows/build.yml` is the approved producer
workflow. The live verifier rejects other workflow paths and events, but this
repository-settings check remains an explicit human trust boundary.

## Promotion

Before a dependent package is promoted, run `verify-public-candidates.yml`
with `before` set to that distribution. The verifier requires every transitive
upstream version, filename, and SHA-256 from the manifest to exist as a
non-yanked PyPI file. With no `before` value it checks all four packages before
the framework can be published. Promotion reuses the selected wheels; it does
not rebuild them.

The framework repository currently contains no publication job. Until the
live manifest exists, the protected environment is configured, and the hosted
positive gate passes, framework publishing remains structurally disabled.

