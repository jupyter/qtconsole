#!/usr/bin/env python

import os.path
from qtconsole.qtconsoleapp import JupyterQtConsoleApp

header = """\
Configuration options
=====================

These options can be set in ``~/.jupyter/jupyter_qtconsole_config.py``, or
at the command line when you start it.
"""

destination = os.path.join(os.path.dirname(__file__), 'source/config_options.rst')

def main():
    with open(destination, 'w') as f:
        f.write(header)
        f.write(JupyterQtConsoleApp().document_config_options())

if __name__ == '__main__':
    main()
