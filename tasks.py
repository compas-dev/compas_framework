import sys
from pathlib import Path

from compas_invocations2 import build
from compas_invocations2 import docs
from compas_invocations2 import mkdocs
from compas_invocations2 import style
from compas_invocations2 import tests
from invoke.collection import Collection
from invoke.tasks import task


@task
def typecheck(ctx):
    """Run static type checking."""
    ctx.run(f'pyright --pythonpath "{sys.executable}" src/compas_framework tests')


ns = Collection(
    docs.help,
    style.check,
    style.lint,
    style.format,
    typecheck,
    mkdocs.docs,
    tests.test,
    tests.testdocs,
    tests.testcodeblocks,
    build.clean,
)
ns.configure(
    {
        "base_folder": str(Path(__file__).resolve().parent),
    }
)
