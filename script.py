import requests
import os
import csv

from dotenv import load_dotenv
# Load environment variables from .env file
load_dotenv()

# Function to fetch active stock tickers and save to CSV-file.
def run_stock_ticker_fetcher(API_KEY=None, next_url=None):
    # Request parameters
    if API_KEY is None:
        API_KEY = os.getenv("POLYGON_API_KEY")  # Get API key from environment variable if not provided
    
    LIMIT=1000 # Number of tickers to fetch per request

    # API endpoint for fetching active stock tickers
    if next_url is None:
        url=f"https://api.polygon.io/v3/reference/tickers?market=stocks&active=true&order=asc&limit={LIMIT}&sort=ticker&apiKey={API_KEY}"
    else:
        url=next_url+f'&apiKey={API_KEY}'

    # Fetch the first page of ticker data
    response = requests.get(url)
    data = response.json()
    page_number=LIMIT

    # Initialize list to store all tickers
    tickers = []
    for ticker in data['results']:
        tickers.append(ticker)

    # Error message returned when request limit is exceeded
    error_pricing="You've exceeded the maximum requests per minute, please wait or upgrade your subscription to continue. https://polygon.io/pricing"

    # Fetch additional pages if 'next_url' is present
    while 'next_url' in data:
        response = requests.get(data['next_url']+f'&apiKey={API_KEY}')
        data = response.json()

        if data.get("error")==error_pricing:
            break
        else:
            next_url = data['next_url']
            for ticker in data['results']:
                tickers.append(ticker)
        
        page_number+=LIMIT

    # Define output CSV file path
    output_csv='data/tickers.csv'

    # Extract CSV column names from the first ticker's keys
    fieldnames=list(tickers[0].keys())

    # Write all ticker data into a CSV file
    with open(output_csv, mode='a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader() # Write header row
        for ticker in tickers:
            # Write each ticker row, fill missing keys with empty string
            row = {key: ticker.get(key,'') for key in fieldnames}
            writer.writerow(row)
    

    return next_url, page_number

if __name__ == "__main__":
    next_url, page_number = run_stock_ticker_fetcher(next_url='https://api.polygon.io/v3/reference/tickers?cursor=YWN0aXZlPXRydWUmYXA9NTAwMCZhcz0mbGltaXQ9MTAwMCZtYXJrZXQ9c3RvY2tzJm9yZGVyPWFzYyZzb3J0PXRpY2tlcg')
    print(next_url)
    print(f"Fetched {page_number} tickers and saved to data/tickers.csv")
    
