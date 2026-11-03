# Geometry Discretization, Tessellation, and Triangulation

## Objective

Modernize and unify the discretization, tessellation, and triangulation APIs across the core COMPAS packages.

Establish consistent methods for converting parametric shapes, surfaces, quad and triangle surfaces, and polygonal meshes into discrete mesh representations.

The resulting interfaces should be intuitive, extensible, and suitable for use by geometry-processing plugins such as `compas_cgal`, which operate on triangle mesh representations.

The initiative should build on existing COMPAS abstractions and conventions, avoiding unnecessary duplication or architectural complexity.

## Scope

The initiative covers:

- Discretization and tessellation of analytical and parametric shapes and surfaces.
- Tessellation of NURBS surfaces, including trimmed surfaces.
- Triangulation of quad meshes and general polygonal meshes.
- Unified conversion to triangle mesh representations.
- Tessellation and triangulation strategies.
- Evaluation of dedicated mesh representations.
- Integration with geometry-processing plugins.
- Consistent testing, documentation, and examples across affected packages.

Relevant packages include `compas`, `compas_occ`, `compas_cgal`, and potentially other packages identified during the investigation.

## Conceptual Terminology

Establish a consistent distinction between the following operations:

| Operation | Meaning |
|---|---|
| Sampling | Evaluating discrete points on continuous geometry |
| Discretization | Representing continuous geometry using discrete samples |
| Tessellation | Approximating continuous surfaces with polygonal meshes |
| Triangulation | Partitioning polygonal faces or domains into triangles |
| Refinement | Increasing mesh resolution |
| Remeshing | Reconstructing or modifying mesh discretization |
| Simplification | Reducing mesh complexity |

These definitions should guide API naming and documentation while remaining compatible with established computational geometry terminology.

## API Design Principles

### 1. Consistent operations and conversions

Investigate a unified set of methods across supported geometry representations.

Candidate operations include:

```python
surface.tessellate(...)
mesh.triangulate(...)
mesh.triangulated(...)
geometry.to_mesh(...)
geometry.to_triangle_mesh(...)
```

Distinguish between:

- **Operations**, such as tessellation and triangulation.
- **Representation conversions**, such as `to_mesh()` and `to_triangle_mesh()`.
- **Mutating and non-mutating methods**, following existing COMPAS conventions.

Avoid introducing redundant methods without a clear semantic distinction.

### 2. Explicit tessellation strategies

Separate the tessellation operation from the strategy controlling how the approximation is constructed.

Investigate at least two strategy families:

**Resolution-controlled tessellation**

```python
surface.tessellate(strategy=UVGrid(nu=32, nv=16))
```

**Error-controlled tessellation**

```python
surface.tessellate(
    strategy=Adaptive(
        max_deviation=0.01,
        max_angle=0.1,
    )
)
```

Strategies should be lightweight, serializable configuration objects, preferably compatible with the COMPAS `Data` infrastructure.

Clearly distinguish resolution control, error estimation, and mathematically guaranteed error bounds.

The strategy should describe the approximation policy without necessarily implementing the underlying geometry algorithm.

### 3. Separate tessellation and triangulation

Tessellation and triangulation should remain conceptually distinct.

For example:

```python
quadmesh = torus.tessellate(strategy=UVGrid(32, 16))

trimesh = quadmesh.triangulated()
```

Triangulation strategies may include diagonal splitting, ear clipping, and constrained triangulation where appropriate.

Consider whether output topology should be specified independently from tessellation strategy.

### 4. Unified triangle mesh interoperability

Provide a consistent interface for obtaining triangle mesh representations from supported geometry objects, regardless of their underlying representation.

Conceptually:

```python
trimesh = geometry.to_triangle_mesh(...)
```

The implementation may internally perform tessellation, triangulation, or a combination of both.

Geometry-processing plugins should not need to understand the specific source geometry representation.

Investigate whether the interface should be implemented through instance methods, a common conversion function, protocols, or a combination of these.

