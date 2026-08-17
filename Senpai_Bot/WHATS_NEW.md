# Senpai_Bot 0.0.4 — Automatic Updates

Welcome to the first substantial Senpai_Bot IDE build.

> Development preview: no public application-release channel is enabled.

## Automatic application updates

- Senpai_Bot checks the latest published GitHub Release during launch.
- A newer version presents a one-click update confirmation.
- The installer and its companion SHA-256 file download directly from the GitHub Release.
- Senpai_Bot verifies the complete installer before Windows is allowed to run it.
- The verified installer updates the application silently and reopens Senpai_Bot.
- Offline startup remains unaffected, and an update is never installed without confirmation.
- **Help → Check for updates…** provides an immediate visible status whenever you want to test it.

## New features

- Integrated, persistent PowerShell terminal with command history, restart, and clear controls.
- Python editor line numbers and current-line highlighting.
- Explorer toolbar for opening a folder and creating files or folders.
- Explorer right-click actions for new files, new folders, rename, and guarded deletion.
- Editor, Terminal, Output, and Problems surfaces in one desktop workspace.
- IDE toolbar, common editing shortcuts, cursor position, encoding, and indentation status.
- Ollama model picker that discovers locally installed models.
- Model refresh and explicit model-pull controls with visible progress.
- Launch-time and on-demand application update checks through verified GitHub Releases.

## Fixes

- The editor now opens into useful release information instead of a blank untitled tab.
- Unsaved editor tabs are protected when closing the tab or application.
- Renaming an open file updates its editor tab path.
- The installer now prevents concurrent duplicate setup instances.
- Application, installer, package, and update-manifest versions are checked for consistency.

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
