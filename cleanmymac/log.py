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

#: log level Disabled
DISABLED = 100
#: log level Critical
CRITICAL = 50
#: log level Error
ERROR = 40
#: log level Warning
WARNING = 30
#: log level Info
INFO = 20
#: log level Debug
DEBUG = 10
#: log level not set
NOTSET = 0


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
            _logger.log(DEBUG, msg, *args)


def info(msg, *args):
    """
    log info messages

    :param msg: the message + format
    :type msg: str
    :param args: message arguments
    :type args: list
    """
    if _logger:
        _logger.log(INFO, msg, *args)


def warn(msg, *args):
    """
    log warning messages

    :param msg: the message + format
    :type msg: str
    :param args: message arguments
    :type args: list
    """
    if _logger:
        _logger.log(WARNING, msg, *args)


def error(msg, *args):
    """
    log error messages

    :param msg: the message + format
    :type msg: str
    :param args: message arguments
    :type args: list
    """
    if _logger:
        _logger.log(ERROR, msg, *args)


def echo_error(msg):
    click.secho(msg, fg='red')


def echo_info(msg):
    click.secho(msg, fg='white')


def echo_warn(msg):
    click.secho(msg, fg='yellow')


def echo_success(msg):
    click.secho(msg, fg='green')


def echo(msg):
    click.echo(msg)

