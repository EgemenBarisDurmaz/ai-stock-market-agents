import yfinance as yf
import json
from config import POSITIONS_FILE


def calculate_ema(ticker: str) -> dict:
    stock = yf.Ticker(ticker)
    hist = stock.history(period="1y")

    if hist.empty:
        return {"error": f"No data found for {ticker}"}

    close = hist["Close"]
    current_price = round(close.iloc[-1], 2)

    return {
        "ticker": ticker,
        "current_price": current_price,
        "ema_20": round(close.ewm(span=20).mean().iloc[-1], 2),
        "ema_50": round(close.ewm(span=50).mean().iloc[-1], 2),
        "ema_100": round(close.ewm(span=100).mean().iloc[-1], 2),
        "ema_200": round(close.ewm(span=200).mean().iloc[-1], 2),
    }


def check_positions() -> list:
    try:
        with open(POSITIONS_FILE, "r") as f:
            data = json.load(f)
        return data.get("positions", [])
    except FileNotFoundError:
        return []