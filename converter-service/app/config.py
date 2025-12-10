import os
from dotenv import load_dotenv

load_dotenv()

DENO_API_BASE_URL = os.environ.get("DENO_API_URL", "http://deno-api:8000")
CSV_DIR = "/app/csv_output" # This should ideally be /converter-service/csv_output for host volume mapping, but keeping /app/csv_output for container internal operations. The docker-compose.yml handles the actual host mapping.

URLS = {
    "btc": os.environ.get("ETF_BTC_URL", "https://farside.co.uk/bitcoin-etf-flow-all-data/"),
    "eth": os.environ.get("ETF_ETH_URL", "https://farside.co.uk/ethereum-etf-flow-all-data/"),
    "sol": os.environ.get("ETF_SOL_URL", "https://farside.co.uk/sol/"),
}
