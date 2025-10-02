"""
NLP Processing Engine
Extracts entities, analyzes sentiment, and processes unstructured text
"""

import logging
from typing import List, Dict, Any, Optional, Tuple
import re
from datetime import datetime
from transformers import pipeline, AutoTokenizer, AutoModelForTokenClassification
from sentence_transformers import SentenceTransformer

from backend.config import settings

logger = logging.getLogger(__name__)


class NLPProcessor:
    """Natural Language Processing for crypto intelligence"""
    
    def __init__(self):
        self.sentiment_analyzer = None
        self.ner_model = None
        self.summarizer = None
        self.embedding_model = None
        self._initialized = False
        
    async def initialize(self):
        """Load NLP models"""
        if self._initialized:
            return
            
        try:
            logger.info("Loading NLP models...")
            
            # Sentiment analysis
            self.sentiment_analyzer = pipeline(
                "sentiment-analysis",
                model="distilbert-base-uncased-finetuned-sst-2-english"
            )
            
            # Named Entity Recognition
            self.ner_model = pipeline(
                "ner",
                model="dslim/bert-base-NER",
                aggregation_strategy="simple"
            )
            
            # Text summarization
            self.summarizer = pipeline(
                "summarization",
                model="facebook/bart-large-cnn"
            )
            
            # Embeddings
            self.embedding_model = SentenceTransformer(settings.EMBEDDING_MODEL)
            
            self._initialized = True
            logger.info("NLP models loaded successfully")
            
        except Exception as e:
            logger.error(f"Error loading NLP models: {e}")
            raise
            
    async def analyze_sentiment(self, text: str) -> Dict[str, Any]:
        """Analyze sentiment of text"""
        try:
            if not text or len(text.strip()) == 0:
                return {"label": "NEUTRAL", "score": 0.5}
                
            result = self.sentiment_analyzer(text[:512])[0]  # Limit to 512 chars
            
            return {
                "label": result["label"],
                "score": result["score"],
                "sentiment": "positive" if result["label"] == "POSITIVE" else "negative"
            }
            
        except Exception as e:
            logger.error(f"Error analyzing sentiment: {e}")
            return {"label": "NEUTRAL", "score": 0.5, "sentiment": "neutral"}
            
    async def extract_entities(self, text: str) -> List[Dict[str, Any]]:
        """Extract named entities from text"""
        try:
            if not text or len(text.strip()) == 0:
                return []
                
            entities = self.ner_model(text[:512])
            
            # Also extract crypto-specific entities
            crypto_entities = self._extract_crypto_entities(text)
            
            # Combine and deduplicate
            all_entities = entities + crypto_entities
            
            return all_entities
            
        except Exception as e:
            logger.error(f"Error extracting entities: {e}")
            return []
            
    def _extract_crypto_entities(self, text: str) -> List[Dict[str, Any]]:
        """Extract cryptocurrency-specific entities"""
        entities = []
        
        # Wallet addresses (TON format: EQ...)
        wallet_pattern = r'\b(EQ[A-Za-z0-9_-]{46})\b'
        wallets = re.findall(wallet_pattern, text)
        for wallet in wallets:
            entities.append({
                "entity_group": "WALLET",
                "word": wallet,
                "score": 1.0
            })
            
        # Token symbols
        token_pattern = r'\$([A-Z]{2,10})\b'
        tokens = re.findall(token_pattern, text)
        for token in tokens:
            entities.append({
                "entity_group": "TOKEN",
                "word": f"${token}",
                "score": 0.9
            })
            
        # Amounts (e.g., "1.5M TON", "250k USD")
        amount_pattern = r'\b(\d+(?:\.\d+)?[KMB]?)\s*(TON|USD|USDT)\b'
        amounts = re.findall(amount_pattern, text, re.IGNORECASE)
        for amount, currency in amounts:
            entities.append({
                "entity_group": "AMOUNT",
                "word": f"{amount} {currency}",
                "score": 0.95
            })
            
        return entities
        
    async def summarize_text(self, text: str, max_length: int = 130) -> str:
        """Generate summary of text"""
        try:
            if not text or len(text.strip()) < 100:
                return text
                
            # Summarize
            summary = self.summarizer(
                text,
                max_length=max_length,
                min_length=30,
                do_sample=False
            )
            
            return summary[0]["summary_text"]
            
        except Exception as e:
            logger.error(f"Error summarizing text: {e}")
            return text[:200] + "..."
            
    async def generate_embedding(self, text: str) -> List[float]:
        """Generate embedding vector for text"""
        try:
            embedding = self.embedding_model.encode(text)
            return embedding.tolist()
            
        except Exception as e:
            logger.error(f"Error generating embedding: {e}")
            return []
            
    async def classify_signal_type(self, text: str) -> str:
        """Classify the type of trading signal"""
        text_lower = text.lower()
        
        # Pattern matching for signal classification
        if any(word in text_lower for word in ["whale", "large transfer", "moved"]):
            return "whale_movement"
        elif any(word in text_lower for word in ["accumulation", "buying", "accumulating"]):
            return "accumulation"
        elif any(word in text_lower for word in ["distribution", "selling", "dump"]):
            return "distribution"
        elif any(word in text_lower for word in ["anomaly", "suspicious", "unusual"]):
            return "anomaly"
        elif any(word in text_lower for word in ["news", "announcement", "update"]):
            return "news_event"
        else:
            return "general"
            
    async def calculate_relevance_score(
        self,
        text: str,
        keywords: List[str]
    ) -> float:
        """Calculate relevance score based on keywords"""
        text_lower = text.lower()
        
        matches = sum(1 for keyword in keywords if keyword.lower() in text_lower)
        score = min(matches / len(keywords), 1.0) if keywords else 0.0
        
        return score
        
    async def detect_market_sentiment(self, texts: List[str]) -> Dict[str, Any]:
        """Analyze overall market sentiment from multiple texts"""
        if not texts:
            return {
                "overall_sentiment": "neutral",
                "positive_ratio": 0.33,
                "negative_ratio": 0.33,
                "neutral_ratio": 0.34,
                "confidence": 0.0
            }
            
        sentiments = []
        for text in texts:
            result = await self.analyze_sentiment(text)
            sentiments.append(result)
            
        positive = sum(1 for s in sentiments if s["sentiment"] == "positive")
        negative = sum(1 for s in sentiments if s["sentiment"] == "negative")
        neutral = len(sentiments) - positive - negative
        
        total = len(sentiments)
        positive_ratio = positive / total
        negative_ratio = negative / total
        neutral_ratio = neutral / total
        
        # Determine overall sentiment
        if positive_ratio > 0.5:
            overall = "bullish"
        elif negative_ratio > 0.5:
            overall = "bearish"
        else:
            overall = "neutral"
            
        # Calculate confidence
        confidence = max(positive_ratio, negative_ratio, neutral_ratio)
        
        return {
            "overall_sentiment": overall,
            "positive_ratio": positive_ratio,
            "negative_ratio": negative_ratio,
            "neutral_ratio": neutral_ratio,
            "confidence": confidence,
            "sample_size": total
        }
        
    async def extract_key_phrases(self, text: str, top_k: int = 5) -> List[str]:
        """Extract key phrases from text"""
        # Simple implementation using word frequency
        # In production, use more sophisticated methods like RAKE or YAKE
        
        # Remove common words
        stop_words = {
            "the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for",
            "of", "with", "by", "from", "as", "is", "was", "are", "were", "be",
            "been", "being", "have", "has", "had", "do", "does", "did", "will",
            "would", "could", "should", "may", "might", "must", "can", "this",
            "that", "these", "those", "i", "you", "he", "she", "it", "we", "they"
        }
        
        # Tokenize and filter
        words = re.findall(r'\b\w+\b', text.lower())
        filtered_words = [w for w in words if w not in stop_words and len(w) > 3]
        
        # Count frequencies
        word_freq = {}
        for word in filtered_words:
            word_freq[word] = word_freq.get(word, 0) + 1
            
        # Get top K
        top_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:top_k]
        
        return [word for word, _ in top_words]
        
    async def process_article(self, article: Dict[str, Any]) -> Dict[str, Any]:
        """Process article with full NLP pipeline"""
        text = f"{article.get('title', '')} {article.get('summary', '')}"
        
        # Run all analyses
        sentiment = await self.analyze_sentiment(text)
        entities = await self.extract_entities(text)
        summary = await self.summarize_text(text)
        key_phrases = await self.extract_key_phrases(text)
        signal_type = await self.classify_signal_type(text)
        
        return {
            **article,
            "sentiment": sentiment["sentiment"],
            "sentiment_score": sentiment["score"],
            "entities": entities,
            "summary": summary,
            "key_phrases": key_phrases,
            "signal_type": signal_type,
            "processed_at": datetime.utcnow().isoformat()
        }
        
    async def process_transaction_description(
        self,
        tx: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Generate natural language description of transaction"""
        value = tx.get("value_ton", 0)
        source = tx.get("source", "unknown")[:8]
        dest = tx.get("destination", "unknown")[:8]
        
        # Determine transaction type
        if value >= settings.WHALE_ALERT_THRESHOLD_TON:
            tx_type = "whale movement"
            severity = "high"
        elif value >= 10000:
            tx_type = "large transfer"
            severity = "medium"
        else:
            tx_type = "transfer"
            severity = "low"
            
        description = (
            f"{tx_type.capitalize()} of {value:.2f} TON "
            f"from {source}... to {dest}..."
        )
        
        return {
            **tx,
            "description": description,
            "transaction_type": tx_type,
            "severity": severity
        }


# Singleton instance
nlp_processor = NLPProcessor()
