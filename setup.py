#!/usr/bin/env python
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
import sys
try:
    from setuptools import setup
except ImportError:
    from ez_setup import use_setuptools

    use_setuptools()
    from setuptools import setup

NAME = 'cleanmymac'
PY2 = sys.version_info[0] == 2

str_version = None
if PY2:
    execfile('{0}/__version__.py'.format(NAME))
else:
    exec(open('{0}/__version__.py'.format(NAME)).read())

# Load up the description from README
with open('README.rst') as f:
    DESCRIPTION = f.read()

deps = [
    'sarge>=0.1.4',
    'pyyaml>=3.11',
    'voluptuous>=0.8.8',
    'colorlog>=2.6.0',
    'natsort>=4.0.4',
    'click>=6.2',
    'click-log>=0.1.3',
    'tabulate>=0.7.5',
    'pytest>=2.8.7',
    'six>=1.10.0',
]

setup(
    name=NAME,
    version=str_version,
    author='Cosmin Basca',
    author_email='cosmin.basca@gmail.com',
    url='https://github.com/cosminbasca/cleanmymac',
    description='A simple utility to clean your mac of old stuff',
    long_description=DESCRIPTION,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Operating System :: MacOS',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Text Processing :: Markup',
        'Topic :: Utilities',
    ],
    platforms=['MacOS'],
    license='Apache',
    packages=[
        NAME,
        '{0}/builtins'.format(NAME),
        '{0}/test'.format(NAME),
    ],
    package_data={
        '{0}/builtins'.format(NAME): ['*.yaml', ],
    },
    install_requires=deps,
    tests_require=deps,
    entry_points={
        'console_scripts': [
            'cleanmymac = cleanmymac.cli:cli'
        ]
    }
)
