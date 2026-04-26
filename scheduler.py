import datetime
import re

import pytz
from apscheduler.schedulers.background import BackgroundScheduler

from agents.orchestrator import run_orchestrator
from config import STOCK_WATCHLIST, CRYPTO_WATCHLIST
from db.database import save_signal
from telegram_sender import send_telegram_message


def parse_report(report: str) -> dict:
    """Extract structured data from the orchestrator report."""
    result = {
        "price": 0.0,
        "signal": "HOLD",
        "reason": "",
        "ema_status": ""
    }
    try:
        price_match = re.search(r'PRICE:\s*\$?([\d,]+\.?\d*)', report)
        if price_match:
            result["price"] = float(price_match.group(1).replace(",", ""))

        signal_match = re.search(r'SIGNAL:\s*(BUY|SELL|HOLD)', report)
        if signal_match:
            result["signal"] = signal_match.group(1)

        reason_match = re.search(r'REASON:\s*(.+?)(?:EMA STATUS:|$)', report, re.DOTALL)
        if reason_match:
            result["reason"] = reason_match.group(1).strip()

        ema_match = re.search(r'EMA STATUS:\s*(.+?)$', report, re.MULTILINE)
        if ema_match:
            result["ema_status"] = ema_match.group(1).strip()
    except Exception:
        pass
    return result


def _analyze_tickers(tickers: list):
    """Core analysis loop — shared by stock and crypto runners."""
    print(f"\nStarting analysis at {datetime.datetime.now()} for: {tickers}")
    for ticker in tickers:
        try:
            report = run_orchestrator(ticker)
            send_telegram_message(f"<b>Stock Alert</b>\n\n{report}")

            parsed = parse_report(report)
            save_signal(
                ticker=ticker,
                price=parsed["price"],
                signal=parsed["signal"],
                reason=parsed["reason"],
                ema_status=parsed["ema_status"]
            )
            print(f"Alert sent and signal saved for {ticker}")
        except Exception as e:
            print(f"Error analyzing {ticker}: {e}")


def run_analysis_stocks():
    """Runs on weekdays only — stock markets are closed on weekends."""
    _analyze_tickers(STOCK_WATCHLIST)


def run_analysis_crypto():
    """Runs every day — crypto trades 24/7 including weekends."""
    _analyze_tickers(CRYPTO_WATCHLIST)


def run_analysis_all():
    """Runs full watchlist — used for manual trigger or initial run."""
    _analyze_tickers(STOCK_WATCHLIST + CRYPTO_WATCHLIST)


def start_scheduler():
    berlin = pytz.timezone("Europe/Berlin")
    scheduler = BackgroundScheduler(timezone=berlin)

    scheduler.add_job(run_analysis_stocks, 'cron', day_of_week='mon-fri', hour=9,  minute=5)
    scheduler.add_job(run_analysis_stocks, 'cron', day_of_week='mon-fri', hour=15, minute=35)

    scheduler.add_job(run_analysis_crypto, 'cron', hour=9,  minute=5)
    scheduler.add_job(run_analysis_crypto, 'cron', hour=15, minute=35)

    scheduler.start()
    print("Scheduler started — Berlin timezone")
    print(f"  Stocks  (mon-fri): 09:05, 15:35 — {STOCK_WATCHLIST}")
    print(f"  Crypto  (daily):   09:05, 15:35 — {CRYPTO_WATCHLIST}")