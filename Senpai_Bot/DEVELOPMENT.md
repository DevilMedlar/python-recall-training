# Senpai_Bot desktop application

Senpai_Bot is a native Windows desktop IDE and local AI tutor. The application preserves
`README.md`, `rules.md`, and `SECURITY.md` as its authoritative contract, starts Ollama without
a visible terminal, discovers installed local models, and exposes a file explorer, tabbed Python
editor, run/output panel, and streaming chat. Its first-run setup scans without changing the
computer, and every runtime or model install requires a separate default-No confirmation.

## Runtime prerequisites

- Windows 10 or Windows 11 (64-bit)
- [Python 3.11+](https://www.python.org/downloads/windows/) for **Run Python File**
- [Ollama for Windows](https://ollama.com/download/windows) for local chat
- Enough disk/RAM for the explicitly selected local model

The packaged Senpai_Bot application is self-contained; external Python is not required merely to
open it. On first launch, Setup & Dependencies detects Python and Ollama without invoking Microsoft
Store aliases or changing the system. On Windows, the user can explicitly approve exact-package
installs through WinGet or skip them and use official manual links. The same window remains
available from the Tools menu for later rescans.

Ollama is intentionally a separately installed dependency. Senpai_Bot locates `ollama.exe`,
launches `ollama serve` with no console window when needed, binds it to `127.0.0.1:11434`, and
disables Ollama cloud features for the process it starts. Model pulls use the local API only after
an explicit user confirmation. Exact packages are verified by their official package manager, and
the resulting executable is detected before ownership is recorded.

## Run from source

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -e ".[test]"
.\.venv\Scripts\python.exe -m senpai_bot
```

PowerShell script activation is not required.

## Tests

```powershell
.\.venv\Scripts\python.exe -m pytest
```

## Build the Windows app and installer

Install Python 3.11+ and Inno Setup 6 from their official sources, then run:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\build_windows.ps1
```

The portable app is written to `dist\Senpai_Bot`. When `ISCC.exe` is available, the Start
Menu installer is written to `dist\installer`.

## Contract handling

The three Markdown files remain unmodified. Every turn receives a bounded persona-first system
prompt plus verbatim sections selected from the contract for the current request. This avoids
repeating roughly 205 KB on every exchange while keeping the source contract authoritative.
No application-level response filter or persona rewriter is installed.

Update checks on launch default to off and can be changed from the Help menu. The Help menu retains
an explicit on-demand check against the repository's latest GitHub Release. A newer semantic
version can open only the exact `DevilMedlar/python-recall-training` release page. Installer
download and execution have been removed until publisher-signature verification is implemented.
Version 0.0.4 is development source only. No public application release or public release workflow
is installed. The obsolete `update.json` channel has been removed, so installed 0.0.3 copies cannot
be directed to an unpublished development build. A future distribution channel must be explicitly
approved before it is enabled.

Version 0.0.4 includes the first IDE-core interface: a numbered Python editor with current-line
highlighting, an explorer toolbar and guarded context actions, a persistent integrated PowerShell
session with command history, terminal/output/problems tabs, common editing shortcuts, a main
toolbar, and cursor/encoding status indicators. It is an IDE foundation, not a claim of full
Visual Studio Code feature parity.

The initial editor tab is the bundled `WHATS_NEW.md` release brief. Chat includes an Ollama model
picker populated from the local `/api/tags` endpoint, a refresh action, and a link to the explicit
setup/download flow.
If the configured model is unavailable but other local models exist, the app selects an installed
model instead of forcing a download. If no models exist, chat remains disabled until the user opens
Setup & Dependencies and explicitly approves an exact model. Ollama itself remains
separately maintained because its Windows installer tracks hardware/runtime compatibility; model
weights are deliberately not duplicated inside every Senpai_Bot application update. Cloud-suffixed
Ollama models are excluded from discovery and rejected by the pull and chat paths.

Successful Senpai-initiated dependency and model installations are written atomically to
`ownership.json` in the application data directory. Pre-existing components are never claimed.
This manifest is the ownership boundary for the future selective complete-uninstall work.

Only one Senpai_Bot application instance can run per user session. A second launch exits after an
already-running notice. When Senpai_Bot starts its own Ollama server, that exact owned process is
stopped on application exit; a server that was already running is left untouched. The Inno Setup
installer has its own setup mutex, disables application restart, skips the launch entry in silent
mode, and presents a single unchecked finish-page launch choice.
