import mock
import unittest

from qtconsole.qt import QtGui
from qtconsole.qt_loaders import load_qtest
from qtconsole.frontend_widget import FrontendWidget
from qtconsole.bracket_matcher import FORMAT_BRACKET_MATCHED, FORMAT_BRACKET_UNMATCHED
import ipython_genutils.testing.decorators as dec

setup = dec.skip_file_no_x11(__name__)
QTest = load_qtest()


class TestBracketMatcher(unittest.TestCase):

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

    def test_stub(self):
        """ Test Stub
        """
        w = FrontendWidget(kind='rich')
        w.enable_calltips=False
        control = w._control
        matcher = w._bracket_matcher
        # Base case

    def test_bracket_highlighting(self):
        """ Test Stub
        """

        # NOTE: All the calls we check for take a position
        # argument. this is *seem* off by 1, becuase the
        # input we set does not include the ">" prompt
        w = FrontendWidget(kind='rich')
        w.enable_calltips=False
        w._prompt = ">"
        w._show_prompt()
        control = w._control
        matcher = w._bracket_matcher
        m = mock.Mock()
        matcher._selection_for_character = m
        m.return_value = QtGui.QTextEdit.ExtraSelection()

        # BracketMatcher identifies unmatched brackets #1
        self.assertEqual(m.call_count, 0)
        w._set_input_buffer('[')
        calls = [
            mock.call(1, FORMAT_BRACKET_UNMATCHED)
        ]
        m.assert_has_calls(calls)
        self.assertEqual(m.call_count, len(calls))

        # BracketMatcher identifies multiple unmatched brackets #2
        m.reset_mock()
        w._set_input_buffer('[{(')
        calls = [
            mock.call(1, FORMAT_BRACKET_UNMATCHED),
            mock.call(2, FORMAT_BRACKET_UNMATCHED),
            mock.call(3, FORMAT_BRACKET_UNMATCHED),
        ]
        m.assert_has_calls(calls)
        self.assertEqual(m.call_count, len(calls))

        # BracketMatcher identifies matched brackets
        # if cursor is positioned after one
        m.reset_mock()
        w._set_input_buffer('( )')
        calls = [
            mock.call(1, FORMAT_BRACKET_MATCHED),
            mock.call(3, FORMAT_BRACKET_MATCHED),
        ]
        m.assert_has_calls(calls)
        self.assertEqual(m.call_count, len(calls))

        # BracketMatcher identifies matched brackets
        # only if cursor is positioned after one
        m.reset_mock()
        c = w._get_cursor()
        c.setPosition(3)
        control.setTextCursor(c)
        self.assertEqual(m.call_count, 0)

        # BM deals with mixed matched/unmatched #1
        # matched is highlighted only depending on cursor position
        m.reset_mock()
        w._set_input_buffer('{}[')
        calls = [
            # mock.call(1, FORMAT_BRACKET_MATCHED), # only when cursor adjacent
            # mock.call(2, FORMAT_BRACKET_MATCHED), #
            mock.call(3, FORMAT_BRACKET_UNMATCHED),
        ]
        m.assert_has_calls(calls)
        self.assertEqual(m.call_count, len(calls))

        # BM deals with mixed matched/unmatched #2
        # highlight matched if cursor is adjacent
        m.reset_mock()
        c = w._get_cursor()
        c.setPosition(2)
        control.setTextCursor(c)
        calls = [
            mock.call(3, FORMAT_BRACKET_UNMATCHED),
            mock.call(1, FORMAT_BRACKET_MATCHED),
            mock.call(2, FORMAT_BRACKET_MATCHED),
        ]
        m.assert_has_calls(calls)
        self.assertEqual(m.call_count, len(calls))

        # BM deals with mixed matched/unmatched #3
        # highlight matched if cursor is adjacent
        m.reset_mock()
        c = w._get_cursor()
        c.setPosition(3)
        control.setTextCursor(c)
        calls = [
            mock.call(3, FORMAT_BRACKET_UNMATCHED),
            mock.call(1, FORMAT_BRACKET_MATCHED),
            mock.call(2, FORMAT_BRACKET_MATCHED),
        ]
        m.assert_has_calls(calls)
        self.assertEqual(m.call_count, len(calls))

        # BM is not confused by string contents
        m.reset_mock()
        w._set_input_buffer('(")")')
        calls = [
            mock.call(1, FORMAT_BRACKET_MATCHED),
            mock.call(5, FORMAT_BRACKET_MATCHED),
        ]
        m.assert_has_calls(calls)
        self.assertEqual(m.call_count, len(calls))

        # BM is not confused by string contents
        # nor by escaped quotes
        m.reset_mock()
        w._set_input_buffer('("\\")")')
        calls = [
            mock.call(1, FORMAT_BRACKET_MATCHED),
            mock.call(7, FORMAT_BRACKET_MATCHED),
        ]
        m.assert_has_calls(calls)
        self.assertEqual(m.call_count, len(calls))

        # BM deals with nesting #1
        m.reset_mock()
        w._set_input_buffer('(())')
        m.reset_mock()
        c = w._get_cursor()
        c.setPosition(2)
        control.setTextCursor(c)
        calls = [
            mock.call(1, FORMAT_BRACKET_MATCHED),
            mock.call(4, FORMAT_BRACKET_MATCHED),
        ]
        m.assert_has_calls(calls)
        self.assertEqual(m.call_count, len(calls))

        # BM deals with nesting #2
        m.reset_mock()
        w._set_input_buffer('(())')
        m.reset_mock()
        c = w._get_cursor()
        c.setPosition(3)
        control.setTextCursor(c)
        calls = [
            mock.call(2, FORMAT_BRACKET_MATCHED),
            mock.call(3, FORMAT_BRACKET_MATCHED),
        ]
        m.assert_has_calls(calls)
        self.assertEqual(m.call_count, len(calls))

        # BM deals with nesting #3
        m.reset_mock()
        w._set_input_buffer('(())')
        m.reset_mock()
        c = w._get_cursor()
        c.setPosition(4)
        control.setTextCursor(c)
        calls = [
            mock.call(2, FORMAT_BRACKET_MATCHED),
            mock.call(3, FORMAT_BRACKET_MATCHED),
        ]
        m.assert_has_calls(calls)
        self.assertEqual(m.call_count, len(calls))

        # BM treats everything after an open-quote
        # as text if there's no close quote
        m.reset_mock()
        w._set_input_buffer('("foo)')
        calls = [
            mock.call(1, FORMAT_BRACKET_UNMATCHED),
        ]
        m.assert_has_calls(calls)
        self.assertEqual(m.call_count, len(calls))

        # BM matching highlight works across multiple lines
        m.reset_mock()
        w._set_input_buffer('( 1\n   )')
        calls = [
            mock.call(1, FORMAT_BRACKET_MATCHED),
            mock.call(12, FORMAT_BRACKET_MATCHED),
        ]
        m.assert_has_calls(calls)
        self.assertEqual(m.call_count, len(calls))

        # BM unmatched highlight works across multiple lines
        m.reset_mock()
        w._set_input_buffer('print("",\n [')
        calls = [
            mock.call(6, FORMAT_BRACKET_UNMATCHED),
            mock.call(16, FORMAT_BRACKET_UNMATCHED),
        ]
        m.assert_has_calls(calls)
        self.assertEqual(m.call_count, len(calls))
