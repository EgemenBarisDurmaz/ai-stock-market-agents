import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
POSITIONS_FILE = os.path.join(BASE_DIR, "data", "positions.json")

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
NEWS_API_KEY = os.getenv("NEWS_API_KEY")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

STOCK_WATCHLIST = ["AAPL", "NVDA", "MC.PA"]
CRYPTO_WATCHLIST = ["BTC-USD", "ETH-USD"]
WATCHLIST = STOCK_WATCHLIST + CRYPTO_WATCHLIST