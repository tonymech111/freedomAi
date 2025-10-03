# InfoFi Platform - Windows Setup Guide

## Option 1: Docker Setup (Recommended)

### Step 1: Install Docker Desktop

1. **Download Docker Desktop for Windows**:
   - Visit: https://www.docker.com/products/docker-desktop/
   - Click "Download for Windows"
   - Run the installer

2. **Install and Start Docker**:
   - Follow the installation wizard
   - Restart your computer if prompted
   - Launch Docker Desktop
   - Wait for Docker to start (whale icon in system tray)

3. **Verify Docker Installation**:
   ```powershell
   docker --version
   docker-compose --version
   ```

### Step 2: Setup InfoFi Platform

```powershell
# Navigate to project
cd C:\Users\DATASOFT\CascadeProjects\infofi-platform

# Copy environment file
Copy-Item .env.example .env

# Edit .env file (use notepad or your preferred editor)
notepad .env

# Start all services
docker-compose up -d

# Check services are running
docker-compose ps

# View logs
docker-compose logs -f
```

### Step 3: Access the Platform

- **API Documentation**: http://localhost:8000/docs
- **Web Dashboard**: http://localhost:3000
- **Health Check**: http://localhost:8000/health

---

## Option 2: Manual Setup (Without Docker)

If you prefer not to use Docker, follow these steps:

### Prerequisites

Install these tools first:

1. **Python 3.11+**: https://www.python.org/downloads/
2. **Node.js 18+**: https://nodejs.org/
3. **PostgreSQL 15+**: https://www.postgresql.org/download/windows/
4. **Redis**: https://github.com/microsoftarchive/redis/releases (or use WSL)

### Step 1: Setup PostgreSQL

```powershell
# After installing PostgreSQL, create database
psql -U postgres
CREATE DATABASE infofi;
\q
```

### Step 2: Setup Backend

```powershell
cd C:\Users\DATASOFT\CascadeProjects\infofi-platform\backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
.\venv\Scripts\Activate.ps1

# If you get execution policy error, run:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Install dependencies
pip install -r requirements.txt

# Copy and configure environment
Copy-Item ..\.env.example .env
notepad .env

# Update DATABASE_URL in .env to match your PostgreSQL setup
# DATABASE_URL=postgresql+asyncpg://postgres:YOUR_PASSWORD@localhost:5432/infofi

# Start backend server
python -m uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
```

### Step 3: Setup Frontend (New Terminal)

```powershell
cd C:\Users\DATASOFT\CascadeProjects\infofi-platform\frontend\web-app

# Install dependencies
npm install

# Create .env file
Copy-Item .env.example .env.local

# Add this to .env.local:
# VITE_API_URL=http://localhost:8000

# Start frontend
npm run dev
```

### Step 4: Verify Installation

Open browser and check:
- Backend API: http://localhost:8000/docs
- Frontend: http://localhost:5173 (Vite default port)

---

## Option 3: Minimal Demo Setup (Fastest)

For a quick demo without full infrastructure:

### Step 1: Install Python Dependencies

```powershell
cd C:\Users\DATASOFT\CascadeProjects\infofi-platform\backend

# Create virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1

# Install minimal dependencies
pip install fastapi uvicorn pydantic pydantic-settings aiohttp
```

### Step 2: Create Minimal Config

```powershell
# Create a simple .env file
@"
APP_NAME=InfoFi Platform
DEBUG=true
TON_API_KEY=demo_mode
DATABASE_URL=sqlite:///./infofi.db
"@ | Out-File -FilePath .env -Encoding utf8
```

### Step 3: Run Backend Only

```powershell
# Start backend in demo mode (without database dependencies)
python -m uvicorn api.main:app --reload --port 8000
```

### Step 4: Test API

```powershell
# In a new terminal, test the API
curl http://localhost:8000/health
curl http://localhost:8000/docs
```

---

## Troubleshooting

### Docker Issues

**"docker-compose not recognized"**:
```powershell
# Try with docker compose (no hyphen)
docker compose up -d

# Or install Docker Desktop from scratch
```

**"Docker daemon not running"**:
- Open Docker Desktop application
- Wait for it to fully start (green icon in system tray)

**Port already in use**:
```powershell
# Find process using port 8000
netstat -ano | findstr :8000

# Kill the process (replace PID with actual number)
taskkill /PID <PID> /F
```

### Python Issues

**"python not recognized"**:
- Reinstall Python and check "Add Python to PATH"
- Or use full path: `C:\Python311\python.exe`

**Virtual environment activation fails**:
```powershell
# Enable script execution
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Then try again
.\venv\Scripts\Activate.ps1
```

**Module not found errors**:
```powershell
# Make sure virtual environment is activated
# You should see (venv) in your prompt

# Reinstall dependencies
pip install -r requirements.txt
```

### Database Issues

**PostgreSQL connection error**:
1. Check PostgreSQL is running:
   ```powershell
   # Check Windows Services
   Get-Service -Name postgresql*
   ```

2. Verify connection:
   ```powershell
   psql -U postgres -d infofi
   ```

3. Update DATABASE_URL in .env with correct credentials

### Node.js Issues

**"npm not recognized"**:
- Reinstall Node.js from https://nodejs.org/
- Restart terminal after installation

**Port 3000 already in use**:
```powershell
# Kill process on port 3000
netstat -ano | findstr :3000
taskkill /PID <PID> /F
```

---

## Recommended Setup Path

**For Development**: Use **Option 1 (Docker)** - easiest and most complete

**For Production**: Follow DEPLOYMENT.md guide

**For Quick Testing**: Use **Option 3 (Minimal Demo)** - fastest to get started

---

## Next Steps After Setup

1. **Get TON API Key** (Free):
   - Visit: https://tonapi.io/
   - Sign up and get API key
   - Add to `.env` file: `TON_API_KEY=your_key_here`

2. **Explore the API**:
   - Open http://localhost:8000/docs
   - Try the interactive API documentation
   - Test endpoints directly in browser

3. **Customize the Platform**:
   - Edit backend code in `backend/` folder
   - Modify frontend in `frontend/web-app/` folder
   - Add your own data sources

4. **Deploy Smart Contracts**:
   - Follow TON documentation
   - Use the contracts in `backend/blockchain/smart_contracts/`

---

## Quick Commands Reference

### Docker Commands
```powershell
# Start services
docker-compose up -d

# Stop services
docker-compose down

# View logs
docker-compose logs -f backend

# Restart a service
docker-compose restart backend

# Remove all data
docker-compose down -v
```

### Backend Commands
```powershell
# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Run server
python -m uvicorn api.main:app --reload

# Run tests (when available)
pytest
```

### Frontend Commands
```powershell
# Install dependencies
npm install

# Run development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

---

## Getting Help

- Check logs: `docker-compose logs -f`
- API docs: http://localhost:8000/docs
- Review README.md for architecture details
- Check ARCHITECTURE.md for system design

## Success Indicators

✅ Backend API responds at http://localhost:8000/health  
✅ API docs load at http://localhost:8000/docs  
✅ Frontend loads at http://localhost:3000 (Docker) or http://localhost:5173 (manual)  
✅ No error messages in logs  

You're ready to build! 🚀
