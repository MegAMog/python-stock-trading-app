# python-stock-trading-app
This project uses the [Polygon.io](https://polygon.io) API to extract stock market data.

## Step 1. Get a Polygon.io API Key
* Register at [polygon.io](https://polygon.io) and generate your API key.
* Create a `.env` file in the project root and add your key:
```env
POLYGON_API_KEY = "your_api_key_here"
```

## Step 2. Set Up the Environment
1. Create virtual environment (with python or python3 depending on your Python version)
```bash
python3 -m venv venv
```
2. Activate it
- macOS/Linux (bash):
``` bash
source venv/bin/activate
```
- Windows (PowerShell):
``` powershell
.\venv\Scripts\activate
```
3. Install dependencies
```bash
pip install -r requirements.txt
```

## Step 3. Run the App
1. Run the main script
Execute script.py using python or python3:
```bash
python3 script.py
```

2. Run the scheduler
Execute scheduler.py to automatically run script.py every 10 minutes:
```bash
python3 scheduler.py
```

## Project Structure
```bash
.
├── data
│   └── tickers.csv
├── LICENSE
├── pythonvenv
│   ├── bin
│   ├── include
│   ├── lib
│   └── pyvenv.cfg
├── README.md
├── requirements.txt
├── scheduler.py
└── script.py
```

## Notes
- Make sure your `.env` file is not committed to Git (add it to .gitignore).
- After installing new packages, update dependencies with:
```bash
pip freeze > requirements.txt
```