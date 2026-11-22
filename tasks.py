import sys
import tempfile
from pathlib import Path

from invoke.context import Context
from invoke.tasks import task


def _build_command(source: Path, output: Path) -> str:
    return f'uv build "{source}" --out-dir "{output}"'


@task
def check(ctx: Context) -> None:
    """Run linting and formatting checks."""
    ctx.run("ruff check .")
    ctx.run("ruff format --check .")


@task
def lint(ctx: Context) -> None:
    """Run Ruff linting."""
    ctx.run("ruff check .")


@task(name="format")
def format_code(ctx: Context) -> None:
    """Apply Ruff fixes and formatting."""
    ctx.run("ruff check --fix .")
    ctx.run("ruff format .")


@task
def typecheck(ctx: Context) -> None:
    """Run Pyright with the active Python interpreter."""
    ctx.run(f'pyright --pythonpath "{sys.executable}"')


@task
def test(ctx: Context) -> None:
    """Run the pure framework package tests."""
    with tempfile.TemporaryDirectory(prefix="compas-framework-tests-") as temporary:
        directory = Path(temporary)
        ctx.run(
            f'pytest --basetemp "{directory / "pytest"}" -o cache_dir="{directory / "pytest-cache"}" tests/test_package.py',
            env={"PYTHONDONTWRITEBYTECODE": "1"},
        )


@task
def docs(ctx: Context) -> None:
    """Build the documentation strictly into a temporary directory."""
    with tempfile.TemporaryDirectory(prefix="compas-framework-docs-") as temporary:
        site_dir = Path(temporary) / "site"
        ctx.run(f'mkdocs build --strict --site-dir "{site_dir}"', env={"PYTHONDONTWRITEBYTECODE": "1"})


@task
def build(ctx: Context, output_directory: str | None = None) -> None:
    """Build the current working tree into an explicit or temporary directory."""
    output = Path(output_directory) if output_directory else Path(tempfile.mkdtemp(prefix="compas-framework-dist-"))
    source = Path(__file__).resolve().parent
    ctx.run(_build_command(source, output))
    print(output)
