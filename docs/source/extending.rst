Extending **cleanmymac**
========================

**cleanmymac** can easily be extended with additional cleanup targets. Form complex cases where cleanup is not
provided by an external program one can extend the base :class:`cleanmymac.target.Target` class and register it
with the global :attr:`cleanmymac.constants.TARGET_ENTRY_POINT` entry-point.
Consider for example (in setup.py) the following case:

.. code-block:: python

    entry_points={
        # ....
        'cleanmymac.target': [
            'my_target_name = my.python.package.MyTargetClass'
        ]
        # ...
    }


In addition, for directory and shell command based targets simply create the associated **YAML** files and
point **cleanmymac** to the folder where the files reside with the *-t* command line option.
See more at: :ref:`cli`.

For examples of **YAML** defined cleanup targets have a look at the :mod:`cleanmymac.builtins` module.
