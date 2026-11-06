# Release Candidate Process

The current workflows prepare and verify release candidates. They cannot
publish packages, create GitHub releases, or deploy documentation. Those paths
remain structurally absent until cross-repository candidate provenance is
approved and implemented.

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

The candidate artifact is not approved for publication. Do not create tags,
GitHub releases, documentation deployments, trusted-publisher environments, or
upload jobs until the candidate-provenance decision is accepted and its gates
pass.
