# InfoFi Platform - Windows Setup Script
# Run this script to automatically set up the platform

Write-Host "🔮 InfoFi Platform - Setup Script" -ForegroundColor Cyan
Write-Host "=================================" -ForegroundColor Cyan
Write-Host ""

# Check if Docker is installed
Write-Host "Checking for Docker..." -ForegroundColor Yellow
$dockerInstalled = Get-Command docker -ErrorAction SilentlyContinue

if ($dockerInstalled) {
    Write-Host "✅ Docker found!" -ForegroundColor Green
    
    # Check if Docker is running
    $dockerRunning = docker info 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Docker is running!" -ForegroundColor Green
        
        Write-Host ""
        Write-Host "Setting up with Docker..." -ForegroundColor Cyan
        
        # Copy .env file
        if (!(Test-Path ".env")) {
            Write-Host "Creating .env file..." -ForegroundColor Yellow
            Copy-Item .env.example .env
            Write-Host "✅ .env file created" -ForegroundColor Green
            Write-Host "⚠️  Please edit .env and add your TON_API_KEY" -ForegroundColor Yellow
            Write-Host "   Get free key from: https://tonapi.io" -ForegroundColor Yellow
        } else {
            Write-Host "✅ .env file already exists" -ForegroundColor Green
        }
        
        Write-Host ""
        Write-Host "Starting Docker services..." -ForegroundColor Yellow
        docker-compose up -d
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host ""
            Write-Host "✅ Services started successfully!" -ForegroundColor Green
            Write-Host ""
            Write-Host "🌐 Access your platform:" -ForegroundColor Cyan
            Write-Host "   API Documentation: http://localhost:8000/docs" -ForegroundColor White
            Write-Host "   Web Dashboard: http://localhost:3000" -ForegroundColor White
            Write-Host "   Health Check: http://localhost:8000/health" -ForegroundColor White
            Write-Host ""
            Write-Host "📊 View logs:" -ForegroundColor Cyan
            Write-Host "   docker-compose logs -f" -ForegroundColor White
            Write-Host ""
            Write-Host "🛑 Stop services:" -ForegroundColor Cyan
            Write-Host "   docker-compose down" -ForegroundColor White
        } else {
            Write-Host "❌ Failed to start services" -ForegroundColor Red
            Write-Host "Check logs with: docker-compose logs" -ForegroundColor Yellow
        }
        
    } else {
        Write-Host "❌ Docker is not running!" -ForegroundColor Red
        Write-Host "Please start Docker Desktop and try again." -ForegroundColor Yellow
        exit 1
    }
    
} else {
    Write-Host "❌ Docker not found!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Please choose a setup option:" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Option 1: Install Docker (Recommended)" -ForegroundColor Cyan
    Write-Host "  1. Download from: https://www.docker.com/products/docker-desktop/" -ForegroundColor White
    Write-Host "  2. Install and restart your computer" -ForegroundColor White
    Write-Host "  3. Run this script again" -ForegroundColor White
    Write-Host ""
    Write-Host "Option 2: Manual Setup (Advanced)" -ForegroundColor Cyan
    Write-Host "  See SETUP_WINDOWS.md for detailed instructions" -ForegroundColor White
    Write-Host ""
    
    # Offer to open Docker download page
    $response = Read-Host "Open Docker download page in browser? (y/n)"
    if ($response -eq "y" -or $response -eq "Y") {
        Start-Process "https://www.docker.com/products/docker-desktop/"
    }
    
    # Offer to show manual setup guide
    $response = Read-Host "Open manual setup guide? (y/n)"
    if ($response -eq "y" -or $response -eq "Y") {
        if (Test-Path "SETUP_WINDOWS.md") {
            notepad SETUP_WINDOWS.md
        }
    }
}

Write-Host ""
Write-Host "For more help, see:" -ForegroundColor Cyan
Write-Host "  - SETUP_WINDOWS.md (detailed setup guide)" -ForegroundColor White
Write-Host "  - README.md (platform overview)" -ForegroundColor White
Write-Host "  - QUICKSTART.md (quick start guide)" -ForegroundColor White
