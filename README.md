# Jupyter Qt Console

[![Google Group](https://img.shields.io/badge/-Google%20Group-lightgrey.svg)](https://groups.google.com/forum/#!forum/jupyter)
[![Build Status](https://travis-ci.org/jupyter/qtconsole.svg?branch=master)](https://travis-ci.org/jupyter/qtconsole)
[![Documentation Status](https://readthedocs.org/projects/qtconsole/badge/?version=stable)](http://qtconsole.readthedocs.org/en/stable/?badge=stable)

A rich Qt-based console for working with Jupyter kernels,
supporting rich media output, session export, and more.

This is a very lightweight widget that
largely feels like a terminal, but provides a number of enhancements only
possible in a GUI, such as inline figures, proper multiline editing with syntax
highlighting, graphical calltips, and much more.


![qtconsole](docs/source/_images/qtconsole.png)

## Installation

### Prerequisites
The qtconsole requires [PyQt][] or [PySide][].
These requirements cannot be installed with pip.
PyQt may be installed with [conda][]:

    conda install pyqt

or your system package manager, e.g. for Linux Debian/Ubuntu:

    apt-get install python3-pyqt5

### Install qtconsole

To install:

    pip install qtconsole

or:

    conda install qtconsole

Note: If you install the Qt console using conda, it will automatically install
PyQt as well.

## Usage

To run qtconsole:

    jupyter qtconsole

[PyQt]: http://www.riverbankcomputing.com/software/pyqt/intro
[PySide]: http://pyside.github.io/docs/pyside
[conda]: http://conda.pydata.org/docs

## Resources
- [Project Jupyter website](https://jupyter.org)
- Documentation for qtconsole
  * [latest version](http://qtconsole.readthedocs.org/en/latest/) [[PDF](https://media.readthedocs.org/pdf/qtconsole/latest/qtconsole.pdf)]
  * [stable version](http://qtconsole.readthedocs.org/en/stable/) [[PDF](https://media.readthedocs.org/pdf/qtconsole/stable/qtconsole.pdf)]
- [Documentation for Project Jupyter](http://jupyter.readthedocs.org/en/latest/index.html) [[PDF](https://media.readthedocs.org/pdf/jupyter/latest/jupyter.pdf)]
- [Issues](https://github.com/jupyter/qtconsole/issues)
- [Technical support - Jupyter Google Group](https://groups.google.com/forum/#!forum/jupyter)
