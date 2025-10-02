"""
Knowledge Layer API Routes
Endpoints for semantic search and entity queries
"""

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import List, Optional

from backend.knowledge_layer.vector_store import vector_store
from backend.knowledge_layer.nlp_processor import nlp_processor

router = APIRouter()


class SemanticSearchRequest(BaseModel):
    query: str
    collection: str = "Signal"
    limit: int = 10


class TextAnalysisRequest(BaseModel):
    text: str


@router.post("/search/semantic")
async def semantic_search(request: SemanticSearchRequest):
    """Perform semantic search across knowledge base"""
    try:
        results = await vector_store.semantic_search(
            query=request.query,
            collection_name=request.collection,
            limit=request.limit
        )
        
        return {
            "query": request.query,
            "results": results,
            "count": len(results)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/entities/wallets")
async def get_wallets(
    is_whale: Optional[bool] = None,
    min_balance: Optional[float] = None,
    limit: int = Query(50, ge=1, le=500)
):
    """Get wallet entities"""
    return {
        "wallets": [],
        "filters": {
            "is_whale": is_whale,
            "min_balance": min_balance
        },
        "count": 0
    }


@router.get("/entities/tokens")
async def get_tokens(
    search: Optional[str] = None,
    limit: int = Query(50, ge=1, le=500)
):
    """Get token entities"""
    return {
        "tokens": [],
        "search": search,
        "count": 0
    }


@router.get("/entities/protocols")
async def get_protocols(limit: int = Query(50, ge=1, le=500)):
    """Get protocol entities"""
    return {
        "protocols": [],
        "count": 0
    }


@router.post("/analyze/sentiment")
async def analyze_sentiment(request: TextAnalysisRequest):
    """Analyze sentiment of text"""
    try:
        result = await nlp_processor.analyze_sentiment(request.text)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/analyze/entities")
async def extract_entities(request: TextAnalysisRequest):
    """Extract entities from text"""
    try:
        entities = await nlp_processor.extract_entities(request.text)
        return {
            "text": request.text,
            "entities": entities,
            "count": len(entities)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/analyze/summarize")
async def summarize_text(request: TextAnalysisRequest):
    """Generate summary of text"""
    try:
        summary = await nlp_processor.summarize_text(request.text)
        return {
            "original": request.text,
            "summary": summary
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/trending/signals")
async def get_trending_signals(
    hours: int = Query(24, ge=1, le=168),
    limit: int = Query(20, ge=1, le=100)
):
    """Get trending signals"""
    try:
        signals = await vector_store.get_trending_signals(hours, limit)
        return {
            "signals": signals,
            "timeframe_hours": hours,
            "count": len(signals)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/similar/transactions/{tx_hash}")
async def find_similar_transactions(
    tx_hash: str,
    limit: int = Query(10, ge=1, le=50)
):
    """Find similar transactions"""
    try:
        similar = await vector_store.find_similar_transactions(tx_hash, limit)
        return {
            "reference_tx": tx_hash,
            "similar_transactions": similar,
            "count": len(similar)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
