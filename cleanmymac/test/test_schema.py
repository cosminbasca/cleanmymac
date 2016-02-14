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
import pytest
from voluptuous import MultipleInvalid
from yaml import load

from cleanmymac.schema import _cmd_spec_schema, _dir_spec_schema


def test_cmd_spec_schema():
    spec = """
update_commands: [
    'cmd1',
    'cmd1'
]
clean_commands: [
    'cmd3'
]
        """.strip()
    obj_spec = load(spec)
    validated_spec = _cmd_spec_schema(strict=False)(obj_spec)
    assert 'update_commands' in validated_spec
    assert 'clean_commands' in validated_spec
    assert set(validated_spec['update_commands']) == set(obj_spec['update_commands'])
    assert set(validated_spec['clean_commands']) == set(obj_spec['clean_commands'])

    # test for invalid keys
    obj_spec['extra_key'] = ['val1', 'val2']
    with pytest.raises(MultipleInvalid):
        _cmd_spec_schema(strict=False)(obj_spec)
    del obj_spec['extra_key']


def test_dir_spec_schema():
    spec = """
update_message: 'a message'
entries: [
    {
        dir: '~',
        pattern: '\d+'
    },
]
        """.strip()
    obj_spec = load(spec)
    validated_spec = _dir_spec_schema(strict=False)(obj_spec)
    assert 'update_message' in validated_spec
    assert 'entries' in validated_spec
    assert validated_spec['update_message'] == obj_spec['update_message']
    assert len(validated_spec['entries']) == len(obj_spec['entries'])

    # test for invalid keys
    obj_spec['extra_key'] = ['val1', 'val2']
    with pytest.raises(MultipleInvalid):
        _dir_spec_schema(strict=False)(obj_spec)
    del obj_spec['extra_key']

    # test for strictness
    assert isinstance(_dir_spec_schema(strict=True)(obj_spec), dict)
    spec = """
update_message: 'a message'
entries: [
    {
        dir: '/____folder/_that/_does/_not/_exist/',
        pattern: '\d+'
    },
]
        """.strip()
    obj_spec = load(spec)
    with pytest.raises(MultipleInvalid):
        _dir_spec_schema(strict=True)(obj_spec)
