# InfoFi Platform - Quick Start Script
# This script starts both backend and frontend in development mode

Write-Host "🔮 InfoFi Platform - Starting Services" -ForegroundColor Cyan
Write-Host "=======================================" -ForegroundColor Cyan
Write-Host ""

# Function to check if port is in use
function Test-Port {
    param($Port)
    $connection = Test-NetConnection -ComputerName localhost -Port $Port -WarningAction SilentlyContinue
    return $connection.TcpTestSucceeded
}

# Kill processes on ports if needed
function Stop-PortProcess {
    param($Port)
    $process = Get-NetTCPConnection -LocalPort $Port -ErrorAction SilentlyContinue | Select-Object -ExpandProperty OwningProcess -Unique
    if ($process) {
        Write-Host "⚠️  Port $Port is in use. Stopping process..." -ForegroundColor Yellow
        Stop-Process -Id $process -Force -ErrorAction SilentlyContinue
        Start-Sleep -Seconds 2
    }
}

# Check and free ports
Write-Host "Checking ports..." -ForegroundColor Yellow
Stop-PortProcess 8000  # Backend
Stop-PortProcess 5173  # Frontend

Write-Host ""
Write-Host "Starting Backend..." -ForegroundColor Cyan
Write-Host "===================" -ForegroundColor Cyan

# Start Backend
$backendPath = Join-Path $PSScriptRoot "backend"
$backendJob = Start-Job -ScriptBlock {
    param($path)
    Set-Location $path
    
    # Activate virtual environment if it exists
    if (Test-Path "venv\Scripts\Activate.ps1") {
        & .\venv\Scripts\Activate.ps1
    }
    
    # Start backend with simple main
    python -m uvicorn api.main_simple:app --host 0.0.0.0 --port 8000 --reload
} -ArgumentList $backendPath

Write-Host "✅ Backend starting on http://localhost:8000" -ForegroundColor Green

# Wait for backend to start
Write-Host "Waiting for backend to be ready..." -ForegroundColor Yellow
$maxAttempts = 30
$attempt = 0
$backendReady = $false

while ($attempt -lt $maxAttempts -and -not $backendReady) {
    Start-Sleep -Seconds 1
    try {
        $response = Invoke-WebRequest -Uri "http://localhost:8000/health" -TimeoutSec 2 -ErrorAction SilentlyContinue
        if ($response.StatusCode -eq 200) {
            $backendReady = $true
        }
    } catch {
        $attempt++
    }
}

if ($backendReady) {
    Write-Host "✅ Backend is ready!" -ForegroundColor Green
} else {
    Write-Host "⚠️  Backend may still be starting..." -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Starting Frontend..." -ForegroundColor Cyan
Write-Host "====================" -ForegroundColor Cyan

# Start Frontend
$frontendPath = Join-Path $PSScriptRoot "frontend\web-app"
$frontendJob = Start-Job -ScriptBlock {
    param($path)
    Set-Location $path
    npm run dev
} -ArgumentList $frontendPath

Write-Host "✅ Frontend starting on http://localhost:5173" -ForegroundColor Green

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "✅ InfoFi Platform is Starting!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "🌐 Access Points:" -ForegroundColor Cyan
Write-Host "   Backend API:  http://localhost:8000" -ForegroundColor White
Write-Host "   API Docs:     http://localhost:8000/docs" -ForegroundColor White
Write-Host "   Frontend:     http://localhost:5173" -ForegroundColor White
Write-Host ""
Write-Host "📊 View Logs:" -ForegroundColor Cyan
Write-Host "   Backend:  Receive-Job $($backendJob.Id) -Keep" -ForegroundColor White
Write-Host "   Frontend: Receive-Job $($frontendJob.Id) -Keep" -ForegroundColor White
Write-Host ""
Write-Host "🛑 To Stop:" -ForegroundColor Cyan
Write-Host "   Press Ctrl+C or close this window" -ForegroundColor White
Write-Host ""
Write-Host "Monitoring services... (Press Ctrl+C to stop)" -ForegroundColor Yellow
Write-Host ""

# Monitor jobs
try {
    while ($true) {
        # Check if jobs are still running
        $backendState = (Get-Job -Id $backendJob.Id).State
        $frontendState = (Get-Job -Id $frontendJob.Id).State
        
        if ($backendState -eq "Failed") {
            Write-Host "❌ Backend failed! Showing errors:" -ForegroundColor Red
            Receive-Job -Id $backendJob.Id
            break
        }
        
        if ($frontendState -eq "Failed") {
            Write-Host "❌ Frontend failed! Showing errors:" -ForegroundColor Red
            Receive-Job -Id $frontendJob.Id
            break
        }
        
        # Show recent output
        $backendOutput = Receive-Job -Id $backendJob.Id -Keep | Select-Object -Last 5
        $frontendOutput = Receive-Job -Id $frontendJob.Id -Keep | Select-Object -Last 5
        
        if ($backendOutput) {
            Write-Host "[Backend] " -ForegroundColor Blue -NoNewline
            Write-Host ($backendOutput -join "`n")
        }
        
        if ($frontendOutput) {
            Write-Host "[Frontend] " -ForegroundColor Magenta -NoNewline
            Write-Host ($frontendOutput -join "`n")
        }
        
        Start-Sleep -Seconds 5
    }
} finally {
    Write-Host ""
    Write-Host "Stopping services..." -ForegroundColor Yellow
    Stop-Job -Id $backendJob.Id -ErrorAction SilentlyContinue
    Stop-Job -Id $frontendJob.Id -ErrorAction SilentlyContinue
    Remove-Job -Id $backendJob.Id -Force -ErrorAction SilentlyContinue
    Remove-Job -Id $frontendJob.Id -Force -ErrorAction SilentlyContinue
    Write-Host "✅ Services stopped" -ForegroundColor Green
}
