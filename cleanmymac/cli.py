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
import click
import click_log
import os
from yaml import load
from time import sleep
from pprint import pformat

from cleanmymac.__version__ import str_version
from cleanmymac.log import info, warn, error, debug, echo_warn, echo_info, echo_target, is_debug, echo, echo_success, \
    debug_param, disable_logger
from cleanmymac.registry import iter_targets, register_yaml_targets, get_targets_as_table
from cleanmymac.schema import validate_yaml_config
from cleanmymac.target import Target
from cleanmymac.util import get_disk_usage, progressbar
from cleanmymac.constants import UNIT_MB, PROGRESSBAR_ADVANCE_DELAY, GLOBAL_CONFIG_FILE

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
        path = os.path.join(os.path.expanduser('~'), GLOBAL_CONFIG_FILE)
    path = os.path.abspath(path)
    debug_param('global config', path)
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


@click.command(name='cleanmymac', context_settings={
    'help_option_names': ['-?', '-h', '--help']
})
@click_log.init()
@click_log.simple_verbosity_option('-L', '--log-level', default='INFO')
@click.option('-u', '--update', is_flag=True, help='update the target if applicable')
@click.option('-d', '--dry_run', is_flag=True, help='describe the actions to be performed, do not execute them')
@click.option('-q', '--quiet', is_flag=True, help='run in quiet mode')
@click.option('--strict/--no-strict', default=True,
              help='strict mode: enforce strict(er) rules when validating targets')
@click.option('-l', '--list', 'list_targets', is_flag=True, help='list registered cleanup targets')
@click.option('-s', '--stop_on_error', is_flag=True, help='stop execution when first error is detected')
@click.option('-c', '--config', default=None, envvar='CLEANMYMAC_CONFIG', help='specify the configuration path')
@click.option('-t', '--targets_path', default=None, type=click.Path(exists=True), multiple=True,
              help='specify extra yaml defined targets path')
@click.version_option(str_version, '-v', '--version')
@click.argument('targets', metavar='TARGETS', type=str, nargs=-1)
def cli(update, dry_run, quiet, strict, list_targets, stop_on_error, config, targets_path, targets, **kwargs):
    """
    the main **run** method, responsible for creating the parser and executing the main logic in
    **cleanmymac**

    :param bool update: perform update of targets (if applicable)
    :param dry_run: do not execute the actions, but log the result
    :param quiet: quiet mode (no output), show a progressbar instead
    :param strict: if set enforce strict(er) rules when validating targets
    :param list_targets: list the installed targets
    :param stop_on_error: abort the execution on first error
    :param config: the configuration path
    :param targets_path: extra targets paths
    :param targets: the targets
    """
    disable_logger('sarge')
    targets = tuple([target.lower() for target in targets])

    debug_param('update', update)
    debug_param('dry run', dry_run)
    debug_param('quiet mode', quiet)
    debug_param('strict mode', strict)
    debug_param('list available targets', list_targets)
    debug_param('stop on error', stop_on_error)
    debug_param('global config path', config)
    debug_param('extra targets path', targets_path)
    debug_param('targets', targets)
    debug('')

    all_targets = dict(iter_targets())
    if is_debug():
        debug("Detailed information about registered targets")
        debug(get_targets_as_table(simple=False, fancy=False))

    if dry_run:
        verbose = True
    else:
        verbose = not quiet
    debug_param('verbose', verbose)

    if targets:
        target_names = set(targets)
    else:
        target_names = set(all_targets.keys())

    echo_info('found {0} registered cleanup targets'.format(len(all_targets)), verbose=verbose)

    config = get_options(path=config)
    # register extra targets if any
    for pth in _config_targets_path(config):
        register_yaml_targets(pth)
    if targets_path and os.path.isdir(targets_path):
        register_yaml_targets(targets_path)

    if list_targets:
        echo_warn(get_targets_as_table(simple=True, fancy=True))
    else:
        with progressbar(verbose, all_targets.items(), label='Processing cleanup targets:',
                         width=40) as all_targets_bar:
            free_space_before = get_disk_usage('/', unit=UNIT_MB).free

            for name, target_initializer in all_targets_bar:
                if name not in target_names:
                    debug('skipping target "{0}"'.format(name))
                    continue
                echo_target('\ncleaning: {0}'.format(name.upper()), verbose=verbose)
                target_cfg = config[name] if name in config else None
                debug("got target configuration: {0}".format(pformat(target_cfg)))

                try:
                    target = target_initializer(target_cfg, update=update, verbose=verbose, strict=strict)

                    if not isinstance(target, Target):
                        error('expected an instance of Target, instead got: {0}'.format(target))
                        continue

                    if dry_run:
                        echo_warn(target.describe())
                    else:
                        target()
                except Exception, ex:
                    error('could not cleanup target "{0}". Reason:\n{1}'.format(name, ex))
                    if stop_on_error:
                        break

                if not verbose:
                    sleep(PROGRESSBAR_ADVANCE_DELAY)  # nicer progress bar display for fast executing targets

            free_space_after = get_disk_usage('/', unit=UNIT_MB).free
            if not dry_run:
                echo_info('\ncleanup complete', verbose=verbose)
                echo_success('\nfreed {0:.3f} MB of disk space'.format(free_space_after - free_space_before),
                             verbose=True, nl=verbose)
