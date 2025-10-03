"""
Off-Chain Data Sources
Aggregates news, social media, GitHub activity, and other external data
"""

import asyncio
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
import aiohttp
import feedparser
from bs4 import BeautifulSoup
from aiokafka import AIOKafkaProducer
import json

from backend.config import settings

logger = logging.getLogger(__name__)


class NewsAggregator:
    """Aggregate crypto news from multiple sources"""
    
    RSS_FEEDS = [
        "https://cointelegraph.com/rss",
        "https://decrypt.co/feed",
        "https://cryptonews.com/news/feed/",
        "https://www.coindesk.com/arc/outboundfeeds/rss/",
    ]
    
    def __init__(self):
        self.session: Optional[aiohttp.ClientSession] = None
        self.kafka_producer: Optional[AIOKafkaProducer] = None
        
    async def start(self):
        """Initialize news aggregator"""
        self.session = aiohttp.ClientSession()
        self.kafka_producer = AIOKafkaProducer(
            bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )
        await self.kafka_producer.start()
        logger.info("News Aggregator started")
        
    async def stop(self):
        """Stop news aggregator"""
        if self.kafka_producer:
            await self.kafka_producer.stop()
        if self.session:
            await self.session.close()
        logger.info("News Aggregator stopped")
        
    async def fetch_rss_feed(self, feed_url: str) -> List[Dict[str, Any]]:
        """Fetch and parse RSS feed"""
        try:
            async with self.session.get(feed_url, timeout=10) as resp:
                content = await resp.text()
                feed = feedparser.parse(content)
                
                articles = []
                for entry in feed.entries[:10]:  # Limit to 10 most recent
                    article = {
                        "title": entry.get("title", ""),
                        "url": entry.get("link", ""),
                        "published": entry.get("published", ""),
                        "summary": entry.get("summary", ""),
                        "source": feed.feed.get("title", "Unknown"),
                        "fetched_at": datetime.utcnow().isoformat()
                    }
                    articles.append(article)
                    
                return articles
                
        except Exception as e:
            logger.error(f"Error fetching RSS feed {feed_url}: {e}")
            return []
            
    async def aggregate_news(self) -> List[Dict[str, Any]]:
        """Aggregate news from all sources"""
        all_articles = []
        
        tasks = [self.fetch_rss_feed(feed) for feed in self.RSS_FEEDS]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        for articles in results:
            if isinstance(articles, list):
                all_articles.extend(articles)
                
        # Filter for TON-related news
        ton_articles = [
            article for article in all_articles
            if self._is_ton_related(article)
        ]
        
        # Publish to Kafka
        for article in ton_articles:
            await self.kafka_producer.send(
                settings.KAFKA_TOPIC_NEWS,
                article
            )
            
        logger.info(f"Aggregated {len(ton_articles)} TON-related articles")
        return ton_articles
        
    def _is_ton_related(self, article: Dict[str, Any]) -> bool:
        """Check if article is related to TON"""
        keywords = ["ton", "the open network", "telegram blockchain", "toncoin"]
        text = f"{article.get('title', '')} {article.get('summary', '')}".lower()
        return any(keyword in text for keyword in keywords)
        
    async def run(self):
        """Main news aggregation loop"""
        while True:
            try:
                await self.aggregate_news()
                await asyncio.sleep(300)  # Run every 5 minutes
            except Exception as e:
                logger.error(f"Error in news aggregation loop: {e}")
                await asyncio.sleep(60)


