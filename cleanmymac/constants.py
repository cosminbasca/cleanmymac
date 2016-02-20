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

#: the main entry point for externally defined :class:`cleanmymac.target.Target` extensions
TARGET_ENTRY_POINT = 'cleanmymac.target'

#: the global config file name
GLOBAL_CONFIG_FILE = '.cleanmymac.yaml'

#: the **YAML** constant used to identify targets of type: :class:`cleanmymac.target.ShellCommandTarget`
TYPE_TARGET_CMD = 'cmd'

#: the **YAML** constant used to identify targets of type: :class:`cleanmymac.target.DirTarget`
TYPE_TARGET_DIR = 'dir'

#: the **YAML** valid target types
VALID_TARGET_TYPES = frozenset([
    TYPE_TARGET_DIR,
    TYPE_TARGET_CMD
])

#: 1 kilobyte
UNIT_KB = 1024

#: 1 megabyte
UNIT_MB = UNIT_KB * 1024

#: 1 gigabyte
UNIT_GB = UNIT_MB * 1024

#: the progress bar advance delay (when in quiet mode). Nicer progress experience for fast targets
PROGRESSBAR_ADVANCE_DELAY = 0.25

DESCRIBE_CLEAN = 'clean'
DESCRIBE_UPDATE = 'update'
VALID_DESCRIBE_MESSAGES = frozenset([
    DESCRIBE_CLEAN,
    DESCRIBE_UPDATE
])