### 5. Dedicated mesh representations

Evaluate the benefits of introducing specialized representations such as:

- `TriangleMesh`
- `QuadMesh`
- `TessellationResult`

Distinguish between rich topological mesh objects and lightweight computational representations based on vertices and faces.

In particular, investigate whether a compact `TriangleMesh` would provide a useful common interchange representation for computational geometry plugins.

Avoid introducing parallel mesh hierarchies without a clear need.

### 6. Tessellation metadata and provenance

Investigate whether tessellation results should optionally retain information such as:

- UV coordinates of generated vertices.
- Correspondence with source surfaces and faces.
- Tessellation parameters and strategies.
- Approximation error estimates.
- Boundary and trimming information.

Determine whether this information belongs on the mesh, in a dedicated result object, or in a separate mapping structure.

Do not require additional metadata for simple conversions unless necessary.

## Geometry and Topology Requirements

The API design should explicitly address:

- Periodic surfaces and parameter-space seams.
- Surface boundaries, trims, and holes.
- Degenerate surface regions and singularities.
- Vertex indexing and face orientation.
- Nonplanar polygon triangulation.
- Watertightness and manifoldness.
- Geometric approximation tolerances.
- Preservation of existing vertices and topology where appropriate.
- Compatibility with downstream geometry-processing algorithms.

Clearly distinguish guarantees from assumptions and optional validation.

## Testing and Documentation

Testing and documentation are integral workstreams and should proceed alongside API design and implementation.

### Testing

- Establish shared behavioral contracts for supported conversions.
- Preserve and extend existing regression tests.
- Test geometric and topological edge cases.
- Verify approximation quality where applicable.
- Test serialization of strategy and result objects.
- Validate interoperability with `compas_cgal` and other relevant plugins.
- Run cross-package integration tests.

### Documentation

- Establish consistent terminology.
- Document method semantics, parameters, and return types.
- Explain available tessellation and triangulation strategies.
- Provide equivalent examples across geometry representations.
- Document limitations, guarantees, and compatibility changes.
- Include migration guidance where existing APIs are modified.

## Implementation Approach

This initiative will be coordinated through `compas_framework` using a multi-agent workflow.

### Phase 1 — Reconnaissance

Investigate existing implementations across the affected packages in parallel.

Organize investigations by architectural concern rather than assigning one agent per package.

Produce an inventory of existing APIs, algorithms, representations, dependencies, tests, and documentation.

### Phase 2 — Architectural Proposal

Develop a unified API proposal based on the inventory.

Compare alternatives, identify tradeoffs, and define the intended responsibilities of geometry objects, strategy objects, conversion functions, and plugin interfaces.

Produce a dependency-aware implementation plan.

**Do not modify package source code before the architectural proposal is reviewed and approved.**

### Phase 3 — Implementation

After approval, divide implementation into independently verifiable tasks.

Execute compatible tasks in parallel, with clear repository and file ownership.

Develop tests and documentation alongside implementation.

### Phase 4 — Integration and Review

Perform independent code review, cross-package testing, compatibility verification, and documentation validation.

Resolve integration issues before considering the initiative complete.

## Definition of Done

The initiative is complete when:

1. A consistent vocabulary and API contract have been established.
2. Supported continuous and discrete geometry representations expose the approved conversion interfaces.
3. Tessellation and triangulation strategies are implemented where appropriate.
4. Triangle mesh representations can be consumed consistently by relevant geometry-processing plugins.
5. Geometric and topological behavior is covered by documented contracts and tests.
6. Cross-package integration tests pass.
7. Documentation and examples reflect the implemented interfaces.
8. Compatibility implications and migration requirements are documented.

## Guiding Principle

**Unify the interfaces and semantics without unnecessarily unifying the underlying algorithms or representations.**

Different geometry types and computational backends may require different implementations. The goal is to provide a coherent and predictable public API while preserving the flexibility and capabilities of the COMPAS ecosystem.