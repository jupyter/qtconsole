# Jupyter Qt Console

A rich Qt-based console for working with Jupyter kernels,
supporting rich media output, session export, and more.

To install:

    pip install qtconsole

And run:

    jupyter qtconsole

The qtconsole requires [PyQt][] or [PySide][],
which cannot be installed with pip.
These can be installed with [conda][]:

    conda install pyqt

or your system package manager, e.g.

    apt-get install python3-pyqt5


[PyQt]: http://www.riverbankcomputing.com/software/pyqt/intro
[PySide]: http://pyside.github.io/docs/pyside
[conda]: http://conda.pydata.org/docs
