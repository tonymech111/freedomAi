import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const client = axios.create({
  baseURL: `${API_URL}/api/v1`,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const api = {
  // Data Layer
  getRecentTransactions: (params?: any) =>
    client.get('/data/on-chain/transactions', { params }).then((r) => r.data),
  
  getWhaleAlerts: (params?: any) =>
    client.get('/data/on-chain/whale-alerts', { params }).then((r) => r.data),
  
  getWalletInfo: (address: string) =>
    client.get(`/data/on-chain/wallet/${address}`).then((r) => r.data),
  
  getNewsFeed: (params?: any) =>
    client.get('/data/off-chain/news', { params }).then((r) => r.data),

  // Knowledge Layer
  semanticSearch: (query: string, collection?: string, limit?: number) =>
    client.post('/knowledge/search/semantic', { query, collection, limit }).then((r) => r.data),
  
  analyzeSentiment: (text: string) =>
    client.post('/knowledge/analyze/sentiment', { text }).then((r) => r.data),
  
  extractEntities: (text: string) =>
    client.post('/knowledge/analyze/entities', { text }).then((r) => r.data),
  
  getTrendingSignals: (params?: any) =>
    client.get('/knowledge/trending/signals', { params }).then((r) => r.data),

  // AI Intelligence
  analyzeMarket: (params?: any) =>
    client.post('/ai/analyze/market', params).then((r) => r.data),
  
  analyzeWallet: (address: string, depth?: number) =>
    client.post('/ai/analyze/wallet', { address, depth }).then((r) => r.data),
  
  getRecentSignals: (params?: any) =>
    client.get('/ai/signals/recent', { params }).then((r) => r.data),
  
  detectAnomalies: (params?: any) =>
    client.get('/ai/anomalies/detect', { params }).then((r) => r.data),

  // Marketplace
  createInfoAsset: (data: any) =>
    client.post('/marketplace/assets/create', data).then((r) => r.data),
  
  browseMarketplace: (params?: any) =>
    client.get('/marketplace/assets/browse', { params }).then((r) => r.data),
  
  getAssetDetails: (assetId: string) =>
    client.get(`/marketplace/assets/${assetId}`).then((r) => r.data),
  
  purchaseAsset: (assetId: string) =>
    client.post(`/marketplace/assets/${assetId}/purchase`).then((r) => r.data),
  
  subscribe: (data: any) =>
    client.post('/marketplace/subscriptions/subscribe', data).then((r) => r.data),

  // Reputation
  getReputation: (address: string) =>
    client.get(`/reputation/${address}`).then((r) => r.data),
  
  stake: (signalId: number, amount: number) =>
    client.post('/reputation/stake', { signal_id: signalId, amount }).then((r) => r.data),
  
  unstake: (amount: number) =>
    client.post('/reputation/unstake', { amount }).then((r) => r.data),
  
  getLeaderboard: (params?: any) =>
    client.get('/reputation/leaderboard', { params }).then((r) => r.data),
};
