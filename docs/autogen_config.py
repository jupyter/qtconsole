#!/usr/bin/env python

from qtconsole.qtconsoleapp import JupyterQtConsoleApp

header = """\
Configuration options
=====================

These options can be set in ``~/.jupyer/jupyter_qtconsole_config.py``, or
at the command line when you start it.
"""

with open("source/config_options.rst", 'w') as f:
    f.write(header)
    f.write(JupyterQtConsoleApp().document_config_options())