class TelegramMonitor:
    """Monitor Telegram channels for TON-related discussions"""
    
    MONITORED_CHANNELS = [
        "@ton_blockchain",
        "@tonblockchain_news",
        "@toncoin",
    ]
    
    def __init__(self):
        self.bot_token = settings.TELEGRAM_BOT_TOKEN
        self.kafka_producer: Optional[AIOKafkaProducer] = None
        
    async def start(self):
        """Initialize Telegram monitor"""
        if not self.bot_token:
            logger.warning("Telegram bot token not configured")
            return
            
        self.kafka_producer = AIOKafkaProducer(
            bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )
        await self.kafka_producer.start()
        logger.info("Telegram Monitor started")
        
    async def stop(self):
        """Stop Telegram monitor"""
        if self.kafka_producer:
            await self.kafka_producer.stop()
        logger.info("Telegram Monitor stopped")
        
    async def fetch_channel_messages(self, channel: str, limit: int = 10) -> List[Dict]:
        """Fetch recent messages from a Telegram channel"""
        # This is a simplified version. In production, use Telethon or Pyrogram
        # For now, return empty list as placeholder
        logger.info(f"Fetching messages from {channel}")
        return []
        
    async def process_message(self, message: Dict[str, Any]):
        """Process and analyze Telegram message"""
        processed = {
            "channel": message.get("channel"),
            "message_id": message.get("id"),
            "text": message.get("text"),
            "timestamp": message.get("timestamp"),
            "views": message.get("views", 0),
            "forwards": message.get("forwards", 0),
            "sentiment": await self._analyze_sentiment(message.get("text", "")),
            "entities": await self._extract_entities(message.get("text", ""))
        }
        
        await self.kafka_producer.send(
            settings.KAFKA_TOPIC_NEWS,
            processed
        )
        
    async def _analyze_sentiment(self, text: str) -> str:
        """Analyze message sentiment (placeholder)"""
        # Would use NLP model in production
        return "neutral"
        
    async def _extract_entities(self, text: str) -> List[str]:
        """Extract entities from text (placeholder)"""
        # Would use NER model in production
        return []


class TwitterMonitor:
    """Monitor Twitter/X for TON-related discussions"""
    
    SEARCH_QUERIES = [
        "#TON",
        "#ThOpenNetwork",
        "#Toncoin",
        "$TON"
    ]
    
    def __init__(self):
        self.bearer_token = settings.TWITTER_BEARER_TOKEN
        self.session: Optional[aiohttp.ClientSession] = None
        self.kafka_producer: Optional[AIOKafkaProducer] = None
        
    async def start(self):
        """Initialize Twitter monitor"""
        if not self.bearer_token:
            logger.warning("Twitter bearer token not configured")
            return
            
        self.session = aiohttp.ClientSession(
            headers={"Authorization": f"Bearer {self.bearer_token}"}
        )
        self.kafka_producer = AIOKafkaProducer(
            bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )
        await self.kafka_producer.start()
        logger.info("Twitter Monitor started")
        
    async def stop(self):
        """Stop Twitter monitor"""
        if self.kafka_producer:
            await self.kafka_producer.stop()
        if self.session:
            await self.session.close()
        logger.info("Twitter Monitor stopped")
        
    async def search_tweets(self, query: str, max_results: int = 100) -> List[Dict]:
        """Search for tweets matching query"""
        try:
            url = "https://api.twitter.com/2/tweets/search/recent"
            params = {
                "query": query,
                "max_results": max_results,
                "tweet.fields": "created_at,public_metrics,entities"
            }
            
            async with self.session.get(url, params=params) as resp:
                data = await resp.json()
                return data.get("data", [])
                
        except Exception as e:
            logger.error(f"Error searching tweets for '{query}': {e}")
            return []
            
    async def process_tweet(self, tweet: Dict[str, Any]):
        """Process and analyze tweet"""
        metrics = tweet.get("public_metrics", {})
        
        processed = {
            "tweet_id": tweet.get("id"),
            "text": tweet.get("text"),
            "created_at": tweet.get("created_at"),
            "likes": metrics.get("like_count", 0),
            "retweets": metrics.get("retweet_count", 0),
            "replies": metrics.get("reply_count", 0),
            "impressions": metrics.get("impression_count", 0),
            "source": "twitter",
            "processed_at": datetime.utcnow().isoformat()
        }
        
        await self.kafka_producer.send(
            settings.KAFKA_TOPIC_NEWS,
            processed
        )
        
    async def run(self):
        """Main Twitter monitoring loop"""
        while True:
            try:
                for query in self.SEARCH_QUERIES:
                    tweets = await self.search_tweets(query)
                    for tweet in tweets:
                        await self.process_tweet(tweet)
                        
                    await asyncio.sleep(1)  # Rate limiting
                    
                await asyncio.sleep(600)  # Run every 10 minutes
                
            except Exception as e:
                logger.error(f"Error in Twitter monitoring loop: {e}")
                await asyncio.sleep(60)


