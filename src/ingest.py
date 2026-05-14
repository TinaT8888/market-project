import yfinance as yf
from pathlib import Path

# Create folders if they do not already exist
Path("data/raw").mkdir(parents=True, exist_ok=True)

# Download S&P 500 data
sp500 = yf.Ticker("^GSPC")
sp500_data = sp500.history(period="1y")
sp500_data.to_csv("data/raw/sp500_data.csv")

# Download VIX data
vix = yf.Ticker("^VIX")
vix_data = vix.history(period="1y")
vix_data.to_csv("data/raw/vix_data.csv")

print("Raw data ingestion complete.")
print("Saved: data/raw/sp500_data.csv")
print("Saved: data/raw/vix_data.csv")