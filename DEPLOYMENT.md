# InfoFi Platform - Deployment Guide

## Prerequisites

- Docker & Docker Compose
- Python 3.11+
- Node.js 18+
- PostgreSQL 15+
- TON API Key (from tonapi.io or toncenter.com)

## Quick Start with Docker

### 1. Clone and Configure

```bash
cd infofi-platform
cp .env.example .env
# Edit .env with your API keys and configuration
```

### 2. Start All Services

```bash
docker-compose up -d
```

This will start:
- PostgreSQL (port 5432)
- Redis (port 6379)
- Kafka + Zookeeper (port 9092)
- Weaviate (port 8080)
- Elasticsearch (port 9200)
- Backend API (port 8000)
- Frontend (port 3000)

### 3. Verify Services

```bash
# Check all services are running
docker-compose ps

# View logs
docker-compose logs -f backend

# Check API health
curl http://localhost:8000/health
```

### 4. Access Applications

- **API Documentation**: http://localhost:8000/docs
- **Web Dashboard**: http://localhost:3000
- **Weaviate Console**: http://localhost:8080/v1

## Manual Deployment

### Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
alembic upgrade head

# Start backend
uvicorn api.main:app --reload
```

### Frontend Setup

```bash
cd frontend/web-app

# Install dependencies
npm install

# Start development server
npm run dev

# Build for production
npm run build
```

## Smart Contract Deployment

### 1. Compile Contracts

```bash
cd backend/blockchain/smart_contracts

# Install FunC compiler
# Follow: https://ton.org/docs/develop/func/cookbook

# Compile contracts
func -o info_token.fif -SPA info_token.fc
func -o info_nft.fif -SPA info_nft.fc
func -o reputation_staking.fif -SPA reputation_staking.fc
```

### 2. Deploy to TON

```python
# Use the TON client to deploy
from backend.blockchain.ton_client import ton_client

# Deploy token contract
token_address = await ton_client.deploy_info_token(
    name="InfoFi Token",
    symbol="INFO",
    total_supply=1000000
)

# Deploy NFT collection
nft_address = await ton_client.deploy_nft_collection(
    collection_name="InfoFi Reports",
    collection_description="Tokenized DeFi Intelligence"
)

# Deploy reputation contract
reputation_address = await ton_client.deploy_reputation_contract(
    min_stake=10
)
```

## Production Deployment

### Using Kubernetes

```bash
# Apply Kubernetes manifests
kubectl apply -f infrastructure/k8s/

# Check deployment status
kubectl get pods -n infofi

# View logs
kubectl logs -f deployment/infofi-backend -n infofi
```

### Environment Variables (Production)

```env
# Production settings
DEBUG=false
ENVIRONMENT=production
SECRET_KEY=<strong-random-key>

# Use production databases
DATABASE_URL=postgresql+asyncpg://user:pass@prod-db:5432/infofi
REDIS_URL=redis://prod-redis:6379/0

# Production TON network
TON_NETWORK=mainnet
TON_API_KEY=<your-production-api-key>

# Enable monitoring
SENTRY_DSN=<your-sentry-dsn>
```

### SSL/TLS Configuration

```nginx
# Nginx configuration for HTTPS
server {
    listen 443 ssl http2;
    server_name api.infofi.io;

    ssl_certificate /etc/ssl/certs/infofi.crt;
    ssl_certificate_key /etc/ssl/private/infofi.key;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## Telegram Mini App Deployment

### 1. Create Telegram Bot

```bash
# Talk to @BotFather on Telegram
/newbot
# Follow instructions to create bot

# Set bot commands
/setcommands
start - Start InfoFi bot
signals - View recent signals
whales - Whale alerts
marketplace - Browse marketplace
reputation - Check reputation
```

### 2. Configure Mini App

```bash
# Set Mini App URL with @BotFather
/newapp
# Select your bot
# Upload icon and screenshots
# Set URL: https://your-domain.com/telegram-mini-app/
```

### 3. Deploy Mini App

```bash
# Upload to your web server
scp -r frontend/telegram-mini-app/* user@server:/var/www/infofi/telegram/

# Or use CDN
aws s3 sync frontend/telegram-mini-app/ s3://your-bucket/telegram-mini-app/
```

## Monitoring & Maintenance

### Health Checks

```bash
# API health
curl http://localhost:8000/health

# Database connection
psql -h localhost -U postgres -d infofi -c "SELECT 1;"

# Kafka topics
kafka-topics --list --bootstrap-server localhost:9092

# Weaviate status
curl http://localhost:8080/v1/.well-known/ready
```

### Logs

```bash
# Backend logs
docker-compose logs -f backend

# Database logs
docker-compose logs -f postgres

# All services
docker-compose logs -f
```

### Backups

```bash
# Backup PostgreSQL
docker exec infofi-postgres pg_dump -U postgres infofi > backup_$(date +%Y%m%d).sql

# Backup Weaviate
curl http://localhost:8080/v1/backups/filesystem -X POST

# Restore PostgreSQL
docker exec -i infofi-postgres psql -U postgres infofi < backup_20251001.sql
```

## Scaling

### Horizontal Scaling

```yaml
# docker-compose.override.yml
services:
  backend:
    deploy:
      replicas: 3
    
  # Add load balancer
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
```

### Database Scaling

```bash
# Add read replicas
# Configure connection pooling
# Use TimescaleDB for time-series data
```

## Troubleshooting

### Common Issues

**Backend won't start:**
```bash
# Check database connection
docker-compose logs postgres

# Verify environment variables
docker-compose exec backend env | grep DATABASE_URL
```

**Kafka connection errors:**
```bash
# Restart Kafka
docker-compose restart kafka zookeeper

# Check topics
docker-compose exec kafka kafka-topics --list --bootstrap-server localhost:9092
```

**Weaviate issues:**
```bash
# Check Weaviate logs
docker-compose logs weaviate

# Verify schema
curl http://localhost:8080/v1/schema
```

## Security Checklist

- [ ] Change default passwords
- [ ] Enable SSL/TLS
- [ ] Configure firewall rules
- [ ] Set up rate limiting
- [ ] Enable authentication
- [ ] Regular security updates
- [ ] Backup encryption
- [ ] API key rotation
- [ ] Monitor for anomalies

## Performance Optimization

- Use connection pooling
- Enable Redis caching
- Optimize database queries
- Use CDN for static assets
- Enable gzip compression
- Implement pagination
- Use async operations
- Monitor resource usage

## Support

For issues and questions:
- GitHub Issues: https://github.com/your-org/infofi-platform/issues
- Documentation: https://docs.infofi.io
- Community: https://t.me/infofi_community
