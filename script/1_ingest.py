"""
Step 1: Data Ingestion
Simulates fetching Google (GOOGL) stock data (2 years of realistic OHLCV data).
In a live environment, replace generate_googl_data() with a yfinance / Alpha Vantage call.
"""

import pandas as pd
import numpy as np
import os
from datetime import date, timedelta

def generate_googl_data(start_price=130.0, days=504, seed=42):
    """Generate realistic GOOGL-like stock data using geometric Brownian motion."""
    np.random.seed(seed)
    end_date   = date(2026, 4, 18)
    start_date = end_date - timedelta(days=int(days * 365 / 252))  # approx calendar days

    # Build business-day date range
    dates = pd.bdate_range(end=end_date, periods=days)

    n = len(dates)  # use actual length of business-day range

    # Simulate log-normal returns (mu=0.0003, sigma=0.018 ~ GOOGL historical)
    mu, sigma = 0.0003, 0.018
    returns = np.random.normal(mu, sigma, n)
    close_prices = start_price * np.exp(np.cumsum(returns))

    # Build OHLCV
    daily_range = np.abs(np.random.normal(0, 0.012, n)) * close_prices
    opens   = close_prices - np.random.uniform(-0.5, 0.5, n) * daily_range
    highs   = np.maximum(opens, close_prices) + np.abs(np.random.normal(0, 0.4, n)) * daily_range
    lows    = np.minimum(opens, close_prices) - np.abs(np.random.normal(0, 0.4, n)) * daily_range
    volumes = (np.random.normal(25e6, 6e6, n)).clip(5e6).astype(int)

    df = pd.DataFrame({
        "Date":   dates,
        "Open":   opens.round(2),
        "High":   highs.round(2),
        "Low":    lows.round(2),
        "Close":  close_prices.round(2),
        "Volume": volumes,
    })
    return df

def fetch_stock_data():
    print("[INFO] Generating GOOGL stock data (2 years, 504 trading days)...")
    df = generate_googl_data()

    os.makedirs("data", exist_ok=True)
    raw_path = "data/raw_googl.csv"
    df.to_csv(raw_path, index=False)

    print(f"[SUCCESS] Raw data saved to '{raw_path}' | Rows: {len(df)}")
    print(df[["Date", "Open", "High", "Low", "Close", "Volume"]].tail(5).to_string(index=False))
    return df

if __name__ == "__main__":
    fetch_stock_data()
