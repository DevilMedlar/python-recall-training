from __future__ import annotations

from pathlib import Path

from PySide6.QtCore import Signal
from PySide6.QtGui import QColor, QFont, QSyntaxHighlighter, QTextCharFormat
from PySide6.QtWidgets import QPlainTextEdit


class PythonHighlighter(QSyntaxHighlighter):
    KEYWORDS = {
        "False", "None", "True", "and", "as", "assert", "async", "await", "break",
        "class", "continue", "def", "del", "elif", "else", "except", "finally", "for",
        "from", "global", "if", "import", "in", "is", "lambda", "nonlocal", "not", "or",
        "pass", "raise", "return", "try", "while", "with", "yield",
    }

    def __init__(self, document):
        super().__init__(document)
        self.keyword_format = QTextCharFormat()
        self.keyword_format.setForeground(QColor("#d65cff"))
        self.keyword_format.setFontWeight(QFont.Bold)
        self.string_format = QTextCharFormat()
        self.string_format.setForeground(QColor("#72e6c1"))
        self.comment_format = QTextCharFormat()
        self.comment_format.setForeground(QColor("#7d8595"))

    def highlightBlock(self, text: str) -> None:
        import re
        for match in re.finditer(r"\b[A-Za-z_][A-Za-z0-9_]*\b", text):
            if match.group() in self.KEYWORDS:
                self.setFormat(match.start(), match.end() - match.start(), self.keyword_format)
        for match in re.finditer(r"(['\"])(?:\\.|(?!\1).)*\1", text):
            self.setFormat(match.start(), match.end() - match.start(), self.string_format)
        comment = text.find("#")
        if comment >= 0:
            self.setFormat(comment, len(text) - comment, self.comment_format)


class CodeEditor(QPlainTextEdit):
    path_changed = Signal(object)

    def __init__(self, path: Path | None = None, parent=None):
        super().__init__(parent)
        self.path = path
        self.setLineWrapMode(QPlainTextEdit.NoWrap)
        font = QFont("Cascadia Code", 11)
        font.setStyleHint(QFont.Monospace)
        self.setFont(font)
        self.setTabStopDistance(self.fontMetrics().horizontalAdvance(" ") * 4)
        self.highlighter = PythonHighlighter(self.document())

    def load(self, path: Path) -> None:
        self.path = path
        self.setPlainText(path.read_text(encoding="utf-8"))
        self.document().setModified(False)
        self.path_changed.emit(path)

    def save(self, path: Path | None = None) -> Path:
        destination = path or self.path
        if destination is None:
            raise ValueError("No destination selected")
        destination.write_text(self.toPlainText(), encoding="utf-8")
        self.path = destination
        self.document().setModified(False)
        self.path_changed.emit(destination)
        return destination
