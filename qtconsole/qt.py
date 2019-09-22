""" A Qt API selector that can be used to switch between PyQt4/5 and PySide.

Fall back on qtpy's selector.
"""
from qtpy import QtCore, QtGui, QtSvg, QT_API, QtWidgets
