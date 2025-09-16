import requests
import os
import csv

from dotenv import load_dotenv
load_dotenv()

#Request parameters
API_KEY=os.getenv("POLYGON_API_KEY")
LIMIT=1000

#API url
url=f"https://api.polygon.io/v3/reference/tickers?market=stocks&active=true&order=asc&limit={LIMIT}&sort=ticker&apiKey={API_KEY}"


response = requests.get(url)
data = response.json()

tickers = []
for ticker in data['results']:
    tickers.append(ticker)

error_pricing="You've exceeded the maximum requests per minute, please wait or upgrade your subscription to continue. https://polygon.io/pricing"

while 'next_url' in data:
    response = requests.get(data['next_url']+f'&apiKey={API_KEY}')
    data = response.json()

    if data.get("error")==error_pricing:
        break
    else:
        for ticker in data['results']:
            tickers.append(ticker)

output_csv='tickers.csv'
fieldnames=list(tickers[0].keys())
with open(output_csv, mode='w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    for ticker in tickers:
        row = {key: ticker.get(key,'') for key in fieldnames}
        writer.writerow(row)

print(f'Wrote {len(tickers)} rows to {output_csv}')
