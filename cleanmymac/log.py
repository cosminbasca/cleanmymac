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
import logging
import click
import click_log

from six import string_types
from pprint import pformat


#: the main **cleanmymac** logger name
LOGGER_NAME = 'cleanmymac'

#: the internal **cleanmymac** logger object
_logger = logging.getLogger(LOGGER_NAME)


def disable_logger(name):
    """
    disable the given logger

    :param name: the name of the logger
    """
    logger = logging.getLogger(name)
    logger.setLevel(100)


def _log(level, msg, *args):
    """
    log messages.

    :param str or object msg: the message + format
    :oaram int level: the logging level
    :param list args: message arguments
    """
    if _logger:
        if not isinstance(msg, string_types):
            msg = pformat(msg)
        _logger.log(level, msg, *args)


def debug(msg, *args):
    """
    log debug messages.

    :param str or object msg: the message + format
    :param list args: message arguments
    """
    _log(logging.DEBUG, msg, *args)


def debug_param(msg, value, padding=30):
    """
    helper method to debug parameter values, with alignment

    :param str msg: the message
    :param str value: the value
    :param int padding: padding for the message
    """
    fmt = '{0: <' + str(padding) + '} : {1}'
    debug(fmt.format(msg, click.style(str(value), fg='yellow')))


def info(msg, *args):
    """
    log info messages

    :param str or object msg: the message + format
    :param list args: message arguments
    """
    _log(logging.INFO, msg, *args)


def warn(msg, *args):
    """
    log warning messages

    :param str or object msg: the message + format
    :param list args: message arguments
    """
    _log(logging.WARN, msg, *args)


def error(msg, *args):
    """
    log error messages

    :param str or object msg: the message + format
    :param list args: message arguments
    """
    _log(logging.ERROR, msg, *args)


def echo_error(msg, verbose=True):
    """
    convenience method to display a message using the **red** ANSI color,
    the method relies on :func:`click.secho`

    :param str msg: the message
    :param bool verbose: echo message only if True
    """
    if verbose:
        click.secho(msg, fg='red')


def echo_info(msg, verbose=True):
    """
    convenience method to display a message using the **white** ANSI color,
    the method relies on :func:`click.secho`

    :param str msg: the message
    :param bool verbose: echo message only if True
    """
    if verbose:
        click.secho(msg, fg='white')


def echo_warn(msg, verbose=True):
    """
    convenience method to display a message using the **yellow** ANSI color,
    the method relies on :func:`click.secho`

    :param str msg: the message
    :param bool verbose: echo message only if True
    """
    if verbose:
        click.secho(msg, fg='yellow')


def echo_success(msg, verbose=True, nl=True):
    """
    convenience method to display a message using the **green** ANSI color,
    the method relies on :func:`click.secho`

    :param str msg: the message
    :param bool verbose: echo message only if True
    :param bool nl: print new line
    """
    if verbose:
        click.secho(msg, fg='green', nl=nl)


def echo_target(msg, verbose=True):
    """
    convenience method to display a message using the **blue** ANSI color,
    the method relies on :func:`click.secho`

    :param str msg: the message
    :param bool verbose: echo message only if True
    """
    if verbose:
        click.secho(msg, fg='blue')


def echo(msg):
    """
    convenience method to display a message,
    the method relies on :func:`click.echo`

    :param str msg: the message
    """
    click.echo(msg)


#: string mapping for logging levels
STR_LEVELS = {
    'critical': logging.CRITICAL,
    'error': logging.ERROR,
    'warn': logging.WARN,
    'warning': logging.WARN,
    'info': logging.INFO,
    'debug': logging.DEBUG,
}


def is_level(level):
    """
    test if the :func:`click_log.get_level` is same as `level`

    :param int or str level: the level to check
    :return: True if level matches
    :rtype: bool
    """
    if isinstance(level, basestring):
        level = STR_LEVELS[level.lower()]
    return click_log.get_level() == level


def is_debug():
    """
    test if the :func:`click_log.get_level` is `logging.DEBUG`

    :return: True if in debug mode
    :rtype: bool
    """
    return is_level(logging.DEBUG)
