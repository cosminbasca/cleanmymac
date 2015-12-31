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

import argparse
from cleanmymac.__version__ import str_version
from cleanmymac.log import info, warn, error, debug

__author__ = 'cosmin'


def get_parser():
    parser = argparse.ArgumentParser(description='cleanmymac v{0}'.format(str_version))
    parser.add_argument('-u', '--update', action='store_true',
                        help='update the target if applicable')
    parser.add_argument('-d', '--dry_run', action='store_true',
                        help='describe the actions to be performed, do not execute them')
    parser.add_argument('-v', '--verbose', action='store_true',
                        help='run in verbose mode')
    parser.add_argument('-c', '--config', action='store', default=None,
                        help='specify the configuration path')
    return parser


def run_cmd():
    parser = get_parser()
    args = parser.parse_args()
    info('clean my mac!')
