""" Provides bracket matching for Q[Plain]TextEdit widgets.
"""

import re

# System library imports
from qtconsole.qt import QtCore, QtGui

FORMAT_BRACKET_MATCHED = 0
FORMAT_BRACKET_UNMATCHED = 1

def _mask_text(x, regex=None):
    """ Tokenize string, "blanking" all quoted str chars, except brackets.

        Tokens are one of:
        - an opening or closing bracket.
        - a blank string of varying length. The length equals the text
          substituted for, including the quotes if the token substitutes
          for a quoted string.
    """
    if not regex:
        regex = "('|\\\\?\"|[(){}\[\]])"
    fields = re.split(regex, x)
    i = 0
    while i < len(fields):
        if fields[i] in ("'", '"'):
            whole_s = " "*len(fields[i])
            for j in range(i+1, len(fields)):
                whole_s += " "*len(fields[j])
                if fields[j] == fields[i]:
                    fields = fields[:i+1]+fields[j+1:]
                    break
                fields[j] = ""
            fields[i] = whole_s
        elif fields[i] not in "()[]{}":
            fields[i] = " "*len(fields[i])
        i += 1
    return fields


def _locate_parens(x, opening_map, closing_map):
    def _to_offieldset(fields, i):
        return len("".join(fields[:i]))

    # To be correct, we should actually pass in regex built
    # from opening/closing_map.
    fields = _mask_text(x)

    stack = []
    pairs = []
    orphans = []
    for i, f in enumerate(fields):
        if f in opening_map:
            stack.append((i, f))
        if f in closing_map:
            if stack:
                prev_i, prev_f = stack[-1]
                if closing_map[f] == prev_f:
                    pairs.append((prev_i, i))
                    fields[prev_i] = fields[i] = "%d" % len(stack)
                    stack = stack[:-1]
                else:
                    # mismatch to top of stack, i.e. "...[ }"
                    orphans.append(i)
            else:
                # bare mismatch,  i.e. "    }"
                orphans.append(i)

    for i, f in stack:
        orphans.append(i)
    orphan_pos = []
    for i, f_index in enumerate(orphans):
        orphan_pos.append(_to_offieldset(fields, f_index))

    pairs_pos = [(_to_offieldset(fields, i), _to_offieldset(fields, j))
                 for i, j in pairs]
    return (pairs_pos, orphan_pos)


class BracketMatcher(QtCore.QObject):
    """ Matches square brackets, braces, and parentheses based on cursor
        position.
    """

    # Protected class variables.
    _opening_map = {'(': ')', '{': '}', '[': ']'}
    _closing_map = {')': '(', '}': '{', ']': '['}

    #--------------------------------------------------------------------------
    # 'QObject' interface
    #--------------------------------------------------------------------------

    def __init__(self, console):
        """ Create a call tip manager that is attached to the specified Qt
            text edit widget.
        """
        assert hasattr(console, '_control')
        assert isinstance(console._control,
                          (QtGui.QTextEdit, QtGui.QPlainTextEdit))
        super(BracketMatcher, self).__init__()

        # The formats to apply to brackets when un/matched.
        self.formats = {_: QtGui.QTextCharFormat() for _
                        in [FORMAT_BRACKET_MATCHED, FORMAT_BRACKET_UNMATCHED]}
        self.formats[FORMAT_BRACKET_MATCHED].setBackground(QtGui.QColor('silver'))
        self.formats[FORMAT_BRACKET_UNMATCHED].setBackground(QtGui.QColor('red'))

        # for back-compatability with spyder
        self.format = self.formats[FORMAT_BRACKET_MATCHED]

        self._console = console
        self._text_edit = console._control
        self._text_edit.cursorPositionChanged.connect(
            self._cursor_position_changed)

    #--------------------------------------------------------------------------
    # Protected interface
    #--------------------------------------------------------------------------
    def _selection_for_character(self, position, format=FORMAT_BRACKET_MATCHED):
        """ Convenience method for selecting a character.
        """
        selection = QtGui.QTextEdit.ExtraSelection()
        cursor = self._text_edit.textCursor()
        cursor.setPosition(position)
        cursor.movePosition(QtGui.QTextCursor.NextCharacter,
                            QtGui.QTextCursor.KeepAnchor)
        selection.format = self.formats[format]
        selection.cursor = cursor
        return selection

    #------ Signal handlers --------------------------------------------------
    def _cursor_position_changed(self):
        """ Updates the document formatting based on the new cursor position.
        """
        # To clear out the old formatting.

        extra_selections = []
        # inspect current cell, and identify all matched/unmatches for brackets
        base_offset = self._console._prompt_pos
        code = self._text_edit.toPlainText()[base_offset:]

        matched_pairs, unmatched = _locate_parens(code,
                                                  self._opening_map,
                                                  self._closing_map)

        # Create formatted selections for all unmatched brackets
        cursor = self._text_edit.textCursor()
        for rel_pos in unmatched:
            pos = base_offset + rel_pos
            cursor.clearSelection()
            sel = self._selection_for_character(pos, FORMAT_BRACKET_UNMATCHED)
            extra_selections.append(sel)

        # Create formatted selection for matched pair
        # iff the cursor is located right after one
        cursor = self._text_edit.textCursor()
        if not cursor.hasSelection():
            for open_pos, close_pos in matched_pairs:
                open_pos += base_offset
                close_pos += base_offset
                if cursor.position() - 1 in (open_pos, close_pos):
                    cursor.clearSelection()
                    for pos in (open_pos, close_pos):
                        sel = self._selection_for_character(
                            pos, FORMAT_BRACKET_MATCHED)
                        extra_selections.append(sel)

        self._text_edit.setExtraSelections(extra_selections)
