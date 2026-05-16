import pandas as pd
import yfinance as yf
from pathlib import Path

# Create folders
Path("data/raw").mkdir(parents=True, exist_ok=True)

# -----------------------------
# Source 1: Yahoo Finance
# S&P 500 market index data
# -----------------------------
sp500 = yf.Ticker("^GSPC")
sp500_data = sp500.history(start="2024-04-01")
sp500_data.to_csv("data/raw/sp500_data.csv")

# -----------------------------
# Source 2: FRED
# VIX volatility index
# -----------------------------
fred_vix_url = "https://fred.stlouisfed.org/graph/fredgraph.csv?id=VIXCLS"

vix_data = pd.read_csv(fred_vix_url)
vix_data.to_csv("data/raw/vix_data.csv", index=False)

print("Raw data ingestion complete.")
print("Saved: data/raw/sp500_data.csv")
print("Saved: data/raw/vix_data.csv")
