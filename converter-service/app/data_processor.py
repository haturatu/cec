import os
import sys
from app import config
from app import fetcher_client
from app.html_converter import html_to_dataframe
from app import file_manager

def process_etfs(dry_run: bool = False) -> bool:
    """
    Fetches HTML and converts it to CSV for each coin type.
    Returns True if all conversions were successful, False otherwise.
    If dry_run is True, no CSV files are actually written.
    """
    print(f"=== Starting ETF CSV Generation Cycle (dry_run={dry_run}) ===")
    file_manager.ensure_csv_directory_exists(config.CSV_DIR)
    all_successful = True

    urls_to_process = config.URLS if not dry_run else {k: v for k, v in config.URLS.items() if v}

    if dry_run and not urls_to_process:
        print("No URLs configured for dry-run. Considering this a failure.")
        return False

    for coin_type, url in urls_to_process.items():
        if not url:
            print(f"Skipping {coin_type.upper()} as its URL is not configured.")
            all_successful = False
            continue
        print(f"--- Processing {coin_type.upper()} ---")
        html_content = fetcher_client.fetch_html_from_deno_api(url)
        if html_content:
            output_filename = os.path.join(config.CSV_DIR, f"etf_{coin_type}.csv")
            try:
                df = html_to_dataframe(html_content, coin_type)
                if df is not None:
                    if not dry_run:
                        file_manager.save_dataframe_to_csv(df, output_filename)
                else:
                    all_successful = False
            except Exception as e:
                print(f"Error converting {coin_type.upper()} HTML to CSV: {e}")
                all_successful = False
        else:
            print(f"Skipping {coin_type.upper()} due to failed HTML fetch.")
            all_successful = False
    print("=== Cycle Completed ===")
    return all_successful