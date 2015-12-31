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
from abc import ABCMeta, abstractmethod
from pkg_resources import iter_entry_points
from cleanmymac.log import debug, info, error, warn
from sarge import shell_format, Capture, run

TARGET_ENTRY_POINT = 'cleanmymac.target'

_targets = {}


class Target(object):
    __metaclass__ = ABCMeta

    def __init__(self, **kwargs):
        pass

    @abstractmethod
    def __call__(self, *args, **kwargs):
        pass


def register(name, target):
    global _targets
    if isinstance(target, Target):
        info('registering : {0}'.format(name))
    else:
        error('target {0} is not of type Target, instead got: {1}'.format(name, target))


def get(name):
    global _targets
    try:
        return _targets[name]
    except KeyError:
        error("no target found for: {0}".format(name))
        return None


# register installed targets (if any)
info("looking for registered cleanup targets...")
for ep in iter_entry_points(TARGET_ENTRY_POINT):
    info("found: {0}".format(ep))


# built in targets
class HomeBrew(Target):
    def __init__(self, update=False, **kwargs):
        super(HomeBrew, self).__init__(**kwargs)


    def __call__(self, *args, **kwargs):
        pass