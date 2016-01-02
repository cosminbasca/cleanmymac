.. _config:

Configuration
=============

The **cleanmymac** utility accepts a configuration file by specifying the *-c* option. If not specified the
file is assumed to be at the following location **~/.cleanmymac.yaml**

the global configuration can be used (for now) to pass specific env vars to shell commands, for example
assume that the *anaconda* :class:`cleanmymac.target.Target` is not in the main path:

.. code-block:: yaml

    anaconda: {
      env: {
        PATH: '~/anaconda/bin',
      },
    }

