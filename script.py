import requests
import os
from dotenv import load_dotenv
load_dotenv()

API_KEY=os.getenv("POLYGON_API_KEY")
LIMIT=1000

url=f"https://api.polygon.io/v3/reference/tickers?market=stocks&active=true&order=asc&limit={LIMIT}&sort=ticker&apiKey={API_KEY}"

response = requests.get(url)
data = response.json()

tickers = []
for ticker in data["results"]:
    tickers.append(ticker)

print(len(tickers))
