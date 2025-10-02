"""
Main FastAPI Application
REST API for InfoFi Platform
"""

from fastapi import FastAPI, HTTPException, Depends, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import logging
from typing import List, Optional

from backend.config import settings
from backend.api.routes import (
    data_routes,
    knowledge_routes,
    ai_routes,
    marketplace_routes,
    reputation_routes
)
from backend.data_layer.ton_indexer import ton_indexer
from backend.data_layer.off_chain_sources import (
    news_aggregator,
    telegram_monitor,
    twitter_monitor,
    github_monitor
)
from backend.knowledge_layer.vector_store import vector_store
from backend.knowledge_layer.nlp_processor import nlp_processor
from backend.ai_layer.agentic_ai import market_analysis_agent
from backend.blockchain.ton_client import ton_client

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    logger.info("Starting InfoFi Platform...")
    
    # Initialize components
    try:
        # Connect to TON blockchain
        await ton_client.connect()
        
        # Connect to vector store
        await vector_store.connect()
        
        # Initialize NLP processor
        await nlp_processor.initialize()
        
        # Initialize AI agent
        await market_analysis_agent.initialize()
        
        # Start data sources
        await ton_indexer.start()
        await news_aggregator.start()
        await telegram_monitor.start()
        await twitter_monitor.start()
        await github_monitor.start()
        
        logger.info("All components initialized successfully")
        
    except Exception as e:
        logger.error(f"Error during startup: {e}")
        raise
    
    yield
    
    # Cleanup
    logger.info("Shutting down InfoFi Platform...")
    
    await ton_indexer.stop()
    await news_aggregator.stop()
    await telegram_monitor.stop()
    await twitter_monitor.stop()
    await github_monitor.stop()
    
    await vector_store.disconnect()
    await ton_client.disconnect()
    
    logger.info("Shutdown complete")


# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="AI-Powered DeFi Intelligence Platform on TON",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
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
        "version": settings.APP_VERSION,
        "environment": settings.ENVIRONMENT
    }


# Root endpoint
@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Welcome to InfoFi Platform API",
        "version": settings.APP_VERSION,
        "docs": "/docs",
        "health": "/health"
    }


# Include routers
app.include_router(
    data_routes.router,
    prefix=f"{settings.API_V1_PREFIX}/data",
    tags=["Data Layer"]
)

app.include_router(
    knowledge_routes.router,
    prefix=f"{settings.API_V1_PREFIX}/knowledge",
    tags=["Knowledge Layer"]
)

app.include_router(
    ai_routes.router,
    prefix=f"{settings.API_V1_PREFIX}/ai",
    tags=["AI Intelligence"]
)

app.include_router(
    marketplace_routes.router,
    prefix=f"{settings.API_V1_PREFIX}/marketplace",
    tags=["Marketplace"]
)

app.include_router(
    reputation_routes.router,
    prefix=f"{settings.API_V1_PREFIX}/reputation",
    tags=["Reputation"]
)


# Error handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail}
    )


@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    logger.error(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={"error": "Internal server error"}
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "backend.api.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG
    )
