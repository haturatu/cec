from pydantic import BaseModel
from typing import Dict, Any

class ETFFlows(BaseModel):
    # This model will dynamically hold the flow data for each institution
    # It's a placeholder to indicate that 'flows' is a dictionary.
    # Actual keys (e.g., 'BlackRock', 'Fidelity') will vary.
    class Config:
        extra = "allow" # Allow extra fields for dynamic flow keys

class ETFRecord(BaseModel):
    date: str
    total: float
    flows: Dict[str, float] # Changed to Dict[str, float] for explicit type
