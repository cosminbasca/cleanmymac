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
import click
import os
import re
from pprint import pformat
from natsort import natsorted
from sarge import run, shell_format, Capture
from abc import ABCMeta, abstractmethod, abstractproperty
from cleanmymac.log import info, debug, error, warn, echo_info, echo_warn, echo_success
from cleanmymac.util import delete_dir_content, DirList, Dir, delete_dirs
from cleanmymac.constants import DESCRIBE_UPDATE, DESCRIBE_CLEAN, VALID_DESCRIBE_MESSAGES


# ----------------------------------------------------------------------------------------
#
# the base Target class
#
# ----------------------------------------------------------------------------------------
class Target(object):
    """
    the main cleanup Target. This is an abstract class.

    :param config: a configuration dictionary
    :type config: dict
    :param update: perform the update before cleanup if True
    :type update: bool
    :param verbose: verbose output if True
    :type verbose: bool
    """
    __metaclass__ = ABCMeta

    def __init__(self, config, update=False, verbose=False):
        self._config = config if isinstance(config, dict) else {}
        self._update = update
        self._verbose = verbose

    def _debug(self, msg, *arg):
        debug('[{0}] {1}'.format(click.style(str(self.__class__.__name__), fg='yellow'), msg))

    @property
    def config(self):
        return self._config

    @abstractmethod
    def update(self, **kwargs):
        """
        the update operation

        :param kwargs: additional arguments
        :type kwargs: dict
        """
        pass

    @abstractmethod
    def clean(self, **kwargs):
        """
        the cleanup operation

        :param kwargs: additional arguments
        :type kwargs: dict
        """
        pass

    @abstractmethod
    def describe(self):
        """
        the description of the combined update and clean operations

        :return: a string describing the steps to be undertaken
        :rtype: str
        """
        return ''

    @staticmethod
    def __describe__(kind, message, fg=None):
        assert kind.lower() in VALID_DESCRIBE_MESSAGES
        max_len = max(map(len, VALID_DESCRIBE_MESSAGES))
        fmt_string = '[ {0: <' + str(max_len+1) + '}]  {1}'
        return click.style(fmt_string.format(kind.lower(), message), fg=fg)

    def _describe_update(self, message, fg='yellow'):
        return self.__describe__(DESCRIBE_UPDATE, message, fg=fg)

    def _describe_clean(self, message, fg='white'):
        return self.__describe__(DESCRIBE_CLEAN, message, fg=fg)

    def __call__(self, **kwargs):
        """
        initiate the cleanup (and update if enabled) operations

        :param kwargs: additional arguments
        :type kwargs: dict
        """
        if self._update:
            self._debug('update target')
            self.update(**kwargs)
        self._debug('clean target')
        self.clean(**kwargs)


# ----------------------------------------------------------------------------------------
#
# the base Shell Target class
#
# ----------------------------------------------------------------------------------------
class ShellCommandTarget(Target):
    """
    Class encapsulating general logic to execute cleanup operations based on predefined
    shell commands. This is an abstract class.

    :param config: a configuration dictionary
    :type config: dict
    :param update: perform the update before cleanup if True
    :type update: bool
    :param verbose: verbose output if True
    :type verbose: bool
    """
    __metaclass__ = ABCMeta

    def __init__(self, config, update=False, verbose=False):
        super(ShellCommandTarget, self).__init__(config, update=update, verbose=verbose)
        self._env = self._config['env'] if 'env' in self._config else {}
        # prepare path if specified
        path = os.environ['PATH']
        if 'PATH' in self._env:
            path = '{0}:{1}'.format(os.environ['PATH'],
                                    os.path.expanduser(self._env['PATH']))
        self._env['PATH'] = path
        self._debug('target local env: {0}'.format(pformat(self._env)))

    @abstractproperty
    def update_commands(self):
        """
        the shell commands executed on **update**. Each command is a string as expected by :func:`sarge.run`

        :return: a list of shell commands
        :rtype: list
        """
        return []

    @abstractproperty
    def clean_commands(self):
        """
        the shell commands executed on **clean**. Each command is a string as expected by :func:`sarge.run`

        :return: a list of shell commands
        :rtype: list
        """
        return []

    def _run(self, commands):
        for cmd in commands:
            self._debug('run command "{0}"'.format(cmd))
            try:
                if self._verbose:
                    with Capture() as err:
                        with Capture() as out:
                            echo_success('running: {0}'.format(cmd))
                            run(cmd, stdout=out, stderr=err, env=self._env)
                            echo_info(out.text)
                            warn(err.text)
                else:
                    with Capture() as err:
                        with Capture() as out:
                            run(cmd, stderr=err, stdout=out, env=self._env)
            except OSError:
                error('command: "{0}" could not be executed (not found?)'.format(cmd))

    @staticmethod
    def _describe(commands):
        return map(shell_format, commands)

    def update(self, **kwargs):
        self._run(self.update_commands)

    def clean(self, **kwargs):
        self._run(self.clean_commands)

    def describe(self):
        commands_to_run = []
        if self._update:
            commands_to_run += map(self._describe_update, self._describe(self.update_commands))
        commands_to_run += map(self._describe_clean, self._describe(self.clean_commands))
        return '\n'.join(commands_to_run)


