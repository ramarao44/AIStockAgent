📘 AIStockAgent — High Level Design & Detailed Requirements
Version: 1.0
Platform: Windows 11 AI PC
Architecture: Python + n8n + Free APIs + WhatsApp + Web UI
🧭 1. Product Overview
🎯 Vision

Build a zero-cost AI-powered stock intelligence system that helps users:

Analyze stocks on demand (web interface + WhatsApp chat)
Receive daily market insights via WhatsApp
Get BUY / SELL / HOLD recommendations
Understand short-term and long-term opportunities
Track risk and market conditions
🧠 Core Idea

“User interacts via WhatsApp or Web → AI analyzes markets → returns structured investment decisions with reasoning”

👤 2. User Requirements
2.1 On-Demand Stock Analysis (Web + WhatsApp)

User can ask:

“AAPL analysis”
“Should I buy Tesla?”
“Top stocks today”
“Short-term opportunities”

System responds with:

Technical analysis
Fundamental summary
News sentiment
Risk level
AI decision
2.2 Daily WhatsApp Market Report

User receives:

Top BUY stocks
Long-term stable picks
Market sentiment summary
Risk warnings
Avoid list
2.3 Conversational AI Behavior

System must support:

follow-up questions
memory of last stock
contextual understanding

Example:

User: AAPL analysis
User: what about long term?
System: understands AAPL context
🏗️ 3. High-Level Architecture
                    ┌──────────────────────┐
                    │  WhatsApp / Web UI   │
                    └─────────┬────────────┘
                              │
               ┌──────────────▼──────────────┐
               │  API Gateway (FastAPI)      │
               └──────────────┬──────────────┘
                              │
      ┌────────────────────────┼────────────────────────┐
      ▼                        ▼                        ▼
┌──────────────┐     ┌────────────────┐      ┌────────────────┐
│ Market Data  │     │ Analysis Layer │      │ News Layer     │
│ Yahoo Finance│     │ TA + FA        │      │ GNews RSS      │
└──────────────┘     └────────────────┘      └────────────────┘
                              │
                              ▼
               ┌──────────────────────────────┐
               │ AI Decision Engine           │
               │ BUY / SELL / HOLD / NONE     │
               └──────────────┬──────────────┘
                              ▼
               ┌──────────────────────────────┐
               │ Response Formatter           │
               │ WhatsApp / Web JSON Output   │
               └──────────────┬──────────────┘
                              ▼
                    ┌──────────────────────┐
                    │ WhatsApp / UI Output │
                    └──────────────────────┘
⚙️ 4. System Components (Detailed Design)
4.1 API Layer (FastAPI)
Responsibilities:
Receive user queries
Route requests
Return structured responses
Endpoints:
POST /analyze-stock

Input:

{
  "symbol": "AAPL"
}

Output:

{
  "symbol": "AAPL",
  "decision": "BUY",
  "confidence": 0.82,
  "short_term": "BUY",
  "long_term": "HOLD",
  "risk_level": "MEDIUM",
  "reasoning": [
    "Strong RSI reversal",
    "Positive earnings news",
    "Stable fundamentals"
  ]
}
POST /chat

Handles WhatsApp + web queries

Input:

{
  "user_id": "123",
  "message": "AAPL good for long term?"
}
4.2 Market Data Layer
Source:
Yahoo Finance (yfinance)
Responsibilities:
Fetch stock price
Volume data
Historical OHLC
Output:
{
  "symbol": "AAPL",
  "price": 190,
  "volume": 1200000,
  "history": []
}
4.3 Technical Analysis Module
Indicators:
RSI
MACD
EMA (20, 50)
Bollinger Bands
Output:
{
  "rsi": 62,
  "macd": 1.1,
  "ema_trend": "bullish",
  "volatility": "medium"
}
4.4 Fundamental Analysis Module
Metrics:
PE ratio
PB ratio
ROE
ROCE
Debt/Equity
Output:
{
  "pe": 28,
  "roe": 18,
  "debt_equity": 0.4,
  "fundamental_score": 8.1
}
4.5 News & Sentiment Module
Data Source:
Google News RSS (free)
Processing:
keyword extraction
sentiment scoring
Output:
{
  "sentiment": "positive",
  "score": 0.65,
  "events": ["earnings_growth"]
}
4.6 AI Decision Engine
Responsibilities:
combine all signals
generate final recommendation
Inputs:
technical score
fundamental score
sentiment score
market regime
Output:
{
  "decision": "BUY",
  "confidence": 0.78,
  "time_horizon": "short_term",
  "risk_level": "medium"
}
4.7 Market Regime Detector (IMPORTANT)
Types:
Bull market
Bear market
Sideways market
Logic:

