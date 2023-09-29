""" Defines miscellaneous Qt-related helper classes and functions.
"""

import inspect

from qtpy import QtCore, QtGui

from traitlets import HasTraits, TraitType

#-----------------------------------------------------------------------------
# Metaclasses
#-----------------------------------------------------------------------------

MetaHasTraits = type(HasTraits)
MetaQObject = type(QtCore.QObject)

class MetaQObjectHasTraits(MetaQObject, MetaHasTraits):
    """ A metaclass that inherits from the metaclasses of HasTraits and QObject.

    Using this metaclass allows a class to inherit from both HasTraits and
    QObject. Using SuperQObject instead of QObject is highly recommended. See
    QtKernelManager for an example.
    """
    def __new__(mcls, name, bases, classdict):
        # FIXME: this duplicates the code from MetaHasTraits.
        # I don't think a super() call will help me here.
        for k,v in iter(classdict.items()):
            if isinstance(v, TraitType):
                v.name = k
            elif inspect.isclass(v):
                if issubclass(v, TraitType):
                    vinst = v()
                    vinst.name = k
                    classdict[k] = vinst
        cls = MetaQObject.__new__(mcls, name, bases, classdict)
        return cls

    def __init__(mcls, name, bases, classdict):
        # Note: super() did not work, so we explicitly call these.
        MetaQObject.__init__(mcls, name, bases, classdict)
        MetaHasTraits.__init__(mcls, name, bases, classdict)

#-----------------------------------------------------------------------------
# Classes
#-----------------------------------------------------------------------------

def superQ(QClass):
    """ Permits the use of super() in class hierarchies that contain Qt classes.

    Unlike QObject, SuperQObject does not accept a QObject parent. If it did,
    super could not be emulated properly (all other classes in the heierarchy
    would have to accept the parent argument--they don't, of course, because
    they don't inherit QObject.)

    This class is primarily useful for attaching signals to existing non-Qt
    classes. See QtKernelManagerMixin for an example.
    """
    class SuperQClass(QClass):

        def __new__(cls, *args, **kw):
            # We initialize QClass as early as possible. Without this, Qt complains
            # if SuperQClass is not the first class in the super class list.
            inst = QClass.__new__(cls)
            QClass.__init__(inst)
            return inst

        def __init__(self, *args, **kw):
            # Emulate super by calling the next method in the MRO, if there is one.
            mro = self.__class__.mro()
            for qt_class in QClass.mro():
                mro.remove(qt_class)
            next_index = mro.index(SuperQClass) + 1
            if next_index < len(mro):
                mro[next_index].__init__(self, *args, **kw)

    return SuperQClass

SuperQObject = superQ(QtCore.QObject)

#-----------------------------------------------------------------------------
# Functions
#-----------------------------------------------------------------------------

def get_font(family, fallback=None):
    """Return a font of the requested family, using fallback as alternative.

    If a fallback is provided, it is used in case the requested family isn't
    found.  If no fallback is given, no alternative is chosen and Qt's internal
    algorithms may automatically choose a fallback font.

    Parameters
    ----------
    family : str
      A font name.
    fallback : str
      A font name.

    Returns
    -------
    font : QFont object
    """
    font = QtGui.QFont(family)
    # Check whether we got what we wanted using QFontInfo, since exactMatch()
    # is overly strict and returns false in too many cases.
    font_info = QtGui.QFontInfo(font)
    if fallback is not None and font_info.family() != family:
        font = QtGui.QFont(fallback)
    return font


