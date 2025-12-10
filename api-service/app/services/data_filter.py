import pandas as pd
from typing import List, Dict, Any
from app.models.etf_data import ETFRecord
from app.utils.date_utils import format_date_to_string

def format_response(df: pd.DataFrame) -> List[ETFRecord]:
    """Formats the DataFrame into a list of ETFRecord objects."""
    output = []
    
    non_flow_columns = {'Date', 'Total'}
    
    for _, row in df.iterrows():
        flows = {
            col: row[col]
            for col in df.columns if col not in non_flow_columns
        }
        
        record = ETFRecord(
            date=format_date_to_string(row['Date']),
            total=row.get('Total', 0),
            flows=flows,
        )
        output.append(record)
        
    return output
