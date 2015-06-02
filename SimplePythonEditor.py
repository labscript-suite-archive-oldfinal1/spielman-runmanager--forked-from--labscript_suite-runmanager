# -*- coding: utf-8 -*-
"""
Created on Thu May 14 16:26:29 2015

@author: Ian Spielman
"""

#-------------------------------------------------------------------------
# qsci_simple_pythoneditor.pyw
#
# QScintilla sample with PyQt
#
# Eli Bendersky (eliben@gmail.com)
# This code is in the public domain
#-------------------------------------------------------------------------
import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.Qsci import QsciScintilla, QsciLexerPython


class SimplePythonEditor(QsciScintilla):
    ARROW_MARKER_NUM = 8

    def __init__(self, parent=None):
        super(SimplePythonEditor, self).__init__(parent)

        # Set the default font
        font = QFont()
        font.setFamily('Courier')
        font.setFixedPitch(True)
        font.setPointSize(9.5)
        self.setFont(font)
        self.setMarginsFont(font)

        # Margin 0 is used for line numbers
        fontmetrics = QFontMetrics(font)
        self.setMarginsFont(font)
        self.setMarginWidth(0, fontmetrics.width("0000") + 6)
        self.setMarginLineNumbers(0, True)
        self.setMarginsBackgroundColor(QColor("#cccccc"))

        # Brace matching: enable for a brace immediately before or after
        # the current position
        #
        self.setBraceMatching(QsciScintilla.SloppyBraceMatch)

        # Current line visible with special background color
        self.setCaretLineVisible(True)
        self.setCaretLineBackgroundColor(QColor("#ffe4e4"))

        # Unix end of line chars
        self.setEolMode(self.EolUnix)
        
        # Set Python lexer
        # Set style for Python comments (style number 1) to a fixed-width
        # courier.
        #
        lexer = QsciLexerPython()
        lexer.setDefaultFont(font)
        lexer.setFoldCompact(False) # so folding ends at the end of functions
                                    # not at the start of the next object
        self.setLexer(lexer)
        self.SendScintilla(QsciScintilla.SCI_STYLESETFONT, 1, 'Courier')

        # Set python tabs
        self.setTabIndents(True)
        self.setTabWidth(4)
        self.setIndentationsUseTabs(False)

        #AutoIndentation
        self.setAutoIndent(True)
        self.setIndentationGuides(True)
        self.setIndentationWidth(4)

        # Code folding
        self.setMarginWidth(1, 14)
        self.setFolding(QsciScintilla.BoxedTreeFoldStyle)

        # Edge Mode shows a red vetical bar at 80 chars
        self.setEdgeMode(QsciScintilla.EdgeLine)
        self.setEdgeColumn(80)
        # self.setEdgeColor(QtGui.QColor("#FF0000"))

        # Don't want to see the horizontal scrollbar at all
        # Use raw message to Scintilla here (all messages are documented
        # here: http://www.scintilla.org/ScintillaDoc.html)
        self.SendScintilla(QsciScintilla.SCI_SETHSCROLLBAR, 1)

        # not too small
        self.setMinimumSize(fontmetrics.averageCharWidth()*92, 450)

    # overload set text to convert to current eol chars
    def setText(self, text, *args, **kwargs):
        super(SimplePythonEditor, self).setText(text, *args, **kwargs)
        
        # Convert EOL chars        
        self.convertEols(self.eolMode())
