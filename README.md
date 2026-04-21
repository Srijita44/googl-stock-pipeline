# 📈 Google Stock Market Data Pipeline

A complete end-to-end **Data Engineering pipeline** built in Python that ingests, transforms, stores, and analyzes Google (GOOGL) stock market data.

---

## 🚀 Pipeline Overview

```
[Yahoo Finance API] → [Ingestion] → [Transformation] → [SQLite Storage] → [Analysis & Visualization]
```

| Step | Script | Description |
|------|--------|-------------|
| 1 | `scripts/1_ingest.py` | Fetches 2 years of GOOGL data from Yahoo Finance |
| 2 | `scripts/2_transform.py` | Cleans data & engineers features (MA, returns, volatility) |
| 3 | `scripts/3_store.py` | Stores processed data in SQLite database |
| 4 | `scripts/4_analyze.py` | Generates 5 analytical charts |

---

## 📁 Project Structure

```
stock_pipeline/
│
├── main.py                    # Run full pipeline
├── requirements.txt
├── README.md
│
├── scripts/
│   ├── 1_ingest.py
│   ├── 2_transform.py
│   ├── 3_store.py
│   └── 4_analyze.py
│
├── data/                      # Auto-created on run
│   ├── raw_googl.csv
│   ├── transformed_googl.csv
│   ├── stock_data.db
│   └── summary_stats.csv
│
└── outputs/                   # Auto-created on run
    ├── chart1_price_ma.png
    ├── chart2_volume.png
    ├── chart3_daily_returns.png
    ├── chart4_return_distribution.png
    └── chart5_volatility.png
```

---

## ⚙️ Features Engineered

| Feature | Description |
|---------|-------------|
| `MA_7` | 7-day moving average of Close price |
| `MA_30` | 30-day moving average of Close price |
| `Daily_Return_%` | Percentage change in Close price day-over-day |
| `Volatility_7d` | 7-day rolling standard deviation of daily returns |
| `Price_Range` | Daily High minus Low |

---

## 🛠️ Tech Stack

- **Python 3.x**
- **yfinance** — Stock data ingestion
- **pandas** — Data transformation
- **SQLite3** — Data storage
- **matplotlib / seaborn** — Visualization

---

## ▶️ How to Run

```bash
# 1. Clone the repo
git clone <your-repo-url>
cd stock_pipeline

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the full pipeline
python main.py
```

---

## 📊 Output Charts

1. **Close Price + Moving Averages** — trend overview
2. **Daily Trading Volume** — market activity
3. **Daily Return %** — gain/loss per day
4. **Return Distribution** — histogram with KDE
5. **7-Day Rolling Volatility** — risk over time

---

## 👤 Author

- **Name:** Srijita Mandal
- **Roll Number:** 23053373
- **Batch/Program:** B.Tech CSE 3rd Year 2027

---
> **Course:** Data Analytics
