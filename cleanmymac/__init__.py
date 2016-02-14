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
from .__version__ import str_version, version
from .constants import *
from .log import (
    debug, debug_param, is_debug,
    is_level,
    echo, echo_info, echo_warn, echo_error, echo_success, echo_target,
    error, info, warn,
    LOGGER_NAME
)
from .registry import (
    get_target,
    get_targets_as_table,
    iter_targets,
    load_target,
    register_target,
    register_yaml_targets
)
from .schema import IsDirUserExpand, validate_yaml_config
from .target import DirTarget, ShellCommandTarget, Target, YamlShellCommandTarget, YamlDirTarget
from .util import (
    delete_dir_content,
    delete_dirs,
    get_disk_usage,
    progressbar,
    yaml_files,
    Dir,
    DirList,
    DiskUsage
)

__author__ = 'cosmin'
