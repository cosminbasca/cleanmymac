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

from voluptuous import Schema, Required, All, Optional, ALLOW_EXTRA, Any, IsDir, In, Or

from cleanmymac.constants import VALID_TARGET_TYPES


def _args_cmd_schema():
    return Schema({
        Required('update_commands', default=[]): All(list),
        Required('clean_commands'): All(list),
    })


def _args_dir_schema():
    return Schema([
        {
            Required('dir'): IsDir(),
            Required('pattern'): str
        }
    ])

__TYPE_SCHEMA__ = {
    'cmd': _args_cmd_schema(),
    'dir': _args_dir_schema()
}


def _target_schema():
    return Schema({
        Required('type'): All(str, In(VALID_TARGET_TYPES)),
        Required('args'): Or(list, dict)
    })


def validate_yaml_target(description):
    global __TYPE_SCHEMA__
    schema = _target_schema()
    description = schema(description)
    _type = description['type']
    _args = description['args']
    description['args'] = __TYPE_SCHEMA__[_type](_args)
    return description


def _config_schema():
    return Schema({
        Optional('env'): dict,
    }, extra=ALLOW_EXTRA)


def validate_yaml_config(config):
    schema = _config_schema()
    return schema(config)
