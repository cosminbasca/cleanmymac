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

#: the main **cleanmymac** logger name
LOGGER_NAME = 'cleanmymac'

_logger = logging.getLogger(LOGGER_NAME)
_logger.setLevel(logging.CRITICAL)


def debug(msg, *args):
    """
    log debug messages. It uses the `__debug__` python special var for speedy processing of
    debug messages when debugging is disabled

    :param msg: the message + format
    :type msg: str
    :param args: message arguments
    :type args: list
    """
    if __debug__:
        if _logger:
            _logger.debug(msg, *args)


def info(msg, *args):
    """
    log info messages

    :param msg: the message + format
    :type msg: str
    :param args: message arguments
    :type args: list
    """
    if _logger:
        _logger.info(msg, *args)


def warn(msg, *args):
    """
    log warning messages

    :param msg: the message + format
    :type msg: str
    :param args: message arguments
    :type args: list
    """
    if _logger:
        _logger.warn(msg, *args)


def error(msg, *args):
    """
    log error messages

    :param msg: the message + format
    :type msg: str
    :param args: message arguments
    :type args: list
    """
    if _logger:
        _logger.error(msg, *args)


def echo_error(msg):
    """
    convenience method to display a message using the **red** ANSI color,
    the method relies on :func:`click.secho`

    :param str msg: the message
    """
    click.secho(msg, fg='red')


def echo_info(msg):
    """
    convenience method to display a message using the **white** ANSI color,
    the method relies on :func:`click.secho`

    :param str msg: the message
    """
    click.secho(msg, fg='white')


def echo_warn(msg):
    """
    convenience method to display a message using the **yellow** ANSI color,
    the method relies on :func:`click.secho`

    :param str msg: the message
    """
    click.secho(msg, fg='yellow')


def echo_success(msg):
    """
    convenience method to display a message using the **green** ANSI color,
    the method relies on :func:`click.secho`

    :param str msg: the message
    """
    click.secho(msg, fg='green')


def echo(msg):
    """
    convenience method to display a message,
    the method relies on :func:`click.echo`

    :param str msg: the message
    """
    click.echo(msg)

