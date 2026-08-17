from __future__ import annotations

import os
import re
from pathlib import Path

from PySide6.QtCore import QEvent, QProcess, Qt
from PySide6.QtGui import QFont, QTextCursor
from PySide6.QtWidgets import QHBoxLayout, QLineEdit, QPlainTextEdit, QPushButton, QVBoxLayout, QWidget


ANSI_RE = re.compile(r"\x1b\[[0-?]*[ -/]*[@-~]")


class TerminalPanel(QWidget):
    """A persistent, line-oriented local shell embedded in the IDE."""

    def __init__(self, working_directory: Path | None = None, parent=None):
        super().__init__(parent)
        self.working_directory = working_directory or Path.home()
        self.history: list[str] = []
        self.history_index = 0
        self.process = QProcess(self)
        self.process.setProcessChannelMode(QProcess.MergedChannels)
        self.process.readyReadStandardOutput.connect(self._read_output)
        self.process.finished.connect(self._process_finished)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        controls = QHBoxLayout()
        self.restart_button = QPushButton("Restart terminal")
        self.clear_button = QPushButton("Clear")
        self.restart_button.clicked.connect(self.restart)
        self.clear_button.clicked.connect(self.output_clear)
        controls.addWidget(self.restart_button)
        controls.addWidget(self.clear_button)
        controls.addStretch()
        self.output = QPlainTextEdit()
        self.output.setReadOnly(True)
        self.output.setMaximumBlockCount(6000)
        font = QFont("Cascadia Mono", 10)
        font.setStyleHint(QFont.Monospace)
        self.output.setFont(font)
        self.input = QLineEdit()
        self.input.setFont(font)
        self.input.setPlaceholderText("Type a command and press Enter")
        self.input.returnPressed.connect(self.send_command)
        self.input.installEventFilter(self)
        layout.addLayout(controls)
        layout.addWidget(self.output)
        layout.addWidget(self.input)
        self.start()

    def shell(self) -> tuple[str, list[str]]:
        if os.name == "nt":
            return "powershell.exe", ["-NoLogo", "-NoProfile", "-NoExit"]
        return "/bin/bash", ["--noprofile", "--norc", "-i"]

    def start(self) -> None:
        program, arguments = self.shell()
        self.process.setWorkingDirectory(str(self.working_directory))
        self.process.start(program, arguments)
        if not self.process.waitForStarted(3000):
            self.output.appendPlainText(f"Could not start terminal: {self.process.errorString()}")

    def restart(self) -> None:
        if self.process.state() != QProcess.NotRunning:
            self.process.kill()
            self.process.waitForFinished(2000)
        self.output.appendPlainText("\n--- terminal restarted ---\n")
        self.start()

    def set_working_directory(self, path: Path) -> None:
        self.working_directory = path
        quoted = str(path).replace("'", "''")
        command = f"Set-Location -LiteralPath '{quoted}'" if os.name == "nt" else f"cd {str(path)!r}"
        self._write(command)

    def send_command(self) -> None:
        command = self.input.text().rstrip()
        if not command:
            return
        self.history.append(command)
        self.history_index = len(self.history)
        self.input.clear()
        self.output.appendPlainText(f"PS> {command}" if os.name == "nt" else f"$ {command}")
        self._write(command)

    def _write(self, command: str) -> None:
        if self.process.state() == QProcess.NotRunning:
            self.start()
        self.process.write((command + "\r\n").encode("utf-8"))

    def _read_output(self) -> None:
        text = bytes(self.process.readAllStandardOutput()).decode("utf-8", errors="replace")
        self.output.moveCursor(QTextCursor.End)
        self.output.insertPlainText(ANSI_RE.sub("", text))
        self.output.ensureCursorVisible()

    def _process_finished(self, exit_code: int, _status) -> None:
        self.output.appendPlainText(f"\nTerminal exited with code {exit_code}. Click Restart terminal to reopen it.")

    def output_clear(self) -> None:
        self.output.clear()

    def stop(self) -> None:
        if self.process.state() != QProcess.NotRunning:
            self.process.write(b"exit\r\n")
            if not self.process.waitForFinished(1000):
                self.process.kill()

    def eventFilter(self, watched, event) -> bool:
        if watched is self.input and event.type() == QEvent.KeyPress:
            if event.key() == Qt.Key_Up and self.history:
                self.history_index = max(0, self.history_index - 1)
                self.input.setText(self.history[self.history_index])
                return True
            if event.key() == Qt.Key_Down and self.history:
                self.history_index = min(len(self.history), self.history_index + 1)
                self.input.setText("" if self.history_index == len(self.history) else self.history[self.history_index])
                return True
        return super().eventFilter(watched, event)
