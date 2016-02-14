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

from voluptuous import Schema, Required, All, Optional, ALLOW_EXTRA, Any, IsDir, In, Or, message, DirInvalid, truth

from cleanmymac.log import error
from cleanmymac.constants import VALID_TARGET_TYPES


@message('not a directory', cls=DirInvalid)
@truth
def IsDirUserExpand(v):
    """Verify the directory exists.

    >>> IsDirUserExpand()('/')
    '/'
    """
    return os.path.isdir(os.path.expanduser(v))


def _cmd_spec_schema(strict=True):
    return Schema({
        Required('update_commands', default=[]): All(list),
        Required('clean_commands'): All(list),
    })


def _dir_spec_schema(strict=True):
    return Schema({
        Optional('update_message'): str,
        Required('entries'): [
            {
                Required('dir'): IsDirUserExpand() if strict else str,
                Optional('pattern'): str
            }
        ]
    })


__TYPE_SCHEMA__ = {
    'cmd': _cmd_spec_schema,
    'dir': _dir_spec_schema
}


def _target_schema():
    return Schema({
        Required('type'): All(str, In(VALID_TARGET_TYPES)),
        Required('spec'): dict
    })


def validate_yaml_target(description, strict=True):
    """
    performs the validation of the **YAML** definition of a :class:`cleanmymac.target.Target`.
    Currently two kinds of schemas are supported.

    * Shell command based Targets

    .. code-block:: yaml

        type: 'cmd'
        spec: {
          update_commands: [
            'conda update conda',
            'conda update anaconda'
          ],
          clean_commands: [
            'conda clean -p -s -t -y'
          ]
        }


    * Directory based Targets

    .. code-block:: yaml

        type: 'dir'
        spec: {
            update_message: 'Get the latest Java version from http://www.oracle.com/technetwork/java/javase/downloads/index.html',
            entries: [
                {
                    dir: '/Library/Java/JavaVirtualMachines',
                    pattern: 'jdk1\.6\.\d_\d+\.jdk'
                },
                {
                    dir: '/Library/Java/JavaVirtualMachines',
                    pattern: 'jdk1\.7\.\d_\d+\.jdk'
                },
                {
                    dir: '/Library/Java/JavaVirtualMachines',
                    pattern: 'jdk1\.8\.\d_\d+\.jdk'
                },
            ]
        }

    :param dict description: the loaded description
    :param bool strict: perform strict validation (fail on invalid specification if True)
    :return: the validate description
    :rtype: dict
    """
    global __TYPE_SCHEMA__
    schema = _target_schema()
    description = schema(description)
    _type = description['type']
    _spec = description['spec']
    try:
        schema = __TYPE_SCHEMA__[_type](strict=strict)
        description['spec'] = schema(_spec)
    except Exception as e:
        error(e)
        if strict:
            raise e
    return description


def _config_schema():
    return Schema({
        Optional('cleanmymac'): Schema({
            Optional('targets_path'): list
        }, extra=ALLOW_EXTRA),
    }, extra=ALLOW_EXTRA)


def validate_yaml_config(config):
    """
    performs the validation of the **YAML** definition of the global **cleanmymac** configuration.
    The current supported syntax allows for the specification of extra environment variables on a
    per target basis. See for example the case when the *anaconda* target is not in **PATH**:

    .. code-block:: yaml

        cleanmymac: {
          targets_path: ['.']
        }
        anaconda: {
          env: {
            PATH: '~/anaconda/bin',
          },
        }

    :param dict config: the loaded configuration
    :return: the validate configuration
    :rtype: dict
    """
    schema = _config_schema()
    return schema(config)
