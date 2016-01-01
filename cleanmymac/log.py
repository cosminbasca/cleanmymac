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
from colorlog import ColoredFormatter
import logging

LOGGER_NAME = 'cleanmymac'

_logger = None

DISABLED = 100
CRITICAL = 50
ERROR = 40
WARNING = 30
INFO = 20
DEBUG = 10
NOTSET = 0


def debug(msg, *args):
    """
    log debug messages. It uses the __debug__ python special var for speedy processing of
    debug messages when debugging is disabled
    :param msg: the message + format
    :param args: message arguments
    :return: nothing
    """
    if __debug__:
        if _logger:
            _logger.log(DEBUG, msg, *args)


def info(msg, *args):
    """
    log info messages
    :param msg: the message + format
    :param args: message arguments
    :return: nothing
    """
    if _logger:
        _logger.log(INFO, msg, *args)


def warn(msg, *args):
    """
    log warning messages
    :param msg: the message + format
    :param args: message arguments
    :return: nothing
    """
    if _logger:
        _logger.log(WARNING, msg, *args)


def error(msg, *args):
    """
    log error messages
    :param msg: the message + format
    :param args: message arguments
    :return: nothing
    """
    if _logger:
        _logger.log(ERROR, msg, *args)


def get_logger(name=LOGGER_NAME, handler=None):
    """
    create a logger
    the method is thread safe
    :param name: the name of the logger, by default LOGGER_NAME is used
    :param handler: add a logging handler, if None, a default console handler is created
    :return: the logger
    """
    # LOG_FORMAT = '%(asctime)s %(levelname)-8s %(name)-15s %(message)s'
    LOG_FORMAT = '%(levelname)-8s %(message)s'
    # COLOR_LOG_FORMAT = '%(log_color)s%(levelname)-8s%(reset)s %(message)s'
    COLOR_LOG_FORMAT = '%(log_color)s%(message)s'
    logging._acquireLock()
    try:
        # general setup
        # formatter = logging.Formatter(LOG_FORMAT)
        formatter = ColoredFormatter(COLOR_LOG_FORMAT)

        if not handler:
            handler = [logging.StreamHandler()]
        elif not isinstance(handler, (list, tuple)):
            handler = [handler]

        logger = logging.getLogger(name)
        logger.propagate = 0
        for hndlr in handler:
            hndlr.setFormatter(formatter)
            logger.addHandler(hndlr)
    finally:
        logging._releaseLock()

    return logger


def setup_logger(name=LOGGER_NAME, handler=None):
    """
    set the module global logger object
    :param name: the logger name
    :param handler: the logger handler, None for console
    :return: nothing
    """
    global _logger
    _logger = get_logger(name=name, handler=handler)


def uninstall_logger():
    """
    uninstalls a previously set up logger
    :return: nothing
    """
    global _logger
    _logger = None


def set_logger(logger):
    """
    install an existing logger as the module global logger
    :param logger: the logger
    :return: nothing
    """
    global _logger
    if logger:
        _logger = logger


def set_logger_level(level, name=None):
    """
    set the logging level for the given logger name
    the method is thread safe
    :param level: the level
    :param name: the logger name, if name is not found the logging.root logger is configured
    :return: nothing
    """
    logging._acquireLock()
    try:
        logger = logging.getLogger(name) if name else logging.root
        if isinstance(level, basestring):
            level = level.upper()
        logger.setLevel(level)
    finally:
        logging._releaseLock()


def disable_logger(name=None):
    """
    disable the given logger. This is a convenience method
    the method is thread safe
    :param name: the logger name
    :return: nothing
    """
    set_logger_level(DISABLED, name=name)
