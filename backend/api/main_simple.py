"""
Simplified FastAPI Application for Development
Works without external dependencies (Kafka, Weaviate, etc.)
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="InfoFi Platform API",
    version="1.0.0",
    description="AI-Powered DeFi Intelligence Platform on TON"
)

# Configure CORS - Allow frontend to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5173",
        "http://localhost:5174",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:5174",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "version": "1.0.0",
        "environment": "development",
        "timestamp": datetime.utcnow().isoformat()
    }


# Root endpoint
@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Welcome to InfoFi Platform API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }


# ============= DATA LAYER ENDPOINTS =============

@app.get("/api/v1/data/on-chain/transactions")
async def get_transactions(limit: int = 100):
    """Get recent TON transactions"""
    return {
        "transactions": [
            {
                "hash": "abc123",
                "source": "EQD...source1",
                "destination": "EQD...dest1",
                "value_ton": 1500.5,
                "timestamp": datetime.utcnow().isoformat(),
                "type": "transfer"
            },
            {
                "hash": "def456",
                "source": "EQD...source2",
                "destination": "EQD...dest2",
                "value_ton": 250000.0,
                "timestamp": datetime.utcnow().isoformat(),
                "type": "whale_movement"
            }
        ],
        "count": 2,
        "limit": limit
    }


@app.get("/api/v1/data/on-chain/whale-alerts")
async def get_whale_alerts(hours: int = 24):
    """Get whale movement alerts"""
    return {
        "alerts": [
            {
                "hash": "whale1",
                "value_ton": 500000.0,
                "source": "EQD...whale1",
                "destination": "EQD...exchange",
                "severity": "high",
                "detected_at": datetime.utcnow().isoformat()
            },
            {
                "hash": "whale2",
                "value_ton": 250000.0,
                "source": "EQD...exchange",
                "destination": "EQD...whale2",
                "severity": "medium",
                "detected_at": datetime.utcnow().isoformat()
            }
        ],
        "timeframe_hours": hours,
        "count": 2
    }


@app.get("/api/v1/data/on-chain/wallet/{address}")
async def get_wallet_info(address: str):
    """Get wallet information"""
    return {
        "address": address,
        "balance": 125000.50,
        "status": "active",
        "is_wallet": True,
        "last_activity": datetime.utcnow().isoformat(),
        "transaction_count": 342
    }


@app.get("/api/v1/data/off-chain/news")
async def get_news(hours: int = 24):
    """Get news feed"""
    return {
        "articles": [
            {
                "title": "TON Blockchain Reaches New Milestone",
                "url": "https://example.com/news1",
                "source": "CryptoNews",
                "published": datetime.utcnow().isoformat(),
                "sentiment": "positive"
            },
            {
                "title": "Major DeFi Protocol Launches on TON",
                "url": "https://example.com/news2",
                "source": "DeFi Daily",
                "published": datetime.utcnow().isoformat(),
                "sentiment": "positive"
            }
        ],
        "count": 2,
        "timeframe_hours": hours
    }


# ============= AI LAYER ENDPOINTS =============

@app.get("/api/v1/ai/signals/recent")
async def get_recent_signals(limit: int = 20):
    """Get recent AI-generated signals"""
    return {
        "signals": [
            {
                "id": "signal1",
                "signal_type": "whale_movement",
                "title": "Large Whale Accumulation Detected",
                "description": "Whale wallet accumulated 500K TON in the last 6 hours",
                "confidence": 0.85,
                "severity": "high",
                "created_at": datetime.utcnow().isoformat(),
                "tags": ["whale", "accumulation", "bullish"]
            },
            {
                "id": "signal2",
                "signal_type": "sentiment_analysis",
                "title": "Positive Market Sentiment",
                "description": "Strong bullish sentiment across social media",
                "confidence": 0.72,
                "severity": "medium",
                "created_at": datetime.utcnow().isoformat(),
                "tags": ["sentiment", "social", "bullish"]
            },
            {
                "id": "signal3",
                "signal_type": "anomaly",
                "title": "Unusual Trading Pattern",
                "description": "Detected abnormal trading volume spike",
                "confidence": 0.68,
                "severity": "medium",
                "created_at": datetime.utcnow().isoformat(),
                "tags": ["anomaly", "volume", "alert"]
            }
        ],
        "count": 3,
        "limit": limit
    }


@app.post("/api/v1/ai/analyze/market")
async def analyze_market(data: dict = None):
    """Analyze market conditions"""
    return {
        "timestamp": datetime.utcnow().isoformat(),
        "market_sentiment": "bullish",
        "confidence": 0.75,
        "key_insights": [
            "Strong whale accumulation detected",
            "Positive social sentiment trending",
            "Increasing transaction volume"
        ],
        "recommendations": [
            "Consider accumulation on dips",
            "Monitor whale wallet movements"
        ],
        "risk_level": "low"
    }


@app.get("/api/v1/ai/anomalies/detect")
async def detect_anomalies(hours: int = 24):
    """Detect anomalies"""
    return {
        "anomalies": [
            {
                "type": "high_frequency_trading",
                "wallet": "EQD...suspicious",
                "severity": "medium",
                "reason": "Wallet executed 150 transactions in 1 hour",
                "detected_at": datetime.utcnow().isoformat()
            }
        ],
        "count": 1,
        "timeframe_hours": hours
    }


# ============= KNOWLEDGE LAYER ENDPOINTS =============

@app.post("/api/v1/knowledge/search/semantic")
async def semantic_search(request: dict):
    """Semantic search"""
    query = request.get("query", "")
    return {
        "query": query,
        "results": [
            {
                "id": "result1",
                "title": "Whale Movement Analysis",
                "content": "Analysis of recent whale wallet movements...",
                "score": 0.92
            }
        ],
        "count": 1
    }


@app.post("/api/v1/knowledge/analyze/sentiment")
async def analyze_sentiment(request: dict):
    """Analyze sentiment"""
    text = request.get("text", "")
    return {
        "text": text,
        "label": "POSITIVE",
        "score": 0.89,
        "sentiment": "positive"
    }


@app.get("/api/v1/knowledge/trending/signals")
async def get_trending_signals(hours: int = 24):
    """Get trending signals"""
    return {
        "signals": [
            {
                "id": "trending1",
                "title": "TON Price Surge Expected",
                "description": "Multiple indicators suggest upward movement",
                "confidence": 0.78,
                "created_at": datetime.utcnow().isoformat()
            }
        ],
        "count": 1,
        "timeframe_hours": hours
    }


# ============= MARKETPLACE ENDPOINTS =============

@app.get("/api/v1/marketplace/assets/browse")
async def browse_marketplace(limit: int = 20):
    """Browse marketplace"""
    return {
        "assets": [
            {
                "id": "asset1",
                "type": "nft",
                "title": "Q4 2025 Whale Analysis Report",
                "description": "Comprehensive whale wallet analysis",
                "price": 10.0,
                "creator": "EQD...creator1",
                "rating": 4.8,
                "purchases": 42
            },
            {
                "id": "asset2",
                "type": "token",
                "title": "Daily Market Signals",
                "description": "AI-generated daily trading signals",
                "price": 5.0,
                "creator": "EQD...creator2",
                "rating": 4.5,
                "purchases": 128
            }
        ],
        "count": 2,
        "limit": limit
    }


@app.get("/api/v1/marketplace/assets/{asset_id}")
async def get_asset_details(asset_id: str):
    """Get asset details"""
    return {
        "asset_id": asset_id,
        "type": "nft",
        "title": "Q4 2025 Whale Analysis Report",
        "description": "Comprehensive analysis of whale wallet movements",
        "creator": "EQD...creator",
        "price": 10.0,
        "views": 1250,
        "purchases": 42,
        "rating": 4.7,
        "created_at": datetime.utcnow().isoformat()
    }


@app.post("/api/v1/marketplace/assets/create")
async def create_asset(data: dict):
    """Create info asset"""
    return {
        "asset_id": "new_asset_123",
        "status": "created",
        "transaction": "tx_hash_123",
        "message": "Asset created successfully"
    }


# ============= REPUTATION ENDPOINTS =============

@app.get("/api/v1/reputation/{address}")
async def get_reputation(address: str):
    """Get reputation"""
    return {
        "address": address,
        "stake": 1000.0,
        "reputation_score": 850,
        "correct_signals": 42,
        "total_signals": 50,
        "accuracy": 0.84
    }


@app.get("/api/v1/reputation/leaderboard")
async def get_leaderboard(limit: int = 50):
    """Get leaderboard"""
    return {
        "leaderboard": [
            {
                "rank": 1,
                "address": "EQD...top1",
                "reputation_score": 950,
                "accuracy": 0.92,
                "total_signals": 120
            },
            {
                "rank": 2,
                "address": "EQD...top2",
                "reputation_score": 920,
                "accuracy": 0.88,
                "total_signals": 95
            }
        ],
        "count": 2
    }


@app.post("/api/v1/reputation/stake")
async def stake_tokens(data: dict):
    """Stake tokens"""
    return {
        "signal_id": data.get("signal_id"),
        "amount": data.get("amount"),
        "status": "staked",
        "transaction": "stake_tx_123"
    }


if __name__ == "__main__":
    import uvicorn
    logger.info("Starting InfoFi Platform API (Simple Mode)...")
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        reload=True
    )
