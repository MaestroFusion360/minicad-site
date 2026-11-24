param(
    [ValidateRange(1, 65535)]
    [int]$Port = 8000
)

$ErrorActionPreference = 'Stop'
Push-Location $PSScriptRoot
$server = $null
$runDirectory = Join-Path ([System.IO.Path]::GetTempPath()) ('minicad-site-' + [guid]::NewGuid().ToString('N'))

try {
    & uv run python tools/build.py
    if ($LASTEXITCODE -ne 0) { throw 'Site build failed.' }

    New-Item -ItemType Directory -Path $runDirectory | Out-Null
    $readyFile = Join-Path $runDirectory 'ready.json'
    $errorFile = Join-Path $runDirectory 'stderr.log'
    $outputFile = Join-Path $runDirectory 'stdout.log'
    $python = Join-Path $PSScriptRoot '.venv\Scripts\python.exe'
    $server = Start-Process -FilePath $python -ArgumentList @(
        '-u', 'tools/serve.py', '--port', "$Port", '--ready-file', ('"' + $readyFile + '"')
    ) -WorkingDirectory $PSScriptRoot -WindowStyle Hidden -PassThru -RedirectStandardOutput $outputFile -RedirectStandardError $errorFile

    $url = $null
    for ($attempt = 0; $attempt -lt 150; $attempt++) {
        $server.Refresh()
        if ($server.HasExited) {
            $details = Get-Content -LiteralPath $errorFile -Raw -ErrorAction SilentlyContinue
            throw "Server exited (code $($server.ExitCode)). $details"
        }
        if (Test-Path -LiteralPath $readyFile) {
            try {
                $state = Get-Content -LiteralPath $readyFile -Raw | ConvertFrom-Json
                $response = Invoke-WebRequest -Uri $state.url -UseBasicParsing -TimeoutSec 2
                if ($response.StatusCode -eq 200 -and $response.Content -match 'MiniCAD') {
                    $url = $state.url
                    break
                }
            } catch {
                # The readiness file may still be in the middle of its first write.
            }
        }
        Start-Sleep -Milliseconds 100
    }
    if (-not $url) { throw "Server startup timed out. Logs: $runDirectory" }

    Start-Process $url
    Write-Host "MiniCAD site: $url"
    Write-Host 'Press Enter to stop the server.'
    Read-Host | Out-Null
} finally {
    if ($null -ne $server) {
        $server.Refresh()
        if (-not $server.HasExited) {
            Stop-Process -Id $server.Id -Force -ErrorAction SilentlyContinue
            $server.WaitForExit()
        }
    }
    Pop-Location
}
