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
from abc import ABCMeta, abstractmethod, abstractproperty

from shutil import rmtree

from cleanmymac.log import info, debug, error, warn
from cleanmymac.util import flatten
from sarge import run, shell_format, Capture
from natsort import natsorted
from pprint import pformat
import os
import re


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

    @abstractmethod
    def update(self, **kwargs):
        """
        the update operation

        :param kwargs: additional arguments
        """
        pass

    @abstractmethod
    def clean(self, **kwargs):
        """
        the cleanup operation

        :param kwargs: additional arguments
        """
        pass

    @abstractmethod
    def describe(self):
        """
        the description of the combined update and clean operations

        :return: a string describing the steps to be undertaken
        """
        return ''

    def __call__(self, **kwargs):
        """
        initiate the cleanup (and update if enabled) operations

        :param kwargs: additional arguments
        """
        if self._update:
            self.update(**kwargs)
        self.clean(**kwargs)


# ----------------------------------------------------------------------------------------
#
# the base Shell Target class
#
# ----------------------------------------------------------------------------------------
class ShellCommandTarget(Target):
    """
    the main cleanup Shell Command Target. This is an abstract class.
    This class encapsulates the basic logic to execute cleanup operations based on
    predefined shell commands.

    :param config: a configuration dictionary
    :param update: perform the update before cleanup if True
    :param verbose: verbose output if True
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

    @abstractproperty
    def update_commands(self):
        return []

    @abstractproperty
    def clean_commands(self):
        return []

    def _run(self, commands):
        for cmd in commands:
            try:
                if self._verbose:
                    with Capture() as err:
                        with Capture() as out:
                            info('running: {0}'.format(cmd))
                            run(cmd, stdout=out, stderr=err, env=self._env)
                            info(out.text)
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
            commands_to_run += self._describe(self.update_commands)
        commands_to_run += self._describe(self.clean_commands)
        return '\n'.join(commands_to_run)


# ----------------------------------------------------------------------------------------
#
# a Shell Target class that can read it's description from a yaml file
#
# ----------------------------------------------------------------------------------------
class YamlShellCommandTarget(ShellCommandTarget):
    def __init__(self, config, update=False, verbose=False):
        self._args = config['args']
        super(YamlShellCommandTarget, self).__init__(config, update=update, verbose=verbose)

    @property
    def update_commands(self):
        return self._args['update_commands']

    @property
    def clean_commands(self):
        return self._args['clean_commands']


# ----------------------------------------------------------------------------------------
#
# a Directory based Target class
#
# ----------------------------------------------------------------------------------------
class DirTarget(Target):
    __metaclass__ = ABCMeta

    def __init__(self, config, update=False, verbose=False):
        super(DirTarget, self).__init__(config, update=update, verbose=verbose)

    def update(self, **kwargs):
        info('update not supported for "dir" targets')

    def _to_remove(self):
        for entry in self.entries:
            _dir = entry['dir']
            _pattern = entry['pattern']
            dirs = [os.path.join(_dir, d) for d in os.listdir(_dir)
                    if os.path.isdir(os.path.join(_dir, d)) and re.match(_pattern, d)]
            dirs = natsorted(dirs, reverse=True)
            yield dirs[1:]

    def clean(self, **kwargs):
        to_remove = flatten(list(self._to_remove()))
        for _dir in to_remove:
            rmtree(_dir)

    def describe(self):
        msgs = []
        if self._update:
            msgs.append('update not supported for "dir" targets')
        to_remove = flatten(list(self._to_remove()))
        if to_remove:
            msgs.append('will remove the following folders: {0}'.format(pformat(to_remove)))
        else:
            msgs.append('no cleanup action necessary at this point')
        return '\n'.join(msgs)

    @abstractproperty
    def entries(self):
        return []


# ----------------------------------------------------------------------------------------
#
# a Dir Target class that can read it's description from a yaml file
#
# ----------------------------------------------------------------------------------------
class YamlDirTarget(DirTarget):
    def __init__(self, config, update=False, verbose=False):
        self._args = config['args']
        super(YamlDirTarget, self).__init__(config, update=update, verbose=verbose)

    @property
    def entries(self):
        return self._args
