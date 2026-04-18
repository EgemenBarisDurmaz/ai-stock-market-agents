# ai-stock-market-agents

Multi-agent AI system that autonomously monitors stocks and crypto,
applies EMA-based technical analysis, and delivers alerts via Telegram.

## Architecture

```
Orchestrator
├── Research Agent
│     ├── get_stock_price()     ← yfinance
│     └── get_recent_news()     ← NewsAPI
│
└── Analysis Agent
├── calculate_ema()       ← 20, 50, 100, 200 days
└── check_positions() ←  active positions
```

## Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3.12 |
| Agent Framework | LangGraph + LangChain |
| LLM | Claude 3 Haiku (Anthropic) |
| Stock Data | yfinance |
| News | NewsAPI |
| Alerts | Telegram Bot API |
| Scheduler | APScheduler (GMT+2) |

## What it monitors

- Stocks: AAPL, NVDA, MSFT, LVMH (MC.PA)
- Crypto: BTC, ETH

## Schedule

**Based on US and EU openings

- Weekdays: 9:00 AM and 3:40 PM (GMT+2)
- Weekends: 9:00 AM (GMT+2)

## Alert format

```
Stock Alert
TICKER: AAPL
PRICE: $270.23
SIGNAL: BUY
REASON: Technical analysis shows bullish momentum...
EMA STATUS: Above key EMAs
```

## Setup

**1. Clone the repo**
```bash
git clone https://github.com/EgemenBarisDurmaz/ai-stock-market-agents
cd ai-stock-market-agents
pip install -r requirements.txt
```

**2. Set environment variables**
```powershell
[System.Environment]::SetEnvironmentVariable("ANTHROPIC_API_KEY", "sk-ant-...", "User")
[System.Environment]::SetEnvironmentVariable("NEWS_API_KEY", "your-key", "User")
[System.Environment]::SetEnvironmentVariable("TELEGRAM_BOT_TOKEN", "your-token", "User")
[System.Environment]::SetEnvironmentVariable("TELEGRAM_CHAT_ID", "your-chat-id", "User")
```

**3. Update your positions**

Edit `data/positions.json` with your open trades.

**4. Run**
```bash
python main.py
```

## Key Design Decisions

- **Multi-agent separation**: Research and Analysis agents are independent —
  research gathers raw data, analysis applies trading logic
- **Local tool execution**: All data fetching happens in Python tools,
  Claude only reasons and decides
- **Timezone-aware scheduling**: APScheduler with Europe/Berlin timezone
  ensures alerts arrive at market-relevant times