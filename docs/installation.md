# Installation

The framework supports Python 3.12, 3.13, and 3.14.

```bash
python -m pip install compas_framework
```

The COMPAS 3 metapackage does not currently provide Rhino, Grasshopper, or
Blender extras. Those bundles will return after their owning packages declare
compatible COMPAS 3 dependencies and pass their host-runtime verification.
Existing COMPAS 2 host integrations remain available through the installation
instructions of their owning packages. Mixing them with this COMPAS 3
metapackage is unsupported.

Some geometry backends rely on native libraries and may be easier to install
from conda-forge.

## Development checkout

Clone the repository and create the locked, tooling-only development
environment:

```bash
git clone https://github.com/compas-dev/compas_framework.git
cd compas_framework
uv sync --frozen --only-group dev --no-install-project
```

Alternatively, `environment.yml` bootstraps Python and uv with Conda. Run the
same `uv sync` command after activating that environment. Installing the
project itself intentionally installs the complete framework dependency set;
use package-specific environments when developing native backends.
