import yfinance as yf
from newsapi import NewsApiClient
from config import NEWS_API_KEY


def get_stock_price(ticker: str) -> dict:
    stock = yf.Ticker(ticker)
    hist = stock.history(period="1d")

    if hist.empty:
        return {"error": f"No data found for {ticker}"}

    current_price = hist["Close"].iloc[-1]
    prev_close = stock.info.get("previousClose", 0)
    change_pct = ((current_price - prev_close) / prev_close * 100) if prev_close else 0

    return {
        "ticker": ticker,
        "current_price": round(current_price, 2),
        "previous_close": round(prev_close, 2),
        "change_percent": round(change_pct, 2),
        "currency": stock.info.get("currency", "USD")
    }


def get_recent_news(ticker: str) -> list:
    try:
        newsapi = NewsApiClient(api_key=NEWS_API_KEY)
        articles = newsapi.get_everything(
            q=ticker,
            language="en",
            sort_by="publishedAt",
            page_size=5
        )

        return [
            {
                "title": a["title"],
                "description": a["description"],
                "published_at": a["publishedAt"],
                "source": a["source"]["name"]
            }
            for a in articles.get("articles", [])
        ]
    except Exception as e:
        return [{"error": str(e)}]