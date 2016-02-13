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
import os
import shutil
import click
from contextlib import contextmanager
from collections import namedtuple

from cleanmymac.log import error
from cleanmymac.constants import UNIT_KB, UNIT_MB, UNIT_GB


def yaml_files(path):
    """
    generator of **YAML** files in the give path.

    :param path: the path to scan for *YAML* files
    :return: a generator
    :raise: :class:`ValueError` if path is not a valid directory
    """
    if not os.path.isdir(path):
        raise ValueError('{0} not a directory'.format(path))
    for _file in os.listdir(path):
        if _file.endswith(".yaml"):
            yield os.path.splitext(_file)[0], os.path.join(path, _file)


#: a :func:`collections.namedtuple` holding disk usage statistics
DiskUsage = namedtuple('DiskUsage', ['total', 'used', 'free'])


def get_disk_usage(path='/', unit=UNIT_KB):
    """
    retrieve disk usage statistics for a given path
    this function was inspired by the following *stackoverflow* discussion:
    http://stackoverflow.com/questions/787776/find-free-disk-space-in-python-on-os-x

    :param str path: the path (defaults to **/**)
    :param long unit: the measurement unit
    :return: the usage statistics
    :rtype: DiskUsage
    """
    stats = os.statvfs(path)
    free = stats.f_bavail * stats.f_frsize
    total = stats.f_blocks * stats.f_frsize
    used = (stats.f_blocks - stats.f_bfree) * stats.f_frsize
    return DiskUsage(float(total) / unit, float(used) / unit, float(free) / unit)


#: a list of directories
DirList = namedtuple('DirList', ['dirs'])

#: a single directory
Dir = namedtuple('Dir', ['path'])


def delete_dir_content(folder):
    """
    delete all the files and directories in path

    :param Dir folder: a valid directory path
    """
    assert isinstance(folder, Dir)
    if not os.path.isdir(folder.path):
        error('{0} not a directory'.format(folder.path))
        return

    for root, dirs, files in os.walk(folder.path):
        for f in files:
            os.unlink(os.path.join(root, f))
        for d in dirs:
            shutil.rmtree(os.path.join(root, d))


def delete_dirs(dir_list):
    """
    delete all directories in list

    :param DirList dir_list: the list of directories
    """
    assert isinstance(dir_list, DirList)
    for d in dir_list.dirs:
        if os.path.isdir(d):
            shutil.rmtree(d)


@contextmanager
def progressbar(verbose, iterable, **kwargs):
    """
    wrapper over the :func:`click.progressbar` context manager

    :param bool verbose: if False use the :func:`click.progressbar`, else return `iterable`
    :param iterable iterable: the iterable object
    :param dict kwargs: extra arguments for :func:`click.progressbar`
    :return: an iterator
    :rtype: iterable
    """
    if verbose:
        yield iterable
    else:
        #: default template '%(label)s  [%(bar)s]  %(info)s'
        kwargs['bar_template'] = '%(label)s  [{0}]  {1}'.format(
            click.style('%(bar)s', fg='blue'),
            click.style('%(info)s', fg='yellow'))
        with click.progressbar(iterable, **kwargs) as bar:
            yield bar
