# InfoFi Platform

A comprehensive DeFi intelligence platform built with React, TypeScript, and Python.

🚀 **Live Demo**: [https://tonymech111.github.io/freedomAi/](https://tonymech111.github.io/freedomAi/)

A decentralized marketplace for AI-powered trading signals on TON blockchain. Connect with top creators, share insights, and earn rewards for your expertise.

## 🏗️ Architecture

### 1. Data Layer
- **On-Chain Indexer**: TON blockchain transaction monitoring, whale alerts, token flows
- **ETL Pipeline**: Kafka-based data ingestion and normalization

### 2. Knowledge Layer
- **Semantic Search**: Weaviate vector database for AI-powered search
- **NLP Processing**: Entity extraction (wallets, tokens, protocols, founders)
- **Indexing Engine**: Real-time data indexing and tagging

### 3. AI Intelligence Layer
- **Agentic AI Models**: Event summarization, anomaly detection, signal correlation
- **LLM Integration**: Open-source models (Llama, Mistral) for analysis
- **Pattern Recognition**: Whale behavior tracking, market manipulation detection

### 4. Monetization Layer
- **Info Tokens**: Jetton-based information assets
- **NFT Reports**: Tokenized research and signals
- **Subscription System**: Tiered access to premium intelligence

### 5. Reputation System
- **Staking Mechanism**: Signal creators stake tokens for credibility
- **Reputation NFTs**: Achievement badges for accurate predictions
- **Trust Scoring**: Algorithm-based creator ranking

## 🚀 Tech Stack

- **Frontend**: React + TypeScript, Vite, TailwindCSS
- **Blockchain**: TON SDK, TonAPI
- **UI Components**: Radix UI, Lucide Icons
- **State Management**: Zustand, React Query
- **Routing**: React Router DOM
- **Styling**: TailwindCSS with custom animations
- **Deployment**: GitHub Pages, Vercel

## 📦 Project Structure

```
freedom-ai-platform/
├── frontend/
│   ├── web-app/             # React landing page & dashboard
│   │   ├── src/
│   │   │   ├── components/  # Reusable UI components
│   │   │   ├── pages/       # Landing, Dashboard, etc.
│   │   │   └── lib/         # Utilities
│   │   └── package.json
│   └── telegram-mini-app/   # Telegram Mini App
└── docs/                    # Documentation
```

## 🔧 Installation

### Prerequisites
- Node.js 18+
- npm or yarn
- Git

### ⚡ Quick Start

**Clone and Setup:**
```bash
git clone https://github.com/yourusername/freedom-ai-platform.git
cd freedom-ai-platform/frontend/web-app
npm install
npm run dev
```

**Access the platform:**
- Local: http://localhost:5173
- Live Demo: https://yourusername.github.io/freedom-ai-platform

### Development

**Install Dependencies:**
```bash
cd frontend/web-app
npm install
```

**Start Development Server:**
```bash
npm run dev
```

**Build for Production:**
```bash
npm run build
```

**Preview Production Build:**
```bash
npm run preview
```

## 🔑 Environment Variables

Create `.env` files in respective directories:

```env
# Backend
TON_API_KEY=your_ton_api_key
DATABASE_URL=postgresql://user:pass@localhost:5432/infofi
KAFKA_BOOTSTRAP_SERVERS=localhost:9092
WEAVIATE_URL=http://localhost:8080
OPENAI_API_KEY=your_openai_key  # Optional for enhanced AI

# Frontend
VITE_API_URL=http://localhost:8000
VITE_TELEGRAM_BOT_TOKEN=your_bot_token
```

## 📊 API Endpoints

### Data Layer
- `GET /api/v1/on-chain/transactions` - Recent TON transactions
- `GET /api/v1/on-chain/whale-alerts` - Large wallet movements
- `GET /api/v1/off-chain/news` - Aggregated news feed

### Knowledge Layer
- `POST /api/v1/search/semantic` - AI-powered semantic search
- `GET /api/v1/entities/{type}` - Get entities (wallets, tokens, etc.)

### AI Intelligence
- `POST /api/v1/ai/analyze` - Analyze wallet or token
- `GET /api/v1/ai/signals` - AI-generated trading signals
- `GET /api/v1/ai/anomalies` - Detected anomalies

### Monetization
- `POST /api/v1/info-assets/create` - Mint info token/NFT
- `GET /api/v1/marketplace` - Browse info marketplace
- `POST /api/v1/subscriptions/subscribe` - Subscribe to creator

### Reputation
- `GET /api/v1/reputation/{address}` - Get creator reputation
- `POST /api/v1/stake` - Stake tokens on signal

## 🎯 Roadmap

- [x] Core architecture design
- [ ] TON indexer implementation
- [ ] Weaviate integration
- [ ] AI agent development
- [ ] Smart contract deployment
- [ ] Telegram Mini App
- [ ] Mainnet launch

## 📄 License

MIT License

## 🤝 Contributing

Contributions welcome! Please read CONTRIBUTING.md for guidelines.
