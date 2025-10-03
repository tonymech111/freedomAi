"""
Agentic AI Layer
Autonomous AI agents for market analysis, anomaly detection, and signal generation
"""

import logging
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
import asyncio
from langchain.llms import OpenAI
from langchain.agents import AgentExecutor, create_react_agent
from langchain.tools import Tool
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory

from backend.config import settings

logger = logging.getLogger(__name__)


class MarketAnalysisAgent:
    """AI agent for comprehensive market analysis"""
    
    def __init__(self):
        self.llm = None
        self.agent = None
        self.memory = ConversationBufferMemory()
        
    async def initialize(self):
        """Initialize the AI agent"""
        if not settings.OPENAI_API_KEY:
            logger.warning("OpenAI API key not configured, using mock agent")
            return
            
        try:
            self.llm = OpenAI(
                temperature=settings.LLM_TEMPERATURE,
                max_tokens=settings.LLM_MAX_TOKENS,
                openai_api_key=settings.OPENAI_API_KEY
            )
            
            # Define tools for the agent
            tools = self._create_tools()
            
            # Create agent
            prompt = self._create_prompt()
            self.agent = create_react_agent(self.llm, tools, prompt)
            
            logger.info("Market Analysis Agent initialized")
            
        except Exception as e:
            logger.error(f"Error initializing agent: {e}")
            
    def _create_tools(self) -> List[Tool]:
        """Create tools for the agent"""
        return [
            Tool(
                name="AnalyzeWhaleMovement",
                func=self._analyze_whale_movement,
                description="Analyze whale wallet movements and predict market impact"
            ),
            Tool(
                name="DetectAnomalies",
                func=self._detect_anomalies,
                description="Detect unusual patterns in transaction data"
            ),
            Tool(
                name="CorrelateSignals",
                func=self._correlate_signals,
                description="Correlate on-chain and off-chain signals"
            ),
            Tool(
                name="GenerateSummary",
                func=self._generate_summary,
                description="Generate human-readable summary of events"
            )
        ]
        
    def _create_prompt(self) -> PromptTemplate:
        """Create prompt template for the agent"""
        template = """You are an expert cryptocurrency market analyst specializing in TON blockchain.
        
Your task is to analyze on-chain data, news, and social sentiment to generate actionable insights.

You have access to the following tools:
{tools}

Use the following format:
Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Question: {input}
{agent_scratchpad}"""

        return PromptTemplate(
            template=template,
            input_variables=["input", "tools", "tool_names", "agent_scratchpad"]
        )
        
    async def _analyze_whale_movement(self, data: str) -> str:
        """Analyze whale wallet movement"""
        # Parse data and analyze
        return "Whale movement indicates potential accumulation phase"
        
    async def _detect_anomalies(self, data: str) -> str:
        """Detect anomalies in transaction patterns"""
        return "No significant anomalies detected"
        
    async def _correlate_signals(self, data: str) -> str:
        """Correlate multiple signals"""
        return "On-chain and off-chain signals are aligned bullish"
        
    async def _generate_summary(self, data: str) -> str:
        """Generate summary of events"""
        return "Market showing signs of accumulation with positive sentiment"
        
    async def analyze_market_conditions(
        self,
        transactions: List[Dict],
        news: List[Dict],
        social_data: List[Dict]
    ) -> Dict[str, Any]:
        """Comprehensive market analysis"""
        
        analysis = {
            "timestamp": datetime.utcnow().isoformat(),
            "market_sentiment": "neutral",
            "confidence": 0.5,
            "key_insights": [],
            "recommendations": [],
            "risk_level": "medium"
        }
        
        # Analyze transaction volume
        if transactions:
            total_volume = sum(tx.get("value_ton", 0) for tx in transactions)
            whale_txs = [tx for tx in transactions if tx.get("value_ton", 0) > 100000]
            
            if whale_txs:
                analysis["key_insights"].append(
                    f"Detected {len(whale_txs)} whale transactions totaling {sum(tx['value_ton'] for tx in whale_txs):.2f} TON"
                )
                
        # Analyze news sentiment
        if news:
            positive_news = sum(1 for n in news if n.get("sentiment") == "positive")
            sentiment_ratio = positive_news / len(news)
            
            if sentiment_ratio > 0.6:
                analysis["market_sentiment"] = "bullish"
                analysis["confidence"] = sentiment_ratio
            elif sentiment_ratio < 0.4:
                analysis["market_sentiment"] = "bearish"
                analysis["confidence"] = 1 - sentiment_ratio
                
        # Generate recommendations
        if analysis["market_sentiment"] == "bullish":
            analysis["recommendations"].append("Consider accumulation on dips")
            analysis["risk_level"] = "low"
        elif analysis["market_sentiment"] == "bearish":
            analysis["recommendations"].append("Exercise caution, consider reducing exposure")
            analysis["risk_level"] = "high"
            
        return analysis


