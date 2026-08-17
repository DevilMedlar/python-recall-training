from __future__ import annotations

import html
import shutil
import subprocess
from pathlib import Path

from PySide6.QtCore import QDir, QThreadPool, Qt, QUrl
from PySide6.QtGui import QAction, QCloseEvent, QDesktopServices, QIcon, QKeySequence, QShortcut, QTextCursor
from PySide6.QtWidgets import (
    QComboBox, QFileDialog, QFileSystemModel, QHBoxLayout, QInputDialog, QLabel, QMainWindow,
    QMenu, QMessageBox, QPlainTextEdit, QPushButton, QSplitter, QTabWidget,
    QTextBrowser, QToolBar, QTreeView, QVBoxLayout, QWidget,
)

from .. import __version__
from ..chat import ChatSession
from ..contract import ContractStore
from ..ollama import OllamaManager
from ..settings import Settings
from ..update import check_for_update
from ..workers import Task
from .editor import CodeEditor
from .terminal import TerminalPanel


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
        self._build_toolbar()
        self.open_whats_new()
        if settings.workspace and Path(settings.workspace).is_dir():
            self.open_workspace(Path(settings.workspace))
        self._start_runtime()
        self._start_update_check()

    def _build_ui(self) -> None:
        root = QSplitter(Qt.Horizontal)
        self.file_model = QFileSystemModel(self)
        self.file_model.setFilter(QDir.AllEntries | QDir.NoDotAndDotDot)
        self.tree = QTreeView()
        self.tree.setModel(self.file_model)
        self.tree.doubleClicked.connect(self._tree_open)
        self.tree.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tree.customContextMenuRequested.connect(self._show_explorer_menu)
        for column in range(1, 4):
            self.tree.hideColumn(column)

        explorer = QWidget()
        explorer_layout = QVBoxLayout(explorer)
        explorer_layout.setContentsMargins(4, 4, 4, 4)
        explorer_header = QHBoxLayout()
        explorer_header.addWidget(QLabel("EXPLORER"))
        explorer_header.addStretch()
        open_folder_button = QPushButton("Open folder")
        new_file_button = QPushButton("+ File")
        new_folder_button = QPushButton("+ Folder")
        open_folder_button.clicked.connect(self.choose_workspace)
        new_file_button.clicked.connect(self.create_explorer_file)
        new_folder_button.clicked.connect(self.create_explorer_folder)
        explorer_header.addWidget(open_folder_button)
        explorer_header.addWidget(new_file_button)
        explorer_header.addWidget(new_folder_button)
        explorer_layout.addLayout(explorer_header)
        explorer_layout.addWidget(self.tree)

        center = QSplitter(Qt.Vertical)
        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_editor)
        self.output = QPlainTextEdit()
        self.output.setReadOnly(True)
        self.output.setMaximumBlockCount(4000)
        terminal_root = Path(self.settings.workspace) if self.settings.workspace else Path.home()
        self.terminal = TerminalPanel(terminal_root)
        self.problems = QPlainTextEdit()
        self.problems.setReadOnly(True)
        self.problems.setPlainText("No problems detected. Static diagnostics will appear here in a later release.")
        self.bottom_tabs = QTabWidget()
        self.bottom_tabs.addTab(self.terminal, "TERMINAL")
        self.bottom_tabs.addTab(self.output, "OUTPUT")
        self.bottom_tabs.addTab(self.problems, "PROBLEMS")
        center.addWidget(self.tabs)
        center.addWidget(self.bottom_tabs)
        center.setSizes([700, 180])

        chat_panel = QWidget()
        chat_layout = QVBoxLayout(chat_panel)
        model_controls = QHBoxLayout()
        model_controls.addWidget(QLabel("MODEL"))
        self.model_combo = QComboBox()
        self.model_combo.setMinimumWidth(180)
        self.model_combo.addItem(self.settings.model)
        self.model_combo.currentTextChanged.connect(self.select_model)
        self.refresh_models_button = QPushButton("Refresh")
        self.pull_model_button = QPushButton("Pull model…")
        self.refresh_models_button.clicked.connect(self.refresh_models)
        self.pull_model_button.clicked.connect(self.pull_model)
        model_controls.addWidget(self.model_combo, 1)
        model_controls.addWidget(self.refresh_models_button)
        model_controls.addWidget(self.pull_model_button)
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
        chat_layout.addLayout(model_controls)
        chat_layout.addWidget(self.runtime_status)
        chat_layout.addWidget(self.chat_view)
        chat_layout.addWidget(self.chat_input)
        chat_layout.addLayout(controls)

        root.addWidget(explorer)
        root.addWidget(center)
        root.addWidget(chat_panel)
        root.setSizes([230, 800, 470])
        self.setCentralWidget(root)
        self.statusBar().showMessage("Ready")
        self.cursor_status = QLabel("Ln 1, Col 1")
        self.encoding_status = QLabel("UTF-8  ·  Spaces: 4  ·  Python")
        self.statusBar().addPermanentWidget(self.cursor_status)
        self.statusBar().addPermanentWidget(self.encoding_status)

    def _build_menu(self) -> None:
        file_menu = self.menuBar().addMenu("&File")
        for label, shortcut, callback in (
            ("New file", "Ctrl+N", self.new_file),
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

        edit_menu = self.menuBar().addMenu("&Edit")
        for label, shortcut, method in (
            ("Undo", "Ctrl+Z", "undo"),
            ("Redo", "Ctrl+Y", "redo"),
            ("Cut", "Ctrl+X", "cut"),
            ("Copy", "Ctrl+C", "copy"),
            ("Paste", "Ctrl+V", "paste"),
            ("Select all", "Ctrl+A", "selectAll"),
        ):
            action = QAction(label, self)
            action.setShortcut(shortcut)
            action.triggered.connect(lambda _checked=False, name=method: self._editor_command(name))
            edit_menu.addAction(action)

        view_menu = self.menuBar().addMenu("&View")
        terminal_action = QAction("Focus terminal", self)
        terminal_action.setShortcut("Ctrl+`")
        terminal_action.triggered.connect(self.focus_terminal)
        view_menu.addAction(terminal_action)

    def _build_toolbar(self) -> None:
        toolbar = QToolBar("Main", self)
        toolbar.setMovable(False)
        self.addToolBar(toolbar)
        for label, callback in (
            ("New", self.new_file),
            ("Open Folder", self.choose_workspace),
            ("Save", self.save_current),
            ("▶ Run", self.run_current),
            (">_ Terminal", self.focus_terminal),
        ):
            action = QAction(label, self)
            action.triggered.connect(callback)
            toolbar.addAction(action)

    def _editor_command(self, method: str) -> None:
        editor = self.current_editor()
        if editor:
            getattr(editor, method)()

    def focus_terminal(self) -> None:
        self.bottom_tabs.setCurrentWidget(self.terminal)
        self.terminal.input.setFocus()

    def _start_runtime(self) -> None:
        task = Task(self._prepare_ollama)
        task.signals.status.connect(self.runtime_status.setText)
        task.signals.result.connect(self._models_ready)
        task.signals.error.connect(self._runtime_error)
        task.signals.finished.connect(lambda: self.send_button.setEnabled(self.ollama.is_ready()))
        self.send_button.setEnabled(False)
        self.thread_pool.start(task)

    def _prepare_ollama(self, signals):
        signals.status.emit("Starting Ollama quietly…")
        self.ollama.start_hidden()
        models = self.ollama.installed_models()
        if not models:
            signals.status.emit(f"No local models found; downloading {self.settings.model}…")
            self.ollama.ensure_model(signals.status.emit)
            models = self.ollama.installed_models()
        signals.status.emit("Local AI ready")
        return sorted(models, key=str.casefold)

    def _runtime_error(self, message: str) -> None:
        self.runtime_status.setText("Local AI unavailable")
        if "not installed" in message.lower() or "path" in message.lower():
            choice = QMessageBox.question(
                self,
                "Ollama is required",
                f"{message}\n\nOpen the official Ollama for Windows download page?",
                QMessageBox.Open | QMessageBox.Cancel,
                QMessageBox.Open,
            )
            if choice == QMessageBox.Open:
                QDesktopServices.openUrl(QUrl("https://ollama.com/download/windows"))
            return
        QMessageBox.critical(self, "Senpai_Bot could not start Ollama", message)

    def _models_ready(self, models: object) -> None:
        if not isinstance(models, list):
            return
        current = self.settings.model
        selected = current if current in models else (models[0] if models else current)
        self.model_combo.blockSignals(True)
        self.model_combo.clear()
        self.model_combo.addItems(models)
        if not models:
            self.model_combo.addItem(current)
        self.model_combo.setCurrentText(selected)
        self.model_combo.blockSignals(False)
        if selected != current:
            self.select_model(selected)
        else:
            self.runtime_status.setText(f"Local AI ready · {selected}")

    def select_model(self, model: str) -> None:
        if not model or model == self.settings.model:
            return
        self.settings.model = model
        self.ollama.model = model
        self.settings.save(self.settings_path)
        self.chat_session.clear()
        self.chat_view.append(f"<p><i>Model changed to {html.escape(model)}. New chat context started.</i></p>")
        self.runtime_status.setText(f"Local AI ready · {model}")

    def refresh_models(self) -> None:
        self.refresh_models_button.setEnabled(False)
        task = Task(self._refresh_models_task)
        task.signals.result.connect(self._models_ready)
        task.signals.error.connect(lambda message: self.runtime_status.setText(f"Model refresh failed: {message}"))
        task.signals.finished.connect(lambda: self.refresh_models_button.setEnabled(True))
        self.thread_pool.start(task)

    def _refresh_models_task(self, signals):
        return sorted(self.ollama.installed_models(), key=str.casefold)

    def pull_model(self) -> None:
        model, accepted = QInputDialog.getText(
            self,
            "Pull Ollama model",
            "Exact model name (models may require several GB):",
            text="",
        )
        model = model.strip()
        if not accepted or not model:
            return
        choice = QMessageBox.question(
            self,
            "Download model",
            f"Download {model} through the local Ollama service?\n\nModel downloads can be very large.",
            QMessageBox.Yes | QMessageBox.Cancel,
            QMessageBox.Cancel,
        )
        if choice != QMessageBox.Yes:
            return
        self.pull_model_button.setEnabled(False)
        task = Task(self._pull_model_task, model)
        task.signals.status.connect(self.runtime_status.setText)
        task.signals.error.connect(lambda message: QMessageBox.critical(self, "Model download failed", message))
        task.signals.result.connect(lambda _value, selected=model: self._model_pulled(selected))
        task.signals.finished.connect(lambda: self.pull_model_button.setEnabled(True))
        self.thread_pool.start(task)

    def _pull_model_task(self, signals, model: str):
        self.ollama.pull_model(model, signals.status.emit)

    def _model_pulled(self, model: str) -> None:
        if self.model_combo.findText(model) < 0:
            self.model_combo.addItem(model)
        self.refresh_models()
        self.model_combo.setCurrentText(model)
        self.runtime_status.setText(f"Model ready · {model}")

    def _start_update_check(self) -> None:
        task = Task(self._check_update_task)
        task.signals.result.connect(self._show_available_update)
        self.thread_pool.start(task)

    @staticmethod
    def _check_update_task(signals):
        return check_for_update(__version__)

    def _show_available_update(self, update: object) -> None:
        if not isinstance(update, dict):
            return
        version = update.get("version", "")
        notes = update.get("notes", "")
        choice = QMessageBox.question(
            self,
            "Senpai_Bot update available",
            f"Version {version} is available.\n\n{notes}\n\nOpen the verified GitHub update page?",
            QMessageBox.Open | QMessageBox.Cancel,
            QMessageBox.Open,
        )
        if choice == QMessageBox.Open:
            QDesktopServices.openUrl(QUrl(update["url"]))

    def choose_workspace(self) -> None:
        chosen = QFileDialog.getExistingDirectory(self, "Open workspace")
        if chosen:
            self.open_workspace(Path(chosen))

    def open_workspace(self, path: Path) -> None:
        index = self.file_model.setRootPath(str(path))
        self.tree.setRootIndex(index)
        self.settings.workspace = str(path)
        self.settings.save(self.settings_path)
        self.terminal.set_working_directory(path)
        self.statusBar().showMessage(f"Workspace: {path}")

    def workspace_root(self) -> Path | None:
        path = Path(self.settings.workspace) if self.settings.workspace else None
        return path if path and path.is_dir() else None

    def selected_explorer_path(self) -> Path | None:
        index = self.tree.currentIndex()
        if not index.isValid():
            return None
        return Path(self.file_model.filePath(index))

    def explorer_target_directory(self) -> Path | None:
        selected = self.selected_explorer_path()
        if selected:
            return selected if selected.is_dir() else selected.parent
        return self.workspace_root()

    def _require_explorer_directory(self) -> Path | None:
        directory = self.explorer_target_directory()
        if directory is None:
            QMessageBox.information(self, "Open a folder", "Open a workspace folder before creating files or folders.")
        return directory

    @staticmethod
    def _valid_child_name(name: str) -> bool:
        return bool(name) and Path(name).name == name and name not in {".", ".."}

    def create_explorer_file(self) -> None:
        directory = self._require_explorer_directory()
        if directory is None:
            return
        name, accepted = QInputDialog.getText(self, "New file", "File name:", text="untitled.py")
        if not accepted:
            return
        if not self._valid_child_name(name):
            QMessageBox.warning(self, "Invalid file name", "Enter one file name without path separators.")
            return
        destination = directory / name
        if destination.exists():
            QMessageBox.warning(self, "Already exists", f"{destination.name} already exists.")
            return
        destination.write_text("", encoding="utf-8")
        self.open_file(destination)

    def create_explorer_folder(self) -> None:
        directory = self._require_explorer_directory()
        if directory is None:
            return
        name, accepted = QInputDialog.getText(self, "New folder", "Folder name:")
        if not accepted:
            return
        if not self._valid_child_name(name):
            QMessageBox.warning(self, "Invalid folder name", "Enter one folder name without path separators.")
            return
        destination = directory / name
        if destination.exists():
            QMessageBox.warning(self, "Already exists", f"{destination.name} already exists.")
            return
        destination.mkdir()

    def rename_explorer_item(self) -> None:
        source = self.selected_explorer_path()
        if source is None:
            return
        name, accepted = QInputDialog.getText(self, "Rename", "New name:", text=source.name)
        if not accepted or name == source.name:
            return
        if not self._valid_child_name(name):
            QMessageBox.warning(self, "Invalid name", "Enter one name without path separators.")
            return
        destination = source.with_name(name)
        if destination.exists():
            QMessageBox.warning(self, "Already exists", f"{destination.name} already exists.")
            return
        source_was_dir = source.is_dir()
        source.rename(destination)
        for index in range(self.tabs.count()):
            editor = self.tabs.widget(index)
            if not isinstance(editor, CodeEditor) or editor.path is None:
                continue
            if editor.path == source:
                editor.path = destination
                self._update_editor_title(editor)
            elif source_was_dir and editor.path.is_relative_to(source):
                editor.path = destination / editor.path.relative_to(source)
                self._update_editor_title(editor)

    def delete_explorer_item(self) -> None:
        target = self.selected_explorer_path()
        if target is None or target == self.workspace_root():
            return
        for index in range(self.tabs.count()):
            editor = self.tabs.widget(index)
            if not isinstance(editor, CodeEditor) or editor.path is None:
                continue
            affected = editor.path == target or (target.is_dir() and editor.path.is_relative_to(target))
            if affected and editor.document().isModified():
                QMessageBox.warning(
                    self,
                    "Unsaved file is open",
                    f"Save or close {editor.path.name} before deleting {target.name}.",
                )
                return
        choice = QMessageBox.warning(
            self,
            "Delete permanently",
            f"Permanently delete {target.name}?\n\nThis does not use the Recycle Bin.",
            QMessageBox.Yes | QMessageBox.Cancel,
            QMessageBox.Cancel,
        )
        if choice != QMessageBox.Yes:
            return
        try:
            if target.is_dir():
                target.rmdir()
            else:
                target.unlink()
        except OSError as exc:
            QMessageBox.critical(self, "Could not delete", str(exc))

    def _show_explorer_menu(self, position) -> None:
        menu = QMenu(self)
        menu.addAction("New file", self.create_explorer_file)
        menu.addAction("New folder", self.create_explorer_folder)
        if self.selected_explorer_path() is not None:
            menu.addSeparator()
            menu.addAction("Rename", self.rename_explorer_item)
            menu.addAction("Delete", self.delete_explorer_item)
        menu.exec(self.tree.viewport().mapToGlobal(position))

    def choose_file(self) -> None:
        chosen, _ = QFileDialog.getOpenFileName(self, "Open file", filter="Python (*.py);;All files (*)")
        if chosen:
            self.open_file(Path(chosen))

    def open_whats_new(self) -> None:
        path = self.contract.root / "WHATS_NEW.md"
        if not path.is_file():
            self.new_file()
            return
        editor = CodeEditor(path)
        editor.load(path)
        editor.setReadOnly(True)
        editor.cursor_location_changed.connect(self._update_cursor_status)
        self.tabs.addTab(editor, "WHATS_NEW.md")
        self.tabs.setCurrentWidget(editor)

    def new_file(self) -> None:
        editor = CodeEditor()
        editor.cursor_location_changed.connect(self._update_cursor_status)
        editor.document().modificationChanged.connect(
            lambda _modified, current=editor: self._update_editor_title(current)
        )
        index = self.tabs.addTab(editor, "Untitled.py")
        self.tabs.setCurrentIndex(index)
        editor.setFocus()

    def _update_editor_title(self, editor: CodeEditor) -> None:
        index = self.tabs.indexOf(editor)
        if index < 0:
            return
        name = editor.path.name if editor.path else "Untitled.py"
        marker = "● " if editor.document().isModified() else ""
        self.tabs.setTabText(index, marker + name)

    def close_editor(self, index: int) -> None:
        editor = self.tabs.widget(index)
        if not isinstance(editor, CodeEditor):
            self.tabs.removeTab(index)
            return
        if editor.document().isModified():
            name = editor.path.name if editor.path else "Untitled.py"
            choice = QMessageBox.warning(
                self,
                "Unsaved changes",
                f"Save changes to {name}?",
                QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel,
                QMessageBox.Save,
            )
            if choice == QMessageBox.Cancel:
                return
            if choice == QMessageBox.Save:
                self.tabs.setCurrentIndex(index)
                if not self.save_current():
                    return
        self.tabs.removeTab(index)

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
        editor.cursor_location_changed.connect(self._update_cursor_status)
        editor.document().modificationChanged.connect(
            lambda _modified, current=editor: self._update_editor_title(current)
        )
        self.tabs.addTab(editor, path.name)
        self.tabs.setCurrentWidget(editor)

    def current_editor(self) -> CodeEditor | None:
        widget = self.tabs.currentWidget()
        return widget if isinstance(widget, CodeEditor) else None

    def _update_cursor_status(self, line: int, column: int) -> None:
        self.cursor_status.setText(f"Ln {line}, Col {column}")

    def save_current(self) -> bool:
        editor = self.current_editor()
        if not editor:
            return False
        if editor.path is None:
            return self.save_current_as()
        editor.save()
        self._update_editor_title(editor)
        return True

    def save_current_as(self) -> bool:
        editor = self.current_editor()
        if not editor:
            return False
        chosen, _ = QFileDialog.getSaveFileName(self, "Save file", filter="Python (*.py);;All files (*)")
        if not chosen:
            return False
        editor.save(Path(chosen))
        self._update_editor_title(editor)
        return True

    def run_current(self) -> None:
        editor = self.current_editor()
        if not editor:
            return
        if not self.save_current() or editor.path is None:
            return
        interpreter = shutil.which("python") or shutil.which("python3")
        command = [interpreter, str(editor.path)] if interpreter else ["py", "-3", str(editor.path)]
        self.output.appendPlainText("> " + " ".join(command))
        self.bottom_tabs.setCurrentWidget(self.output)
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
        for index in range(self.tabs.count() - 1, -1, -1):
            count = self.tabs.count()
            self.close_editor(index)
            if self.tabs.count() == count:
                event.ignore()
                return
        self.settings.save(self.settings_path)
        self.terminal.stop()
        event.accept()
