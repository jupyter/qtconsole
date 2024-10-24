import os
import unittest
import sys

from flaky import flaky
import pytest

from qtpy import QtCore, QtGui, QtWidgets
from qtpy.QtTest import QTest

from qtconsole.console_widget import ConsoleWidget
from qtconsole.qtconsoleapp import JupyterQtConsoleApp

from . import no_display

from IPython.core.inputtransformer2 import TransformerManager


SHELL_TIMEOUT = 20000

@pytest.mark.skipif(no_display, reason="Doesn't work without a display")
class TestTraitletsConfig(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """ Create the application for the test cases.
        """
        cls._app = QtWidgets.QApplication.instance()
        if cls._app is None:
            cls._app = QtWidgets.QApplication([])
        cls._app.setQuitOnLastWindowClosed(False)

    @classmethod
    def tearDownClass(cls):
        """ Exit the application.
        """
        QtWidgets.QApplication.quit()

    def test_custom_shortcut_manager(self):
        """ Verify that the shortcuts traitlets are set with a custom value.
        """
        # Simulate startup with a command-line argument that changes 'shortcut_full_screen'
        test_args = ["test", "--JupyterQtConsoleApp.shortcut_full_screen=F11"]
        sys.argv = test_args

        # Initialize the application with the simulated arguments
        app = JupyterQtConsoleApp()
        app.initialize()

        # Check if the shortcut_full_screen traitlet has the expected value
        self.assertEqual(app.shortcut_full_screen, "F11")

    def test_other_traitlets(self):
        """ Verify that other traitlets are also set correctly.
        """
        # Simulate startup with a command-line argument that changes 'shortcut_full_screen'
        test_args = ["test", "--JupyterQtConsoleApp.shortcut_full_screen=F10"]
        sys.argv = test_args

        app = JupyterQtConsoleApp()
        app.initialize()

        # Check if the shortcut_full_screen traitlet has the expected value
        self.assertEqual(app.shortcut_full_screen, "F10")
