import requests
import os
import csv
import time

from dotenv import load_dotenv
# Load environment variables from .env file
load_dotenv()

# Function to fetch active stock tickers and save to CSV-file.
def run_stock_ticker_fetcher(API_KEY=None):
    # Request parameters
    if API_KEY is None:
        API_KEY = os.getenv("POLYGON_API_KEY")  # Get API key from environment variable if not provided
    
    LIMIT=1000 # Number of tickers to fetch per request

    # API endpoint for fetching active stock tickers
    url=f"https://api.polygon.io/v3/reference/tickers?market=stocks&active=true&order=asc&limit={LIMIT}&sort=ticker&apiKey={API_KEY}"

    # Fetch the first page of ticker data
    response = requests.get(url)
    data = response.json()
    page_number= data.get('count',0)

    # Initialize list to store all tickers
    tickers = []
    for ticker in data['results']:
        tickers.append(ticker)

    # Error message returned when request limit is exceeded
    error_pricing="You've exceeded the maximum requests per minute, please wait or upgrade your subscription to continue. https://polygon.io/pricing"

    # Fetch additional pages if 'next_url' is present
    next_url = data.get('next_url','end')
    while next_url and next_url != 'end':
        response = requests.get(next_url+f'&apiKey={API_KEY}')
        data = response.json()
       
        if data.get("error")==error_pricing:
            print(f"Fetched {page_number} tickers so far.")
            print("Rate limit exceeded. Waiting 1 minute...")
            time.sleep(60)
            continue
        else:
            next_url = data.get('next_url','end')

            for ticker in data['results']:
                tickers.append(ticker)
            
            page_number+=data.get('count',0)

    # Define output CSV file path
    output_csv='data/tickers.csv'

    # Extract CSV column names from the first ticker's keys
    fieldnames=list(tickers[0].keys())

    # Check if the CSV file is not exist and is empty
    write_header = not os.path.exists(output_csv) or os.path.getsize(output_csv) == 0

    # Write all ticker data into a CSV file
    with open(output_csv, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader() # Write header row
        for ticker in tickers:
            # Write each ticker row, fill missing keys with empty string
            row = {key: ticker.get(key,'') for key in fieldnames}
            writer.writerow(row)
    
    return page_number

if __name__ == "__main__":
    page_number = run_stock_ticker_fetcher()
    print(f"Fetched {page_number} tickers and saved to data/tickers.csv")
    
