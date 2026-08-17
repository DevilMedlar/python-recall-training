$ErrorActionPreference = "Stop"
Set-Location (Split-Path -Parent $PSScriptRoot)

if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    throw "Python 3.11 or newer is required to build Senpai_Bot."
}

python -m venv .build-venv
& .\.build-venv\Scripts\python.exe -m pip install --upgrade pip
& .\.build-venv\Scripts\python.exe -m pip install ".[build]"
& .\.build-venv\Scripts\pyinstaller.exe --noconfirm --clean .\Senpai_Bot.spec

$isccCommand = Get-Command ISCC.exe -ErrorAction SilentlyContinue
$isccPath = if ($isccCommand) { $isccCommand.Source } else { $null }

if (-not $isccPath) {
    $isccCandidates = @(
        (Join-Path $env:LOCALAPPDATA "Programs\Inno Setup 6\ISCC.exe"),
        (Join-Path ${env:ProgramFiles(x86)} "Inno Setup 6\ISCC.exe"),
        (Join-Path $env:ProgramFiles "Inno Setup 6\ISCC.exe")
    )
    $isccPath = $isccCandidates | Where-Object { Test-Path $_ } | Select-Object -First 1
}

if ($isccPath) {
    Write-Host "Building installer with $isccPath"
    & $isccPath .\installer\Senpai_Bot.iss
} else {
    Write-Warning "Inno Setup 6 is not installed; portable build is ready in dist\Senpai_Bot."
}
