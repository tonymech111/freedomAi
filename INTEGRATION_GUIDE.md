# FreedomAI + InfoFi Integration Guide

This repository now contains both FreedomAI and InfoFi platforms, integrated to work together.

## 🏗️ Repository Structure

```
freedomAi/ (root)
├── backend-infofi/           # InfoFi DeFi Intelligence Backend
│   ├── api/
│   ├── data_layer/
│   ├── ai_layer/
│   └── blockchain/
├── frontend-infofi/          # InfoFi React Dashboard
│   └── web-app/
├── freedomai-backend/        # Your existing FreedomAI backend
├── freedomai-frontend/       # Your existing FreedomAI frontend
├── shared/                   # Shared utilities and configs
└── docker-compose.integrated.yml
```

## 🚀 Running Both Platforms

### Option 1: Docker (Recommended)

```bash
# Start all services
docker-compose -f docker-compose.integrated.yml up -d

# Access points:
# InfoFi Dashboard: http://localhost:3000
# InfoFi API: http://localhost:8000
# FreedomAI: http://localhost:8001 (adjust as needed)
```

### Option 2: Manual Start

**Terminal 1 - InfoFi Backend:**
```powershell
cd backend-infofi
python -m uvicorn api.main_simple:app --reload --port 8000
```

**Terminal 2 - InfoFi Frontend:**
```powershell
cd frontend-infofi/web-app
npm run dev
```

**Terminal 3 - FreedomAI (your existing setup):**
```powershell
# Your existing FreedomAI startup commands
```

## 🔗 Integration Points

### 1. Shared Database
Both platforms can use the same PostgreSQL instance with different schemas:
- `infofi_*` tables for InfoFi data
- `freedomai_*` tables for FreedomAI data

### 2. Cross-Platform API Calls
InfoFi can call FreedomAI APIs and vice versa:

```python
# In InfoFi backend - call FreedomAI
import aiohttp

async def get_freedomai_data():
    async with aiohttp.ClientSession() as session:
        async with session.get('http://localhost:8001/api/freedomai/data') as resp:
            return await resp.json()
```

### 3. Shared Authentication
Use the same JWT tokens across both platforms:

```python
# Shared auth middleware
from fastapi import Depends
from shared.auth import verify_token

@app.get("/protected")
async def protected_route(user = Depends(verify_token)):
    return {"user": user}
```

### 4. Combined Frontend
Create a unified dashboard that shows both FreedomAI and InfoFi data:

```typescript
// Combined dashboard component
const CombinedDashboard = () => {
  const { data: freedomaiData } = useQuery(['freedomai'], fetchFreedomAIData);
  const { data: infofiData } = useQuery(['infofi'], fetchInfoFiData);
  
  return (
    <div>
      <FreedomAISection data={freedomaiData} />
      <InfoFiSection data={infofiData} />
    </div>
  );
};
```

## 🔧 Configuration

### Environment Variables

Create a shared `.env` file:

```env
# Shared Database
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/combined_db

# InfoFi Specific
TON_API_KEY=your_ton_api_key
INFOFI_API_PORT=8000

# FreedomAI Specific  
FREEDOMAI_API_PORT=8001
OPENAI_API_KEY=your_openai_key

# Shared Services
REDIS_URL=redis://localhost:6379/0
```

### API Gateway (Optional)

Create a unified API gateway that routes requests:

```python
# api_gateway.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import httpx

app = FastAPI(title="FreedomAI + InfoFi Gateway")

@app.api_route("/api/infofi/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def proxy_infofi(path: str, request: Request):
    async with httpx.AsyncClient() as client:
        response = await client.request(
            method=request.method,
            url=f"http://localhost:8000/api/v1/{path}",
            params=request.query_params,
            content=await request.body()
        )
        return Response(content=response.content, status_code=response.status_code)

@app.api_route("/api/freedomai/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def proxy_freedomai(path: str, request: Request):
    async with httpx.AsyncClient() as client:
        response = await client.request(
            method=request.method,
            url=f"http://localhost:8001/api/{path}",
            params=request.query_params,
            content=await request.body()
        )
        return Response(content=response.content, status_code=response.status_code)
```

## 📊 Data Flow

```
User Request
    ↓
API Gateway (Port 9000)
    ↓
┌─────────────────┬─────────────────┐
│   InfoFi API    │  FreedomAI API  │
│   (Port 8000)   │   (Port 8001)   │
└─────────────────┴─────────────────┘
    ↓                       ↓
┌─────────────────┬─────────────────┐
│ InfoFi Frontend │FreedomAI Frontend│
│   (Port 3000)   │   (Port 3001)   │
└─────────────────┴─────────────────┘
```

## 🎯 Use Cases

### 1. AI-Powered DeFi Analysis
- FreedomAI provides general AI capabilities
- InfoFi provides DeFi-specific intelligence
- Combined: AI-enhanced DeFi trading strategies

### 2. Cross-Platform Insights
- InfoFi detects whale movements
- FreedomAI analyzes market sentiment
- Combined: Comprehensive trading signals

### 3. Unified User Experience
- Single login for both platforms
- Shared user preferences
- Combined analytics dashboard

## 🚀 Deployment

### Development
```bash
# Start all services
docker-compose -f docker-compose.integrated.yml up -d
```

### Production
```bash
# Build and deploy
docker-compose -f docker-compose.integrated.yml -f docker-compose.prod.yml up -d
```

## 📝 Next Steps

1. ✅ Merge repositories
2. ✅ Set up shared infrastructure
3. ✅ Create integration APIs
4. ✅ Build unified frontend
5. ✅ Deploy combined platform

## 🔧 Troubleshooting

### Port Conflicts
If ports conflict, update docker-compose.integrated.yml:
```yaml
services:
  infofi-backend:
    ports:
      - "8000:8000"  # InfoFi API
  freedomai-backend:
    ports:
      - "8001:8000"  # FreedomAI API (mapped to different port)
```

### Database Issues
Create separate schemas:
```sql
CREATE SCHEMA infofi;
CREATE SCHEMA freedomai;
```

### CORS Issues
Update CORS settings in both backends:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

This integration gives you the best of both worlds - FreedomAI's capabilities plus InfoFi's DeFi intelligence! 🚀
