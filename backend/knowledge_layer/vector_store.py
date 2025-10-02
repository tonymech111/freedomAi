"""
Vector Store using Weaviate
Enables semantic search and AI-powered knowledge retrieval
"""

import logging
from typing import List, Dict, Any, Optional
from datetime import datetime
import weaviate
from weaviate.classes.config import Configure, Property, DataType
from sentence_transformers import SentenceTransformer

from backend.config import settings

logger = logging.getLogger(__name__)


class VectorStore:
    """Weaviate-based vector database for semantic search"""
    
    def __init__(self):
        self.client: Optional[weaviate.WeaviateClient] = None
        self.embedding_model = SentenceTransformer(settings.EMBEDDING_MODEL)
        
    async def connect(self):
        """Connect to Weaviate instance"""
        try:
            auth_config = None
            if settings.WEAVIATE_API_KEY:
                auth_config = weaviate.auth.AuthApiKey(settings.WEAVIATE_API_KEY)
                
            self.client = weaviate.connect_to_local(
                host=settings.WEAVIATE_URL.replace("http://", "").replace("https://", ""),
                auth_credentials=auth_config
            )
            
            # Create schemas
            await self._create_schemas()
            
            logger.info("Connected to Weaviate vector store")
            
        except Exception as e:
            logger.error(f"Error connecting to Weaviate: {e}")
            raise
            
    async def disconnect(self):
        """Disconnect from Weaviate"""
        if self.client:
            self.client.close()
            logger.info("Disconnected from Weaviate")
            
    async def _create_schemas(self):
        """Create Weaviate schemas for different data types"""
        
        # Transaction schema
        if not self.client.collections.exists("Transaction"):
            self.client.collections.create(
                name="Transaction",
                properties=[
                    Property(name="hash", data_type=DataType.TEXT),
                    Property(name="source", data_type=DataType.TEXT),
                    Property(name="destination", data_type=DataType.TEXT),
                    Property(name="value_ton", data_type=DataType.NUMBER),
                    Property(name="timestamp", data_type=DataType.DATE),
                    Property(name="block", data_type=DataType.INT),
                    Property(name="description", data_type=DataType.TEXT),
                ],
                vectorizer_config=Configure.Vectorizer.text2vec_transformers()
            )
            
        # Wallet schema
        if not self.client.collections.exists("Wallet"):
            self.client.collections.create(
                name="Wallet",
                properties=[
                    Property(name="address", data_type=DataType.TEXT),
                    Property(name="balance", data_type=DataType.NUMBER),
                    Property(name="is_whale", data_type=DataType.BOOL),
                    Property(name="first_seen", data_type=DataType.DATE),
                    Property(name="last_activity", data_type=DataType.DATE),
                    Property(name="transaction_count", data_type=DataType.INT),
                    Property(name="labels", data_type=DataType.TEXT_ARRAY),
                    Property(name="risk_score", data_type=DataType.NUMBER),
                ],
                vectorizer_config=Configure.Vectorizer.text2vec_transformers()
            )
            
        # News/Article schema
        if not self.client.collections.exists("Article"):
            self.client.collections.create(
                name="Article",
                properties=[
                    Property(name="title", data_type=DataType.TEXT),
                    Property(name="content", data_type=DataType.TEXT),
                    Property(name="url", data_type=DataType.TEXT),
                    Property(name="source", data_type=DataType.TEXT),
                    Property(name="published_at", data_type=DataType.DATE),
                    Property(name="sentiment", data_type=DataType.TEXT),
                    Property(name="entities", data_type=DataType.TEXT_ARRAY),
                    Property(name="relevance_score", data_type=DataType.NUMBER),
                ],
                vectorizer_config=Configure.Vectorizer.text2vec_transformers()
            )
            
        # Signal schema (AI-generated insights)
        if not self.client.collections.exists("Signal"):
            self.client.collections.create(
                name="Signal",
                properties=[
                    Property(name="signal_type", data_type=DataType.TEXT),
                    Property(name="title", data_type=DataType.TEXT),
                    Property(name="description", data_type=DataType.TEXT),
                    Property(name="confidence", data_type=DataType.NUMBER),
                    Property(name="severity", data_type=DataType.TEXT),
                    Property(name="created_at", data_type=DataType.DATE),
                    Property(name="creator", data_type=DataType.TEXT),
                    Property(name="tags", data_type=DataType.TEXT_ARRAY),
                    Property(name="related_entities", data_type=DataType.TEXT_ARRAY),
                ],
                vectorizer_config=Configure.Vectorizer.text2vec_transformers()
            )
            
        logger.info("Weaviate schemas created/verified")
        
    async def add_transaction(self, tx_data: Dict[str, Any]) -> str:
        """Add transaction to vector store"""
        try:
            collection = self.client.collections.get("Transaction")
            
            # Create description for embedding
            description = (
                f"Transaction of {tx_data.get('value_ton', 0):.2f} TON "
                f"from {tx_data.get('source', 'unknown')} "
                f"to {tx_data.get('destination', 'unknown')}"
            )
            
            uuid = collection.data.insert({
                "hash": tx_data.get("hash"),
                "source": tx_data.get("source"),
                "destination": tx_data.get("destination"),
                "value_ton": tx_data.get("value_ton"),
                "timestamp": tx_data.get("datetime"),
                "block": tx_data.get("block"),
                "description": description,
            })
            
            return str(uuid)
            
        except Exception as e:
            logger.error(f"Error adding transaction to vector store: {e}")
            return ""
            
    async def add_wallet(self, wallet_data: Dict[str, Any]) -> str:
        """Add wallet to vector store"""
        try:
            collection = self.client.collections.get("Wallet")
            
            uuid = collection.data.insert({
                "address": wallet_data.get("address"),
                "balance": wallet_data.get("balance", 0),
                "is_whale": wallet_data.get("is_whale", False),
                "first_seen": wallet_data.get("first_seen"),
                "last_activity": wallet_data.get("last_activity"),
                "transaction_count": wallet_data.get("transaction_count", 0),
                "labels": wallet_data.get("labels", []),
                "risk_score": wallet_data.get("risk_score", 0),
            })
            
            return str(uuid)
            
        except Exception as e:
            logger.error(f"Error adding wallet to vector store: {e}")
            return ""
            
    async def add_article(self, article_data: Dict[str, Any]) -> str:
        """Add article/news to vector store"""
        try:
            collection = self.client.collections.get("Article")
            
            uuid = collection.data.insert({
                "title": article_data.get("title"),
                "content": article_data.get("summary", ""),
                "url": article_data.get("url"),
                "source": article_data.get("source"),
                "published_at": article_data.get("published"),
                "sentiment": article_data.get("sentiment", "neutral"),
                "entities": article_data.get("entities", []),
                "relevance_score": article_data.get("relevance_score", 0.5),
            })
            
            return str(uuid)
            
        except Exception as e:
            logger.error(f"Error adding article to vector store: {e}")
            return ""
            
    async def add_signal(self, signal_data: Dict[str, Any]) -> str:
        """Add AI signal to vector store"""
        try:
            collection = self.client.collections.get("Signal")
            
            uuid = collection.data.insert({
                "signal_type": signal_data.get("signal_type"),
                "title": signal_data.get("title"),
                "description": signal_data.get("description"),
                "confidence": signal_data.get("confidence", 0.5),
                "severity": signal_data.get("severity", "medium"),
                "created_at": signal_data.get("created_at", datetime.utcnow().isoformat()),
                "creator": signal_data.get("creator", "system"),
                "tags": signal_data.get("tags", []),
                "related_entities": signal_data.get("related_entities", []),
            })
            
            return str(uuid)
            
        except Exception as e:
            logger.error(f"Error adding signal to vector store: {e}")
            return ""
            
    async def semantic_search(
        self,
        query: str,
        collection_name: str = "Signal",
        limit: int = 10,
        filters: Optional[Dict] = None
    ) -> List[Dict[str, Any]]:
        """Perform semantic search across collection"""
        try:
            collection = self.client.collections.get(collection_name)
            
            # Perform vector search
            response = collection.query.near_text(
                query=query,
                limit=limit
            )
            
            results = []
            for obj in response.objects:
                results.append({
                    "id": str(obj.uuid),
                    "properties": obj.properties,
                    "score": obj.metadata.score if hasattr(obj.metadata, 'score') else None
                })
                
            return results
            
        except Exception as e:
            logger.error(f"Error performing semantic search: {e}")
            return []
            
    async def find_similar_transactions(
        self,
        tx_hash: str,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """Find similar transactions based on patterns"""
        try:
            collection = self.client.collections.get("Transaction")
            
            # Get the reference transaction
            response = collection.query.fetch_objects(
                filters=weaviate.classes.query.Filter.by_property("hash").equal(tx_hash),
                limit=1
            )
            
            if not response.objects:
                return []
                
            # Find similar
            similar = collection.query.near_object(
                near_object=response.objects[0].uuid,
                limit=limit
            )
            
            results = []
            for obj in similar.objects:
                results.append({
                    "id": str(obj.uuid),
                    "properties": obj.properties
                })
                
            return results
            
        except Exception as e:
            logger.error(f"Error finding similar transactions: {e}")
            return []
            
    async def get_wallet_by_address(self, address: str) -> Optional[Dict[str, Any]]:
        """Get wallet data by address"""
        try:
            collection = self.client.collections.get("Wallet")
            
            response = collection.query.fetch_objects(
                filters=weaviate.classes.query.Filter.by_property("address").equal(address),
                limit=1
            )
            
            if response.objects:
                obj = response.objects[0]
                return {
                    "id": str(obj.uuid),
                    **obj.properties
                }
                
            return None
            
        except Exception as e:
            logger.error(f"Error getting wallet by address: {e}")
            return None
            
    async def get_trending_signals(self, hours: int = 24, limit: int = 20) -> List[Dict]:
        """Get trending signals from the last N hours"""
        try:
            collection = self.client.collections.get("Signal")
            
            # Calculate timestamp
            cutoff = datetime.utcnow().timestamp() - (hours * 3600)
            
            response = collection.query.fetch_objects(
                limit=limit,
                sort=weaviate.classes.query.Sort.by_property("created_at", ascending=False)
            )
            
            results = []
            for obj in response.objects:
                results.append({
                    "id": str(obj.uuid),
                    **obj.properties
                })
                
            return results
            
        except Exception as e:
            logger.error(f"Error getting trending signals: {e}")
            return []


# Singleton instance
vector_store = VectorStore()
