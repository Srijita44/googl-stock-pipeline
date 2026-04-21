"""
Step 4: Analysis & Visualization
Generates 5 insightful charts from the processed Google stock data.
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
import sqlite3
import os

sns.set_theme(style="darkgrid")
COLORS = {"blue": "#4285F4", "red": "#EA4335", "green": "#34A853", "yellow": "#FBBC05", "purple": "#7B2FBE"}

def load_data():
    conn = sqlite3.connect("data/stock_data.db")
    df = pd.read_sql("SELECT * FROM googl_stock", conn, parse_dates=["Date"])
    conn.close()
    return df

def plot1_price_and_ma(df, out_dir):
    fig, ax = plt.subplots(figsize=(14, 5))
    ax.plot(df["Date"], df["Close"],  label="Close Price",  color=COLORS["blue"],   linewidth=1.5, alpha=0.9)
    ax.plot(df["Date"], df["MA_7"],   label="7-Day MA",     color=COLORS["yellow"], linewidth=1.5, linestyle="--")
    ax.plot(df["Date"], df["MA_30"],  label="30-Day MA",    color=COLORS["red"],    linewidth=2,   linestyle="-.")
    ax.set_title("Google (GOOGL) — Close Price with Moving Averages", fontsize=14, fontweight="bold")
    ax.set_xlabel("Date"); ax.set_ylabel("Price (USD)")
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
    ax.legend(); fig.tight_layout()
    path = f"{out_dir}/chart1_price_ma.png"
    fig.savefig(path, dpi=150); plt.close()
    print(f"[SAVED] {path}")

def plot2_volume(df, out_dir):
    fig, ax = plt.subplots(figsize=(14, 4))
    ax.bar(df["Date"], df["Volume"] / 1e6, color=COLORS["blue"], alpha=0.6, width=1.5)
    ax.set_title("Google (GOOGL) — Daily Trading Volume", fontsize=14, fontweight="bold")
    ax.set_xlabel("Date"); ax.set_ylabel("Volume (Millions)")
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
    fig.tight_layout()
    path = f"{out_dir}/chart2_volume.png"
    fig.savefig(path, dpi=150); plt.close()
    print(f"[SAVED] {path}")

def plot3_daily_returns(df, out_dir):
    fig, ax = plt.subplots(figsize=(14, 4))
    colors = [COLORS["green"] if x >= 0 else COLORS["red"] for x in df["Daily_Return_%"].fillna(0)]
    ax.bar(df["Date"], df["Daily_Return_%"], color=colors, alpha=0.8, width=1.5)
    ax.axhline(0, color="white", linewidth=0.8, linestyle="--")
    ax.set_title("Google (GOOGL) — Daily Return %", fontsize=14, fontweight="bold")
    ax.set_xlabel("Date"); ax.set_ylabel("Return (%)")
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
    fig.tight_layout()
    path = f"{out_dir}/chart3_daily_returns.png"
    fig.savefig(path, dpi=150); plt.close()
    print(f"[SAVED] {path}")

def plot4_return_distribution(df, out_dir):
    fig, ax = plt.subplots(figsize=(9, 5))
    returns = df["Daily_Return_%"].dropna()
    sns.histplot(returns, bins=60, kde=True, color=COLORS["blue"], ax=ax, edgecolor="none")
    ax.axvline(returns.mean(), color=COLORS["red"],    linestyle="--", label=f"Mean: {returns.mean():.2f}%")
    ax.axvline(returns.median(), color=COLORS["green"], linestyle="-.", label=f"Median: {returns.median():.2f}%")
    ax.set_title("Distribution of Daily Returns — GOOGL", fontsize=14, fontweight="bold")
    ax.set_xlabel("Daily Return (%)"); ax.set_ylabel("Frequency")
    ax.legend(); fig.tight_layout()
    path = f"{out_dir}/chart4_return_distribution.png"
    fig.savefig(path, dpi=150); plt.close()
    print(f"[SAVED] {path}")

def plot5_volatility(df, out_dir):
    fig, ax = plt.subplots(figsize=(14, 4))
    ax.fill_between(df["Date"], df["Volatility_7d"], color=COLORS["purple"], alpha=0.5, label="7-Day Volatility")
    ax.plot(df["Date"], df["Volatility_7d"], color=COLORS["purple"], linewidth=1)
    ax.set_title("Google (GOOGL) — 7-Day Rolling Volatility", fontsize=14, fontweight="bold")
    ax.set_xlabel("Date"); ax.set_ylabel("Volatility (Std Dev of Returns)")
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
    ax.legend(); fig.tight_layout()
    path = f"{out_dir}/chart5_volatility.png"
    fig.savefig(path, dpi=150); plt.close()
    print(f"[SAVED] {path}")

def print_insights(df):
    print("\n" + "="*55)
    print("         📊 KEY INSIGHTS — GOOGL STOCK")
    print("="*55)
    latest = df.iloc[-1]
    print(f"  Latest Close Price   : ${latest['Close']:.2f}")
    print(f"  Latest Date          : {latest['Date'].strftime('%Y-%m-%d')}")
    print(f"  52-Week High         : ${df['High'].max():.2f}")
    print(f"  52-Week Low          : ${df['Low'].min():.2f}")
    returns = df["Daily_Return_%"].dropna()
    print(f"  Avg Daily Return     : {returns.mean():.4f}%")
    print(f"  Best Day Return      : {returns.max():.4f}%")
    print(f"  Worst Day Return     : {returns.min():.4f}%")
    print(f"  Avg Daily Volume     : {df['Volume'].mean()/1e6:.2f}M")
    print("="*55 + "\n")

def analyze():
    print("[INFO] Loading data from database...")
    df = load_data()
    out_dir = "outputs"
    os.makedirs(out_dir, exist_ok=True)

    print("[INFO] Generating charts...")
    plot1_price_and_ma(df, out_dir)
    plot2_volume(df, out_dir)
    plot3_daily_returns(df, out_dir)
    plot4_return_distribution(df, out_dir)
    plot5_volatility(df, out_dir)
    print_insights(df)
    print("[SUCCESS] All charts saved to 'outputs/' folder.")

if __name__ == "__main__":
    analyze()
