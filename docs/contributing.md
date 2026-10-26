# Contributing

Install the project with development and documentation dependencies:

```bash
python -m pip install -e ".[dev,docs]"
```

Run focused tests while developing, then run the repository checks:

```bash
invoke test
invoke check
invoke typecheck
invoke docs
```

Integration tests and examples should use public APIs and span package
boundaries. Package-local fixes belong in the owning package repository.
