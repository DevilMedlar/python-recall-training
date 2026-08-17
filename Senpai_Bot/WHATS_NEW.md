# Senpai_Bot 0.0.4 — Safety Baseline

Welcome to the first substantial Senpai_Bot IDE build.

> Development preview: no public application-release channel is enabled.

## Application updates

- Update checks on launch are off by default and can be toggled from the Help menu.
- **Help → Check for updates…** remains available for an explicit manual check.
- Only the exact `DevilMedlar/python-recall-training` GitHub Release page is accepted.
- Installer download and execution are disabled until publisher-signature verification exists.
- No public application release or automated release workflow is enabled.

## New features

- Integrated, persistent PowerShell terminal with command history, restart, and clear controls.
- Python editor line numbers and current-line highlighting.
- Explorer toolbar for opening a folder and creating files or folders.
- Explorer right-click actions for new files, new folders, rename, and guarded deletion.
- Editor, Terminal, Output, and Problems surfaces in one desktop workspace.
- IDE toolbar, common editing shortcuts, cursor position, encoding, and indentation status.
- Ollama model picker that discovers locally installed models.
- Model refresh and explicit model-pull controls with visible progress.
- A native one-instance application guard that rejects a second launch with a clear notice.

## Fixes

- The editor now opens into useful release information instead of a blank untitled tab.
- Unsaved editor tabs are protected when closing the tab or application.
- Renaming an open file updates its editor tab path.
- The installer now prevents concurrent duplicate setup instances.
- Application, installer, and package versions are checked for consistency.
- The obsolete update manifest was removed so development source cannot be mistaken for a
  published application release.
- Chat is locked to `127.0.0.1:11434`; saved settings cannot redirect it to a remote endpoint.
- Missing models are never downloaded silently and chat stays disabled until a model is approved.
- Ollama is stopped on exit only when the current Senpai_Bot process launched it.

## Dependencies and models

Senpai_Bot already bundles its Python and Qt application dependencies. Ollama remains a separately
maintained local inference runtime so it can stay compatible with GPU drivers and new model formats.
Model weights are managed by Ollama instead of being copied into every Senpai_Bot installer.

Use the model controls above chat to select any model already installed in Ollama or explicitly pull
another model. Model quality, speed, context size, memory use, and contract-following ability vary.

## Getting started

1. Select **Open Folder** and choose the folder where you want to write Python projects.
2. Use **+ File**, the Explorer context menu, or **Ctrl+N** to create code.
3. Select an installed Ollama model above chat.
4. Use **Ctrl+`** to focus the integrated terminal and **F5** to run the active Python file.
