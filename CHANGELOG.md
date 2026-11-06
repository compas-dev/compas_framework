# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## Unreleased

### Added

* Added the geometry-tessellation initiative inventory, architecture proposal, accepted decision records, and coordinated implementation plan.
* Added cross-package integration tests for continuous-geometry tessellation, triangle-processing plugin boundaries, serialization, and native geometry backends.

### Changed

* Documented the COMPAS 3 geometry package compatibility matrix, native backend prerequisites, and geometry integration test workflow.
* Replaced legacy development extras and mutable workflows with locked PEP 735 tool groups, uv-based contributor commands, immutable actions, and Python 3.12–3.14 checks.
* Modernized release-candidate automation to build and verify one temporary
  artifact set while keeping publication, GitHub releases, and documentation
  deployment disabled pending the candidate-provenance decision.

### Removed

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
