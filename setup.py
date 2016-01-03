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
try:
    from setuptools import setup
except ImportError:
    from ez_setup import use_setuptools

    use_setuptools()
    from setuptools import setup

NAME = 'cleanmymac'

str_version = None
execfile('{0}/__version__.py'.format(NAME))

# Load up the description from README
with open('README.rst') as f:
    DESCRIPTION = f.read()

pip_deps = [
    'sarge>=0.1.4',
    'tqdm>=3.4.0',
    'pyyaml>=3.11',
    'voluptuous>=0.8.8',
    'colorlog>=2.6.0',
    'natsort>=4.0.4',
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
        'Topic :: Text Processing :: Markup',
        'Topic :: Utilities',
    ],
    packages=[
        NAME,
        '{0}/builtins'.format(NAME),
    ],
    package_data={
        '{0}/builtins'.format(NAME): ['*.yaml', ],
    },
    install_requires=pip_deps,
    entry_points={
        'console_scripts': [
            'cleanmymac = cleanmymac.cli:run_cmd'
        ]
    }
)
