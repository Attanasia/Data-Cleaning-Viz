"""
STEP 1:
 - Load raw CSV
 - Inspect + normalize headers
 - Normalize values
 - Apply your exact formatting rules per column
 - Fix trade_date to yyyy-mm-dd
 - Save cleaned_step1.csv
 - Print summary preview

Missing value standard = "NA" (all caps)
"""

import sys
import os
from datetime import datetime
import pandas as pd

PRINT_PREFIX = ">>>"
def safe_read_csv(path):
    return pd.read_csv(path, dtype="object", keep_default_na=False)

def to_snake_case(cols):
    return (
        cols
        .str.strip()
        .str.replace(r'[^\w\s]', '', regex=True)  
        .str.replace(r'\s+', '_', regex=True)    
        .str.lower()
    )

def normalize_cell(val, missing_set):
    """Convert empty-like values → 'NA'."""
    if pd.isna(val):
        return "NA"
    if isinstance(val, str):
        v = val.strip()
        if v == "":
            return "NA"
        if v.lower() in missing_set:
            return "NA"
        return v
    return val


def main():
    csv_file = "stock_market.csv"
    if not os.path.exists(csv_file):
        print(f"{PRINT_PREFIX} ERROR: {csv_file} not found in cwd: {os.getcwd()}")
        sys.exit(2)

    print(f"{PRINT_PREFIX} Starting Step 1: reading {csv_file}")

    # 1) Load file
    try:
        df = safe_read_csv(csv_file)
    except Exception as e:
        print(f"{PRINT_PREFIX} ERROR reading CSV: {e}")
        raise

    print(f"{PRINT_PREFIX} Raw shape: {df.shape}")
    print(f"{PRINT_PREFIX} Raw columns: {list(df.columns)}")
    print()

    print(f"{PRINT_PREFIX} --- RAW PREVIEW (top 5) ---")
    print(df.head(5).to_string(index=False))
    print()

    # 2) Normalize headers
    df.columns = to_snake_case(df.columns.astype(str))
    print(f"{PRINT_PREFIX} Normalized columns: {list(df.columns)}")
    print()

    # 3) Normalize missing-like values across all object columns
    missing_markers = {"", "na", "n/a", "n\\a", "null", "nan", "-", "none", "na "}
    missing_lower = set(x.lower() for x in missing_markers)

    obj_cols = df.select_dtypes(include="object").columns.tolist()

    for c in obj_cols:
        df[c] = df[c].apply(lambda v: normalize_cell(v, missing_lower))

    # 4) Column-specific VALUE rules exactly as you defined:

    # TICKER (keep original case, only replace missing → NA)
    if "ticker" in df.columns:
        df["ticker"] = df["ticker"].apply(
            lambda v: v if v != "NA" else "NA"
        )

    # SECTOR (keep original capitalization, only missing → NA)
    if "sector" in df.columns:
        df["sector"] = df["sector"].apply(lambda v: "NA" if v == "NA" else v)

    # VALIDATED (normalize to YES / NO / NA)
    if "validated" in df.columns:
        def fix_validated(v):
            if not isinstance(v, str):
                return "NA"
            v2 = v.strip().upper()
            if v2 in {"Y", "YES"}:
                return "YES"
            if v2 in {"N", "NO"}:
                return "NO"
            return "NA"
        df["validated"] = df["validated"].apply(fix_validated)

    # CURRENCY (ALL CAPS, missing NA)
    if "currency" in df.columns:
        df["currency"] = df["currency"].apply(
            lambda v: v.upper() if isinstance(v, str) and v != "NA" else "NA"
        )

    # EXCHANGE (ALL CAPS, missing NA)
    if "exchange" in df.columns:
        df["exchange"] = df["exchange"].apply(
            lambda v: v.upper() if isinstance(v, str) and v != "NA" else "NA"
        )

    # NOTES (keep original case, only missing NA)
    if "notes" in df.columns:
        df["notes"] = df["notes"].apply(lambda v: "NA" if v == "NA" else v)

    # 5) Fix trade_date to yyyy-mm-dd
    if "trade_date" in df.columns:
        def parse_date(v):
            if v == "NA":
                return pd.NaT
            for fmt in ("%m/%d/%Y", "%Y-%m-%d", "%Y/%m/%d"):
                try:
                    return pd.to_datetime(v, format=fmt)
                except Exception:
                    continue
            return pd.to_datetime(v, errors="coerce")

        parsed = df["trade_date"].apply(parse_date)
        df["trade_date"] = parsed.dt.strftime("%Y-%m-%d")
        df["trade_date"] = df["trade_date"].fillna("NA")
    else:
        print(">>> WARNING: no trade_date column found")

    # 6) PREVIEW AFTER NORMALIZATION
    print(f"{PRINT_PREFIX} --- POST-NORMALIZATION PREVIEW (top 8) ---")
    print(df.head(8).to_string(index=False))
    print()

    # Count NA per column
    na_counts = (df == "NA").sum()
    print(f"{PRINT_PREFIX} Counts of 'NA' per column:")
    print(na_counts)
    print()

    # 7) Save intermediate
    out_csv = "cleaned_step1.csv"
    try:
        df.to_csv(out_csv, index=False)
        print(f"{PRINT_PREFIX} Wrote intermediate file: {out_csv}")
    except Exception as e:
        print(f"{PRINT_PREFIX} ERROR writing {out_csv}: {e}")

if __name__ == "__main__":
    main()
