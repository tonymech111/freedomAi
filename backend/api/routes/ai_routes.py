"""
AI Intelligence API Routes
Endpoints for AI-powered analysis and signals
"""

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import List, Optional, Dict, Any

from backend.ai_layer.agentic_ai import (
    market_analysis_agent,
    anomaly_detector,
    signal_generator
)

router = APIRouter()


class MarketAnalysisRequest(BaseModel):
    timeframe_hours: int = 24
    include_on_chain: bool = True
    include_off_chain: bool = True


class WalletAnalysisRequest(BaseModel):
    address: str
    depth: int = 100  # Number of transactions to analyze


@router.post("/analyze/market")
async def analyze_market(request: MarketAnalysisRequest):
    """Comprehensive market analysis"""
    try:
        # Fetch data (would come from database)
        transactions = []
        news = []
        social_data = []
        
        analysis = await market_analysis_agent.analyze_market_conditions(
            transactions, news, social_data
        )
        
        return analysis
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/analyze/wallet")
async def analyze_wallet(request: WalletAnalysisRequest):
    """Analyze wallet behavior and risk"""
    try:
        # Fetch wallet transactions
        recent_activity = []  # Would query from database
        
        anomalies = await anomaly_detector.detect_wallet_anomalies(
            request.address,
            recent_activity
        )
        
        return {
            "wallet": request.address,
            "anomalies": anomalies,
            "risk_score": len(anomalies) * 0.2,  # Simple risk calculation
            "analysis_depth": request.depth
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/signals/recent")
async def get_recent_signals(
    limit: int = Query(20, ge=1, le=100),
    signal_type: Optional[str] = None,
    min_confidence: float = Query(0.0, ge=0.0, le=1.0)
):
    """Get recent AI-generated signals"""
    try:
        signals = await signal_generator.get_recent_signals(limit)
        
        # Filter by type and confidence
        if signal_type:
            signals = [s for s in signals if s.get("signal_type") == signal_type]
        
        signals = [s for s in signals if s.get("confidence", 0) >= min_confidence]
        
        return {
            "signals": signals,
            "count": len(signals),
            "filters": {
                "type": signal_type,
                "min_confidence": min_confidence
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/signals/types")
async def get_signal_types():
    """Get available signal types"""
    return {
        "types": [
            "whale_movement",
            "accumulation",
            "distribution",
            "anomaly",
            "news_event",
            "sentiment_analysis",
            "general"
        ]
    }


@router.get("/anomalies/detect")
async def detect_anomalies(
    timeframe_hours: int = Query(24, ge=1, le=168),
    severity: Optional[str] = Query(None, regex="^(low|medium|high)$")
):
    """Detect anomalies in recent data"""
    try:
        # Fetch recent transactions
        transactions = []  # Would query from database
        
        anomalies = await anomaly_detector.detect_transaction_anomalies(transactions)
        
        # Filter by severity
        if severity:
            anomalies = [a for a in anomalies if a.get("severity") == severity]
        
        return {
            "anomalies": anomalies,
            "count": len(anomalies),
            "timeframe_hours": timeframe_hours,
            "severity_filter": severity
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/signals/generate/whale")
async def generate_whale_signal(whale_tx: Dict[str, Any]):
    """Generate signal from whale transaction"""
    try:
        signal = await signal_generator.generate_whale_signal(whale_tx)
        return signal
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/signals/generate/sentiment")
async def generate_sentiment_signal(sentiment_data: Dict[str, Any]):
    """Generate signal from sentiment analysis"""
    try:
        signal = await signal_generator.generate_sentiment_signal(sentiment_data)
        return signal
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/predictions/price")
async def get_price_predictions(
    timeframe: str = Query("24h", regex="^(1h|4h|24h|7d)$")
):
    """Get AI price predictions (placeholder)"""
    return {
        "timeframe": timeframe,
        "prediction": "neutral",
        "confidence": 0.5,
        "note": "Price prediction model not yet implemented"
    }
