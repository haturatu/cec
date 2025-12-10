import os
from fastapi import FastAPI

# --- Configuration ---
CSV_DATA_DIR = os.environ.get("CSV_DATA_DIR", "/csv_data")

def create_app() -> FastAPI:
    """
    Creates and configures the FastAPI application.
    """
    app = FastAPI(
        title="ETF Flow Data API",
        description="Provides access to cryptocurrency ETF flow data.",
        version="2.0.0",
    )
    return app

