import threading
import datetime
import uvicorn
from apscheduler.schedulers.background import BackgroundScheduler
import pytz

from agents.orchestrator import run_orchestrator
from telegram_sender import send_telegram_message
from config import WATCHLIST
from db.database import init_db, save_signal
import re


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


def run_analysis():
    print(f"\nStarting analysis at {datetime.datetime.now()}")
    for ticker in WATCHLIST:
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


def start_scheduler():
    scheduler = BackgroundScheduler(timezone=pytz.timezone("Europe/Berlin"))
    scheduler.add_job(run_analysis, 'cron', day_of_week='mon-fri', hour=9, minute=0)
    scheduler.add_job(run_analysis, 'cron', day_of_week='mon-fri', hour=15, minute=40)
    scheduler.add_job(run_analysis, 'cron', day_of_week='sat,sun', hour=9, minute=0)
    scheduler.start()
    print("Scheduler started — Berlin timezone")


if __name__ == "__main__":
    init_db()

    thread = threading.Thread(target=run_analysis)
    thread.start()

    start_scheduler()

    uvicorn.run("api.dashboard:app", host="0.0.0.0", port=8000, reload=False)