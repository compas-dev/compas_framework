# ADR 022: ShapeOp Similarity Correspondence Flags

**Status:** Proposed

## Context

`Solver.add_similarity_constraint(...)` and
`Solver.add_shape_constraint(...)` expose a Boolean named
`allow_translation`. Both wrappers pass it unchanged as the final Boolean to
ShapeOp's `SimilarityConstraint(indices, weight, positions, scaling, rotate,
flip)` constructor.

The backend does not use this value to control translation. During projection,
ShapeOp always centers the input and target configurations before fitting them.
The final Boolean controls whether reversed vertex order is included among the
candidate correspondences. The backend implements this with its `flipMatrix_`
permutation.

The neighboring `allow_rotation` Boolean also concerns correspondence rather
than a spatial transform: it enables cyclic permutations of the ordered
vertices. The existing Python documentation describing configurable
translation and spatial rotation is therefore false.

ADR 019 requires ShapeOp modernization to preserve solver behavior unless a
separate public API decision is approved. Correcting these public names and
descriptions requires that decision.

## Options

1. **Preserve both existing names.** Correct their documentation so that
   `allow_rotation` means cyclic rotation of correspondence order and
   `allow_translation` means reversed order. This avoids keyword compatibility
   breaks but leaves two names that appear to control spatial transformations.
2. **Rename both correspondence flags without aliases.** Replace
   `allow_rotation` with `allow_cyclic_permutations` and
   `allow_translation` with `allow_flip` consistently in both public methods,
   the private native wrapper, and its stub. Preserve their positions, default
   values, and native behavior. This introduces explicit keyword compatibility
   breaks while giving each operation one accurate public name.
3. **Add the accurate names while retaining the old names as deprecated
   aliases.** Define precedence or reject calls supplying both forms. This
   temporarily preserves keyword calls but introduces overlapping names,
   conflict handling, warnings, and compatibility paths without an approved
   need.
4. **Rename only `allow_translation`.** This corrects the least defensible
   name but knowingly retains `allow_rotation`, whose spatial interpretation
   is also false.
5. **Implement actual spatial translation and rotation controls.** ShapeOp
   currently removes translation unconditionally. This would change the
   numerical algorithm rather than correct the wrapper contract and is outside
   repository modernization.

## Recommendation

Choose option 2.

Use this public correspondence contract on both
`add_similarity_constraint(...)` and `add_shape_constraint(...)`:

- `allow_scaling` controls whether the fitted similarity may include scale;
- `allow_cyclic_permutations` controls whether cyclic shifts of ordered vertex
  correspondence are considered; and
- `allow_flip` controls whether reversed vertex order, and its cyclic shifts
  when `allow_cyclic_permutations=True`, are considered.

Keep both correspondence defaults `True`, preserving the current positional
runtime behavior. Do not retain `allow_rotation` or `allow_translation` as
aliases. Spatial translation remains removed unconditionally and spatial
rotation remains part of the ordinary Umeyama fit; neither is presented as a
separately configurable operation.

For `add_shape_constraint(...)`, these correspondence options apply only to
the `"similarity"` and `"custom"` paths. The `"regular_polygon"` path
continues to use its dedicated constraint and ignores them; this must be
documented rather than represented as configurable behavior.

## Consequences

Calls using the old keywords `allow_rotation=` or `allow_translation=` fail
and must migrate to `allow_cyclic_permutations=` or `allow_flip=`
respectively. Positional calls retain the same value ordering and numerical
behavior. Both defaults remain unchanged.

The Python signatures, NumPy-style docstrings, C++ wrapper names and comments,
private `_shapeop.pyi`, typing fixtures, examples, and changelog all use the
same terminology. No compatibility alias or new numerical feature is added.

## Verification

- Inspect both public signatures and the packaged private stub to prove
  `allow_cyclic_permutations` and `allow_flip` are present and the two old
  names are absent.
- Add a strict Pyright fixture using both accurate keywords on both methods.
- Use an asymmetric custom target with cyclic correspondence disabled to prove
  that `allow_flip=False` excludes reversed order and `allow_flip=True`
  considers it.
- Verify cyclic permutations are excluded or considered according to
  `allow_cyclic_permutations` using an asymmetric ordered target.
- Verify both defaults remain `True` and positional calls preserve existing
  behavior.
- Verify translated copies remain translation-invariant independently of the
  correspondence flags.
- Verify and document that the regular-polygon path does not consume the
  correspondence flags.
- Run focused solver tests, Ruff, Pyright, strict MkDocs, installed-wheel
  typing consumer, and wheel/sdist checks.

## Dependencies

ADR 019.
