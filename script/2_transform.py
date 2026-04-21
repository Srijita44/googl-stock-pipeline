"""
Step 2: Data Transformation
Cleans raw data and engineers features:
- Moving Averages (7-day, 30-day)
- Daily Return %
- Volatility (rolling std)
- Price Range (High - Low)
"""

import pandas as pd
import os

def transform_data(input_path="data/raw_googl.csv"):
    print("[INFO] Loading raw data...")
    df = pd.read_csv(input_path, parse_dates=["Date"])

    print("[INFO] Cleaning data...")
    df = df[["Date", "Open", "High", "Low", "Close", "Volume"]].copy()
    df.dropna(inplace=True)
    df.sort_values("Date", inplace=True)
    df.reset_index(drop=True, inplace=True)

    print("[INFO] Engineering features...")

    # Moving Averages
    df["MA_7"]  = df["Close"].rolling(window=7).mean().round(2)
    df["MA_30"] = df["Close"].rolling(window=30).mean().round(2)

    # Daily Return %
    df["Daily_Return_%"] = (df["Close"].pct_change() * 100).round(4)

    # Volatility (7-day rolling std of daily return)
    df["Volatility_7d"] = df["Daily_Return_%"].rolling(window=7).std().round(4)

    # Price Range
    df["Price_Range"] = (df["High"] - df["Low"]).round(2)

    # Round price columns
    for col in ["Open", "High", "Low", "Close"]:
        df[col] = df[col].round(2)

    os.makedirs("data", exist_ok=True)
    out_path = "data/transformed_googl.csv"
    df.to_csv(out_path, index=False)

    print(f"[SUCCESS] Transformed data saved to '{out_path}' | Rows: {len(df)}")
    print(df[["Date", "Close", "MA_7", "MA_30", "Daily_Return_%", "Volatility_7d"]].tail(5).to_string(index=False))
    return df

if __name__ == "__main__":
    transform_data()
