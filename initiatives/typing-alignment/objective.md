# Typing Alignment Initiative

## Objective

Establish one simple, explicit, and consistent typing contract across the core
COMPAS framework, initially focusing on:

- `compas`
- `compas_occ`
- `compas_cgal`
- `compas_libigl`

The initiative should make public Python APIs, plugin boundaries, native
extension adapters, tests, and documentation agree on the values they accept
and return. A specific priority is correct and practical support for NumPy
types without weakening ordinary Python sequence support or obscuring runtime
requirements.

## Questions to resolve

1. Which public APIs accept Python sequences, NumPy arrays, NumPy scalar types,
   or COMPAS geometry objects?
2. Which reusable aliases, protocols, or overloads should express those
   contracts without introducing speculative abstraction?
3. How should array dtype, dimensionality, shape, contiguity, mutability, and
   ownership be documented and typed when Python's type system cannot express
   every runtime constraint?
4. Where should conversion and validation occur: core API, plugin boundary,
   backend adapter, or native extension?
5. How should `compas_occ` isolate untyped PythonOCC/SWIG APIs?
6. How should `compas_cgal` type NumPy/native buffers and distribute stubs for
   compiled extension modules?
7. How should `compas_libigl` replace native import suppressions with accurate
   stubs and coordinate its public results with core and CGAL?
8. Which uses of `Any`, casts, ignores, forward references, and broad concrete
   unions can be removed or localized?
9. Which Pyright, Ruff, test, and CI configuration should be shared across the
   four packages?

## Design principles

- Prefer simple, readable annotations that describe actual runtime behavior.
- Prefer capability- and operation-based duck typing at public Python
  boundaries. Type aliases describe verified common inputs; they are not
  runtime nominal allow-lists.
- Do not add nominal type checks, copies, or conversions solely to mirror an
  annotation. Validate eagerly only to protect a stated invariant, preserve
  object validity, or make a native call safe.
- Align with established COMPAS terminology and naming.
- Do not add conversions or runtime validation solely to satisfy a type
  checker.
- Keep NumPy optional where the runtime API is genuinely sequence-based.
- Use NumPy-specific types where dtype, buffer layout, or vectorized behavior
  is part of the real contract.
- Isolate untyped native-library boundaries instead of spreading `Any` through
  public APIs.
- Be explicit about constraints that annotations cannot enforce.
- Avoid speculative generic frameworks, shape-typing systems, or compatibility
  layers without current consumers.
- Keep code, annotations, runtime validation, tests, documentation, and stubs
  consistent.

## Initial deliverables

1. `inventory.md` describing current conventions, inconsistencies, NumPy
   boundaries, tooling, tests, and risks in all four packages.
2. `proposal.md` defining recommended public and native-boundary contracts,
   alternatives, migration effects, verification, and implementation phases.
3. One ADR per significant independent typing decision.
4. An implementation plan with package/file ownership, dependencies, and safe
   opportunities for parallel work.

## Verification target

Use the `compas3` environment. Before completion, affected packages must pass:

- relevant and full feasible tests;
- Ruff check and format verification;
- Pyright with zero errors;
- NumPy compatibility tests covering supported scalar, array, dtype, shape,
  and layout cases;
- native-extension import and stub checks where applicable;
- documentation verification for changed public contracts.

## Non-goals for the initial phase

- Changing runtime behavior merely to make annotations easier.
- Typing every optional COMPAS ecosystem package.
- Introducing a universal tensor/array abstraction.
- Replacing NumPy or PythonOCC/native APIs.
- Preserving incorrect or misleading annotations for compatibility.
- Editing package source before the architecture and ADRs are approved.

## Current status

Implementation is in progress. ADRs 001–017 and Geometry ADRs 022–023 are
Accepted. Their remaining source slices are authorized in dependency order but
remain incomplete and unverified. Approved work preserves duck typing through
Python code and localizes normalization to explicit native, serialization,
ownership, and retained-representation boundaries. `compas_libigl` joined the
initiative on 2026-11-05 to align its native mesh plugins and replace
incomplete native typing with the shared contract. CGAL skeletonisation output
remains a known correctness limitation: typing, stub, or packaging checks must not be treated
as functional validation of that module.
