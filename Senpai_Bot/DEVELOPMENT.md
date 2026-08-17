# Senpai_Bot desktop application

Senpai_Bot is a native Windows desktop IDE and local AI tutor. The application preserves
`README.md`, `rules.md`, and `SECURITY.md` as its authoritative contract, starts Ollama without
a visible terminal, checks for `llama3.1:latest`, and exposes a file explorer, tabbed Python
editor, run/output panel, and streaming chat.

## Runtime prerequisites

- Windows 10 or Windows 11 (64-bit)
- [Ollama for Windows](https://ollama.com/download/windows)
- Enough disk/RAM for `llama3.1:latest`

Ollama is intentionally a separately installed dependency. Senpai_Bot locates the official
`ollama.exe`, launches `ollama serve` with no console window when needed, and pulls the model
through Ollama's local API. It does not download or execute opaque installers.

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

At launch, version 0.0.4 and newer query the repository's latest GitHub Release in a background
thread. The check remains silent when current or offline. When a newer semantic version exists,
the app asks for confirmation, downloads the versioned installer and its SHA-256 sidecar from
approved GitHub HTTPS hosts, verifies the checksum, and launches Inno Setup silently. Unsaved
editors are guarded before the app exits, and the installer relaunches Senpai_Bot when complete.
The Help menu also exposes an on-demand check that confirms when the installed version is current.
The legacy `update.json` manifest intentionally remains at version 0.0.3 so existing installations
stay quiet while 0.0.4 is development source. No public release workflow is installed. A future
distribution channel must be explicitly approved before it is enabled.

Version 0.0.3 adds the first IDE-core interface: a numbered Python editor with current-line
highlighting, an explorer toolbar and guarded context actions, a persistent integrated PowerShell
session with command history, terminal/output/problems tabs, common editing shortcuts, a main
toolbar, and cursor/encoding status indicators. It is an IDE foundation, not a claim of full
Visual Studio Code feature parity.

The initial editor tab is the bundled `WHATS_NEW.md` release brief. Chat includes an Ollama model
picker populated from the local `/api/tags` endpoint, a refresh action, and an explicit pull flow.
If the configured model is unavailable but other local models exist, the app selects an installed
model instead of forcing a `llama3.1:latest` download. If no models exist, it bootstraps the current
default through Ollama. Ollama itself remains separately maintained because its Windows installer
tracks hardware/runtime compatibility; model weights are deliberately not duplicated inside every
Senpai_Bot application update.
