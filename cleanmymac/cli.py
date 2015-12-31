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
from cleanmymac.target import iter_targets, Target
from tqdm import tqdm
from yaml import load
import os

__author__ = 'cosmin'


def get_options(path=None):
    if not path:
        path = '~/.cleanmymac.yaml'
    if not os.path.exists(path):
        warn('global configuration file not found, proceeding without.')
        return {}
    else:
        with open(path, 'r+') as cfg:
            return load(cfg)


def get_parser():
    parser = argparse.ArgumentParser(description='cleanmymac v{0}, a simple utility designed to help clean your mac '
                                                 'from old/unwanted stuff'.format(str_version))
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
    targets = dict(iter_targets())

    targets_iterator = targets.iteritems() if args.verbose else tqdm(targets.iteritems())

    _log = info if args.verbose else debug
    _log('found {0} registered cleanup targets'.format(len(targets)))

    config = get_options(args.config)

    for name, TargetClass in targets_iterator:
        if not issubclass(TargetClass, Target):
            error('expected a subclass of Target, instead got: {0}'.format(TargetClass))
            continue
        _log('cleaning: {0}'.format(name))
        target_cfg = config[name] if name in config else None
        target = TargetClass(target_cfg, update=args.update, verbose=args.verbose)
        if args.dry_run:
            _log('commands to run: \n{0}'.format(target.describe()))
        else:
            target()
    _log('cleanup complete')
