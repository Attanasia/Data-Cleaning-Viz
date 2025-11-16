"""
STEP 3:
- Load cleaned.parquet
- Create 3 small aggregations: average close price per sector, daily average close price across all tickers, average volume by sector
- Save aggregations as agg1.parquet, agg2.parquet, agg3.parquet
"""

import os
import pandas as pd

PRINT_PREFIX = ">>>"

def main():
    parquet_file = "cleaned.parquet"
    if not os.path.exists(parquet_file):
        print(f"{PRINT_PREFIX} ERROR: {parquet_file} not found. Run data_cleaner2.py first.")
        return

    print(f"{PRINT_PREFIX} Loading {parquet_file}")
    df = pd.read_parquet(parquet_file)

    # Ensure numeric columns are numeric
    df["close_price"] = pd.to_numeric(df["close_price"], errors="coerce")
    df["open_price"] = pd.to_numeric(df["open_price"], errors="coerce")
    df["volume"] = pd.to_numeric(df["volume"], errors="coerce")


    # 1) Average closing price per sector
    agg1 = df.groupby("sector", as_index=False)["close_price"].mean()
    agg1.rename(columns={"close_price": "avg_close_price"}, inplace=True)
    agg1["avg_close_price"] = agg1["avg_close_price"].round(2)  
    agg1.to_parquet("agg1.parquet", index=False)
    print(f"{PRINT_PREFIX} Saved agg1.parquet (avg close price per sector)")

 
    # 2) Daily average close price across all tickers
    agg2 = df.groupby("trade_date", as_index=False)["close_price"].mean()
    agg2.rename(columns={"close_price": "daily_avg_close"}, inplace=True)
    agg2["daily_avg_close"] = agg2["daily_avg_close"].round(2)
    agg2.to_parquet("agg2.parquet", index=False)
    print(f"{PRINT_PREFIX} Saved agg2.parquet (daily avg close price across all tickers)")

    # 3) Average volume by sector
    agg3 = df.groupby("sector", as_index=False)["volume"].mean()
    agg3.rename(columns={"volume": "avg_volume"}, inplace=True)
    agg3["avg_volume"] = agg3["avg_volume"].round(0)
    agg3.to_parquet("agg3.parquet", index=False)
    print(f"{PRINT_PREFIX} Saved agg3.parquet (avg volume by sector)")

    print(f"{PRINT_PREFIX} Step 3 complete!")

if __name__ == "__main__":
    main()
