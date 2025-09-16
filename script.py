import requests
import os
import csv

from dotenv import load_dotenv
# Load environment variables from .env file
load_dotenv()

# Request parameters
API_KEY=os.getenv("POLYGON_API_KEY")  # Polygon.io API key
LIMIT=1000 # Number of tickers to fetch per request

# API endpoint for fetching active stock tickers
url=f"https://api.polygon.io/v3/reference/tickers?market=stocks&active=true&order=asc&limit={LIMIT}&sort=ticker&apiKey={API_KEY}"

# Fetch the first page of ticker data
response = requests.get(url)
data = response.json()

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
        for ticker in data['results']:
            tickers.append(ticker)

# Define output CSV file path
output_csv='data/tickers.csv'

# Extract CSV column names from the first ticker's keys
fieldnames=list(tickers[0].keys())

# Write all ticker data into a CSV file
with open(output_csv, mode='w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader() # Write header row
    for ticker in tickers:
        # Write each ticker row, fill missing keys with empty string
        row = {key: ticker.get(key,'') for key in fieldnames}
        writer.writerow(row)

print(f'Wrote {len(tickers)} rows to {output_csv}.')
