from __future__ import annotations

import html
from pathlib import Path

from PySide6.QtCore import Qt, QThreadPool, QUrl, Signal
from PySide6.QtGui import QCloseEvent, QDesktopServices
from PySide6.QtWidgets import (
    QComboBox,
    QDialog,
    QFileDialog,
    QGridLayout,
    QGroupBox,
    QHBoxLayout,
    QInputDialog,
    QLabel,
    QMessageBox,
    QPushButton,
    QTextBrowser,
    QVBoxLayout,
)

from ..dependencies import (
    OLLAMA_MODELS_URL,
    OLLAMA_OFFICIAL_URL,
    PYTHON_OFFICIAL_URL,
    EnvironmentReport,
    detect_ollama,
    detect_python,
    scan_environment,
)
from ..installers import InstallCoordinator, InstallOutcome
from ..model_catalog import (
    OFFICIAL_MODEL_LIBRARY_URL,
    RECOMMENDED_MODELS,
    canonical_installed_model,
    model_by_name,
)
from ..ollama import OllamaManager
from ..ownership import ComponentRecord, OwnershipManifest
from ..settings import Settings
from ..workers import Task


class SetupDialog(QDialog):
    environment_changed = Signal()

    def __init__(
        self,
        settings: Settings,
        settings_path: Path,
        manifest: OwnershipManifest,
        data_path: Path,
        ollama_manager: OllamaManager,
        first_run: bool = False,
        parent=None,
    ):
        super().__init__(parent)
        self.settings = settings
        self.settings_path = settings_path
        self.manifest = manifest
        self.data_path = data_path
        self.ollama = ollama_manager
        self.first_run = first_run
        self.report: EnvironmentReport | None = None
        self.thread_pool = QThreadPool.globalInstance()
        self._busy = False
        self.setWindowTitle("First-time setup" if first_run else "Setup & Dependencies")
        self.setMinimumSize(820, 680)
        self._build_ui()
        self.rescan()

    def _build_ui(self) -> None:
        root = QVBoxLayout(self)
        intro = QLabel(
            "Senpai itself is self-contained. Python enables running workspace files; "
            "Ollama plus one local model enables private local chat. Nothing on this page "
            "is installed or downloaded without an explicit Yes."
        )
        intro.setWordWrap(True)
        root.addWidget(intro)

        status_group = QGroupBox("Environment status")
        status_layout = QGridLayout(status_group)
        self.python_status = QLabel("Not scanned")
        self.ollama_status = QLabel("Not scanned")
        self.api_status = QLabel("Not scanned")
        self.models_status = QLabel("Not scanned")
        self.disk_status = QLabel("Not scanned")
        rows = (
            ("Python", self.python_status),
            ("Ollama", self.ollama_status),
            ("Local Ollama service", self.api_status),
            ("Local models", self.models_status),
            ("Free disk space", self.disk_status),
        )
        for row, (name, label) in enumerate(rows):
            title = QLabel(f"<b>{html.escape(name)}</b>")
            title.setAlignment(Qt.AlignTop)
            label.setWordWrap(True)
            status_layout.addWidget(title, row, 0)
            status_layout.addWidget(label, row, 1)
        root.addWidget(status_group)

        python_group = QGroupBox("Python for Run Python File")
        python_layout = QHBoxLayout(python_group)
        self.install_python_button = QPushButton("Install official Python…")
        self.choose_python_button = QPushButton("Choose python.exe…")
        self.python_page_button = QPushButton("Official Python page")
        self.install_python_button.clicked.connect(self.install_python)
        self.choose_python_button.clicked.connect(self.choose_python)
        self.python_page_button.clicked.connect(
            lambda: QDesktopServices.openUrl(QUrl(PYTHON_OFFICIAL_URL))
        )
        python_layout.addWidget(self.install_python_button)
        python_layout.addWidget(self.choose_python_button)
        python_layout.addWidget(self.python_page_button)
        python_layout.addStretch()
        root.addWidget(python_group)

        ollama_group = QGroupBox("Ollama for local AI")
        ollama_layout = QHBoxLayout(ollama_group)
        self.install_ollama_button = QPushButton("Install official Ollama…")
        self.choose_ollama_button = QPushButton("Choose ollama.exe…")
        self.start_ollama_button = QPushButton("Start local service")
        self.ollama_page_button = QPushButton("Official Ollama page")
        self.install_ollama_button.clicked.connect(self.install_ollama)
        self.choose_ollama_button.clicked.connect(self.choose_ollama)
        self.start_ollama_button.clicked.connect(self.start_ollama)
        self.ollama_page_button.clicked.connect(
            lambda: QDesktopServices.openUrl(QUrl(OLLAMA_OFFICIAL_URL))
        )
        ollama_layout.addWidget(self.install_ollama_button)
        ollama_layout.addWidget(self.choose_ollama_button)
        ollama_layout.addWidget(self.start_ollama_button)
        ollama_layout.addWidget(self.ollama_page_button)
        root.addWidget(ollama_group)

        model_group = QGroupBox("Local model")
        model_layout = QVBoxLayout(model_group)
        active_row = QHBoxLayout()
        active_row.addWidget(QLabel("Active installed model:"))
        self.active_model_combo = QComboBox()
        self.active_model_combo.currentTextChanged.connect(self.select_active_model)
        active_row.addWidget(self.active_model_combo, 1)
        model_layout.addLayout(active_row)

        recommended_row = QHBoxLayout()
        recommended_row.addWidget(QLabel("Recommended download:"))
        self.recommended_model_combo = QComboBox()
        for model in RECOMMENDED_MODELS:
            self.recommended_model_combo.addItem(model.display_text, model.name)
        self.recommended_model_combo.currentIndexChanged.connect(
            self._update_model_detail
        )
        self.download_model_button = QPushButton("Download selected…")
        self.exact_model_button = QPushButton("Advanced exact name…")
        self.model_page_button = QPushButton("Official model library")
        self.download_model_button.clicked.connect(self.download_recommended_model)
        self.exact_model_button.clicked.connect(self.download_exact_model)
        self.model_page_button.clicked.connect(
            lambda: QDesktopServices.openUrl(QUrl(OFFICIAL_MODEL_LIBRARY_URL))
        )
        recommended_row.addWidget(self.recommended_model_combo, 1)
        recommended_row.addWidget(self.download_model_button)
        recommended_row.addWidget(self.exact_model_button)
        recommended_row.addWidget(self.model_page_button)
        model_layout.addLayout(recommended_row)
        self.model_detail = QTextBrowser()
        self.model_detail.setMaximumHeight(120)
        self.model_detail.setOpenExternalLinks(True)
        model_layout.addWidget(self.model_detail)
        self._update_model_detail()
        root.addWidget(model_group)

        self.operation_status = QLabel("Ready to scan")
        self.operation_status.setWordWrap(True)
        root.addWidget(self.operation_status)

        controls = QHBoxLayout()
        self.rescan_button = QPushButton("Rescan")
        self.rescan_button.clicked.connect(self.rescan)
        close_button = QPushButton("Continue to Senpai" if self.first_run else "Close")
        close_button.clicked.connect(self.accept)
        controls.addWidget(self.rescan_button)
        controls.addStretch()
        controls.addWidget(close_button)
        root.addLayout(controls)

    @staticmethod
    def _status_html(state: str, detail: str, owned: bool = False) -> str:
        colors = {
            "ready": "#62d38b",
            "missing": "#f2ba52",
            "unsupported": "#ff7a85",
            "stopped": "#f2ba52",
        }
        color = colors.get(state, "#c7cad7")
        ownership = " · installed by Senpai" if owned else ""
        return (
            f"<span style='color:{color}'><b>{html.escape(state.upper())}</b></span> — "
            f"{html.escape(detail)}{ownership}"
        )

    def _set_busy(self, busy: bool, text: str = "") -> None:
        self._busy = busy
        for button in (
            self.rescan_button,
            self.install_python_button,
            self.choose_python_button,
            self.install_ollama_button,
            self.choose_ollama_button,
            self.start_ollama_button,
            self.download_model_button,
            self.exact_model_button,
        ):
            button.setEnabled(not busy)
        if text:
            self.operation_status.setText(text)
        if not busy and self.report is not None:
            self.install_python_button.setEnabled(not self.report.python.ready)
            self.install_ollama_button.setEnabled(not self.report.ollama.ready)
            self.start_ollama_button.setEnabled(
                self.report.ollama.ready and not self.report.ollama_api.ready
            )
            self.download_model_button.setEnabled(self.report.ollama_api.ready)
            self.exact_model_button.setEnabled(self.report.ollama_api.ready)

    def _scan_task(self, signals):
        return scan_environment(
            configured_python=self.settings.python_executable,
            configured_ollama=self.settings.ollama_executable,
            disk_path=self.data_path,
        )

    def rescan(self) -> None:
        if self._busy:
            return
        self._set_busy(
            True, "Scanning installed components without changing the computer…"
        )
        task = Task(self._scan_task)
        task.signals.result.connect(self._scan_complete)
        task.signals.error.connect(self._task_error)
        task.signals.finished.connect(lambda: self._set_busy(False))
        self.thread_pool.start(task)

    def _scan_complete(self, value: object) -> None:
        if not isinstance(value, EnvironmentReport):
            return
        self.report = value
        python_owned = bool(
            (record := self.manifest.get("python-runtime"))
            and record.installed_by_senpai
        )
        ollama_owned = bool(
            (record := self.manifest.get("ollama")) and record.installed_by_senpai
        )
        self.python_status.setText(
            self._status_html(value.python.state, value.python.detail, python_owned)
        )
        self.ollama_status.setText(
            self._status_html(value.ollama.state, value.ollama.detail, ollama_owned)
        )
        self.api_status.setText(
            self._status_html(value.ollama_api.state, value.ollama_api.detail)
        )
        model_detail = (
            ", ".join(value.models)
            if value.models
            else "No local model installed; chat remains disabled."
        )
        self.models_status.setText(
            self._status_html("ready" if value.models else "missing", model_detail)
        )
        self.disk_status.setText(
            f"{value.free_disk_bytes / (1024**3):.1f} GB available"
        )
        self.install_python_button.setVisible(not value.python.ready)
        self.install_ollama_button.setVisible(not value.ollama.ready)
        self.start_ollama_button.setVisible(
            value.ollama.ready and not value.ollama_api.ready
        )
        self.download_model_button.setEnabled(value.ollama_api.ready and not self._busy)
        self.exact_model_button.setEnabled(value.ollama_api.ready and not self._busy)

        self.active_model_combo.blockSignals(True)
        self.active_model_combo.clear()
        self.active_model_combo.addItems(value.models)
        if self.settings.model in value.models:
            self.active_model_combo.setCurrentText(self.settings.model)
        self.active_model_combo.setEnabled(bool(value.models))
        self.active_model_combo.blockSignals(False)

        settings_changed = False
        if value.python.ready and self.settings.python_executable != value.python.path:
            self.settings.python_executable = value.python.path
            settings_changed = True
        if value.ollama.ready and self.settings.ollama_executable != value.ollama.path:
            self.settings.ollama_executable = value.ollama.path
            self.ollama.executable = value.ollama.path
            settings_changed = True
        if settings_changed:
            self.settings.save(self.settings_path)
            self.environment_changed.emit()
        self.operation_status.setText("Scan complete. No installation was performed.")

    def _task_error(self, message: str) -> None:
        self.operation_status.setText(message)
        QMessageBox.critical(self, "Setup operation failed", message)

    def _run_install(self, component: str) -> None:
        coordinator = InstallCoordinator(self.manifest)

        def operation(signals):
            signals.status.emit(
                f"Installing {component} from its exact official package…"
            )
            if component == "Ollama":
                return coordinator.install_ollama(self.settings.ollama_executable)
            return coordinator.install_python(self.settings.python_executable)

        self._set_busy(True, f"Installing {component}…")
        task = Task(operation)
        task.signals.status.connect(self.operation_status.setText)
        task.signals.result.connect(self._install_complete)
        task.signals.error.connect(self._task_error)
        task.signals.finished.connect(lambda: self._set_busy(False))
        task.signals.finished.connect(self.rescan)
        self.thread_pool.start(task)

    def _install_complete(self, value: object) -> None:
        if not isinstance(value, InstallOutcome):
            return
        if value.component_id == "ollama" and value.path:
            self.settings.ollama_executable = value.path
            self.ollama.executable = value.path
        if value.component_id == "python-runtime" and value.path:
            self.settings.python_executable = value.path
        self.settings.save(self.settings_path)
        self.environment_changed.emit()
        self.operation_status.setText(value.detail)

    def install_ollama(self) -> None:
        choice = QMessageBox.question(
            self,
            "Install official Ollama",
            "Senpai will ask Windows Package Manager for the exact Ollama.Ollama package from "
            "the official winget source. WinGet performs package hash verification.\n\n"
            "Install it now?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )
        if choice == QMessageBox.Yes:
            self._run_install("Ollama")

    def install_python(self) -> None:
        choice = QMessageBox.question(
            self,
            "Install official Python",
            "Senpai will install the official Python Install Manager from Microsoft's Store source, "
            "then install the same Python major/minor version used to build Senpai. The runtime is "
            "needed only for running workspace Python files.\n\nInstall it now?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )
        if choice == QMessageBox.Yes:
            self._run_install("Python")

    def choose_python(self) -> None:
        path, _ = QFileDialog.getOpenFileName(
            self,
            "Choose Python interpreter",
            filter="Python executable (python.exe);;Executables (*.exe);;All files (*)",
        )
        if not path:
            return
        status = detect_python(path)
        if not status.ready:
            QMessageBox.warning(self, "Unsupported Python", status.detail)
            return
        self.settings.python_executable = status.path
        self.settings.save(self.settings_path)
        self.environment_changed.emit()
        self.rescan()

    def choose_ollama(self) -> None:
        path, _ = QFileDialog.getOpenFileName(
            self,
            "Choose Ollama executable",
            filter="Ollama executable (ollama.exe);;Executables (*.exe);;All files (*)",
        )
        if not path:
            return
        status = detect_ollama(path)
        if not status.ready:
            QMessageBox.warning(self, "Invalid Ollama executable", status.detail)
            return
        self.settings.ollama_executable = status.path
        self.ollama.executable = status.path
        self.settings.save(self.settings_path)
        self.environment_changed.emit()
        self.rescan()

    def start_ollama(self) -> None:
        def operation(signals):
            signals.status.emit("Starting the configured local Ollama service…")
            self.ollama.executable = self.settings.ollama_executable
            self.ollama.start_hidden()
            return True

        self._set_busy(True, "Starting Ollama…")
        task = Task(operation)
        task.signals.status.connect(self.operation_status.setText)
        task.signals.error.connect(self._task_error)
        task.signals.finished.connect(lambda: self._set_busy(False))
        task.signals.finished.connect(self.rescan)
        self.thread_pool.start(task)

    def _update_model_detail(self) -> None:
        name = self.recommended_model_combo.currentData()
        model = model_by_name(str(name))
        if model is None:
            self.model_detail.clear()
            return
        self.model_detail.setHtml(
            f"<b>{html.escape(model.name)}</b><br>"
            f"{html.escape(model.purpose)}<br>"
            f"Publisher: {html.escape(model.publisher)} · License: {html.escape(model.license_name)} · "
            f"Approximate download: {model.approximate_download_gb:g} GB<br>"
            f"{html.escape(model.memory_note)} · "
            f"<a href='{html.escape(model.official_url)}'>Official listing</a>"
        )

    def download_recommended_model(self) -> None:
        self._confirm_and_download_model(
            str(self.recommended_model_combo.currentData())
        )

    def download_exact_model(self) -> None:
        model, accepted = QInputDialog.getText(
            self,
            "Advanced model name",
            "Enter an exact local Ollama model name. Verify it in Ollama's official model library first:",
        )
        model = model.strip()
        if accepted and model:
            self._confirm_and_download_model(model)

    def _confirm_and_download_model(self, name: str) -> None:
        if (
            not name
            or any(character.isspace() for character in name)
            or name.casefold().endswith("-cloud")
        ):
            QMessageBox.warning(
                self,
                "Invalid local model",
                "Choose a valid non-cloud model name without spaces.",
            )
            return
        model = model_by_name(name)
        if model:
            required_bytes = int((model.approximate_download_gb + 2.0) * (1024**3))
            if (
                self.report
                and self.report.free_disk_bytes
                and self.report.free_disk_bytes < required_bytes
            ):
                QMessageBox.warning(
                    self,
                    "Not enough free disk space",
                    f"{model.name} is approximately {model.approximate_download_gb:g} GB. "
                    "Senpai also reserves 2 GB of working space. Free disk space before "
                    "downloading or choose a smaller model.",
                )
                return
            description = (
                f"Exact model: {model.name}\nPublisher: {model.publisher}\n"
                f"License: {model.license_name}\nApproximate download: {model.approximate_download_gb:g} GB"
            )
        else:
            description = (
                f"Exact model: {name}\n\nThis name is not in Senpai's reviewed list. "
                f"Verify it at {OLLAMA_MODELS_URL} before continuing."
            )
        choice = QMessageBox.question(
            self,
            "Download local model",
            f"{description}\n\nDownload through the local Ollama service?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )
        if choice != QMessageBox.Yes:
            return
        self._download_model(name)

    def _download_model(self, name: str) -> None:
        def operation(signals):
            self.ollama.executable = self.settings.ollama_executable
            self.ollama.model = name
            if not self.ollama.is_ready():
                self.ollama.start_hidden()
            canonical_name = canonical_installed_model(
                name, self.ollama.installed_models()
            )
            if canonical_name:
                return canonical_name
            self.ollama.pull_model(name, signals.status.emit)
            canonical_name = canonical_installed_model(
                name, self.ollama.installed_models()
            )
            if not canonical_name:
                raise RuntimeError(
                    "Ollama finished the download request, but the exact model was not found "
                    "in the local inventory."
                )
            self._record_model_install(canonical_name)
            return canonical_name

        self._set_busy(True, f"Downloading {name}…")
        task = Task(operation)
        task.signals.status.connect(self.operation_status.setText)
        task.signals.error.connect(self._task_error)
        task.signals.result.connect(
            lambda value: self._model_download_complete(str(value))
        )
        task.signals.finished.connect(lambda: self._set_busy(False))
        task.signals.finished.connect(self.rescan)
        self.thread_pool.start(task)

    def _record_model_install(self, name: str) -> None:
        model = model_by_name(name)
        self.manifest.record(
            ComponentRecord(
                component_id=f"ollama-model:{name}",
                kind="model",
                version=name,
                source=f"ollama-registry:{name}",
                install_method="ollama-local-api-explicit-consent",
                installed_by_senpai=True,
                previously_present=False,
                path=name,
                verification=(
                    "Ollama reported download completion and the exact model appeared "
                    "in the local inventory"
                ),
                removal_policy="confirmation-required",
                metadata={
                    "official_url": model.official_url
                    if model
                    else OFFICIAL_MODEL_LIBRARY_URL,
                    "approximate_download_gb": model.approximate_download_gb
                    if model
                    else None,
                },
            )
        )

    def _model_download_complete(self, name: str) -> None:
        self.settings.model = name
        self.ollama.model = name
        self.settings.save(self.settings_path)
        self.environment_changed.emit()
        self.operation_status.setText(f"Model ready: {name}")

    def select_active_model(self, model: str) -> None:
        if not model or model == self.settings.model:
            return
        self.settings.model = model
        self.settings.save(self.settings_path)
        self.environment_changed.emit()

    def _mark_seen(self) -> None:
        if not self.settings.setup_wizard_seen:
            self.settings.setup_wizard_seen = True
            self.settings.save(self.settings_path)

    def accept(self) -> None:
        self._mark_seen()
        super().accept()

    def reject(self) -> None:
        self._mark_seen()
        super().reject()

    def closeEvent(self, event: QCloseEvent) -> None:
        self._mark_seen()
        super().closeEvent(event)
