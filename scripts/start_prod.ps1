// Production start script for SAARTHI app
# Ensure script stops on errors
$ErrorActionPreference = "Stop"

# Paths
$frontendDir = Join-Path $PSScriptRoot "..\frontend"

# Start backend (FastAPI) in a new process
Write-Host "Starting FastAPI backend..."
$backend = Start-Process -FilePath "python" -ArgumentList "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000" -WorkingDirectory (Join-Path $PSScriptRoot "..\backend") -NoNewWindow -PassThru

# Wait a short moment for backend to be ready
Start-Sleep -Seconds 2

# Start Next.js production server
Write-Host "Starting Next.js frontend (production)..."
$frontend = Start-Process -FilePath "npm" -ArgumentList "start" -WorkingDirectory $frontendDir -NoNewWindow -PassThru

Write-Host "Both services are running. Frontend: http://localhost:3000   Backend: http://localhost:8000"

# Wait for processes (optional). Keep script alive until user aborts.
Wait-Process -Id $backend.Id, $frontend.Id
