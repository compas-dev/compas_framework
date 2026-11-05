# Title: When should public APIs return Python, COMPAS, or NumPy values?

## Status

Accepted

## Context

Ordinary APIs, numerical modules, Tessellation, and plugins currently expose a
mixture of Python containers, core objects, arrays, and NumPy scalar results.
Some backend results disagree with the core declaration.

## Options

1. Standardize every return on NumPy.
2. Standardize every return on Python lists and built-in scalars.
3. Use Python/core values by default, NumPy for explicitly numerical APIs, and
   retained buffers only for explicitly buffer-backed representations.

## Recommendation

Choose option 3. Ordinary geometry/datastructure APIs return core objects,
Python containers, and Python `int`/`float`. Explicit NumPy-oriented operations
return typed arrays. `Tessellation` retains buffers by design. Plugins conform
to the core return representation. Serialization normalizes arrays/scalars to
lists and built-ins.

Declare Python built-in scalar representations for logical counts and ranks
unless the API is explicitly NumPy-oriented. Ordinary Python producers should
naturally return those representations; normalize a backend-specific scalar
once at the public or plugin boundary only when needed to satisfy the declared
contract. Do not introduce broad serialization `TypedDict` hierarchies; type
only stable versioned records.

Built-in scalar or container normalization happens once at a declared public,
plugin, or serialization return boundary only when representation is part of
the contract. Do not scatter `float()`, `int()`, or `list()` calls through
internal Python code or convert compatible values solely for checker
satisfaction.

## Consequences

- Return behavior becomes predictable across backends.
- Some scalar normalization is a runtime change and needs focused approval,
  tests, and documentation.
- Backend arrays may need wrapping or conversion at the plugin boundary.
- Zero-copy behavior remains limited to APIs that state it explicitly.

## Affected packages

`compas`, `compas_occ`, `compas_cgal`.

## Dependencies

- [002 — Numeric and array inputs](002-numeric-array-inputs.md)
- [004 — Tessellation buffers](004-tessellation-buffers.md)
- [005 — Native normalization](005-native-normalization.md)
- [006 — Plugin conformance](006-plugin-conformance.md)
- [007 — Backend substitutability](007-backend-substitutability.md)
