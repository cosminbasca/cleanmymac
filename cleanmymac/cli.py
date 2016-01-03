# coding=utf-8
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
from cleanmymac.registry import iter_targets, register_yaml_targets
from cleanmymac.schema import validate_yaml_config
from cleanmymac.target import Target
from cleanmymac.util import get_disk_usage
from cleanmymac.constants import UNIT_KB, UNIT_MB
from tqdm import tqdm
from yaml import load
import os

__author__ = 'cosmin'


def get_options(path=None):
    """
    Return the global configuration options. This method also expands the user home folder
    specified by '~'. In addition, the yaml config file is validated after parse.
    If the path is not specified, the ~/.cleanmymac.yaml configuration file is looked up, if not
    found, the global configuration is set to an empty dict.

    :param path: optional path to a yaml configuration file
    :type path: str
    :return: a python object containing the actual configuration
    :rtype: dict
    """
    cfg = {}
    if not path:
        path = os.path.join(os.path.expanduser('~'), '.cleanmymac.yaml')
    path = os.path.abspath(path)
    if not os.path.exists(path):
        warn('global configuration file not found, proceeding without.')
    else:
        with open(path, 'r+') as cfg:
            cfg = load(cfg)
    return validate_yaml_config(cfg)


def _config_targets_path(config):
    if 'cleanmymac' in config:
        if 'targets_path' in config['cleanmymac']:
            return config['cleanmymac']['targets_path']
    return []


def get_parser():
    """
    creates and returns the parsed used by the command line utility

    :return: the command line parser
    :rtype: :class:`argparse.ArgumentParser`
    """
    parser = argparse.ArgumentParser(description='cleanmymac v{0}, a simple utility designed to help clean your mac '
                                                 'from old/unwanted stuff'.format(str_version))
    parser.add_argument('targets', metavar='TARGETS', type=str, nargs='*',
                        help='the list of targets to execute. Execute all if not specified.')
    parser.add_argument('-u', '--update', action='store_true',
                        help='update the target if applicable')
    parser.add_argument('-d', '--dry_run', action='store_true',
                        help='describe the actions to be performed, do not execute them')
    parser.add_argument('-q', '--quiet', action='store_true',
                        help='run in quiet mode')
    parser.add_argument('-l', '--list', action='store_true',
                        help='list registered cleanup targets')
    parser.add_argument('-s', '--stop_on_error', action='store_true',
                        help='stop execution when first error is detected')
    parser.add_argument('-c', '--config', action='store', default=None,
                        help='specify the configuration path')
    parser.add_argument('-t', '--targets_path', action='store', default=None,
                        help='specify extra yaml defined targets path')
    return parser


def run_cmd():
    """
    the main **run** method, responsible for creating the parser and executing the main logic in
    **cleanmymac**
    """
    parser = get_parser()
    args = parser.parse_args()
    targets = dict(iter_targets())

    update = args.update
    verbose = not args.quiet
    dry_run = args.dry_run
    targets_path = args.targets_path
    stop_on_error = args.stop_on_error
    list_targets = args.list
    if args.targets:
        targets_to_execute = set(args.targets)
    else:
        targets_to_execute = set(targets.keys())

    targets_iterator = targets.iteritems() if verbose else tqdm(targets.iteritems())

    _log = info if verbose else debug
    _describe = warn if verbose else debug

    _log('found {0} registered cleanup targets'.format(len(targets)))

    config = get_options(path=args.config)
    # register extra targets if any
    for pth in _config_targets_path(config):
        register_yaml_targets(pth)
    if targets_path and os.path.isdir(targets_path):
        register_yaml_targets(targets_path)

    if list_targets:
        for name, target_initializer in targets_iterator:
            warn(' > {0}'.format(name))
    else:
        free_space_before = get_disk_usage('/', unit=UNIT_MB).free
        for name, target_initializer in targets_iterator:
            if name not in targets_to_execute:
                continue
            _log('\ncleaning: {0}'.format(name.upper()))
            target_cfg = config[name] if name in config else None
            target = target_initializer(target_cfg, update=update, verbose=verbose)

            if not isinstance(target, Target):
                error('expected an instance of Target, instead got: {0}'.format(target))
                continue

            if dry_run:
                _describe(target.describe())
            else:
                try:
                    target()
                except Exception, ex:
                    error('could not cleanup target "{0}". Reason:\n{1}'.format(
                        name, ex))
                    if stop_on_error:
                        break

        free_space_after = get_disk_usage('/', unit=UNIT_MB).free
        if not dry_run:
            _log('\ncleanup complete')
            _log('freed {0:.3f} MB of disk space'.format(free_space_after-free_space_before))
