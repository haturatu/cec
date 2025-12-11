import os
import pandas as pd
from typing import Optional
from app import config

def load_and_clean_data(coin_type: str, include_seed: bool) -> Optional[pd.DataFrame]:
    """Loads, cleans, and pre-processes the ETF data from a CSV file."""
    csv_file = os.path.join(config.CSV_DATA_DIR, f"etf_{coin_type}.csv")
    if not os.path.exists(csv_file):
        return None

    df = pd.read_csv(csv_file)

    # Handle "Seed" row
    if not include_seed:
        df = df[df['Date'] != 'Seed']

    # Convert Date column to datetime objects, coercing errors
    # This standardizes the date format for reliable filtering and sorting
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    df.dropna(subset=['Date'], inplace=True) # Drop rows where date conversion failed
    df = df.sort_values(by='Date', ascending=False)

    # Fill NaN values in all columns (except Date) with 0
    for col in df.columns:
        if col != 'Date':
            df[col] = df[col].fillna(0)

    return df
