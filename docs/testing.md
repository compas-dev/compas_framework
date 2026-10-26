# Testing Strategy

Framework tests are organized by the contract they exercise:

- plugin discovery and dispatch through public COMPAS APIs;
- data roundtrips across serialization formats and package boundaries;
- end-to-end workflows combining geometry, algorithms, models, and viewing;
- performance baselines for representative cross-package operations; and
- packaging checks for the supported Python and operating-system matrix.

Use the `integration`, `roundtrip`, `performance`, `gui`, and `native_backend`
markers to select tests by capability. Tests needing a display or native
backend should skip with a precise reason when that capability is unavailable.
