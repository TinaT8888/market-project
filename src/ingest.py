import yfinance as yf

# Download S&P 500 data
sp500 = yf.Ticker("^GSPC")
data = sp500.history(period="max")

# Save as CSV
data.to_csv("data/raw/sp500_data.csv")   