# ----------------------------------------------------------------------------------------
#
# a Shell Target class that can read it's description from a yaml file
#
# ----------------------------------------------------------------------------------------
class YamlShellCommandTarget(ShellCommandTarget):
    """
    Class encapsulating logic to initialize and execute cleanup targets defined in **YAML** files.
    See predefined builtins in :mod:`cleanmymac.builtins`.

    :param config: a configuration dictionary
    :type config: dict
    :param update: perform the update before cleanup if True
    :type update: bool
    :param verbose: verbose output if True
    :type verbose: bool
    """
    def __init__(self, config, update=False, verbose=False):
        self._spec = config['spec']
        self._debug('spec: {0}'.format(pformat(self._spec)))
        super(YamlShellCommandTarget, self).__init__(config, update=update, verbose=verbose)

    @property
    def update_commands(self):
        return self._spec['update_commands']

    @property
    def clean_commands(self):
        return self._spec['clean_commands']


# ----------------------------------------------------------------------------------------
#
# a Directory based Target class
#
# ----------------------------------------------------------------------------------------
class DirTarget(Target):
    """
    Class encapsulating the logic to execute directory based cleanup operations. The main operation
    consists of identifying and removing all matching directories in a given path with the exception
    of the most recent version.
    This is an abstract class.

    .. warning::

        if `pattern` is not specified: all files and folders in `dir` will be removed

    :param config: a configuration dictionary
    :type config: dict
    :param update: perform the update before cleanup if True
    :type update: bool
    :param verbose: verbose output if True
    :type verbose: bool
    """
    __metaclass__ = ABCMeta

    def __init__(self, config, update=False, verbose=False):
        super(DirTarget, self).__init__(config, update=update, verbose=verbose)

    @property
    def update_message(self):
        """
        message to be displayed during the update operation

        :return: the message
        :rtype: str
        """
        return 'update not supported for "dir" targets'

    def update(self, **kwargs):
        if self._verbose and self.update_message:
            echo_info(self.update_message)

    def _to_remove(self):
        for entry in self.entries:
            self._debug('check entry "{0}" to clean'.format(entry['dir']))
            _dir = os.path.expanduser(entry['dir'])
            if 'pattern' in entry:
                _pattern = entry['pattern']
                dirs = [os.path.join(_dir, d) for d in os.listdir(_dir)
                        if os.path.isdir(os.path.join(_dir, d)) and re.match(_pattern, d)]
                dirs = natsorted(dirs, reverse=True)
                dir_list = DirList(dirs[1:])
                self._debug('\tremove multiple directories: {0}'.format(dir_list.dirs))
                yield dir_list
            else:
                self._debug('\tremove single directory: {0}'.format(_dir))
                yield Dir(_dir)

    def clean(self, **kwargs):
        for entry in self._to_remove():
            if isinstance(entry, DirList):
                if self._verbose:
                    echo_warn('delete folders: {0}'.format(pformat(entry.dirs)))
                delete_dirs(entry)
            elif isinstance(entry, Dir):
                if self._verbose:
                    echo_warn('delete folder contents: {0}'.format(entry.path))
                delete_dir_content(entry)

    def describe(self):
        msgs = []
        if self._update and self.update_message:
            msgs.append(self._describe_update(self.update_message))

        nothing_to_remove = True
        for entry in self._to_remove():
            if isinstance(entry, DirList) and entry.dirs:
                msgs.append(self._describe_clean('delete folders: {0}'.format(pformat(entry.dirs))))
                nothing_to_remove = False
            elif isinstance(entry, Dir):
                msgs.append(self._describe_clean('delete folder contents: {0}'.format(entry.path)))
                nothing_to_remove = False

        if nothing_to_remove:
            msgs.append(self._describe_clean('There are no folders to delete/clean'))
        return '\n'.join(msgs)

    @abstractproperty
    def entries(self):
        """
        the list of entries (pairs of path: regex pattern) to scan for cleanup. Keeps latest versions only.

        :return: a list of entries path:pattern pairs
        :rtype: list
        """
        return []


# ----------------------------------------------------------------------------------------
#
# a Dir Target class that can read it's description from a yaml file
#
# ----------------------------------------------------------------------------------------
class YamlDirTarget(DirTarget):
    """
    Class encapsulating the logic to execute directory based cleanup operations. The main operation
    consists of identifying and removing all matching directories in a given path with the exception
    of the most recent version. This concrete implementation allows for the specification of entries
    in a **YAML** configuration file. See predefined builtins in :mod:`cleanmymac.builtins`.

    :param config: a configuration dictionary
    :type config: dict
    :param update: perform the update before cleanup if True
    :type update: bool
    :param verbose: verbose output if True
    :type verbose: bool
    """
    def __init__(self, config, update=False, verbose=False):
        self._spec = config['spec']
        self._debug('spec: {0}'.format(pformat(self._spec)))
        super(YamlDirTarget, self).__init__(config, update=update, verbose=verbose)

    @property
    def entries(self):
        return self._spec['entries']

    @property
    def update_message(self):
        return self._spec['update_message'] if 'update_message' in self._spec else ''
