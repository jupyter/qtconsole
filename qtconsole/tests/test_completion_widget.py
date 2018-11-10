# -*- coding: utf-8 -*-
import unittest

import pytest

from qtconsole.qt import QtCore, QtGui
from qtconsole.qt_loaders import load_qtest
from qtconsole.console_widget import ConsoleWidget
from qtconsole.completion_widget import CompletionWidget
from . import no_display


QTest = load_qtest()


@pytest.mark.skipif(no_display, reason="Doesn't work without a display")
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

    def test_droplist_completer_shows(self):
        w = CompletionWidget(self.console)
        w.show_items(self.text_edit.textCursor(), ["item1", "item2", "item3"])
        self.assertTrue(w.isVisible())

    def test_droplist_completer_keyboard(self):
        w = CompletionWidget(self.console)
        w.show_items(self.text_edit.textCursor(), ["item1", "item2", "item3"])
        QTest.keyClick(w, QtCore.Qt.Key_PageDown)
        QTest.keyClick(w, QtCore.Qt.Key_Enter)
        self.assertEqual(self.text_edit.toPlainText(), "item3")

    def test_droplist_completer_mousepick(self):
        leftButton = QtCore.Qt.LeftButton

        w = CompletionWidget(self.console)
        w.show_items(self.text_edit.textCursor(), ["item1", "item2", "item3"])

        QTest.mouseClick(w.viewport(), leftButton, pos=QtCore.QPoint(19, 8))
        QTest.mouseRelease(w.viewport(), leftButton, pos=QtCore.QPoint(19, 8))
        QTest.mouseDClick(w.viewport(), leftButton, pos=QtCore.QPoint(19, 8))

        self.assertEqual(self.text_edit.toPlainText(), "item1")
        self.assertFalse(w.isVisible())
