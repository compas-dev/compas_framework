# Release Candidate Process

The current workflows prepare and verify release candidates. They cannot
publish packages, create GitHub releases, or deploy documentation. Publication
remains structurally absent while the live coordinated-candidate manifest and
protected retrieval environment are unconfigured.

1. Run **prepare-release** and select `patch`, `minor`, or `major`.
2. Review the generated release pull request, including the version and
   changelog changes.
   Confirm that the built COMPAS 3 metadata exposes no `rhino`, `blender`, or
   `hosts` extra. Those extras may return only after a later accepted decision,
   compatible dependency metadata, candidate artifacts, and real host-runtime
   verification.
3. After an explicitly approved merge, the release-candidate workflow detects
   the version change, runs quality and strict documentation checks, builds the
   wheel and source distribution once in temporary storage, and verifies them.
4. The workflow uploads the verified files only as a temporary GitHub Actions
   candidate artifact.

For a coordinated native release, every owning repository builds its wheel
once through its protected workflow. The reviewed framework manifest records
the producing run and immutable archive/wheel hashes. After the hosted native
gate passes, promotion follows this order:

```text
compas -> compas_occ / compas_cgal / compas_libigl -> compas_framework
```

Before each dependent promotion, the reusable public-file verifier checks that
all transitive upstream versions, filenames, and hashes match non-yanked PyPI
files. Before framework publication it checks the complete manifest. A missing
version, rebuilt filename, changed hash, or yanked file blocks promotion.

The candidate artifact is not approved for publication merely because it was
built. Do not create tags, GitHub releases, documentation deployments,
trusted-publisher environments, or upload jobs until the live manifest is
reviewed, the protected GitHub App environment is configured, and the hosted
positive integration gate passes. See the
[native candidate operations guide](https://github.com/compas-dev/compas_framework/blob/main/.github/candidates/README.md)
for the exact update and failure procedure.
