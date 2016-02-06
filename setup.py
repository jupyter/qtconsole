#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

from __future__ import print_function

# the name of the package
name = 'qtconsole'

#-----------------------------------------------------------------------------
# Minimal Python version sanity check
#-----------------------------------------------------------------------------

import sys

v = sys.version_info
if v[:2] < (2,7) or (v[0] >= 3 and v[:2] < (3,3)):
    error = "ERROR: %s requires Python version 2.7 or 3.3 or above." % name
    print(error, file=sys.stderr)
    sys.exit(1)

PY3 = (sys.version_info[0] >= 3)

#-----------------------------------------------------------------------------
# get on with it
#-----------------------------------------------------------------------------

import os
from glob import glob

from distutils.core import setup

pjoin = os.path.join
here = os.path.abspath(os.path.dirname(__file__))
pkg_root = pjoin(here, name)

packages = []
for d, _, _ in os.walk(pjoin(here, name)):
    if os.path.exists(pjoin(d, '__init__.py')):
        packages.append(d[len(here)+1:].replace(os.path.sep, '.'))

package_data = {
    'qtconsole' : ['resources/icon/*.svg'],
}

version_ns = {}
with open(pjoin(here, name, '_version.py')) as f:
    exec(f.read(), {}, version_ns)


setup_args = dict(
    name            = name,
    version         = version_ns['__version__'],
    scripts         = glob(pjoin('scripts', '*')),
    packages        = packages,
    package_data    = package_data,
    description     = "Jupyter Qt console",
    long_description= "Qt-based console for Jupyter with support for rich media output",
    author          = 'Jupyter Development Team',
    author_email    = 'jupyter@googlegroups.com',
    url             = 'http://jupyter.org',
    license         = 'BSD',
    platforms       = "Linux, Mac OS X, Windows",
    keywords        = ['Interactive', 'Interpreter', 'Shell'],
    classifiers     = [
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
    ],
)

if 'develop' in sys.argv or any(a.startswith('bdist') for a in sys.argv):
    import setuptools

setuptools_args = {}
install_requires = setuptools_args['install_requires'] = [
    'traitlets',
    'jupyter_core',
    'jupyter_client>=4.1',
    'pygments',
    'ipykernel>=4.1', # not a real dependency, but require the reference kernel
]

extras_require = setuptools_args['extras_require'] = {
    'test:python_version=="2.7"': ['mock'],
    'test:sys_platform != "win32"': ['pexpect'],
    'doc': 'Sphinx>=1.3'
}

if 'setuptools' in sys.modules:
    setup_args['entry_points'] = {
        'gui_scripts': [
            'jupyter-qtconsole = qtconsole.qtconsoleapp:main',
        ]
    }
    setup_args.pop('scripts')
    setup_args.update(setuptools_args)

if __name__ == '__main__':
    setup(**setup_args)
