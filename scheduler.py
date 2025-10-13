import schedule
import time
from script import run_stock_ticker_fetcher

from datetime import datetime


# Run every 10 minutes
print(f"Scheduler started at {datetime.now()}")
print("Fetching stock tickers every 10 minutes...")
schedule.every(10).minutes.do(run_stock_ticker_fetcher)

# # Run every day at 09:30 AM
# schedule.every().day.at("09:30").do(run_stock_ticker_fetcher)

while True:
    schedule.run_pending()
    time.sleep(1)