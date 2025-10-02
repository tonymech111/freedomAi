# InfoFi Platform - Complete Installation and Startup Script
# This script installs dependencies and starts the platform

Write-Host "🔮 InfoFi Platform - Complete Setup & Start" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

$projectRoot = $PSScriptRoot

# Check Python
Write-Host "Checking Python..." -ForegroundColor Yellow
$pythonInstalled = Get-Command python -ErrorAction SilentlyContinue
if (!$pythonInstalled) {
    Write-Host "❌ Python not found! Please install Python 3.11+" -ForegroundColor Red
    exit 1
}
$pythonVersion = python --version
Write-Host "✅ $pythonVersion" -ForegroundColor Green

# Check Node.js
Write-Host "Checking Node.js..." -ForegroundColor Yellow
$nodeInstalled = Get-Command node -ErrorAction SilentlyContinue
if (!$nodeInstalled) {
    Write-Host "❌ Node.js not found! Please install Node.js 18+" -ForegroundColor Red
    exit 1
}
$nodeVersion = node --version
Write-Host "✅ Node.js $nodeVersion" -ForegroundColor Green

Write-Host ""
Write-Host "Setting up Backend..." -ForegroundColor Cyan
Write-Host "=====================" -ForegroundColor Cyan

Set-Location (Join-Path $projectRoot "backend")

# Create virtual environment if it doesn't exist
if (!(Test-Path "venv")) {
    Write-Host "Creating virtual environment..." -ForegroundColor Yellow
    python -m venv venv
    Write-Host "✅ Virtual environment created" -ForegroundColor Green
}

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
& .\venv\Scripts\Activate.ps1

if ($LASTEXITCODE -ne 0) {
    Write-Host "Setting execution policy..." -ForegroundColor Yellow
    Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser -Force
    & .\venv\Scripts\Activate.ps1
}

# Install minimal dependencies
Write-Host "Installing backend dependencies..." -ForegroundColor Yellow
pip install --quiet --upgrade pip
pip install --quiet fastapi uvicorn pydantic pydantic-settings aiohttp python-dotenv

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Backend dependencies installed" -ForegroundColor Green
} else {
    Write-Host "⚠️  Some dependencies may have issues, but continuing..." -ForegroundColor Yellow
}

# Create .env if it doesn't exist
if (!(Test-Path ".env")) {
    Write-Host "Creating backend .env file..." -ForegroundColor Yellow
    @"
APP_NAME=InfoFi Platform
APP_VERSION=1.0.0
DEBUG=true
ENVIRONMENT=development
SECRET_KEY=dev-secret-key-change-in-production
TON_API_KEY=demo_mode
"@ | Out-File -FilePath .env -Encoding utf8
    Write-Host "✅ Backend .env created" -ForegroundColor Green
}

Set-Location $projectRoot

Write-Host ""
Write-Host "Setting up Frontend..." -ForegroundColor Cyan
Write-Host "======================" -ForegroundColor Cyan

Set-Location (Join-Path $projectRoot "frontend\web-app")

# Install frontend dependencies
if (!(Test-Path "node_modules")) {
    Write-Host "Installing frontend dependencies (this may take a few minutes)..." -ForegroundColor Yellow
    npm install --silent
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Frontend dependencies installed" -ForegroundColor Green
    } else {
        Write-Host "⚠️  Some frontend dependencies may have issues" -ForegroundColor Yellow
    }
} else {
    Write-Host "✅ Frontend dependencies already installed" -ForegroundColor Green
}

# Create .env.local if it doesn't exist
if (!(Test-Path ".env.local")) {
    Write-Host "Creating frontend .env.local file..." -ForegroundColor Yellow
    @"
VITE_API_URL=http://localhost:8000
"@ | Out-File -FilePath .env.local -Encoding utf8
    Write-Host "✅ Frontend .env.local created" -ForegroundColor Green
}

Set-Location $projectRoot

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "✅ Setup Complete! Starting Platform..." -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""

# Start the platform
& (Join-Path $projectRoot "START.ps1")