Based on:

moving averages
trend direction
volatility
4.8 Risk Engine
Responsibilities:
volatility scoring
drawdown estimation
trade validity check
Output:
{
  "risk_score": 0.72,
  "risk_level": "HIGH",
  "trade_allowed": true
}
4.9 WhatsApp Integration Layer
Mode:
WhatsApp Cloud API OR Twilio Sandbox
Responsibilities:
receive messages (webhook)
send responses
send daily reports
4.10 n8n Automation Layer
Responsibilities:
scheduled daily execution
trigger backend API
format messages
send WhatsApp updates
🧠 5. AI Behavior Rules
Decision Rules:
Condition	Action
Strong technical + positive news	BUY
Weak fundamentals	SELL
Mixed signals	HOLD
High risk	NO TRADE
🧱 6. Project Structure
AIStockAgent/
│
├── backend/
│   ├── api/
│   ├── core/
│   ├── data/
│   ├── indicators/
│   ├── fundamentals/
│   ├── news/
│   ├── risk/
│   ├── regime/
│   └── main.py
│
├── frontend/
│   ├── web_app.py
│
├── automation/
│   ├── n8n_workflow.json
│
├── docs/
│   ├── architecture.md
│   ├── requirements.md
│
├── tests/
├── requirements.txt
└── README.md
📊 7. Execution Flow
Web Request Flow:
User → API → Data Fetch → Analysis → AI Engine → Response → UI
WhatsApp Flow:
User → WhatsApp → Webhook → API → AI Engine → Response → WhatsApp
Daily Flow:
n8n Cron → API → Batch Analysis → Ranking → WhatsApp Report
🧪 8. Non-Functional Requirements
Response time < 3 seconds per stock
Fail-safe per stock (no system crash)
Stateless API design
Modular components
Fully offline-capable core logic (except APIs)
💰 9. Zero-Cost Constraints

Must use only:

Yahoo Finance
Google News RSS
Free WhatsApp API tier or sandbox
Local Python execution
n8n self-hosted
🚀 10. MVP Development Phases
Phase 1:
Market data
Technical indicators
API layer
Phase 2:
Fundamental analysis
News sentiment
Phase 3:
AI decision engine
Phase 4:
WhatsApp integration
Phase 5:
n8n automation
Phase 6:
Web UI
🧠 11. Key Design Principles
Modular architecture
No external paid dependencies
Structured JSON outputs only
Event-driven automation
Risk-first decision making
Multi-timeframe analysis

🧩 12. Current Implementation Mapping
The repository currently implements a lightweight version of the architecture above.

Flow:
1. Input layer
   - [Python/services/watchlist_service.py](../Python/services/watchlist_service.py) reads a local watchlist.
   - [api/app.py](../api/app.py) accepts HTTP requests for on-demand analysis.
2. Data layer
   - [Python/data_sources/yahoo.py](../Python/data_sources/yahoo.py) fetches stock history from Yahoo Finance.
   - [Python/services/market_data_service.py](../Python/services/market_data_service.py) normalizes the data for the analysis modules.
3. Analysis layer
   - [Python/analysis/techincal_analysis.py](../Python/analysis/techincal_analysis.py) computes simple technical signals.
   - [Python/analysis/fundamental_analysis.py](../Python/analysis/fundamental_analysis.py) creates a basic fundamental score.
   - [Python/analysis/decision_engine.py](../Python/analysis/decision_engine.py) converts those signals into BUY/SELL/HOLD output.
4. Delivery layer
   - [Python/main.py](../Python/main.py) runs the pipeline from the terminal.
   - [n8n/workflow.json](../n8n/workflow.json) wires the analysis into scheduled automation.
   - [Python/integrations/whatsapp.py](../Python/integrations/whatsapp.py) provides the outbound WhatsApp helper.

This modular structure keeps each layer easy to extend: the input source can change, the data provider can be swapped, the analysis can become more advanced, and the delivery channel can expand to new interfaces.