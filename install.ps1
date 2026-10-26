param(
    [ValidateSet("all", "codex", "claude")]
    [string]$Provider = "all",
    [string]$Repository = $(if ($env:BOARDROOM_GITHUB_REPOSITORY) { $env:BOARDROOM_GITHUB_REPOSITORY } else { "rshageer/boardroom" })
)

$ErrorActionPreference = "Stop"
$temporary = Join-Path ([System.IO.Path]::GetTempPath()) ("boardroom-" + [System.Guid]::NewGuid())
$archive = Join-Path $temporary "boardroom.zip"
$url = "https://github.com/$Repository/releases/latest/download/boardroom.zip"

try {
    New-Item -ItemType Directory -Path $temporary | Out-Null
    Write-Host "Downloading Boardroom from $url"
    Invoke-WebRequest -Uri $url -OutFile $archive
    Expand-Archive -Path $archive -DestinationPath $temporary
    $installer = Join-Path $temporary "boardroom\scripts\install_global.py"

    if (Get-Command py -ErrorAction SilentlyContinue) {
        & py -3 $installer --provider $Provider
    } elseif (Get-Command python -ErrorAction SilentlyContinue) {
        & python $installer --provider $Provider
    } else {
        throw "Boardroom requires Python 3.10 or later. Install Python and ensure py or python is on PATH."
    }
    if ($LASTEXITCODE -ne 0) {
        throw "Boardroom installation failed with exit code $LASTEXITCODE."
    }
} finally {
    if (Test-Path $temporary) {
        Remove-Item -Recurse -Force $temporary
    }
}
