"""
Step 3: Data Storage
Stores transformed data into a SQLite database.
Also saves a summary statistics CSV.
"""

import pandas as pd
import sqlite3
import os

def store_data(input_path="data/transformed_googl.csv"):
    print("[INFO] Loading transformed data...")
    df = pd.read_csv(input_path, parse_dates=["Date"])

    os.makedirs("data", exist_ok=True)
    db_path = "data/stock_data.db"

    print(f"[INFO] Storing data into SQLite database at '{db_path}'...")
    conn = sqlite3.connect(db_path)
    df.to_sql("googl_stock", conn, if_exists="replace", index=False)
    conn.close()
    print(f"[SUCCESS] Data stored in table 'googl_stock' | Rows: {len(df)}")

    # Also save summary statistics
    summary = df[["Open", "High", "Low", "Close", "Volume", "Daily_Return_%", "Volatility_7d"]].describe().round(4)
    summary_path = "data/summary_stats.csv"
    summary.to_csv(summary_path)
    print(f"[SUCCESS] Summary statistics saved to '{summary_path}'")
    print(summary)

    # Verify by reading back
    conn = sqlite3.connect(db_path)
    verify = pd.read_sql("SELECT COUNT(*) as total_rows FROM googl_stock", conn)
    conn.close()
    print(f"[VERIFY] Rows in DB: {verify['total_rows'][0]}")

if __name__ == "__main__":
    store_data()
