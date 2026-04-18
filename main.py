from agents.orchestrator import run_orchestrator
from telegram_sender import send_telegram_message
from config import WATCHLIST
from apscheduler.schedulers.blocking import BlockingScheduler
import datetime
import pytz


def run_analysis():
    print(f"\nStarting analysis at {datetime.datetime.now()}")
    for ticker in WATCHLIST:
        report = run_orchestrator(ticker)
        send_telegram_message(f"<b>Stock Alert</b>\n\n{report}")
        print(f"Alert sent for {ticker}")


if __name__ == "__main__":
    run_analysis()

    scheduler = BlockingScheduler(timezone=pytz.timezone("Europe/Berlin"))

    scheduler.add_job(run_analysis, 'cron', day_of_week='mon-fri', hour=9, minute=0)
    scheduler.add_job(run_analysis, 'cron', day_of_week='mon-fri', hour=15, minute=40)
    scheduler.add_job(run_analysis, 'cron', day_of_week='sat,sun', hour=9, minute=0)

    print("\nScheduler started")
    scheduler.start()