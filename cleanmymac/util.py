#
# author: Cosmin Basca
#
# Copyright 2015 Cosmin Basca
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import os
import sys
import itertools


def exists(cmd, mode=os.F_OK | os.X_OK, path=None):
    """
    checks to see if a command exists. The function is an adaptation of :func:`shutil.which`
    introduced in Python 3.3. See more here:
    https://hg.python.org/cpython/file/default/Lib/shutil.py in Python 3.3

    :param str cmd: the command to check
    :param int mode: the command access mode
    :param str path: lookup the command in `path` if specified. Default None
    :return:
    """
    # function based on: which from https://hg.python.org/cpython/file/default/Lib/shutil.py
    # Check that a given file can be accessed with the correct mode.
    # Additionally check that `file` is not a directory, as on Windows
    # directories pass the os.access check.
    def _access_check(fn, mode):
        return os.path.exists(fn) and os.access(fn, mode) and not os.path.isdir(fn)

    # If we're given a path with a directory part, look it up directly rather
    # than referring to PATH directories. This includes checking relative to the
    # current directory, e.g. ./script
    if os.path.dirname(cmd):
        if _access_check(cmd, mode):
            return True
        return False

    if path is None:
        path = os.environ.get("PATH", os.defpath)
    if not path:
        return False
    path = path.split(os.pathsep)

    if sys.platform == "win32":
        # The current directory takes precedence on Windows.
        if os.curdir not in path:
            path.insert(0, os.curdir)

        # PATHEXT is necessary to check on Windows.
        pathext = os.environ.get("PATHEXT", "").split(os.pathsep)
        # See if the given file matches any of the expected path extensions.
        # This will allow us to short circuit when given "python.exe".
        # If it does match, only test that one, otherwise we have to try
        # others.
        if any(cmd.lower().endswith(ext.lower()) for ext in pathext):
            files = [cmd]
        else:
            files = [cmd + ext for ext in pathext]
    else:
        # On other platforms you don't have things like PATHEXT to tell you
        # what file suffixes are executable, so just pass on cmd as-is.
        files = [cmd]

    seen = set()
    for _dir in path:
        normdir = os.path.normcase(_dir)
        if normdir not in seen:
            seen.add(normdir)
            for thefile in files:
                name = os.path.join(_dir, thefile)
                if _access_check(name, mode):
                    return True
    return False


def yaml_files(path):
    """
    generator of **YAML** files in the give path.

    :param path: the path to scan for *YAML* files
    :return: a generator
    :raise: :class:`ValueError` if path is not a valid directory
    """
    if not os.path.isdir(path):
        raise ValueError('{0} not a directory'.format(path))
    for _file in os.listdir(path):
        if _file.endswith(".yaml"):
            yield os.path.splitext(_file)[0], os.path.join(path, _file)


def flatten(lst):
    """
    simple flatten operation for a list of lists

    :param lst: the list of lists
    :type lst: list
    :return: the flattened list
    :rtype: list
    """
    assert isinstance(lst, list)
    return list(itertools.chain(*lst))