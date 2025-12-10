from pydantic import BaseModel
from typing import List
from app.models.etf_data import ETFRecord

class ETFDataResponse(BaseModel):
    data: List[ETFRecord]
