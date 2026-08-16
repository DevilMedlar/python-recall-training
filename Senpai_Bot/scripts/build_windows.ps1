$ErrorActionPreference = "Stop"
Set-Location (Split-Path -Parent $PSScriptRoot)

if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    throw "Python 3.11 or newer is required to build Senpai_Bot."
}

python -m venv .build-venv
& .\.build-venv\Scripts\python.exe -m pip install --upgrade pip
& .\.build-venv\Scripts\python.exe -m pip install ".[build]"
& .\.build-venv\Scripts\pyinstaller.exe --noconfirm --clean .\Senpai_Bot.spec

if (Get-Command ISCC.exe -ErrorAction SilentlyContinue) {
    ISCC.exe .\installer\Senpai_Bot.iss
} else {
    Write-Warning "Inno Setup 6 is not installed; portable build is ready in dist\Senpai_Bot."
}