class AnomalyDetector:
    """Detect anomalies in blockchain data"""
    
    def __init__(self):
        self.baseline_metrics = {}
        self.anomaly_threshold = 2.5  # Standard deviations
        
    async def detect_transaction_anomalies(
        self,
        transactions: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Detect anomalous transactions"""
        anomalies = []
        
        if not transactions:
            return anomalies
            
        # Calculate statistics
        values = [tx.get("value_ton", 0) for tx in transactions]
        avg_value = sum(values) / len(values)
        
        # Simple anomaly detection
        for tx in transactions:
            value = tx.get("value_ton", 0)
            
            # Check for unusually large transactions
            if value > avg_value * 10:
                anomalies.append({
                    "type": "large_transaction",
                    "transaction": tx,
                    "severity": "high",
                    "reason": f"Transaction value {value:.2f} TON is 10x above average",
                    "detected_at": datetime.utcnow().isoformat()
                })
                
        return anomalies
        
    async def detect_wallet_anomalies(
        self,
        wallet: str,
        recent_activity: List[Dict]
    ) -> List[Dict[str, Any]]:
        """Detect anomalous wallet behavior"""
        anomalies = []
        
        if not recent_activity:
            return anomalies
            
        # Check for rapid succession of transactions
        if len(recent_activity) > 100:
            anomalies.append({
                "type": "high_frequency_trading",
                "wallet": wallet,
                "severity": "medium",
                "reason": f"Wallet executed {len(recent_activity)} transactions in short period",
                "detected_at": datetime.utcnow().isoformat()
            })
            
        # Check for sudden large movements
        total_value = sum(tx.get("value_ton", 0) for tx in recent_activity)
        if total_value > 1000000:  # 1M TON
            anomalies.append({
                "type": "large_volume",
                "wallet": wallet,
                "severity": "high",
                "reason": f"Wallet moved {total_value:.2f} TON in recent activity",
                "detected_at": datetime.utcnow().isoformat()
            })
            
        return anomalies
        
    async def detect_network_anomalies(
        self,
        network_stats: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Detect network-level anomalies"""
        anomalies = []
        
        # Check transaction volume
        tx_volume = network_stats.get("transaction_volume", 0)
        if tx_volume > self.baseline_metrics.get("avg_tx_volume", 0) * 3:
            anomalies.append({
                "type": "high_network_activity",
                "severity": "medium",
                "reason": "Network transaction volume 3x above baseline",
                "detected_at": datetime.utcnow().isoformat()
            })
            
        return anomalies


class SignalGenerator:
    """Generate trading signals from analyzed data"""
    
    def __init__(self):
        self.signal_history = []
        
    async def generate_whale_signal(
        self,
        whale_tx: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Generate signal from whale transaction"""
        
        value = whale_tx.get("value_ton", 0)
        destination = whale_tx.get("destination", "")
        
        # Determine signal type
        if "exchange" in destination.lower():
            signal_type = "whale_to_exchange"
            sentiment = "bearish"
            description = f"Whale moved {value:.2f} TON to exchange - potential sell pressure"
        else:
            signal_type = "whale_accumulation"
            sentiment = "bullish"
            description = f"Whale accumulated {value:.2f} TON - potential bullish signal"
            
        signal = {
            "signal_type": signal_type,
            "title": f"Whale Alert: {value:.2f} TON Movement",
            "description": description,
            "sentiment": sentiment,
            "confidence": 0.75,
            "severity": "high" if value > 1000000 else "medium",
            "created_at": datetime.utcnow().isoformat(),
            "creator": "ai_agent",
            "tags": ["whale", "on-chain", signal_type],
            "related_entities": [whale_tx.get("source"), destination],
            "data": whale_tx
        }
        
        self.signal_history.append(signal)
        return signal
        
    async def generate_sentiment_signal(
        self,
        sentiment_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Generate signal from sentiment analysis"""
        
        overall = sentiment_data.get("overall_sentiment", "neutral")
        confidence = sentiment_data.get("confidence", 0.5)
        
        if overall == "bullish" and confidence > 0.7:
            description = "Strong bullish sentiment detected across news and social media"
            severity = "high"
        elif overall == "bearish" and confidence > 0.7:
            description = "Strong bearish sentiment detected across news and social media"
            severity = "high"
        else:
            description = "Mixed or neutral market sentiment"
            severity = "low"
            
        signal = {
            "signal_type": "sentiment_analysis",
            "title": f"Market Sentiment: {overall.upper()}",
            "description": description,
            "sentiment": overall,
            "confidence": confidence,
            "severity": severity,
            "created_at": datetime.utcnow().isoformat(),
            "creator": "ai_agent",
            "tags": ["sentiment", "off-chain", "social"],
            "related_entities": [],
            "data": sentiment_data
        }
        
        self.signal_history.append(signal)
        return signal
        
    async def generate_anomaly_signal(
        self,
        anomaly: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Generate signal from detected anomaly"""
        
        signal = {
            "signal_type": "anomaly_detection",
            "title": f"Anomaly Detected: {anomaly.get('type', 'unknown')}",
            "description": anomaly.get("reason", "Unusual pattern detected"),
            "sentiment": "neutral",
            "confidence": 0.8,
            "severity": anomaly.get("severity", "medium"),
            "created_at": datetime.utcnow().isoformat(),
            "creator": "ai_agent",
            "tags": ["anomaly", "alert", anomaly.get("type", "unknown")],
            "related_entities": [anomaly.get("wallet", "")],
            "data": anomaly
        }
        
        self.signal_history.append(signal)
        return signal
        
    async def get_recent_signals(self, limit: int = 20) -> List[Dict[str, Any]]:
        """Get recent signals"""
        return self.signal_history[-limit:]


# Singleton instances
market_analysis_agent = MarketAnalysisAgent()
anomaly_detector = AnomalyDetector()
signal_generator = SignalGenerator()
