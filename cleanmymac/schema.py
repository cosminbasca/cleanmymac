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
from voluptuous import Schema, Required, All, Optional, ALLOW_EXTRA


def get_yaml_shell_command_schema():
    return Schema({
        Required('update_commands', default=[]): All(list),
        Required('clean_commands'): All(list),
    })


def validate_yaml_shell_command(description):
    assert isinstance(description, dict)
    schema = get_yaml_shell_command_schema()
    return schema(description)


def get_yaml_config_schema():
    return Schema({
        Optional('env'): dict,
    }, extra=ALLOW_EXTRA)


def validate_yaml_config(config):
    schema = get_yaml_config_schema()
    return schema(config)