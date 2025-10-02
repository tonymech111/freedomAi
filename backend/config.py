from pydantic_settings import BaseSettings
from typing import Optional
import os


class Settings(BaseSettings):
    """Application configuration settings"""
    
    # Application
    APP_NAME: str = "InfoFi Platform"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    ENVIRONMENT: str = "development"
    
    # API
    API_V1_PREFIX: str = "/api/v1"
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days
    
    # Database
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "postgresql+asyncpg://postgres:postgres@localhost:5432/infofi"
    )
    DB_POOL_SIZE: int = 20
    DB_MAX_OVERFLOW: int = 40
    
    # TON Blockchain
    TON_API_KEY: str = os.getenv("TON_API_KEY", "")
    TON_API_URL: str = "https://tonapi.io/v2"
    TON_CENTER_URL: str = "https://toncenter.com/api/v2"
    TON_NETWORK: str = "mainnet"  # mainnet or testnet
    TON_INDEXER_START_BLOCK: int = 0
    
    # Kafka
    KAFKA_BOOTSTRAP_SERVERS: str = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
    KAFKA_TOPIC_TRANSACTIONS: str = "ton-transactions"
    KAFKA_TOPIC_WHALE_ALERTS: str = "whale-alerts"
    KAFKA_TOPIC_NEWS: str = "news-feed"
    KAFKA_TOPIC_SIGNALS: str = "ai-signals"
    KAFKA_CONSUMER_GROUP: str = "infofi-consumers"
    
    # Weaviate (Vector Database)
    WEAVIATE_URL: str = os.getenv("WEAVIATE_URL", "http://localhost:8080")
    WEAVIATE_API_KEY: Optional[str] = os.getenv("WEAVIATE_API_KEY")
    WEAVIATE_BATCH_SIZE: int = 100
    
    # Elasticsearch
    ELASTICSEARCH_URL: str = os.getenv("ELASTICSEARCH_URL", "http://localhost:9200")
    ELASTICSEARCH_INDEX_PREFIX: str = "infofi"
    
    # Redis
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    REDIS_CACHE_TTL: int = 3600  # 1 hour
    
    # AI/ML Models
    OPENAI_API_KEY: Optional[str] = os.getenv("OPENAI_API_KEY")
    OPENAI_MODEL: str = "gpt-4-turbo-preview"
    EMBEDDING_MODEL: str = "sentence-transformers/all-MiniLM-L6-v2"
    LLM_TEMPERATURE: float = 0.7
    LLM_MAX_TOKENS: int = 2000
    
    # Data Sources
    TWITTER_BEARER_TOKEN: Optional[str] = os.getenv("TWITTER_BEARER_TOKEN")
    TELEGRAM_BOT_TOKEN: Optional[str] = os.getenv("TELEGRAM_BOT_TOKEN")
    GITHUB_TOKEN: Optional[str] = os.getenv("GITHUB_TOKEN")
    
    # Whale Alert Thresholds
    WHALE_ALERT_THRESHOLD_TON: float = 100000.0  # 100k TON
    WHALE_ALERT_THRESHOLD_USD: float = 250000.0  # $250k
    
    # Reputation System
    INITIAL_REPUTATION_SCORE: int = 100
    MIN_STAKE_AMOUNT: float = 10.0  # Minimum TON to stake
    REPUTATION_DECAY_RATE: float = 0.95  # Weekly decay for inactive users
    
    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = 60
    RATE_LIMIT_PER_HOUR: int = 1000
    
    # Monitoring
    SENTRY_DSN: Optional[str] = os.getenv("SENTRY_DSN")
    PROMETHEUS_PORT: int = 9090
    
    # CORS
    CORS_ORIGINS: list[str] = [
        "http://localhost:3000",
        "http://localhost:5173",
        "https://t.me"
    ]
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
