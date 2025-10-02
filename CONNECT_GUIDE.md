# Backend-Frontend Connection Guide

This guide explains how the backend and frontend are connected and how to run them together.

## Quick Start (Easiest Way)

### Option 1: Use the START Script

```powershell
cd C:\Users\DATASOFT\CascadeProjects\infofi-platform
.\START.ps1
```

This script will:
- ✅ Start the backend on port 8000
- ✅ Start the frontend on port 5173
- ✅ Monitor both services
- ✅ Show you access URLs

### Option 2: Manual Start (Two Terminals)

**Terminal 1 - Backend:**
```powershell
cd C:\Users\DATASOFT\CascadeProjects\infofi-platform\backend
python -m uvicorn api.main_simple:app --reload --host 0.0.0.0 --port 8000
```

**Terminal 2 - Frontend:**
```powershell
cd C:\Users\DATASOFT\CascadeProjects\infofi-platform\frontend\web-app
npm run dev
```

## How They Connect

### 1. Backend (FastAPI)

**File:** `backend/api/main_simple.py`

- Runs on: `http://localhost:8000`
- API endpoints: `http://localhost:8000/api/v1/*`
- API docs: `http://localhost:8000/docs`

**CORS Configuration:**
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5173",  # Frontend URL
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### 2. Frontend (React + Vite)

**File:** `frontend/web-app/src/lib/api.ts`

- Runs on: `http://localhost:5173`
- Connects to backend via: `http://localhost:8000/api/v1`

**API Client:**
```typescript
const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const client = axios.create({
  baseURL: `${API_URL}/api/v1`,
  headers: {
    'Content-Type': 'application/json',
  },
});
```

### 3. Proxy Configuration (Optional)

**File:** `frontend/web-app/vite.config.ts`

```typescript
server: {
  proxy: {
    '/api': {
      target: 'http://localhost:8000',
      changeOrigin: true,
    },
  },
}
```

## Testing the Connection

### 1. Test Backend

```powershell
# Health check
curl http://localhost:8000/health

# Get signals
curl http://localhost:8000/api/v1/ai/signals/recent

# API documentation
# Open in browser: http://localhost:8000/docs
```

### 2. Test Frontend

```powershell
# Open in browser
start http://localhost:5173
```

### 3. Test Full Integration

1. Open frontend: http://localhost:5173
2. Navigate to "Dashboard"
3. You should see:
   - Market stats
   - Recent signals
   - Whale alerts

## API Endpoints Available

### Data Layer
- `GET /api/v1/data/on-chain/transactions` - Recent transactions
- `GET /api/v1/data/on-chain/whale-alerts` - Whale alerts
- `GET /api/v1/data/on-chain/wallet/{address}` - Wallet info
- `GET /api/v1/data/off-chain/news` - News feed

### AI Layer
- `GET /api/v1/ai/signals/recent` - Recent signals
- `POST /api/v1/ai/analyze/market` - Market analysis
- `GET /api/v1/ai/anomalies/detect` - Anomaly detection

### Marketplace
- `GET /api/v1/marketplace/assets/browse` - Browse assets
- `GET /api/v1/marketplace/assets/{id}` - Asset details
- `POST /api/v1/marketplace/assets/create` - Create asset

### Reputation
- `GET /api/v1/reputation/{address}` - Get reputation
- `GET /api/v1/reputation/leaderboard` - Leaderboard
- `POST /api/v1/reputation/stake` - Stake tokens

## Frontend Pages

1. **Dashboard** (`/`) - Overview with stats, signals, whale alerts
2. **Signals** (`/signals`) - All AI-generated signals
3. **Marketplace** (`/marketplace`) - Browse and purchase info assets
4. **Analytics** (`/analytics`) - Market analysis and insights
5. **Reputation** (`/reputation`) - Creator leaderboard

## Troubleshooting

### Backend won't start

```powershell
# Check if port 8000 is in use
netstat -ano | findstr :8000

# Kill the process (replace PID)
taskkill /PID <PID> /F

# Restart backend
cd backend
python -m uvicorn api.main_simple:app --reload
```

### Frontend won't start

```powershell
# Check if port 5173 is in use
netstat -ano | findstr :5173

# Kill the process
taskkill /PID <PID> /F

# Reinstall dependencies
cd frontend\web-app
npm install

# Restart frontend
npm run dev
```

### CORS Errors

If you see CORS errors in browser console:

1. Check backend CORS settings in `backend/api/main_simple.py`
2. Make sure frontend URL is in `allow_origins` list
3. Restart backend after changes

### API Not Responding

1. Check backend is running: `curl http://localhost:8000/health`
2. Check frontend API URL in `.env.local`:
   ```
   VITE_API_URL=http://localhost:8000
   ```
3. Clear browser cache and reload

### Connection Refused

1. Make sure backend started successfully
2. Check firewall isn't blocking ports 8000 or 5173
3. Try accessing via `127.0.0.1` instead of `localhost`

## Environment Variables

### Backend `.env`

```env
APP_NAME=InfoFi Platform
DEBUG=true
TON_API_KEY=demo_mode
DATABASE_URL=sqlite:///./infofi.db
```

### Frontend `.env.local`

```env
VITE_API_URL=http://localhost:8000
```

## Development Workflow

1. **Start Backend First:**
   ```powershell
   cd backend
   python -m uvicorn api.main_simple:app --reload
   ```

2. **Then Start Frontend:**
   ```powershell
   cd frontend\web-app
   npm run dev
   ```

3. **Make Changes:**
   - Backend changes auto-reload (--reload flag)
   - Frontend changes auto-reload (Vite HMR)

4. **Test in Browser:**
   - Open http://localhost:5173
   - Open DevTools (F12) to see network requests
   - Check Console for errors

## Production Deployment

For production, see `DEPLOYMENT.md` for:
- Docker deployment
- Environment configuration
- SSL/TLS setup
- Performance optimization

## Next Steps

1. ✅ Get both services running
2. ✅ Test the connection
3. ✅ Explore the API docs
4. ✅ Customize the frontend
5. ✅ Add your own features

Need help? Check the logs and error messages!
