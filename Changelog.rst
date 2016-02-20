Changelog
=========

All major changes between **cleanmymac** releases

Version 0.1.15
--------------

- compatibility with python 2.6 / 2.7 / 3.5 and pypy
- tox support for py26, py27, py35 and pypy
- early test module (only the schema is tested so far), more tests to come
- new pytest and six dependencies are in
- nicer message formatting in dry-run mode

Version 0.1.14
--------------

- fixed issue with registering global config as a target when config file is in *extra_targets* path
- update *requirements.txt* in docs, to depend on cleanmymac (needed by readthedocs in order to get the CLI help)
- adding early testing skeleton (no tests yet)
- defined *tox.ini* for cross python testing
- Changelog is in

Version 0.1.13
--------------

- logging adapted to click-log, improved logging
- dropped tqdm in favour of click.progressbar
- updated docs to include the CLI output with the new click command
- new **--strict/--no-strict** argument (avoid validation checks)
- parse / validation errors are caught with target cleanups

Version 0.1.12
--------------

- moving from argparse to click, nicer CLI definition & handling

Version 0.1.11
--------------

- fixed anaconda update bug in description (no more waiting for yes on update)

Version 0.1.10
--------------

- version reporting in CLI now
- updated setup.py *license* and *platforms*

Version 0.1.9
-------------

- fixed potential delete error
- improved messages on folder deletions
- more documentation

Version 0.1.8
-------------

- modified yaml schema for yaml based targets
- introduced update message for dir based targets
- switched to restructured text for Readme, instead of Markdown
- topic update in setup.py, *beta* classifier, and url update

Version 0.1.7
-------------

- optimised imports
- superfluous debug statement removed

Version 0.1.6 - 0.1.2
---------------------

- entry-point based target loading
- early documentation skeleton

Version 0.1.1
-------------

- new targets: jdk and mactex

Version 0.1.0
-------------

- refactored to support directory based targets
- -q / --quiet mode, displays a progressbar instead of verbose info messages
