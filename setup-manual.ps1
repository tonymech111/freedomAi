# InfoFi Platform - Manual Setup Script (Without Docker)
# For users who prefer not to use Docker

Write-Host "🔮 InfoFi Platform - Manual Setup" -ForegroundColor Cyan
Write-Host "==================================" -ForegroundColor Cyan
Write-Host ""

# Check Python
Write-Host "Checking for Python..." -ForegroundColor Yellow
$pythonInstalled = Get-Command python -ErrorAction SilentlyContinue

if (!$pythonInstalled) {
    Write-Host "❌ Python not found!" -ForegroundColor Red
    Write-Host "Please install Python 3.11+ from: https://www.python.org/downloads/" -ForegroundColor Yellow
    $response = Read-Host "Open Python download page? (y/n)"
    if ($response -eq "y" -or $response -eq "Y") {
        Start-Process "https://www.python.org/downloads/"
    }
    exit 1
}

$pythonVersion = python --version
Write-Host "✅ Found: $pythonVersion" -ForegroundColor Green

# Check Node.js
Write-Host "Checking for Node.js..." -ForegroundColor Yellow
$nodeInstalled = Get-Command node -ErrorAction SilentlyContinue

if (!$nodeInstalled) {
    Write-Host "❌ Node.js not found!" -ForegroundColor Red
    Write-Host "Please install Node.js 18+ from: https://nodejs.org/" -ForegroundColor Yellow
    $response = Read-Host "Open Node.js download page? (y/n)"
    if ($response -eq "y" -or $response -eq "Y") {
        Start-Process "https://nodejs.org/"
    }
    exit 1
}

$nodeVersion = node --version
Write-Host "✅ Found Node.js: $nodeVersion" -ForegroundColor Green

Write-Host ""
Write-Host "Setting up Backend..." -ForegroundColor Cyan
Write-Host "=====================" -ForegroundColor Cyan

# Setup Backend
Set-Location backend

# Create virtual environment
if (!(Test-Path "venv")) {
    Write-Host "Creating Python virtual environment..." -ForegroundColor Yellow
    python -m venv venv
    Write-Host "✅ Virtual environment created" -ForegroundColor Green
}

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
& .\venv\Scripts\Activate.ps1

if ($LASTEXITCODE -ne 0) {
    Write-Host "⚠️  Execution policy may be blocking activation" -ForegroundColor Yellow
    Write-Host "Running: Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser" -ForegroundColor Yellow
    Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser -Force
    & .\venv\Scripts\Activate.ps1
}

# Install dependencies
Write-Host "Installing Python dependencies..." -ForegroundColor Yellow
Write-Host "(This may take a few minutes)" -ForegroundColor Gray
pip install --upgrade pip
pip install fastapi uvicorn pydantic pydantic-settings aiohttp python-dotenv

Write-Host "✅ Backend dependencies installed" -ForegroundColor Green

# Create .env file
if (!(Test-Path ".env")) {
    Write-Host "Creating backend .env file..." -ForegroundColor Yellow
    @"
APP_NAME=InfoFi Platform
APP_VERSION=1.0.0
DEBUG=true
ENVIRONMENT=development
SECRET_KEY=dev-secret-key-change-in-production
TON_API_KEY=demo_mode
DATABASE_URL=sqlite:///./infofi.db
REDIS_URL=redis://localhost:6379/0
KAFKA_BOOTSTRAP_SERVERS=localhost:9092
WEAVIATE_URL=http://localhost:8080
"@ | Out-File -FilePath .env -Encoding utf8
    Write-Host "✅ Backend .env created" -ForegroundColor Green
}

Set-Location ..

Write-Host ""
Write-Host "Setting up Frontend..." -ForegroundColor Cyan
Write-Host "======================" -ForegroundColor Cyan

Set-Location frontend\web-app

# Install frontend dependencies
Write-Host "Installing Node.js dependencies..." -ForegroundColor Yellow
Write-Host "(This may take a few minutes)" -ForegroundColor Gray
npm install

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Frontend dependencies installed" -ForegroundColor Green
} else {
    Write-Host "⚠️  Some frontend dependencies may have issues" -ForegroundColor Yellow
}

# Create frontend .env
if (!(Test-Path ".env.local")) {
    Write-Host "Creating frontend .env.local file..." -ForegroundColor Yellow
    @"
VITE_API_URL=http://localhost:8000
"@ | Out-File -FilePath .env.local -Encoding utf8
    Write-Host "✅ Frontend .env.local created" -ForegroundColor Green
}

Set-Location ..\..

Write-Host ""
Write-Host "✅ Setup Complete!" -ForegroundColor Green
Write-Host ""
Write-Host "To start the platform:" -ForegroundColor Cyan
Write-Host ""
Write-Host "1. Start Backend (in terminal 1):" -ForegroundColor Yellow
Write-Host "   cd backend" -ForegroundColor White
Write-Host "   .\venv\Scripts\Activate.ps1" -ForegroundColor White
Write-Host "   python -m uvicorn api.main:app --reload" -ForegroundColor White
Write-Host ""
Write-Host "2. Start Frontend (in terminal 2):" -ForegroundColor Yellow
Write-Host "   cd frontend\web-app" -ForegroundColor White
Write-Host "   npm run dev" -ForegroundColor White
Write-Host ""
Write-Host "3. Access the platform:" -ForegroundColor Yellow
Write-Host "   Backend API: http://localhost:8000/docs" -ForegroundColor White
Write-Host "   Frontend: http://localhost:5173" -ForegroundColor White
Write-Host ""
Write-Host "⚠️  Note: Full functionality requires additional services:" -ForegroundColor Yellow
Write-Host "   - PostgreSQL (database)" -ForegroundColor White
Write-Host "   - Redis (caching)" -ForegroundColor White
Write-Host "   - Kafka (message queue)" -ForegroundColor White
Write-Host "   - Weaviate (vector database)" -ForegroundColor White
Write-Host ""
Write-Host "For full setup, use Docker: .\setup.ps1" -ForegroundColor Cyan
