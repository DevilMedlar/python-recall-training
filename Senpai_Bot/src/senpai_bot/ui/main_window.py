from __future__ import annotations

import html
import shutil
import subprocess
from pathlib import Path

from PySide6.QtCore import QDir, QThreadPool, Qt
from PySide6.QtGui import QAction, QCloseEvent, QIcon, QKeySequence, QShortcut, QTextCursor
from PySide6.QtWidgets import (
    QFileDialog, QFileSystemModel, QHBoxLayout, QLabel, QMainWindow, QMessageBox,
    QPlainTextEdit, QPushButton, QSplitter, QTabWidget, QTextBrowser, QTreeView,
    QVBoxLayout, QWidget,
)

from ..chat import ChatSession
from ..contract import ContractStore
from ..ollama import OllamaManager
from ..settings import Settings
from ..workers import Task
from .editor import CodeEditor


class MainWindow(QMainWindow):
    def __init__(self, contract: ContractStore, settings: Settings, settings_path: Path, icon_path: Path):
        super().__init__()
        self.contract = contract
        self.settings = settings
        self.settings_path = settings_path
        self.ollama = OllamaManager(settings.ollama_url, settings.model)
        self.chat_session = ChatSession(contract, settings.max_history_messages)
        self.thread_pool = QThreadPool.globalInstance()
        self._assistant_buffer = ""
        self._busy = False
        self.setWindowTitle("Senpai_Bot")
        self.setWindowIcon(QIcon(str(icon_path)))
        self.resize(1500, 920)
        self._build_ui()
        self._build_menu()
        if settings.workspace and Path(settings.workspace).is_dir():
            self.open_workspace(Path(settings.workspace))
        self._start_runtime()

    def _build_ui(self) -> None:
        root = QSplitter(Qt.Horizontal)
        self.file_model = QFileSystemModel(self)
        self.file_model.setFilter(QDir.AllEntries | QDir.NoDotAndDotDot)
        self.tree = QTreeView()
        self.tree.setModel(self.file_model)
        self.tree.doubleClicked.connect(self._tree_open)
        for column in range(1, 4):
            self.tree.hideColumn(column)

        center = QSplitter(Qt.Vertical)
        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.tabs.removeTab)
        self.output = QPlainTextEdit()
        self.output.setReadOnly(True)
        self.output.setMaximumBlockCount(4000)
        center.addWidget(self.tabs)
        center.addWidget(self.output)
        center.setSizes([700, 180])

        chat_panel = QWidget()
        chat_layout = QVBoxLayout(chat_panel)
        self.runtime_status = QLabel("Starting local AI…")
        self.chat_view = QTextBrowser()
        self.chat_input = QPlainTextEdit()
        self.chat_input.setPlaceholderText("Message Senpai…  (Ctrl+Enter to send)")
        self.chat_input.setMaximumHeight(130)
        self.send_shortcut = QShortcut(QKeySequence("Ctrl+Return"), self.chat_input)
        self.send_shortcut.activated.connect(self.send_chat)
        controls = QHBoxLayout()
        self.clear_chat_button = QPushButton("New chat")
        self.send_button = QPushButton("Send")
        self.clear_chat_button.clicked.connect(self.clear_chat)
        self.send_button.clicked.connect(self.send_chat)
        controls.addWidget(self.clear_chat_button)
        controls.addStretch()
        controls.addWidget(self.send_button)
        chat_layout.addWidget(self.runtime_status)
        chat_layout.addWidget(self.chat_view)
        chat_layout.addWidget(self.chat_input)
        chat_layout.addLayout(controls)

        root.addWidget(self.tree)
        root.addWidget(center)
        root.addWidget(chat_panel)
        root.setSizes([230, 800, 470])
        self.setCentralWidget(root)
        self.statusBar().showMessage("Ready")

    def _build_menu(self) -> None:
        file_menu = self.menuBar().addMenu("&File")
        for label, shortcut, callback in (
            ("Open workspace…", "Ctrl+K, Ctrl+O", self.choose_workspace),
            ("Open file…", "Ctrl+O", self.choose_file),
            ("Save", "Ctrl+S", self.save_current),
            ("Save as…", "Ctrl+Shift+S", self.save_current_as),
        ):
            action = QAction(label, self)
            action.setShortcut(shortcut)
            action.triggered.connect(callback)
            file_menu.addAction(action)
        run_action = QAction("Run Python file", self)
        run_action.setShortcut("F5")
        run_action.triggered.connect(self.run_current)
        self.menuBar().addAction(run_action)

    def _start_runtime(self) -> None:
        task = Task(self._prepare_ollama)
        task.signals.status.connect(self.runtime_status.setText)
        task.signals.error.connect(self._runtime_error)
        task.signals.finished.connect(lambda: self.send_button.setEnabled(self.ollama.is_ready()))
        self.send_button.setEnabled(False)
        self.thread_pool.start(task)

    def _prepare_ollama(self, signals):
        signals.status.emit("Starting Ollama quietly…")
        self.ollama.start_hidden()
        signals.status.emit(f"Checking {self.settings.model}…")
        self.ollama.ensure_model(signals.status.emit)
        signals.status.emit(f"Local AI ready · {self.settings.model}")

    def _runtime_error(self, message: str) -> None:
        self.runtime_status.setText("Local AI unavailable")
        QMessageBox.critical(self, "Senpai_Bot could not start Ollama", message)

    def choose_workspace(self) -> None:
        chosen = QFileDialog.getExistingDirectory(self, "Open workspace")
        if chosen:
            self.open_workspace(Path(chosen))

    def open_workspace(self, path: Path) -> None:
        index = self.file_model.setRootPath(str(path))
        self.tree.setRootIndex(index)
        self.settings.workspace = str(path)
        self.settings.save(self.settings_path)
        self.statusBar().showMessage(f"Workspace: {path}")

    def choose_file(self) -> None:
        chosen, _ = QFileDialog.getOpenFileName(self, "Open file", filter="Python (*.py);;All files (*)")
        if chosen:
            self.open_file(Path(chosen))

    def _tree_open(self, index) -> None:
        path = Path(self.file_model.filePath(index))
        if path.is_file():
            self.open_file(path)

    def open_file(self, path: Path) -> None:
        for index in range(self.tabs.count()):
            editor = self.tabs.widget(index)
            if isinstance(editor, CodeEditor) and editor.path == path:
                self.tabs.setCurrentIndex(index)
                return
        editor = CodeEditor(path)
        editor.load(path)
        self.tabs.addTab(editor, path.name)
        self.tabs.setCurrentWidget(editor)

    def current_editor(self) -> CodeEditor | None:
        widget = self.tabs.currentWidget()
        return widget if isinstance(widget, CodeEditor) else None

    def save_current(self) -> None:
        editor = self.current_editor()
        if not editor:
            return
        if editor.path is None:
            self.save_current_as()
            return
        editor.save()
        self.tabs.setTabText(self.tabs.currentIndex(), editor.path.name)

    def save_current_as(self) -> None:
        editor = self.current_editor()
        if not editor:
            return
        chosen, _ = QFileDialog.getSaveFileName(self, "Save file", filter="Python (*.py);;All files (*)")
        if chosen:
            path = editor.save(Path(chosen))
            self.tabs.setTabText(self.tabs.currentIndex(), path.name)

    def run_current(self) -> None:
        editor = self.current_editor()
        if not editor:
            return
        self.save_current()
        if editor.path is None:
            return
        interpreter = shutil.which("python") or shutil.which("python3")
        command = [interpreter, str(editor.path)] if interpreter else ["py", "-3", str(editor.path)]
        self.output.appendPlainText("> " + " ".join(command))
        task = Task(self._run_python_task, command, editor.path.parent)
        task.signals.result.connect(self._show_run_result)
        task.signals.error.connect(lambda message: self.output.appendPlainText(message + "\n"))
        self.thread_pool.start(task)

    @staticmethod
    def _run_python_task(signals, command: list[str], cwd: Path):
        return subprocess.run(command, cwd=cwd, capture_output=True, text=True, timeout=60)

    def _show_run_result(self, process: subprocess.CompletedProcess[str]) -> None:
        if process.stdout:
            self.output.appendPlainText(process.stdout.rstrip())
        if process.stderr:
            self.output.appendPlainText(process.stderr.rstrip())
        self.output.appendPlainText(f"Process exited with code {process.returncode}\n")

    def _workspace_context(self) -> str:
        editor = self.current_editor()
        if not editor:
            return "No editor tab is active."
        path = str(editor.path) if editor.path else "Untitled"
        content = editor.toPlainText()
        return f"Active file: {path}\n```python\n{content[-12000:]}\n```"

    def send_chat(self) -> None:
        user_text = self.chat_input.toPlainText().strip()
        if not user_text or self._busy:
            return
        self.chat_input.clear()
        self.chat_view.append(f"<p><b>Daddy</b><br>{html.escape(user_text)}</p>")
        self.chat_view.append("<p><b>Senpai</b><br><span id='stream'></span></p>")
        self._assistant_buffer = ""
        self._busy = True
        self.send_button.setEnabled(False)
        messages = self.chat_session.build_messages(user_text, self._workspace_context())
        task = Task(self._chat_task, messages)
        task.signals.token.connect(self._append_token)
        task.signals.error.connect(lambda error: self.chat_view.append(f"<p style='color:#ff6b7a'>{html.escape(error)}</p>"))
        task.signals.finished.connect(lambda: self._chat_finished(user_text))
        self.thread_pool.start(task)

    def _chat_task(self, signals, messages):
        self.ollama.stream_chat(messages, signals.token.emit)

    def _append_token(self, token: str) -> None:
        self._assistant_buffer += token
        cursor = self.chat_view.textCursor()
        cursor.movePosition(QTextCursor.End)
        cursor.insertText(token)
        self.chat_view.setTextCursor(cursor)
        self.chat_view.ensureCursorVisible()

    def _chat_finished(self, user_text: str) -> None:
        if self._assistant_buffer:
            self.chat_session.record(user_text, self._assistant_buffer)
        self._busy = False
        self.send_button.setEnabled(True)

    def clear_chat(self) -> None:
        self.chat_session.clear()
        self.chat_view.clear()
        self.chat_view.append("<p><i>New local session started.</i></p>")

    def closeEvent(self, event: QCloseEvent) -> None:
        self.settings.save(self.settings_path)
        event.accept()
