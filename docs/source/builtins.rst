Builtin cleanup Targets
=======================

**cleanmymac** comes with a few builtin cleanup targets defined as **YAML**
files in the :mod:`cleanmymac.builtins` module.

Homebrew
--------

.. code-block:: bash

    $ # update
    $ brew update
    $ brew outdated | brew upgrade
    $ # cleanup
    $ brew cleanup


Anaconda
--------

.. code-block:: bash

    $ # update
    $ conda update conda
    $ conda update anaconda
    $ # cleanup
    $ conda clean -p -s -t -y


Java JDK's
----------

keep the latest 1.7 and 1.8 JDK's under */Library/Java/JavaVirtualMachines*

.. note::

    may require sudo privileges


MacTex
-------

keep the latest texlive distribution under */usr/local/texlive/*

.. note::

    may require sudo privileges