# -----------------------------------------------------------------------------
# Vendored from ipython_genutils
# -----------------------------------------------------------------------------
def _col_chunks(l, max_rows, row_first=False):
    """Yield successive max_rows-sized column chunks from l."""
    if row_first:
        ncols = (len(l) // max_rows) + (len(l) % max_rows > 0)
        for i in range(ncols):
            yield [l[j] for j in range(i, len(l), ncols)]
    else:
        for i in range(0, len(l), max_rows):
            yield l[i : (i + max_rows)]


def _find_optimal(rlist, row_first=False, separator_size=2, displaywidth=80):
    """Calculate optimal info to columnize a list of string"""
    for max_rows in range(1, len(rlist) + 1):
        col_widths = list(map(max, _col_chunks(rlist, max_rows, row_first)))
        sumlength = sum(col_widths)
        ncols = len(col_widths)
        if sumlength + separator_size * (ncols - 1) <= displaywidth:
            break
    return {
        "num_columns": ncols,
        "optimal_separator_width": (displaywidth - sumlength) // (ncols - 1)
        if (ncols - 1)
        else 0,
        "max_rows": max_rows,
        "column_widths": col_widths,
    }


def _get_or_default(mylist, i, default=None):
    """return list item number, or default if don't exist"""
    if i >= len(mylist):
        return default
    else:
        return mylist[i]


def compute_item_matrix(items, row_first=False, empty=None, *args, **kwargs):
    """Returns a nested list, and info to columnize items

    Parameters
    ----------
    items
        list of strings to columize
    row_first : (default False)
        Whether to compute columns for a row-first matrix instead of
        column-first (default).
    empty : (default None)
        default value to fill list if needed
    separator_size : int (default=2)
        How much characters will be used as a separation between each columns.
    displaywidth : int (default=80)
        The width of the area onto which the columns should enter

    Returns
    -------
    strings_matrix
        nested list of string, the outer most list contains as many list as
        rows, the innermost lists have each as many element as columns. If the
        total number of elements in `items` does not equal the product of
        rows*columns, the last element of some lists are filled with `None`.
    dict_info
        some info to make columnize easier:

        num_columns
          number of columns
        max_rows
          maximum number of rows (final number may be less)
        column_widths
          list of with of each columns
        optimal_separator_width
          best separator width between columns

    Examples
    --------
    ::

        In [1]: l = ['aaa','b','cc','d','eeeee','f','g','h','i','j','k','l']
        In [2]: list, info = compute_item_matrix(l, displaywidth=12)
        In [3]: list
        Out[3]: [['aaa', 'f', 'k'], ['b', 'g', 'l'], ['cc', 'h', None], ['d', 'i', None], ['eeeee', 'j', None]]
        In [4]: ideal = {'num_columns': 3, 'column_widths': [5, 1, 1], 'optimal_separator_width': 2, 'max_rows': 5}
        In [5]: all((info[k] == ideal[k] for k in ideal.keys()))
        Out[5]: True
    """
    info = _find_optimal(list(map(len, items)), row_first, *args, **kwargs)
    nrow, ncol = info["max_rows"], info["num_columns"]
    if row_first:
        return (
            [
                [
                    _get_or_default(items, r * ncol + c, default=empty)
                    for c in range(ncol)
                ]
                for r in range(nrow)
            ],
            info,
        )
    else:
        return (
            [
                [
                    _get_or_default(items, c * nrow + r, default=empty)
                    for c in range(ncol)
                ]
                for r in range(nrow)
            ],
            info,
        )


def columnize(items, row_first=False, separator="  ", displaywidth=80, spread=False):
    """Transform a list of strings into a single string with columns.

    Parameters
    ----------
    items : sequence of strings
        The strings to process.
    row_first : (default False)
        Whether to compute columns for a row-first matrix instead of
        column-first (default).
    separator : str, optional [default is two spaces]
        The string that separates columns.
    displaywidth : int, optional [default is 80]
        Width of the display in number of characters.

    Returns
    -------
    The formatted string.
    """
    if not items:
        return "\n"
    matrix, info = compute_item_matrix(
        items,
        row_first=row_first,
        separator_size=len(separator),
        displaywidth=displaywidth,
    )
    if spread:
        separator = separator.ljust(int(info["optimal_separator_width"]))
    fmatrix = [filter(None, x) for x in matrix]
    sjoin = lambda x: separator.join(
        [y.ljust(w, " ") for y, w in zip(x, info["column_widths"])]
    )
    return "\n".join(map(sjoin, fmatrix)) + "\n"


def get_text_list(list_, last_sep=" and ", sep=", ", wrap_item_with=""):
    """
    Return a string with a natural enumeration of items

    >>> get_text_list(['a', 'b', 'c', 'd'])
    'a, b, c and d'
    >>> get_text_list(['a', 'b', 'c'], ' or ')
    'a, b or c'
    >>> get_text_list(['a', 'b', 'c'], ', ')
    'a, b, c'
    >>> get_text_list(['a', 'b'], ' or ')
    'a or b'
    >>> get_text_list(['a'])
    'a'
    >>> get_text_list([])
    ''
    >>> get_text_list(['a', 'b'], wrap_item_with="`")
    '`a` and `b`'
    >>> get_text_list(['a', 'b', 'c', 'd'], " = ", sep=" + ")
    'a + b + c = d'
    """
    if len(list_) == 0:
        return ""
    if wrap_item_with:
        list_ = ["%s%s%s" % (wrap_item_with, item, wrap_item_with) for item in list_]
    if len(list_) == 1:
        return list_[0]
    return "%s%s%s" % (sep.join(i for i in list_[:-1]), last_sep, list_[-1])


def import_item(name):
    """Import and return ``bar`` given the string ``foo.bar``.

    Calling ``bar = import_item("foo.bar")`` is the functional equivalent of
    executing the code ``from foo import bar``.

    Parameters
    ----------
    name : string
      The fully qualified name of the module/package being imported.

    Returns
    -------
    mod : module object
       The module that was imported.
    """

    parts = name.rsplit(".", 1)
    if len(parts) == 2:
        # called with 'foo.bar....'
        package, obj = parts
        module = __import__(package, fromlist=[obj])
        try:
            pak = getattr(module, obj)
        except AttributeError:
            raise ImportError("No module named %s" % obj)
        return pak
    else:
        # called with un-dotted string
        return __import__(parts[0])
