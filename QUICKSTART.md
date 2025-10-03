# InfoFi Platform - Quick Start Guide

Get your InfoFi platform running in under 10 minutes!

## Prerequisites

- Docker Desktop installed and running
- Git
- Text editor

## Step 1: Clone & Configure (2 minutes)

```bash
# Navigate to projects directory
cd C:\Users\DATASOFT\CascadeProjects\infofi-platform

# Copy environment template
copy .env.example .env

# Edit .env file with your preferred text editor
notepad .env
```

**Minimum required configuration**:
```env
# Just set these for basic functionality
TON_API_KEY=get_free_key_from_tonapi.io
SECRET_KEY=change_this_to_random_string
```

## Step 2: Start Services (3 minutes)

```bash
# Start all services with Docker Compose
docker-compose up -d

# Wait for services to be ready (check status)
docker-compose ps
```

You should see all services running:
- ✅ postgres
- ✅ redis
- ✅ kafka
- ✅ weaviate
- ✅ backend
- ✅ frontend

## Step 3: Verify Installation (1 minute)

Open your browser and check:

1. **API Documentation**: http://localhost:8000/docs
   - You should see the Swagger UI with all endpoints

2. **Health Check**: http://localhost:8000/health
   - Should return: `{"status": "healthy"}`

3. **Web Dashboard**: http://localhost:3000
   - Should load the React dashboard

## Step 4: Test the Platform (4 minutes)

### Test 1: Get Recent Signals

```bash
curl http://localhost:8000/api/v1/ai/signals/recent?limit=5
```

### Test 2: Semantic Search

```bash
curl -X POST http://localhost:8000/api/v1/knowledge/search/semantic \
  -H "Content-Type: application/json" \
  -d '{"query": "whale movements", "limit": 10}'
```

### Test 3: Analyze Sentiment

```bash
curl -X POST http://localhost:8000/api/v1/knowledge/analyze/sentiment \
  -H "Content-Type: application/json" \
  -d '{"text": "TON price is looking very bullish today!"}'
```

### Test 4: Browse Marketplace

```bash
curl http://localhost:8000/api/v1/marketplace/assets/browse?limit=20
```

## What's Running?

### Backend Services
- **FastAPI Server**: http://localhost:8000
- **PostgreSQL**: localhost:5432
- **Redis**: localhost:6379
- **Kafka**: localhost:9092
- **Weaviate**: http://localhost:8080
- **Elasticsearch**: http://localhost:9200

### Frontend
- **Web App**: http://localhost:3000

## Next Steps

### 1. Get TON API Key (Free)

Visit https://tonapi.io and sign up for a free API key to enable:
- Real-time transaction monitoring
- Whale alert detection
- Wallet analysis

### 2. Configure Data Sources (Optional)

For enhanced functionality, add these to your `.env`:

```env
# Twitter monitoring
TWITTER_BEARER_TOKEN=your_token

# Telegram monitoring
TELEGRAM_BOT_TOKEN=your_bot_token

# GitHub tracking
GITHUB_TOKEN=your_github_token

# AI enhancement (optional)
OPENAI_API_KEY=your_openai_key
```

### 3. Deploy Smart Contracts

```bash
# Access backend container
docker-compose exec backend bash

# Run deployment script
python scripts/deploy_contracts.py
```

### 4. Create Your First Signal

Using the web dashboard at http://localhost:3000:
1. Navigate to "Marketplace"
2. Click "Create Info Asset"
3. Fill in signal details
4. Submit and mint NFT

## Common Commands

```bash
# View logs
docker-compose logs -f backend

# Restart a service
docker-compose restart backend

# Stop all services
docker-compose down

# Stop and remove all data
docker-compose down -v

# Update code and restart
git pull
docker-compose up -d --build
```

## Troubleshooting

### Backend won't start
```bash
# Check logs
docker-compose logs backend

# Common fix: restart database
docker-compose restart postgres
docker-compose restart backend
```

### Port already in use
```bash
# Find what's using the port (Windows)
netstat -ano | findstr :8000

# Kill the process
taskkill /PID <process_id> /F
```

### Database connection error
```bash
# Reset database
docker-compose down -v
docker-compose up -d postgres
# Wait 10 seconds
docker-compose up -d backend
```

### Weaviate not responding
```bash
# Restart Weaviate and transformers
docker-compose restart weaviate t2v-transformers
```

## Development Mode

### Backend Development

```bash
# Stop Docker backend
docker-compose stop backend

# Run locally with hot reload
cd backend
pip install -r requirements.txt
uvicorn api.main:app --reload
```

### Frontend Development

```bash
# Stop Docker frontend
docker-compose stop frontend

# Run locally
cd frontend/web-app
npm install
npm run dev
```

## Production Deployment

See [DEPLOYMENT.md](DEPLOYMENT.md) for production setup instructions.

## Getting Help

- **Documentation**: Check README.md and ARCHITECTURE.md
- **API Docs**: http://localhost:8000/docs
- **Logs**: `docker-compose logs -f`
- **Issues**: Create an issue on GitHub

## What You Can Do Now

✅ **Browse AI Signals**: View real-time trading signals  
✅ **Monitor Whale Activity**: Track large wallet movements  
✅ **Search Knowledge Base**: Semantic search across all data  
✅ **Analyze Wallets**: Get AI-powered wallet risk analysis  
✅ **Create Info Assets**: Tokenize your research as NFTs  
✅ **Build Reputation**: Stake tokens on your signals  
✅ **Earn Revenue**: Sell information on the marketplace  

## Success! 🎉

Your InfoFi platform is now running. Start exploring the dashboard at http://localhost:3000 or interact with the API at http://localhost:8000/docs.

Happy building! 🚀
