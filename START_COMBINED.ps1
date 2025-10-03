# FreedomAI + InfoFi Combined Startup Script

Write-Host "🚀 Starting FreedomAI + InfoFi Combined Platform" -ForegroundColor Cyan
Write-Host "=================================================" -ForegroundColor Cyan
Write-Host ""

# Function to check if port is in use
function Test-Port {
    param($Port)
    $connection = Test-NetConnection -ComputerName localhost -Port $Port -WarningAction SilentlyContinue
    return $connection.TcpTestSucceeded
}

# Function to stop process on port
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
Stop-PortProcess 8000  # InfoFi Backend
Stop-PortProcess 8001  # FreedomAI Backend (if exists)
Stop-PortProcess 3000  # InfoFi Frontend
Stop-PortProcess 3001  # FreedomAI Frontend (if exists)

Write-Host ""
Write-Host "🔮 Starting InfoFi Backend (DeFi Intelligence)..." -ForegroundColor Cyan
Write-Host "=================================================" -ForegroundColor Cyan

# Start InfoFi Backend
$infofiBackendPath = Join-Path $PSScriptRoot "backend"
$infofiBackendJob = Start-Job -ScriptBlock {
    param($path)
    Set-Location $path
    
    # Activate virtual environment if it exists
    if (Test-Path "venv\Scripts\Activate.ps1") {
        & .\venv\Scripts\Activate.ps1
    }
    
    # Start InfoFi backend
    python -m uvicorn api.main_simple:app --host 0.0.0.0 --port 8000 --reload
} -ArgumentList $infofiBackendPath

Write-Host "[OK] InfoFi Backend starting on http://localhost:8000" -ForegroundColor Green

# Check if FreedomAI backend exists
$freedomaiBackendPath = Join-Path $PSScriptRoot "freedomai-backend"
if (Test-Path $freedomaiBackendPath) {
    Write-Host ""
    Write-Host "🤖 Starting FreedomAI Backend..." -ForegroundColor Magenta
    Write-Host "=================================" -ForegroundColor Magenta
    
    $freedomaiBackendJob = Start-Job -ScriptBlock {
        param($path)
        Set-Location $path
        # Add your FreedomAI backend startup commands here
        # Example: python app.py --port 8001
    } -ArgumentList $freedomaiBackendPath
    
    Write-Host "[OK] FreedomAI Backend starting on http://localhost:8001" -ForegroundColor Green
}

# Wait for InfoFi backend to be ready
Write-Host ""
Write-Host "Waiting for InfoFi backend to be ready..." -ForegroundColor Yellow
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
    Write-Host "[OK] InfoFi Backend is ready!" -ForegroundColor Green
} else {
    Write-Host "⚠️  InfoFi Backend may still be starting..." -ForegroundColor Yellow
}

Write-Host ""
Write-Host "🌐 Starting InfoFi Frontend (Dashboard)..." -ForegroundColor Cyan
Write-Host "===========================================" -ForegroundColor Cyan

# Start InfoFi Frontend
$infofiFrontendPath = Join-Path $PSScriptRoot "frontend\web-app"
$infofiFrontendJob = Start-Job -ScriptBlock {
    param($path)
    Set-Location $path
    npm run dev
} -ArgumentList $infofiFrontendPath

Write-Host "[OK] InfoFi Frontend starting on http://localhost:5173" -ForegroundColor Green

