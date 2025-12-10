import pandas as pd
import datetime
from fastapi import HTTPException

def parse_date_param(date_str: str, param_name: str) -> datetime.datetime:
    """
    Parses a date string in YYYY-MM-DD format into a datetime object.
    Raises HTTPException if the format is invalid.
    """
    try:
        return pd.to_datetime(date_str)
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid '{param_name}' date format. Please use YYYY-MM-DD."
        )

def format_date_to_string(date_obj: pd.Timestamp) -> str:
    """
    Formats a pandas Timestamp object to a YYYY-MM-DD string.
    """
    return date_obj.strftime('%Y-%m-%d')
