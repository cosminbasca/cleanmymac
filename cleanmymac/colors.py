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

_color_map = {
    'warn': 'yellow',
    'error': 'red',
    'info': 'white',
    'success': 'green',
    'target': 'blue',
    'debug': 'yellow',
}

_with_colors = True


def set_pretty_print(value):
    """
    toggle pretty printing of messages (with colors)

    :param bool value: enable / disable pretty printing mode
    """
    global _with_colors
    _with_colors = True if value else False


def get_color(key):
    """
    gets the color for the given key

    :param str key: a key denoting a specific colored output (i.e., debug or success)
    :return: the colour
    :rtype: str or None
    """
    if _with_colors:
        return _color_map.get(key, None)
    return None
