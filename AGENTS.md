# COMPAS Framework — Agent Instructions

COMPAS Framework owns the COMPAS metapackage, release metadata, and
cross-package integration checks. Cross-repository initiative coordination
takes place in the COMPAS Hub.

## Engineering Principles

- Prefer the simplest solution that fully satisfies the approved requirements.
- Treat complexity as a design warning. If a solution is not simple, clean,
  transparent, and easy to explain, reconsider the design before implementing
  it.
- Do not add speculative abstractions, extension points, metadata, compatibility
  layers, or future-oriented features without a current requirement and an
  approved architectural decision.
- Follow established COMPAS style, terminology, naming, data models, and API
  conventions whenever they fit the approved design.
- Be explicit about inputs, outputs, units, validation, failure modes,
  approximation, mutation, ownership, and unsupported cases.
- Keep equivalent concepts and operations consistent across packages.
- Prefer one clear public path over overlapping aliases or multiple ways to
  perform the same operation.
- Document public behavior and significant internal design choices. Include
  explanations, examples, mathematical assumptions, and references where they
  help users or maintainers understand the contract.

## Default Environment

- Use the locked, tooling-only uv environment for ordinary checks. Sync with
  `uv sync --locked --only-group dev --no-install-project`, then use
  `uv run --no-sync invoke` with the tasks listed in the contributor guide.
- Use `compas3` for local native and sibling-checkout integration unless the
  owning package specifies another environment. The maintainer's interpreter is:

  ```text
  /Users/vanmelet/miniforge3/envs/compas3/bin/python
  ```

- Verify native package imports with `compas3` before reporting a compiled
  extension as unavailable.

## Checkouts and Progress

- Work in each repository's canonical checkout on the agreed task branch.
  Check the branch and working tree before editing, and preserve existing changes.
- Create an additional worktree only when explicitly requested. Use an agreed,
  visible path outside system temporary directories and record its path, branch,
  owner, and cleanup status in the pull request.
- At meaningful checkpoints, report the checkout, branch, changed files, and
  verification status. When commits and pushes are authorized, keep the draft PR
  current so progress is visible.

## Documentation and Public API

- Follow the documentation instructions of the repository that owns the code.
- For COMPAS repositories, use MkDocs/mkdocstrings-compatible NumPy-style
  docstrings with Markdown content. Never add Sphinx or reStructuredText
  markup.
- Apply the repository-local `update-docstrings` skill whenever docstrings,
  rendered API pages, examples, or documentation-facing signatures are
  touched.
- Documentation-only changes must not alter runtime behavior.
- Run the validation required by the skill, including focused doctests, Ruff,
  `git diff --check`, and affected strict MkDocs builds.

## Repository Skills

- Use `update-docs` for project documentation, MkDocs navigation, tutorials,
  examples, API pages, license, and changelog work.
- Use `update-docstrings` for Python docstrings, rendered signatures, and
  documentation-facing Python examples.
- Use `update-type-hints` for Python type annotations and typed integration
  boundaries.
- Read the selected skill completely before acting. Skills provide workflow
  guidance; `AGENTS.md`, accepted ADRs, and implemented behavior remain
  authoritative.

## Verification Responsibilities

- Local checks provide fast, focused feedback before work is pushed. Run the
  narrowest relevant tests, Ruff, Pyright, documentation checks, and native
  imports in the documented package environment.
- Package CI is the authoritative clean-environment check for one repository.
  It verifies that the committed package branch builds and passes its own
  configured quality, test, documentation, and artifact jobs.
- Framework integration CI verifies coordinated package revisions together.
  Pin the exact candidate commits and exercise cross-package runtime, plugin
  discovery, typing, serialization, and native-backend contracts that cannot
  be established by an individual package workflow.
- Candidate-artifact CI verifies the exact wheels and distributions intended
  for admission or release. A source build or editable install does not count
  as evidence that independently built or published artifacts work together.
- Record the evidence for every applicable verification layer in the pull
  request. Report each result as passed, failed, not run, or unavailable.
- Completion requires all applicable local, package, framework-integration,
  and candidate-artifact checks. If a layer does not apply, state why. If a
  required layer cannot run, leave that layer explicitly unverified.

## Rules

- Do not modify package source code before approval.
- Never assume an API exists without inspecting code.
- Keep changes focused, reversible, and within the accepted decisions.
- Preserve existing behavior unless approved.
- Do not claim tests passed without running them.
- Do not claim implementation completion unless relevant tests, Ruff, and
  Pyright pass. If a required check cannot run because of an environmental or
  dependency limitation, report that limitation explicitly and leave the work
  unverified rather than treating the check as passed.
- Add or update tests for every changed contract, failure mode, and regression.
- Tests must write generated files, exported geometry, snapshots, caches, and
  other runtime artifacts to an isolated temporary directory, such as pytest's
  `tmp_path` or `tmp_path_factory`, never to the project root, package source,
  documentation, or committed fixture directories. Committed fixtures must be
  explicit, read-only test inputs; a test must not depend on an ignored or
  locally generated file being present in the working tree.
- Add or update documentation with every public API or behavior change.
- Keep code, tests, type annotations, documentation, ADRs, and examples
  mutually consistent.
- Record architectural decisions.
- Do not merge or publish without explicit approval.

## Architecture Decision Records

For significant architectural changes affecting COMPAS Framework:

1. Identify significant architectural decisions during the proposal phase.
2. Create one ADR per independent decision.
3. Compare viable alternatives and recommend a preferred option.
4. Mark new ADRs as Proposed.
5. Never mark an ADR Accepted without explicit user approval.
6. Record approved choices and their rationale.
7. Identify dependencies between ADRs.
8. Do not implement tasks blocked by unresolved ADRs.
9. Revisit accepted ADRs only when new evidence warrants reconsideration.
