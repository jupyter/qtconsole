"""
Usage information for QtConsole
"""

# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.


def page_guiref(arg_s=None):
    """Show a basic reference about QtConsole."""
    from IPython.core import page
    page.page(gui_reference)


gui_reference = """\
=====================
The Jupyter QtConsole
=====================

This console is designed to emulate the look, feel and workflow of a terminal
environment, while adding a number of enhancements that are simply not possible
in a real terminal, such as inline syntax highlighting, true multiline editing,
inline graphics and much more.

This quick reference document contains the basic information you'll need to
know to make the most efficient use of it.  For the various command line
options available at startup, type ``jupyter qtconsole --help`` at the command
line.


Multiline editing
=================

The graphical console is capable of true multiline editing, but it also tries
to behave intuitively like a terminal when possible.  If you are used to
IPython's old terminal behavior, you should find the transition painless, and
once you learn a few basic keybindings it will be a much more efficient
environment.

For single expressions or indented blocks, the console behaves almost like the
terminal IPython: single expressions are immediately evaluated, and indented
blocks are evaluated once a single blank line is entered::

    In [1]: print "Hello Jupyter!"  # Enter was pressed at the end of the line
    Hello Jupyter!

    In [2]: for i in range(10):
       ...:     print i,
       ...:
    0 1 2 3 4 5 6 7 8 9

If you want to enter more than one expression in a single input block
(something not possible in the terminal), you can use ``Control-Enter`` at the
end of your first line instead of ``Enter``.  At that point the console goes
into 'cell mode' and even if your inputs are not indented, it will continue
accepting arbitrarily many lines until either you enter an extra blank line or
you hit ``Shift-Enter`` (the key binding that forces execution).  When a
multiline cell is entered, the console analyzes it and executes its code producing
an ``Out[n]`` prompt only for the last expression in it, while the rest of the
cell is executed as if it was a script.  An example should clarify this::

    In [3]: x=1  # Hit C-Enter here
       ...: y=2  # from now on, regular Enter is sufficient
       ...: z=3
       ...: x**2  # This does *not* produce an Out[] value
       ...: x+y+z  # Only the last expression does
       ...:
    Out[3]: 6

The behavior where an extra blank line forces execution is only active if you
are actually typing at the keyboard each line, and is meant to make it mimic
the IPython terminal behavior.  If you paste a long chunk of input (for example
a long script copied form an editor or web browser), it can contain arbitrarily
many intermediate blank lines and they won't cause any problems.  As always,
you can then make it execute by appending a blank line *at the end* or hitting
``Shift-Enter`` anywhere within the cell.

With the up arrow key, you can retrieve previous blocks of input that contain
multiple lines.  You can move inside of a multiline cell like you would in any
text editor.  When you want it executed, the simplest thing to do is to hit the
force execution key, ``Shift-Enter`` (though you can also navigate to the end
and append a blank line by using ``Enter`` twice).

If you've edited a multiline cell and accidentally navigate out of it with the
up or down arrow keys, the console will clear the cell and replace it with the
contents of the one above or below that you navigated to.  If this was an
accident and you want to retrieve the cell you were editing, use the Undo
keybinding, ``Control-z``.


Key bindings
============

The Jupyter QtConsole supports most of the basic Emacs line-oriented keybindings,
in addition to some of its own.

The keybinding prefixes mean:

- ``C``: Control
- ``S``: Shift
- ``M``: Meta (typically the Alt key)

The keybindings themselves are:

- ``Enter``: insert new line (may cause execution, see above).
- ``C-Enter``: *force* new line, *never* causes execution.
- ``S-Enter``: *force* execution regardless of where cursor is, no newline added.
- ``Up``: step backwards through the history.
- ``Down``: step forwards through the history.
- ``S-Up``: search backwards through the history (like ``C-r`` in bash).
- ``S-Down``: search forwards through the history.
- ``C-c``: copy highlighted text to clipboard (prompts are automatically stripped).
- ``C-S-c``: copy highlighted text to clipboard (prompts are not stripped).
- ``C-v``: paste text from clipboard.
- ``C-z``: undo (retrieves lost text if you move out of a cell with the arrows).
- ``C-S-z``: redo.
- ``C-o``: move to 'other' area, between pager and terminal.
- ``C-l``: clear terminal.
- ``C-a``: go to beginning of line.
- ``C-e``: go to end of line.
- ``C-u``: kill from cursor to the begining of the line.
- ``C-k``: kill from cursor to the end of the line.
- ``C-y``: yank (paste)
- ``C-p``: previous line (like up arrow)
- ``C-n``: next line (like down arrow)
- ``C-f``: forward (like right arrow)
- ``C-b``: back (like left arrow)
- ``C-d``: delete next character, or exits if input is empty
- ``M-<``: move to the beginning of the input region.
- ``M->``: move to the end of the input region.
- ``M-d``: delete next word.
- ``M-Backspace``: delete previous word.
- ``C-.``: force a kernel restart (a confirmation dialog appears).
- ``C-+``: increase font size.
- ``C--``: decrease font size.
- ``C-M-Space``: toggle full screen. (Command-Control-Space on Mac OS X)

The pager
=========

The Jupyter QtConsole will show long blocks of text from many sources using a
builtin pager. You can control where this pager appears with the ``--paging``
command-line flag:

- ``inside`` [default]: the pager is overlaid on top of the main terminal. You
  must quit the pager to get back to the terminal (similar to how a pager such
  as ``less`` or ``more`` works).

- ``vsplit``: the console is made double-tall, and the pager appears on the
  bottom area when needed.  You can view its contents while using the terminal.

- ``hsplit``: the console is made double-wide, and the pager appears on the
  right area when needed.  You can view its contents while using the terminal.

- ``none``: the console never pages output.

If you use the vertical or horizontal paging modes, you can navigate between
terminal and pager as follows:

- Tab key: goes from pager to terminal (but not the other way around).
- Control-o: goes from one to another always.
- Mouse: click on either.

In all cases, the ``q`` or ``Escape`` keys quit the pager (when used with the
focus on the pager area).

Running subprocesses
====================

The Jupyter QtConsole uses the ``pexpect`` module to run subprocesses
when you type ``!command``.  This has a number of advantages (true asynchronous
output from subprocesses as well as very robust termination of rogue
subprocesses with ``Control-C``), as well as some limitations.  The main
limitation is that you can *not* interact back with the subprocess, so anything
that invokes a pager or expects you to type input into it will block and hang
(you can kill it with ``Control-C``).

We have provided as magics ``%less`` to page files (aliased to ``%more``),
``%clear`` to clear the terminal, and ``%man`` on Linux/OSX.  These cover the
most common commands you'd want to call in your subshell and that would cause
problems if invoked via ``!cmd``, but you need to be aware of this limitation.

Display
=======

The Jupyter QtConsole can now display objects in a variety of formats, including
PNG and SVG. This is accomplished using the display functions in
``IPython.display``::

    In [4]: from IPython.display import display

    In [5]: from IPython.display import display_png, display_svg

Python objects can simply be passed to these functions and the appropriate
representations will be displayed in the console as long as the objects know
how to compute those representations. The easiest way of teaching objects how
to format themselves in various representations is to define special methods
such as: ``_repr_svg_`` and ``_repr_png_``. IPython's display formatters
can also be given custom formatter functions for various types::

    In [6]: ip = get_ipython()

    In [7]: png_formatter = ip.display_formatter.formatters['image/png']

    In [8]: png_formatter.for_type(Foo, foo_to_png)

For further details, see ``IPython.core.formatters``.

Inline matplotlib graphics
==========================

The Jupyter QtConsole is capable of displaying matplotlib figures inline, in SVG
or PNG format.  If started with the ``matplotlib=inline``, then all figures are
rendered inline automatically (PNG by default).  If started with ``--matplotlib``
or ``matplotlib=<your backend>``, then a GUI backend will be used, but IPython's
``display()`` and ``getfigs()`` functions can be used to view plots inline::

    In [9]: display(*getfigs())    # display all figures inline

    In[10]: display(*getfigs(1,2)) # display figures 1 and 2 inline
"""
