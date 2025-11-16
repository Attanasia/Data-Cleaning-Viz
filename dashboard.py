"""
STEP 4: Streamlit Dashboard
- Load aggregate parquet files
- Add filters: date range, ticker, sector
- Show charts
"""

import streamlit as st
import pandas as pd

# Load data
@st.cache_data
def load_data():
    agg1 = pd.read_parquet("agg1.parquet")  # avg close price per sector
    agg2 = pd.read_parquet("agg2.parquet")  # daily avg close price across all tickers
    agg3 = pd.read_parquet("agg3.parquet")  # avg volume by sector
    return agg1, agg2, agg3

agg1, agg2, agg3 = load_data()

# Sidebar Filters
st.sidebar.header("Filters")

# Date range filter (for agg2)
if "trade_date" in agg2.columns:
    min_date = pd.to_datetime(agg2["trade_date"].min())
    max_date = pd.to_datetime(agg2["trade_date"].max())
    start_date, end_date = st.sidebar.date_input(
        "Select Date Range", [min_date, max_date], min_value=min_date, max_value=max_date
    )
else:
    start_date, end_date = None, None

# Sector filter (for agg1 and agg3)
sectors = agg1["sector"].dropna().unique().tolist()
selected_sectors = st.sidebar.multiselect("Select Sector(s)", sectors, default=sectors)

# Filter Data
agg1_filtered = agg1[agg1["sector"].isin(selected_sectors)]
agg3_filtered = agg3[agg3["sector"].isin(selected_sectors)]

agg2_filtered = agg2.copy()
if start_date and end_date:
    agg2_filtered["trade_date"] = pd.to_datetime(agg2_filtered["trade_date"])
    agg2_filtered = agg2_filtered[
        (agg2_filtered["trade_date"] >= pd.to_datetime(start_date)) &
        (agg2_filtered["trade_date"] <= pd.to_datetime(end_date))
    ]

# Main Dashboard
st.title("Stock Market Aggregates Dashboard ")

st.header("Average Closing Price per Sector")
st.dataframe(agg1_filtered)
st.bar_chart(data=agg1_filtered.set_index("sector")["avg_close_price"])

st.header("Daily Average Close Price Across All Tickers")
st.line_chart(agg2_filtered.set_index("trade_date")["daily_avg_close"])

st.header("Average Volume per Sector")
st.dataframe(agg3_filtered)
st.bar_chart(data=agg3_filtered.set_index("sector")["avg_volume"])
