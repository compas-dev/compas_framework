********************************************************************************
Installation
********************************************************************************

Stable
======

For installation WITHOUT `compas_occ`

.. code-block:: bash

    pip install compas_framework

For installation WITH `compas_occ`

.. code-block:: bash

    conda create -n compas-dev -c conda-forge compas_occ
    conda activate compas-dev
    pip install compas_framework

In both cases, for installation with support for Jupyter notebooks

.. code-block:: bash

    pip install "compas_framework[notebook]"


Development
===========

To install `compas_framework` for development, install from local source.

.. code-block:: bash

    git clone https://github.com/compas-dev/compas_framework.git
    cd compas_framework
    conda env create -f environment.yml