# Check if FreedomAI frontend exists
$freedomaiFrontendPath = Join-Path $PSScriptRoot "freedomai-frontend"
if (Test-Path $freedomaiFrontendPath) {
    Write-Host ""
    Write-Host "🎨 Starting FreedomAI Frontend..." -ForegroundColor Magenta
    Write-Host "=================================" -ForegroundColor Magenta
    
    $freedomaiFrontendJob = Start-Job -ScriptBlock {
        param($path)
        Set-Location $path
        # Add your FreedomAI frontend startup commands here
        # Example: npm run dev --port 3001
    } -ArgumentList $freedomaiFrontendPath
    
    Write-Host "[OK] FreedomAI Frontend starting on http://localhost:3001" -ForegroundColor Green
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "🚀 Combined Platform is Starting!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "🌐 Access Points:" -ForegroundColor Cyan
Write-Host "   InfoFi API:       http://localhost:8000" -ForegroundColor White
Write-Host "   InfoFi Docs:      http://localhost:8000/docs" -ForegroundColor White
Write-Host "   InfoFi Dashboard: http://localhost:5173" -ForegroundColor White
if (Test-Path $freedomaiBackendPath) {
    Write-Host "   FreedomAI API:    http://localhost:8001" -ForegroundColor White
}
if (Test-Path $freedomaiFrontendPath) {
    Write-Host "   FreedomAI UI:     http://localhost:3001" -ForegroundColor White
}
Write-Host ""
Write-Host "📊 Features Available:" -ForegroundColor Cyan
Write-Host "   🔮 InfoFi: DeFi Intelligence, Whale Tracking, AI Signals" -ForegroundColor White
Write-Host "   🤖 FreedomAI: Your existing AI capabilities" -ForegroundColor White
Write-Host "   🔗 Integration: Cross-platform data sharing" -ForegroundColor White
Write-Host ""
Write-Host "📚 Documentation:" -ForegroundColor Cyan
Write-Host "   See INTEGRATION_GUIDE.md for details" -ForegroundColor White
Write-Host ""
Write-Host "Monitoring services... (Press Ctrl+C to stop)" -ForegroundColor Yellow
Write-Host ""

# Monitor jobs
try {
    while ($true) {
        # Check InfoFi backend
        $infofiBackendState = (Get-Job -Id $infofiBackendJob.Id).State
        if ($infofiBackendState -eq "Failed") {
            Write-Host "❌ InfoFi Backend failed!" -ForegroundColor Red
            Receive-Job -Id $infofiBackendJob.Id
            break
        }
        
        # Check InfoFi frontend
        $infofiFrontendState = (Get-Job -Id $infofiFrontendJob.Id).State
        if ($infofiFrontendState -eq "Failed") {
            Write-Host "❌ InfoFi Frontend failed!" -ForegroundColor Red
            Receive-Job -Id $infofiFrontendJob.Id
            break
        }
        
        # Show recent output
        $infofiBackendOutput = Receive-Job -Id $infofiBackendJob.Id -Keep | Select-Object -Last 3
        $infofiFrontendOutput = Receive-Job -Id $infofiFrontendJob.Id -Keep | Select-Object -Last 3
        
        if ($infofiBackendOutput) {
            Write-Host "[InfoFi Backend] " -ForegroundColor Blue -NoNewline
            Write-Host ($infofiBackendOutput -join "`n")
        }
        
        if ($infofiFrontendOutput) {
            Write-Host "[InfoFi Frontend] " -ForegroundColor Magenta -NoNewline
            Write-Host ($infofiFrontendOutput -join "`n")
        }
        
        Start-Sleep -Seconds 10
    }
} finally {
    Write-Host ""
    Write-Host "Stopping all services..." -ForegroundColor Yellow
    
    Stop-Job -Id $infofiBackendJob.Id -ErrorAction SilentlyContinue
    Stop-Job -Id $infofiFrontendJob.Id -ErrorAction SilentlyContinue
    
    if ($freedomaiBackendJob) {
        Stop-Job -Id $freedomaiBackendJob.Id -ErrorAction SilentlyContinue
    }
    if ($freedomaiFrontendJob) {
        Stop-Job -Id $freedomaiFrontendJob.Id -ErrorAction SilentlyContinue
    }
    
    Remove-Job -Id $infofiBackendJob.Id -Force -ErrorAction SilentlyContinue
    Remove-Job -Id $infofiFrontendJob.Id -Force -ErrorAction SilentlyContinue
    
    if ($freedomaiBackendJob) {
        Remove-Job -Id $freedomaiBackendJob.Id -Force -ErrorAction SilentlyContinue
    }
    if ($freedomaiFrontendJob) {
        Remove-Job -Id $freedomaiFrontendJob.Id -Force -ErrorAction SilentlyContinue
    }
    
    Write-Host "All services stopped" -ForegroundColor Green
}
