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
import tempfile
import pytest
import os

from cleanmymac.util import yaml_files, delete_dir_content, Dir


def test_yaml_files():
    with tempfile.NamedTemporaryFile(suffix='.yaml') as a_file:
        files = list(yaml_files(tempfile.gettempdir()))
        assert len(files) == 1


def test_delete_dir_content():
    tmp_dir = tempfile.mkdtemp()

    start_len = len(os.listdir(tmp_dir))
    with tempfile.NamedTemporaryFile(dir=tmp_dir) as a_file:
        with tempfile.NamedTemporaryFile(dir=tmp_dir) as b_file:
            assert len(os.listdir(tmp_dir)) == start_len + 2
    delete_dir_content(Dir(tmp_dir))
    assert len(os.listdir(tmp_dir)) == 0
    with pytest.raises(AssertionError):
        delete_dir_content(tmp_dir)
