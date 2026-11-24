# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## Unreleased

### Added

* Added the geometry-tessellation initiative inventory, architecture proposal, accepted decision records, and coordinated implementation plan.
* Added cross-package integration tests for continuous-geometry tessellation, triangle-processing plugin boundaries, serialization, and native geometry backends.
* Added immutable cross-repository candidate manifests, provenance and wheel
  verification, secret-isolated native integration, and release-order checks.
* Added a framework package matrix and a manual clean-install check for the
  declared Python and operating system targets.

### Changed

* Use canonical checkouts for initiative work and run ordinary CI on pull
  requests targeting any base branch.
* Keep sibling-checkout fixtures outside the pure suite and validate scene
  candidate pins without duplicating their revisions.
* Documented the COMPAS 3 geometry package compatibility matrix, native backend prerequisites, and geometry integration test workflow.
* Replaced legacy development extras and mutable workflows with locked PEP 735 tool groups, uv-based contributor commands, immutable actions, and Python 3.12–3.14 checks.
* Modernized release-candidate automation to build and verify one temporary
  artifact set while keeping publication, GitHub releases, and documentation
  deployment disabled until the reviewed live candidate set passes its hosted
  integration gate.

### Removed

* Moved initiative coordination plans, handoffs, and Codex agent roles to
  the COMPAS Hub. Framework retains the technical decision records.
* Removed the `rhino`, `blender`, and `hosts` extras from the COMPAS 3
  metapackage until their owning packages declare compatible dependencies and
  pass host-runtime verification. Existing COMPAS 2 releases are unchanged.

## [0.1.3] 2025-06-04

### Added

### Changed

* Changed `compas_notebook` to optional requirments.

### Removed


## [0.1.2] 2025-05-28

### Added

### Changed

### Removed


## [0.1.1] 2025-05-28

### Added

### Changed

### Removed
