"""
Data Layer API Routes
Endpoints for on-chain and off-chain data
"""

from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from datetime import datetime, timedelta

from backend.data_layer.ton_indexer import ton_indexer, whale_tracker
from backend.data_layer.off_chain_sources import news_aggregator

router = APIRouter()


@router.get("/on-chain/transactions")
async def get_recent_transactions(
    limit: int = Query(100, ge=1, le=1000),
    min_value: Optional[float] = None
):
    """Get recent TON transactions"""
    # In production, query from database
    return {
        "transactions": [],
        "count": 0,
        "limit": limit
    }


@router.get("/on-chain/whale-alerts")
async def get_whale_alerts(
    hours: int = Query(24, ge=1, le=168),
    min_value: float = Query(100000)
):
    """Get whale movement alerts"""
    return {
        "alerts": [],
        "timeframe_hours": hours,
        "min_value_ton": min_value
    }


@router.get("/on-chain/wallet/{address}")
async def get_wallet_info(address: str):
    """Get wallet information"""
    try:
        wallet_info = await ton_indexer.get_wallet_info(address)
        return wallet_info
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/on-chain/jetton-transfers")
async def get_jetton_transfers(limit: int = Query(100, ge=1, le=1000)):
    """Get recent Jetton (token) transfers"""
    try:
        transfers = await ton_indexer.get_jetton_transfers(limit)
        return {
            "transfers": transfers,
            "count": len(transfers)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/off-chain/news")
async def get_news_feed(
    hours: int = Query(24, ge=1, le=168),
    source: Optional[str] = None
):
    """Get aggregated news feed"""
    return {
        "articles": [],
        "timeframe_hours": hours,
        "source": source
    }


@router.get("/off-chain/social-sentiment")
async def get_social_sentiment(
    platform: Optional[str] = Query(None, regex="^(twitter|telegram|all)$"),
    hours: int = Query(24, ge=1, le=168)
):
    """Get social media sentiment analysis"""
    return {
        "platform": platform or "all",
        "timeframe_hours": hours,
        "sentiment": {
            "overall": "neutral",
            "positive_ratio": 0.33,
            "negative_ratio": 0.33,
            "neutral_ratio": 0.34
        },
        "trending_topics": []
    }


@router.get("/off-chain/github-activity")
async def get_github_activity(
    repo: Optional[str] = None,
    hours: int = Query(24, ge=1, le=168)
):
    """Get GitHub development activity"""
    return {
        "repos": [],
        "commits": [],
        "timeframe_hours": hours
    }


@router.get("/analytics/whale-behavior/{address}")
async def analyze_whale_behavior(address: str):
    """Analyze whale wallet behavior patterns"""
    try:
        # Get recent transactions for wallet
        transactions = []  # Would query from database
        
        analysis = await whale_tracker.analyze_whale_behavior(address, transactions)
        return analysis
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
