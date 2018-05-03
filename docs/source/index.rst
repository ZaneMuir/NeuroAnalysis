.. neuroanalysis documentation master file, created by
   sphinx-quickstart on Tue May  1 18:41:53 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to neuroanalysis's documentation!
=========================================
Basic analysis methods for spike trains sorted from electrodes and fluorescence recorded from
two-photon imaging.

Quick Start
-----------
for python3 module:

.. code-block:: bash

    $ git clone git@github.com:ZaneMuir/NeuroAnalysis.git
    $ cd NeuroAnalysis
    $ python3 setup.py install
    $ pip3 install -r requirements.txt

for julia module (in julia REPL):

.. code-block:: julia

    >>> Pkg.clone("https://github.com/ZaneMuir/NeuralModel.jl.git")

Contents
--------

.. toctree::
    :maxdepth: 2
    :glob:

    install
    workflow_mea
    workflow_tpi
    module/module




Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
