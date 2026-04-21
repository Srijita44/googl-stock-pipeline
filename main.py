"""
main.py — Run the complete Google Stock Market Data Pipeline
Usage:  python main.py
"""

import importlib.util, os

def load(path):
    spec = importlib.util.spec_from_file_location("mod", path)
    mod  = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

def run_pipeline():
    base = os.path.dirname(os.path.abspath(__file__))

    print("\n" + "="*55)
    print("   GOOGLE STOCK MARKET DATA PIPELINE")
    print("   Student : Srijita Mandal | Roll: 23053373")
    print("   Course  : Data Analytics | B.Tech CSE 3rd Year")
    print("="*55)

    print("\n[STEP 1] DATA INGESTION")
    load(os.path.join(base, "scripts", "1_ingest.py")).fetch_stock_data()

    print("\n[STEP 2] DATA TRANSFORMATION")
    load(os.path.join(base, "scripts", "2_transform.py")).transform_data()

    print("\n[STEP 3] DATA STORAGE")
    load(os.path.join(base, "scripts", "3_store.py")).store_data()

    print("\n[STEP 4] ANALYSIS & VISUALIZATION")
    load(os.path.join(base, "scripts", "4_analyze.py")).analyze()

    print("\n[DONE] Pipeline Complete!")
    print("  -> Charts saved in: outputs/")
    print("  -> Database saved in: data/stock_data.db")
    print("="*55 + "\n")

if __name__ == "__main__":
    run_pipeline()
