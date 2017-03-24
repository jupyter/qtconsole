import unittest

from qtconsole.qt import QtGui
from qtconsole.qt_loaders import load_qtest

from qtconsole.jupyter_widget import JupyterWidget
import ipython_genutils.testing.decorators as dec

setup = dec.skip_file_no_x11(__name__)
QTest = load_qtest()

class TestConsoleWidget(unittest.TestCase):

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

    def test_stylesheet_changed(self):
        """ Test changing stylesheets.
        """
        w = JupyterWidget(kind='rich')

        # By default, the background is light. White text is rendered as black
        self.assertEqual(w._ansi_processor.get_color(15).name(), '#000000')

        # Change to a dark colorscheme. White text is rendered as white
        w.syntax_style = 'monokai'
        self.assertEqual(w._ansi_processor.get_color(15).name(), '#ffffff')
