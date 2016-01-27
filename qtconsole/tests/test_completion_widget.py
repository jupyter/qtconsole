# -*- coding: utf-8 -*-
import unittest

from qtconsole.qt import QtCore, QtGui

from qtconsole.qt_loaders import (loaded_api, QT_API_PYQT, QT_API_PYQT5,
QT_API_PYQTv1, QT_API_PYQT_DEFAULT, QT_API_PYSIDE)

from qtconsole.console_widget import ConsoleWidget
from qtconsole.completion_widget import CompletionWidget
import ipython_genutils.testing.decorators as dec

api = loaded_api()
if api in (QT_API_PYQT, QT_API_PYQTv1, QT_API_PYQT_DEFAULT):
    from PyQt4.QtTest import QTest
elif api == QT_API_PYQT5:
    from PyQt5.QtTest import QTest
elif api == QT_API_PYSIDE:
    from PySide.QtTest import QTest


class TestCompletionWidget(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """ Create the application for the test case.
        """
        cls._app = QtGui.QApplication.instance()
        if cls._app is None:
            cls._app = QtGui.QApplication([])
        cls._app.setQuitOnLastWindowClosed(False)

    @classmethod
    def tearDownClass(cls):
        """ Exit the application.
        """
        QtGui.QApplication.quit()

    def setUp(self):
        """ Create the main widgets (ConsoleWidget)
        """
        self.console = ConsoleWidget()
        self.text_edit = self.console._control

    def test_html_completer_shows(self):
        w = CompletionWidget(self.console)
        w.show_items(self.text_edit.textCursor(), ["item1", "item2", "item3"])
        self.assertTrue(w.isVisible())

    def test_html_completer_keyboard(self):
        w = CompletionWidget(self.console)
        w.show_items(self.text_edit.textCursor(), ["item1", "item2", "item3"])
        QTest.keyClick(self.text_edit, QtCore.Qt.Key_PageDown)
        QTest.keyClick(self.text_edit, QtCore.Qt.Key_Enter)
        self.assertEqual(self.text_edit.toPlainText(), "item3")

    def test_html_completer_mousepick(self):
        leftButton = QtCore.Qt.LeftButton

        w = CompletionWidget(self.console)
        w.show_items(self.text_edit.textCursor(), ["item1", "item2", "item3"])

        QTest.mouseClick(w.viewport(), leftButton, pos=QtCore.QPoint(19, 8))
        QTest.mouseRelease(w.viewport(), leftButton, pos=QtCore.QPoint(19, 8))
        QTest.mouseDClick(w.viewport(), leftButton, pos=QtCore.QPoint(19, 8))

        self.assertEqual(self.text_edit.toPlainText(), "item1")
        self.assertFalse(w.isVisible())
