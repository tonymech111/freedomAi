"""
TON Blockchain Indexer
Monitors on-chain transactions, whale movements, and smart contract events
"""

import asyncio
import logging
from typing import Optional, Dict, Any, List
from datetime import datetime
import aiohttp
from pytoniq import LiteClient, Address
from aiokafka import AIOKafkaProducer
import json

from backend.config import settings

logger = logging.getLogger(__name__)


class TONIndexer:
    """Real-time TON blockchain indexer"""
    
    def __init__(self):
        self.api_url = settings.TON_API_URL
        self.api_key = settings.TON_API_KEY
        self.kafka_producer: Optional[AIOKafkaProducer] = None
        self.session: Optional[aiohttp.ClientSession] = None
        self.last_processed_block = settings.TON_INDEXER_START_BLOCK
        self.is_running = False
        
    async def start(self):
        """Initialize indexer and start monitoring"""
        logger.info("Starting TON Indexer...")
        
        # Initialize Kafka producer
        self.kafka_producer = AIOKafkaProducer(
            bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )
        await self.kafka_producer.start()
        
        # Initialize HTTP session
        self.session = aiohttp.ClientSession(
            headers={"Authorization": f"Bearer {self.api_key}"}
        )
        
        self.is_running = True
        logger.info("TON Indexer started successfully")
        
    async def stop(self):
        """Stop indexer and cleanup resources"""
        logger.info("Stopping TON Indexer...")
        self.is_running = False
        
        if self.kafka_producer:
            await self.kafka_producer.stop()
        
        if self.session:
            await self.session.close()
            
        logger.info("TON Indexer stopped")
        
    async def get_latest_block(self) -> int:
        """Get the latest block number from TON"""
        try:
            async with self.session.get(f"{self.api_url}/blockchain/masterchain-head") as resp:
                data = await resp.json()
                return data.get("last", {}).get("seqno", 0)
        except Exception as e:
            logger.error(f"Error fetching latest block: {e}")
            return self.last_processed_block
            
    async def get_block_transactions(self, block_number: int) -> List[Dict[str, Any]]:
        """Fetch all transactions in a specific block"""
        try:
            async with self.session.get(
                f"{self.api_url}/blockchain/blocks/{block_number}/transactions"
            ) as resp:
                data = await resp.json()
                return data.get("transactions", [])
        except Exception as e:
            logger.error(f"Error fetching block {block_number} transactions: {e}")
            return []
            
    async def process_transaction(self, tx: Dict[str, Any]):
        """Process individual transaction and extract insights"""
        try:
            # Extract transaction details
            tx_hash = tx.get("hash")
            timestamp = tx.get("utime", 0)
            
            # Get sender and receiver
            in_msg = tx.get("in_msg", {})
            source = in_msg.get("source", {}).get("address")
            destination = in_msg.get("destination", {}).get("address")
            
            # Get amount (in nanoTON)
            value = int(in_msg.get("value", 0))
            value_ton = value / 1e9  # Convert to TON
            
            # Skip small transactions
            if value_ton < 1.0:
                return
                
            transaction_data = {
                "hash": tx_hash,
                "timestamp": timestamp,
                "datetime": datetime.fromtimestamp(timestamp).isoformat(),
                "source": source,
                "destination": destination,
                "value_nano": value,
                "value_ton": value_ton,
                "type": "transfer",
                "block": self.last_processed_block
            }
            
            # Send to Kafka
            await self.kafka_producer.send(
                settings.KAFKA_TOPIC_TRANSACTIONS,
                transaction_data
            )
            
            # Check if it's a whale transaction
            if value_ton >= settings.WHALE_ALERT_THRESHOLD_TON:
                await self.process_whale_alert(transaction_data)
                
            logger.debug(f"Processed transaction {tx_hash}: {value_ton:.2f} TON")
            
        except Exception as e:
            logger.error(f"Error processing transaction: {e}")
            
    async def process_whale_alert(self, tx_data: Dict[str, Any]):
        """Process and publish whale alert"""
        whale_alert = {
            **tx_data,
            "alert_type": "whale_movement",
            "severity": "high" if tx_data["value_ton"] > 1000000 else "medium",
            "detected_at": datetime.utcnow().isoformat()
        }
        
        await self.kafka_producer.send(
            settings.KAFKA_TOPIC_WHALE_ALERTS,
            whale_alert
        )
        
        logger.info(
            f"🐋 WHALE ALERT: {tx_data['value_ton']:.2f} TON "
            f"from {tx_data['source'][:8]}... to {tx_data['destination'][:8]}..."
        )
        
    async def get_wallet_info(self, address: str) -> Dict[str, Any]:
        """Get detailed wallet information"""
        try:
            async with self.session.get(f"{self.api_url}/accounts/{address}") as resp:
                data = await resp.json()
                
                return {
                    "address": address,
                    "balance": int(data.get("balance", 0)) / 1e9,
                    "status": data.get("status"),
                    "last_activity": data.get("last_activity"),
                    "is_wallet": data.get("is_wallet", False),
                    "interfaces": data.get("interfaces", [])
                }
        except Exception as e:
            logger.error(f"Error fetching wallet info for {address}: {e}")
            return {}
            
    async def get_jetton_transfers(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Get recent Jetton (token) transfers"""
        try:
            async with self.session.get(
                f"{self.api_url}/events",
                params={"limit": limit, "event_type": "JettonTransfer"}
            ) as resp:
                data = await resp.json()
                return data.get("events", [])
        except Exception as e:
            logger.error(f"Error fetching Jetton transfers: {e}")
            return []
            
    async def monitor_smart_contract(self, contract_address: str):
        """Monitor specific smart contract for events"""
        try:
            async with self.session.get(
                f"{self.api_url}/accounts/{contract_address}/events"
            ) as resp:
                data = await resp.json()
                events = data.get("events", [])
                
                for event in events:
                    event_data = {
                        "contract": contract_address,
                        "event_id": event.get("event_id"),
                        "timestamp": event.get("timestamp"),
                        "event_type": event.get("event_type"),
                        "data": event.get("data")
                    }
                    
                    await self.kafka_producer.send(
                        settings.KAFKA_TOPIC_TRANSACTIONS,
                        event_data
                    )
                    
        except Exception as e:
            logger.error(f"Error monitoring contract {contract_address}: {e}")
            
    async def run(self):
        """Main indexer loop"""
        logger.info("Starting indexer main loop...")
        
        while self.is_running:
            try:
                # Get latest block
                latest_block = await self.get_latest_block()
                
                # Process new blocks
                while self.last_processed_block < latest_block:
                    self.last_processed_block += 1
                    
                    # Fetch and process transactions
                    transactions = await self.get_block_transactions(self.last_processed_block)
                    
                    for tx in transactions:
                        await self.process_transaction(tx)
                        
                    logger.info(f"Processed block {self.last_processed_block} ({len(transactions)} txs)")
                    
                    # Small delay to avoid overwhelming the API
                    await asyncio.sleep(0.1)
                    
                # Wait before checking for new blocks
                await asyncio.sleep(5)
                
            except Exception as e:
                logger.error(f"Error in indexer main loop: {e}")
                await asyncio.sleep(10)


class WhaleTracker:
    """Track and analyze whale wallet behavior"""
    
    def __init__(self):
        self.tracked_wallets: Dict[str, Dict] = {}
        self.whale_threshold = settings.WHALE_ALERT_THRESHOLD_TON
        
    async def identify_whales(self, indexer: TONIndexer) -> List[str]:
        """Identify whale wallets based on balance"""
        # This would query top wallets from database
        # For now, return empty list
        return []
        
    async def analyze_whale_behavior(self, wallet: str, transactions: List[Dict]) -> Dict:
        """Analyze whale wallet transaction patterns"""
        if not transactions:
            return {}
            
        total_volume = sum(tx.get("value_ton", 0) for tx in transactions)
        avg_transaction = total_volume / len(transactions)
        
        # Detect patterns
        patterns = {
            "total_transactions": len(transactions),
            "total_volume": total_volume,
            "average_transaction": avg_transaction,
            "is_accumulating": self._detect_accumulation(transactions),
            "is_distributing": self._detect_distribution(transactions),
            "exchange_interactions": self._count_exchange_interactions(transactions)
        }
        
        return patterns
        
    def _detect_accumulation(self, transactions: List[Dict]) -> bool:
        """Detect if whale is accumulating"""
        incoming = sum(1 for tx in transactions if tx.get("destination") == tx.get("wallet"))
        return incoming > len(transactions) * 0.6
        
    def _detect_distribution(self, transactions: List[Dict]) -> bool:
        """Detect if whale is distributing"""
        outgoing = sum(1 for tx in transactions if tx.get("source") == tx.get("wallet"))
        return outgoing > len(transactions) * 0.6
        
    def _count_exchange_interactions(self, transactions: List[Dict]) -> int:
        """Count transactions with known exchanges"""
        # Known exchange addresses (simplified)
        exchange_addresses = set()  # Would be populated from database
        
        count = 0
        for tx in transactions:
            if tx.get("source") in exchange_addresses or tx.get("destination") in exchange_addresses:
                count += 1
                
        return count


# Singleton instance
ton_indexer = TONIndexer()
whale_tracker = WhaleTracker()
