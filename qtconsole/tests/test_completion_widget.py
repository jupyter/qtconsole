# -*- coding: utf-8 -*-
import unittest

from qtconsole.qt import QtCore, QtGui

from qtconsole.console_widget import ConsoleWidget
from qtconsole.completion_widget import CompletionWidget
import ipython_genutils.testing.decorators as dec

setup = dec.skip_file_no_x11(__name__)


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
        noModifiers = QtCore.Qt.KeyboardModifiers(0)
        w = CompletionWidget(self.console)
        w.show_items(self.text_edit.textCursor(), ["item1", "item2", "item3"])
        downEvent = QtGui.QKeyEvent(QtCore.QEvent.KeyPress,
                                    QtCore.Qt.Key_PageDown, noModifiers)
        self._app.sendEvent(self.text_edit, downEvent)
        enterEvent = QtGui.QKeyEvent(QtCore.QEvent.KeyPress,
                                     QtCore.Qt.Key_Enter, noModifiers)
        self._app.sendEvent(self.text_edit, enterEvent)
        self.assertEqual(self.text_edit.toPlainText(), "item3")
