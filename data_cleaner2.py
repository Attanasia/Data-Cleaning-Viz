"""
STEP 2:
 - Load cleaned_step1.csv
 - Define target schema for each column
 - Parse dates
 - Convert numeric and boolean columns
 - Deduplicate rows
 - Save final cleaned.parquet
"""

import os
import sys
import pandas as pd

PRINT_PREFIX = ">>>"

def main():
    csv_file = "cleaned_step1.csv"
    if not os.path.exists(csv_file):
        print(f"{PRINT_PREFIX} ERROR: {csv_file} not found. Run Step 1 first.")
        sys.exit(2)

    print(f"{PRINT_PREFIX} Loading {csv_file}")
    df = pd.read_csv(csv_file, dtype="object")

    print(f"{PRINT_PREFIX} Shape before typing: {df.shape}")
    print(f"{PRINT_PREFIX} Columns: {list(df.columns)}\n")

    schema = {
        "ticker": "string",
        "sector": "string",
        "exchange": "string",
        "currency": "string",
        "notes": "string",

        "trade_date": "date",   
        "open_price": "float",
        "close_price": "float",
        "volume": "int",

        "validated": "bool",   
    }

    # DATE 
    if "trade_date" in df.columns:
        df["trade_date"] = pd.to_datetime(
            df["trade_date"].replace("NA", pd.NA),
            errors="coerce"
        )

    # FLOAT COLUMNS
    for col, t in schema.items():
        if t == "float" and col in df.columns:
            df[col] = pd.to_numeric(df[col].replace("NA", pd.NA), errors="coerce")

    # INTEGER COLUMNS 
    for col, t in schema.items():
        if t == "int" and col in df.columns:
            df[col] = pd.to_numeric(df[col].replace("NA", pd.NA), errors="coerce").astype("Int64")

    # BOOLEAN 
    if schema.get("validated") == "bool" and "validated" in df.columns:
        mapping = {
            "YES": True,
            "NO": False,
            "NA": pd.NA
        }
        df["validated"] = df["validated"].map(mapping)

    # DEDUPLICATE ROWS
    before = len(df)
    df = df.drop_duplicates()
    after = len(df)
    print(f"{PRINT_PREFIX} Deduplicated rows: {before - after} removed")

    # SAVE AS PARQUET
    
    output = "cleaned.parquet"
    df.to_parquet(output, index=False)
    print(f"{PRINT_PREFIX} Saved final file: {output}")


if __name__ == "__main__":
    main()
