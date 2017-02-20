import unittest

from qtconsole.qt import QtCore, QtGui
from qtconsole.qt_loaders import load_qtest

from qtconsole.console_widget import ConsoleWidget
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

    def test_special_characters(self):
        """ Are special characters displayed correctly?
        """
        w = ConsoleWidget()
        cursor = w._get_prompt_cursor()

        test_inputs = ['xyz\b\b=\n', 'foo\b\nbar\n', 'foo\b\nbar\r\n', 'abc\rxyz\b\b=']
        expected_outputs = [u'x=z\u2029', u'foo\u2029bar\u2029', u'foo\u2029bar\u2029', 'x=z']
        for i, text in enumerate(test_inputs):
            w._insert_plain_text(cursor, text)
            cursor.select(cursor.Document)
            selection = cursor.selectedText()
            self.assertEqual(expected_outputs[i], selection)
            # clear all the text
            cursor.insertText('')

    def test_link_handling(self):
        noKeys = QtCore.Qt
        noButton = QtCore.Qt.MouseButton(0)
        noButtons = QtCore.Qt.MouseButtons(0)
        noModifiers = QtCore.Qt.KeyboardModifiers(0)
        MouseMove = QtCore.QEvent.MouseMove
        QMouseEvent = QtGui.QMouseEvent
        
        w = ConsoleWidget()
        cursor = w._get_prompt_cursor()
        w._insert_html(cursor, '<a href="http://python.org">written in</a>')
        obj = w._control
        tip = QtGui.QToolTip
        self.assertEqual(tip.text(), u'')
        
        # should be somewhere else
        elsewhereEvent = QMouseEvent(MouseMove, QtCore.QPoint(50,50),
                                     noButton, noButtons, noModifiers)
        w.eventFilter(obj, elsewhereEvent)
        self.assertEqual(tip.isVisible(), False)
        self.assertEqual(tip.text(), u'')
        
        #self.assertEqual(tip.text(), u'')
        # should be over text
        overTextEvent = QMouseEvent(MouseMove, QtCore.QPoint(1,5),
                                    noButton, noButtons, noModifiers)
        w.eventFilter(obj, overTextEvent)
        self.assertEqual(tip.isVisible(), True)
        self.assertEqual(tip.text(), "http://python.org")
        
        # should still be over text
        stillOverTextEvent = QMouseEvent(MouseMove, QtCore.QPoint(1,5),
                                         noButton, noButtons, noModifiers)
        w.eventFilter(obj, stillOverTextEvent)
        self.assertEqual(tip.isVisible(), True)
        self.assertEqual(tip.text(), "http://python.org")

    def test_width_height(self):
        # width()/height() QWidget properties should not be overridden.
        w = ConsoleWidget()
        self.assertEqual(w.width(), QtGui.QWidget.width(w))
        self.assertEqual(w.height(), QtGui.QWidget.height(w))

    def test_prompt_cursors(self):
        """Test the cursors that keep track of where the prompt begins and
        ends"""
        w = ConsoleWidget()
        w._prompt = 'prompt>'
        doc = w._control.document()

        # Fill up the QTextEdit area with the maximum number of blocks
        doc.setMaximumBlockCount(10)
        for _ in range(9):
            w._append_plain_text('line\n')

        # Draw the prompt, this should cause the first lines to be deleted
        w._show_prompt()
        self.assertEqual(doc.blockCount(), 10)

        # _prompt_pos should be at the end of the document
        self.assertEqual(w._prompt_pos, w._get_end_pos())

        # _append_before_prompt_pos should be at the beginning of the prompt
        self.assertEqual(w._append_before_prompt_pos,
                         w._prompt_pos - len(w._prompt))

        # insert some more text without drawing a new prompt
        w._append_plain_text('line\n')
        self.assertEqual(w._prompt_pos,
                         w._get_end_pos() - len('line\n'))
        self.assertEqual(w._append_before_prompt_pos,
                         w._prompt_pos - len(w._prompt))

        # redraw the prompt
        w._show_prompt()
        self.assertEqual(w._prompt_pos, w._get_end_pos())
        self.assertEqual(w._append_before_prompt_pos,
                         w._prompt_pos - len(w._prompt))

        # insert some text before the prompt
        w._append_plain_text('line', before_prompt=True)
        self.assertEqual(w._prompt_pos, w._get_end_pos())
        self.assertEqual(w._append_before_prompt_pos,
                         w._prompt_pos - len(w._prompt))

    def test_keypresses(self):
        """Test the event handling code for keypresses."""
        w = ConsoleWidget()
        w._append_plain_text('Header\n')
        w._prompt = 'prompt>'
        w._show_prompt()
        control = w._control

        # Test setting the input buffer
        w._set_input_buffer('test input')
        self.assertEqual(w._get_input_buffer(), 'test input')

        # Ctrl+K kills input until EOL
        w._set_input_buffer('test input')
        c = control.textCursor()
        c.setPosition(c.position() - 3)
        control.setTextCursor(c)
        QTest.keyClick(control, QtCore.Qt.Key_K, QtCore.Qt.ControlModifier)
        self.assertEqual(w._get_input_buffer(), 'test in')

        # Ctrl+V pastes
        w._set_input_buffer('test input ')
        QtGui.qApp.clipboard().setText('pasted text')
        QTest.keyClick(control, QtCore.Qt.Key_V, QtCore.Qt.ControlModifier)
        self.assertEqual(w._get_input_buffer(), 'test input pasted text')
        self.assertEqual(control.document().blockCount(), 2)

        # Paste should strip indentation
        w._set_input_buffer('test input ')
        QtGui.qApp.clipboard().setText('    pasted text')
        QTest.keyClick(control, QtCore.Qt.Key_V, QtCore.Qt.ControlModifier)
        self.assertEqual(w._get_input_buffer(), 'test input pasted text')
        self.assertEqual(control.document().blockCount(), 2)

        # Multiline paste, should also show continuation marks
        w._set_input_buffer('test input ')
        QtGui.qApp.clipboard().setText('line1\nline2\nline3')
        QTest.keyClick(control, QtCore.Qt.Key_V, QtCore.Qt.ControlModifier)
        self.assertEqual(w._get_input_buffer(), 'test input line1\nline2\nline3')
        self.assertEqual(control.document().blockCount(), 4)
        self.assertEqual(control.document().findBlockByNumber(1).text(), 'prompt>test input line1')
        self.assertEqual(control.document().findBlockByNumber(2).text(), '> line2')
        self.assertEqual(control.document().findBlockByNumber(3).text(), '> line3')

        # TODO: many more keybindings
        
