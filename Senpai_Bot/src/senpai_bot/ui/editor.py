from __future__ import annotations

from pathlib import Path

from PySide6.QtCore import QRect, QSize, Qt, Signal
from PySide6.QtGui import QColor, QFont, QPainter, QSyntaxHighlighter, QTextCharFormat, QTextFormat
from PySide6.QtWidgets import QPlainTextEdit, QTextEdit, QWidget


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


class LineNumberArea(QWidget):
    def __init__(self, editor: "CodeEditor"):
        super().__init__(editor)
        self.editor = editor

    def sizeHint(self) -> QSize:
        return QSize(self.editor.line_number_area_width(), 0)

    def paintEvent(self, event) -> None:
        self.editor.paint_line_number_area(event)


class CodeEditor(QPlainTextEdit):
    path_changed = Signal(object)
    cursor_location_changed = Signal(int, int)

    def __init__(self, path: Path | None = None, parent=None):
        super().__init__(parent)
        self.path = path
        self.line_number_area = LineNumberArea(self)
        self.setLineWrapMode(QPlainTextEdit.NoWrap)
        font = QFont("Cascadia Code", 11)
        font.setStyleHint(QFont.Monospace)
        self.setFont(font)
        self.setTabStopDistance(self.fontMetrics().horizontalAdvance(" ") * 4)
        self.highlighter = PythonHighlighter(self.document())
        self.blockCountChanged.connect(self.update_line_number_area_width)
        self.updateRequest.connect(self.update_line_number_area)
        self.cursorPositionChanged.connect(self._cursor_moved)
        self.cursorPositionChanged.connect(self.highlight_current_line)
        self.update_line_number_area_width()
        self.highlight_current_line()

    def line_number_area_width(self) -> int:
        digits = len(str(max(1, self.blockCount())))
        return 14 + self.fontMetrics().horizontalAdvance("9") * digits

    def update_line_number_area_width(self, _blocks: int = 0) -> None:
        self.setViewportMargins(self.line_number_area_width(), 0, 0, 0)

    def update_line_number_area(self, rect: QRect, dy: int) -> None:
        if dy:
            self.line_number_area.scroll(0, dy)
        else:
            self.line_number_area.update(0, rect.y(), self.line_number_area.width(), rect.height())
        if rect.contains(self.viewport().rect()):
            self.update_line_number_area_width()

    def resizeEvent(self, event) -> None:
        super().resizeEvent(event)
        contents = self.contentsRect()
        self.line_number_area.setGeometry(
            QRect(contents.left(), contents.top(), self.line_number_area_width(), contents.height())
        )

    def paint_line_number_area(self, event) -> None:
        painter = QPainter(self.line_number_area)
        painter.fillRect(event.rect(), QColor("#151821"))
        block = self.firstVisibleBlock()
        block_number = block.blockNumber()
        top = round(self.blockBoundingGeometry(block).translated(self.contentOffset()).top())
        bottom = top + round(self.blockBoundingRect(block).height())
        while block.isValid() and top <= event.rect().bottom():
            if block.isVisible() and bottom >= event.rect().top():
                painter.setPen(QColor("#c7cad5") if block_number == self.textCursor().blockNumber() else QColor("#6f7484"))
                painter.drawText(
                    0,
                    top,
                    self.line_number_area.width() - 7,
                    self.fontMetrics().height(),
                    Qt.AlignRight,
                    str(block_number + 1),
                )
            block = block.next()
            top = bottom
            bottom = top + round(self.blockBoundingRect(block).height())
            block_number += 1

    def highlight_current_line(self) -> None:
        selection = QTextEdit.ExtraSelection()
        selection.format.setBackground(QColor("#202433"))
        selection.format.setProperty(QTextFormat.FullWidthSelection, True)
        selection.cursor = self.textCursor()
        selection.cursor.clearSelection()
        self.setExtraSelections([selection])

    def _cursor_moved(self) -> None:
        cursor = self.textCursor()
        self.cursor_location_changed.emit(cursor.blockNumber() + 1, cursor.positionInBlock() + 1)

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
