import pandas as pd
from pathlib import Path
from datetime import datetime

# Create folders if they do not exist
Path("data/curated").mkdir(parents=True, exist_ok=True)
Path("logs").mkdir(parents=True, exist_ok=True)

# File paths
sp500_path = "data/raw/sp500_data.csv"
vix_path = "data/raw/vix_data.csv"
output_path = "data/curated/market_base.csv"
log_path = "logs/data_quality_log.csv"

# Quality log storage
quality_logs = []

def log_issue(source, issue_type, record_count, action_taken):
    quality_logs.append({
        "timestamp": datetime.now().isoformat(),
        "source": source,
        "issue_type": issue_type,
        "record_count": record_count,
        "action_taken": action_taken
    })

# Read raw CSV files
sp500 = pd.read_csv(sp500_path)
vix = pd.read_csv(vix_path)

# Convert dates and standardise timezone handling
sp500["Date"] = pd.to_datetime(sp500["Date"], utc=True).dt.date
vix["Date"] = pd.to_datetime(vix["Date"], utc=True).dt.date

# Keep required columns only
sp500 = sp500[["Date", "Open", "High", "Low", "Close", "Volume"]].copy()
vix = vix[["Date", "Close"]].copy()

# Rename columns
sp500 = sp500.rename(columns={
    "Open": "SP500_Open",
    "High": "SP500_High",
    "Low": "SP500_Low",
    "Close": "SP500_Close",
    "Volume": "SP500_Volume"
})

vix = vix.rename(columns={
    "Close": "VIX_Close"
})

# Basic data quality checks
sp500_nulls = sp500.isnull().sum().sum()
vix_nulls = vix.isnull().sum().sum()

if sp500_nulls > 0:
    log_issue(
        "S&P 500",
        "Null values detected",
        int(sp500_nulls),
        "Retained rows and flagged for review"
    )

if vix_nulls > 0:
    log_issue(
        "VIX",
        "Null values detected",
        int(vix_nulls),
        "Retained rows and flagged for review"
    )

# Merge datasets on Date
market_base = pd.merge(
    sp500,
    vix,
    on="Date",
    how="outer"
)

# Sort by Date
market_base = market_base.sort_values("Date")

# Check merged dataset for missing values
alignment_nulls = market_base.isnull().sum().sum()

if alignment_nulls > 0:
    log_issue(
        "Merged dataset",
        "Missing values after alignment",
        int(alignment_nulls),
        "Retained rows for Power BI visibility"
    )

# Save curated dataset
market_base.to_csv(output_path, index=False)

# Save quality log
pd.DataFrame(quality_logs).to_csv(log_path, index=False)

print("Transformation complete.")
print(f"Saved curated dataset: {output_path}")
print(f"Saved quality log: {log_path}")