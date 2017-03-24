.. _changelog:

Changes in Jupyter Qt console
=============================

.. _4.3:

4.3
---

`4.3 on GitHub <https://github.com/jupyter/qtconsole/milestones/4.3>`__

- Rename `ConsoleWidget.width/height` traits to `console_width/console_height`
  to avoid a name clash with the `QWidget` properties. Note: the name change
  could be, in rare cases if a name collision exists, a code-breaking
  change.
- Add Shift+Tab shortcut to unindent text
- Add Ctrl+R shortcut to rename the current tab
- Add Alt+R shortcut to set the main window title
- Add Cmd+Alt+Left/Right shortcut to switch tabs on OSX
- Change Tab key behavior to always indent to the next increment of 4 spaces
- Change Home key behavior to alternate cursor between the beginning of text (ignoring leading spaces) and beginning of the line
- Add option to create new tab connected to the existing kernel
- Add support for PySide2
- Add support for Python 3.5
- Add support for 24bit ANSI color codes
- Improve documentation of various options and carified the docs in some places
- Move documentation to readthedocs
- Fix automatic indentation of new lines that are inserted in the middle of a cell
- Fix regression where prompt would never be shown for --existing consoles
- Fix "python.exe -m qtconsole" on windows
- Fix showing error messages when running a script using %run
- Fix "invalid cursor position" error and subsequent freezing of user input
- Fix syntax coloring when attaching to non-ipython kernels
- Fix printing when using QT5
- Fix Ctrl+K shortcut (delete until end of line) on OSX
- Fix history browsing (Up/Down keys) when lines are longer than the terminal width
- Fix saving HTML with inline PNG for Python 3 
- Various internal bugfixes 

.. _4.2:

4.2
---

`4.2 on GitHub <https://github.com/jupyter/qtconsole/milestones/4.2>`__

- various latex display fixes
- improvements for embedding in Qt applications (use existing Qt API if one is already loaded)


.. _4.1:

4.1
---

.. _4.1.1:

4.1.1
-----

`4.1.1 on GitHub <https://github.com/jupyter/qtconsole/milestones/4.1.1>`__

- Set AppUserModelID for taskbar icon on Windows 7 and later

.. _4.1.0:

4.1.0
~~~~~

`4.1 on GitHub <https://github.com/jupyter/qtconsole/milestones/4.1>`__

-  fix regressions in copy/paste, completion
-  fix issues with inprocess IPython kernel
-  fix ``jupyter qtconsole --generate-config``

.. _4.0:

4.0
---

.. _4.0.1:

4.0.1
~~~~~

-  fix installation issues, including setuptools entrypoints for Windows
-  Qt5 fixes

.. _4.0.0:

4.0.0
~~~~~

`4.0 on GitHub <https://github.com/jupyter/qtconsole/milestones/4.0>`__

First release of the Qt console as a standalone package.
