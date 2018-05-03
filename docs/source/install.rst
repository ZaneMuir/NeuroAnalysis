.. Installation guide

Installation
************

Python3 version
===============

Preparation
-----------

install Python3
^^^^^^^^^^^^^^^
* MacOS user: 
    * Homebrew: ``$ brew install python3``
    * download binary package from `python.org`_

* Windows users:
    * download binary package from `python.org`_

get Pip
^^^^^^^
* MacOS users:
    .. code-block:: bash

        $ curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
        $ python get-pip.py

* Windows users:
    * download the linked file from `this link <https://bootstrap.pypa.io/get-pip.py>`_
    * run the ``get-pip.py`` with ``python.exe``

From Github
-----------

.. code-block:: bash

    $ git clone git@github.com:ZaneMuir/NeuroAnalysis.git
    $ cd NeuroAnalysis
    $ python setup.py install
    $ pip install -r requirements.txt


.. _python.org: https://www.python.org/downloads/

Julia version
=============

Preparation
-----------

install Julia
^^^^^^^^^^^^^^^

* MacOS users:
    * download binary package from `Julia downlaod page`_
    * Homebrew: ``brew cask install julia``

* Windows users:
    * download binary package from `Julia downlaod page`_



.. _Julia downlaod page: https://julialang.org/downloads/