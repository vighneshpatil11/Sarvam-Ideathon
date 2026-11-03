# SAARTHI One-Click Startup Script for Windows PowerShell
$ErrorActionPreference = "Stop"

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   Starting SAARTHI Full-Stack Platform " -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

$Root = Resolve-Path "$PSScriptRoot\.."
$ToolsNode = "$Root\..\tools\node"

# 1. Add tools to PATH if present
if (Test-Path $ToolsNode) {
    $env:PATH = "$ToolsNode;$env:PATH"
}
$env:PATH = "$env:APPDATA\Python\Python314\Scripts;$env:PATH"

# 2. Check Python
Write-Host "[1/3] Checking Backend Python environment..." -ForegroundColor Green
cd "$Root\backend"

# 3. Start Backend in separate process
Write-Host "[2/3] Launching FastAPI Backend on http://127.0.0.1:8000..." -ForegroundColor Green
$BackendJob = Start-Process -FilePath "python" -ArgumentList "-m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload" -PassThru -NoNewWindow

Start-Sleep -Seconds 2

# 4. Start Frontend
Write-Host "[3/3] Launching Next.js Frontend on http://localhost:3000..." -ForegroundColor Green
cd "$Root\frontend"

Write-Host "========================================" -ForegroundColor Yellow
Write-Host " SAARTHI is LIVE:" -ForegroundColor Yellow
Write-Host "   Frontend: http://localhost:3000" -ForegroundColor White
Write-Host "   Backend API: http://127.0.0.1:8000" -ForegroundColor White
Write-Host "   API Docs (Swagger): http://127.0.0.1:8000/docs" -ForegroundColor White
Write-Host "========================================" -ForegroundColor Yellow

& npm run dev
