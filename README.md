This project consists of cleaning stock market data, enforcing a schema, generating analytical aggregations, and building an interactive dashboard using Streamlit.

Below are the steps l took to then end up with charts using Streamlit.

Step 1:
-Initial Cleaning (data_cleaner1.py)
-Loads the raw CSV (stock_market.csv)
-Strips whitespace
-Standardizes missing values to “NA”
-Preserves capitalization rules per column (e.g., ticker = all caps)
-Ensures consistent formatting across all columns:
-The output is saved to cleaned_step1.csv

Step 2:
-Schema Enforcement (data_cleaner2.py)
-Loads cleaned_step1.csv
-Applies a target schema: Dates-> datetime, Prices -> float,Volume -> integer, Validated -> boolean (YES→True, NO→False, NA→None)
-Removes duplicate rows
-Saves the dataset as Parquet: cleaned.parquet

Step 3:
-Aggregations (data_cleaner3.py)
-This code loads the cleaned dataset(cleaned.parquet) and produces 3 aggregations: average closing price per sector -> agg1.parquet, daily average close price across all tickers -> agg2.parquet, average trading volume per sector -> agg3.parquet

Step 4: 
-Streamlit Dashboard (dashboard.py)
-This dashboard allows users to load the aggregated parquet files
-Filter by: date range, ticker
-Visualize: average prices, volume trends, sector level performance
-Run the dashboard -> streamlit run dashboard.py

The visualizer.ipynb notebook is included for: Exploratory data analysis (EDA)

The StreamLit Dashboard Screenshots.pdf has the charts from the Streamlit Dashboard.