class GitHubMonitor:
    """Monitor GitHub for TON ecosystem development activity"""
    
    MONITORED_REPOS = [
        "ton-blockchain/ton",
        "ton-blockchain/wallet-contract",
        "ton-community/ton-docs",
    ]
    
    def __init__(self):
        self.token = settings.GITHUB_TOKEN
        self.session: Optional[aiohttp.ClientSession] = None
        self.kafka_producer: Optional[AIOKafkaProducer] = None
        
    async def start(self):
        """Initialize GitHub monitor"""
        headers = {}
        if self.token:
            headers["Authorization"] = f"token {self.token}"
            
        self.session = aiohttp.ClientSession(headers=headers)
        self.kafka_producer = AIOKafkaProducer(
            bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )
        await self.kafka_producer.start()
        logger.info("GitHub Monitor started")
        
    async def stop(self):
        """Stop GitHub monitor"""
        if self.kafka_producer:
            await self.kafka_producer.stop()
        if self.session:
            await self.session.close()
        logger.info("GitHub Monitor stopped")
        
    async def fetch_repo_commits(self, repo: str, since: Optional[datetime] = None) -> List[Dict]:
        """Fetch recent commits from repository"""
        try:
            url = f"https://api.github.com/repos/{repo}/commits"
            params = {}
            if since:
                params["since"] = since.isoformat()
                
            async with self.session.get(url, params=params) as resp:
                commits = await resp.json()
                return commits if isinstance(commits, list) else []
                
        except Exception as e:
            logger.error(f"Error fetching commits for {repo}: {e}")
            return []
            
    async def fetch_repo_activity(self, repo: str) -> Dict[str, Any]:
        """Fetch repository activity metrics"""
        try:
            url = f"https://api.github.com/repos/{repo}"
            async with self.session.get(url) as resp:
                data = await resp.json()
                
                return {
                    "repo": repo,
                    "stars": data.get("stargazers_count", 0),
                    "forks": data.get("forks_count", 0),
                    "watchers": data.get("watchers_count", 0),
                    "open_issues": data.get("open_issues_count", 0),
                    "updated_at": data.get("updated_at"),
                    "fetched_at": datetime.utcnow().isoformat()
                }
                
        except Exception as e:
            logger.error(f"Error fetching activity for {repo}: {e}")
            return {}
            
    async def run(self):
        """Main GitHub monitoring loop"""
        while True:
            try:
                since = datetime.utcnow() - timedelta(hours=1)
                
                for repo in self.MONITORED_REPOS:
                    # Fetch commits
                    commits = await self.fetch_repo_commits(repo, since)
                    
                    for commit in commits:
                        commit_data = {
                            "repo": repo,
                            "sha": commit.get("sha"),
                            "message": commit.get("commit", {}).get("message"),
                            "author": commit.get("commit", {}).get("author", {}).get("name"),
                            "date": commit.get("commit", {}).get("author", {}).get("date"),
                            "source": "github"
                        }
                        
                        await self.kafka_producer.send(
                            settings.KAFKA_TOPIC_NEWS,
                            commit_data
                        )
                        
                    # Fetch activity metrics
                    activity = await self.fetch_repo_activity(repo)
                    if activity:
                        await self.kafka_producer.send(
                            settings.KAFKA_TOPIC_NEWS,
                            activity
                        )
                        
                    await asyncio.sleep(2)  # Rate limiting
                    
                await asyncio.sleep(3600)  # Run every hour
                
            except Exception as e:
                logger.error(f"Error in GitHub monitoring loop: {e}")
                await asyncio.sleep(300)


# Singleton instances
news_aggregator = NewsAggregator()
telegram_monitor = TelegramMonitor()
twitter_monitor = TwitterMonitor()
github_monitor = GitHubMonitor()
