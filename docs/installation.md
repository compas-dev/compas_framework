# Installation

The framework requires Python 3.12 or newer.

```bash
python -m pip install compas_framework
```

Install host integrations only where they are needed:

```bash
python -m pip install "compas_framework[rhino]"
python -m pip install "compas_framework[blender]"
```

The `hosts` extra installs the Rhino, Grasshopper, and Blender integrations
together:

```bash
python -m pip install "compas_framework[hosts]"
```

Some geometry backends rely on native libraries and may be easier to install
from conda-forge. For development, create the Conda environment and install the
repository in editable mode:

```bash
conda env create -f environment.yml
conda activate compas-framework
python -m pip install -e ".[dev,docs]"
```
