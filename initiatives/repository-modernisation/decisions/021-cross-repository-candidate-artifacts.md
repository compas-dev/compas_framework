# ADR 021: Cross-Repository Candidate Artifact Provenance

**Status:** Proposed

## Context

Accepted ADR 013 requires the framework integration gate to install the exact
candidate artifacts of coordinated core packages before downstream release.
The initial workflow draft instead pins Git commits and runs `pip install` on
their source URLs. That can rebuild different artifacts, resolve undeclared
members of the candidate set from an index, and does not prove which hosted
workflow produced the installed wheel. Pytest can also exit successfully when
a required native-backend test is skipped.

The framework repository's token is scoped to that repository and must not be
assumed to read Actions artifacts from `compas`, `compas_occ`, `compas_cgal`,
or `compas_libigl`. Cross-repository artifact access and its credential model
therefore need an explicit decision. This is distinct from configuring the
credential or publishing any package.

## Options

### 1. Install immutable Git source revisions

Keep a constraints file of full commit SHAs and let pip build or install each
repository.

This proves source identity but not artifact identity. Build isolation and
dependency resolution may select packages outside the declared candidate set,
and the result is not necessarily the wheel later promoted by the owning
repository.

### 2. Test only already-published exact versions and hashes

Release every upstream package first, then install exact PyPI files by version
and hash before publishing `compas_framework`.

This needs no cross-repository Actions credential and proves the files used by
the final metapackage. It cannot prevent publication of an incompatible
upstream candidate because integration occurs only after those packages are
already public.

### 3. Verify a manifest of hosted candidate artifacts

Each owning repository builds and uploads its candidate wheel through its
normal protected workflow. A framework-owned manifest records, for each
coordinated package:

- repository and successful workflow run;
- exact head commit;
- artifact name and archive digest;
- distribution version, selected wheel filename, and wheel SHA-256; and
- dependencies on other entries in the candidate set.

The manifest also fixes the integration target—initially Python 3.12 on the
Linux x86-64 runner—and each selected wheel must have a compatible Python,
ABI, and platform tag. A single filename without this execution context is not
an adequate artifact contract.

A read-only organization GitHub App grants the framework workflow Actions
artifact access only to the repositories in the manifest. The workflow checks
run provenance and every digest, installs only the selected wheels with
`--no-index --no-deps`, installs the framework candidate wheel, and then runs
the cross-package contracts. A JUnit post-check treats any failed, errored,
skipped, or zero-test native suite as a failed gate.

## Recommendation

Choose option 3.

This is the only option that verifies the same immutable candidate artifacts
before dependent packages are published. Keep the mechanism narrow:

- one JSON manifest is the sole candidate-set authority;
- source URLs, editable installs, and a second candidate constraints file are
  forbidden;
- the GitHub App receives read-only Actions access to only the admitted core
  repositories;
- the private key is stored as a repository or organization Actions secret and
  is never exposed to pull requests from forks;
- credentialed retrieval and candidate execution run in separate jobs: the
  retrieval job validates provenance, hashes, and wheel metadata, emits one
  verified bundle, revokes its token, and ends; the execution job receives no
  secrets or write permission before installing or importing candidate code;
- third-party native runtimes are pinned separately from COMPAS candidates;
- candidate wheels are installed without dependency or index resolution; and
- the framework publication job depends on successful candidate verification.

Candidate verification happens before any coordinated candidate is published.
Promotion then follows this explicit dependency order:

```text
candidate set passes integration
             ↓
           compas
        ↙     ↓     ↘
compas_occ compas_cgal compas_libigl
        ↘     ↓     ↙
      compas_framework
```

Every package is built once. Before publishing a dependent package, its
release job verifies that every declared upstream distribution is already
published and that the selected public filename, version, and SHA-256 match
the candidate manifest. `compas_framework` is published only after every
declared upstream artifact passes the same public-file match. Promotion never
rebuilds a wheel.

The manifest records only packages participating in the coordinated change.
Adding another package is an explicit manifest and test change, not implicit
resolution from PyPI.

## Compatibility and operational implications

- `compas` and `compas_occ` must upload installable candidate distributions;
  CGAL and libigl may reuse their verified platform wheel artifacts.
- Successful hosted run IDs, filenames, versions, and digests cannot be filled
  speculatively. Placeholder, expired, failed, or mismatched artifacts are hard
  failures.
- The initial integration manifest selects Python 3.12 and the Linux x86-64
  runner. Additional required platforms use explicit selected artifacts and
  hosted gates; they are not inferred from one Linux result.
- Repository owners must install and configure the read-only GitHub App before
  hosted positive verification can pass. This ADR does not authorize that
  settings change.
- Only explicitly admitted commits and successful artifacts from protected
  owning workflows enter the manifest. A fork-origin run is not trusted merely
  because its archive digest is recorded.
- Framework publishing remains disabled or blocked until the candidate gate is
  configured and passes.
- No package merge, release, publication, deployment, or settings mutation is
  authorized by this decision.

## Implementation consequences

After acceptance:

1. add candidate artifact jobs to `compas` and `compas_occ` and verify the
   selected CGAL/libigl wheel artifacts;
2. replace the Git-source constraints draft with one validated JSON manifest;
3. add focused scripts for artifact retrieval/provenance, wheel metadata and
   hash verification, exact installation, and JUnit skip enforcement;
4. split the workflow into a minimal credentialed retrieval job and a
   secret-free candidate execution job, without persisted checkout or App
   credentials;
5. make the native-integration workflow reusable from framework build and
   release workflows;
6. add release-order checks that match each published upstream file back to
   the approved candidate version, filename, and SHA-256 before dependents can
   publish;
7. make framework publication depend on both the native gate and successful
   public-file matches for every declared upstream artifact; and
8. document the candidate update, dependency order, credential ownership, and
   failure modes.

## Verification

- Unit tests cover manifest schema, duplicate packages, unknown dependencies,
  dependency cycles/order, placeholders, wrong run SHA/conclusion, expired or
  missing artifacts, wrong archive/wheel hashes, wrong wheel metadata, and
  missing wheels.
- JUnit tests cover pass, failure, error, skip, and zero-test results.
- Workflow security checks cover immutable actions, least permissions, fork
  admission, retrieval/execution job isolation, absence of secrets during
  candidate execution, and absence of credential persistence.
- A hosted positive run installs the exact four recorded package artifacts and
  the framework wheel in a clean Python 3.12 native environment.
- Hosted negative checks prove that a changed digest and a skipped required
  backend both fail the gate.
- Release-order fixtures prove that a missing upstream publication, different
  version, rebuilt filename, or changed public-file hash blocks every
  dependent promotion.
- The framework publish job remains blocked when candidate verification fails.

## Dependencies

ADRs 008, 010, 012, and 013.
