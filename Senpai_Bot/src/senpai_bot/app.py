from __future__ import annotations

import sys

from PySide6.QtWidgets import QApplication, QMessageBox

from .contract import ContractStore
from .paths import bundle_root, contract_dir, data_dir
from .settings import Settings
from .ui.main_window import MainWindow


STYLE = """
QWidget { background: #171923; color: #e8e9f2; }
QMenuBar, QMenu, QStatusBar { background: #11131b; }
QToolBar { background: #151821; border-bottom: 1px solid #323647; spacing: 6px; padding: 4px; }
QPlainTextEdit, QTextBrowser, QTreeView { background: #10121a; border: 1px solid #323647; }
QLineEdit { background: #10121a; border: 1px solid #454a60; border-radius: 3px; padding: 7px; }
QTreeView::item { padding: 3px; }
QTreeView::item:selected { background: #373d55; }
QTabWidget::pane { border: 1px solid #323647; }
QTabBar::tab { background: #222534; padding: 8px 14px; }
QTabBar::tab:selected { background: #712d91; }
QPushButton { background: #7c36a5; border: 0; border-radius: 5px; padding: 8px 16px; }
QPushButton:hover { background: #984bc2; }
QPushButton:disabled { background: #343747; color: #777b8d; }
QSplitter::handle { background: #2c3040; }
"""


def main() -> int:
    app = QApplication(sys.argv)
    app.setApplicationName("Senpai_Bot")
    app.setOrganizationName("DevilMedlar")
    app.setStyleSheet(STYLE)
    try:
        contract = ContractStore(contract_dir())
    except Exception as exc:
        QMessageBox.critical(None, "Senpai_Bot contract error", str(exc))
        return 1
    settings_path = data_dir() / "settings.json"
    settings = Settings.load(settings_path)
    window = MainWindow(contract, settings, settings_path, bundle_root() / "assets" / "senpai_bot.ico")
    window.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
