
import pandas as pd
import os
import sys
from tqdm import tqdm
import nselib
from nselib import capital_market

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from config import settings
from src.data_ingestion import fetcher, processor
from src.metrics import compute_metrics

def get_all_nse_tickers():
    """
    Fetches the list of all equity tickers from NSE using nselib.
    Returns a list of ticker symbols.
    """
    try:
        print("Fetching equity list from NSE...")
        # equity_list returns a DataFrame with 'SYMBOL' column
        df = capital_market.equity_list()
        tickers = df['SYMBOL'].tolist()
        # Filter out ETFs or weird symbols if needed, but usually SYMBOL is clean
        return tickers
    except Exception as e:
        print(f"Error fetching NSE ticker list: {e}")
        return []

def run():
    print("Starting Data Pipeline for Full Universe...")
    
    # 1. Get Tickers
    all_tickers = get_all_nse_tickers()
    if not all_tickers:
        print("No tickers found. Exiting.")
        return
        
    print(f"Total tickers found: {len(all_tickers)}")
    
    # 2. Resumability Logic
    output_path = settings.PROCESSED_DATA_PATH
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    processed_tickers = set()
    if os.path.exists(output_path):
        try:
            existing_df = pd.read_csv(output_path)
            processed_tickers = set(existing_df['ticker'].tolist())
            print(f"Resuming... {len(processed_tickers)} tickers already processed.")
        except Exception:
            print("Could not read existing file. Starting from scratch.")
            
    # Remove processed from todo
    tickers_to_process = [t for t in all_tickers if t not in processed_tickers]
    print(f"Tickers remaining to process: {len(tickers_to_process)}")
    
    if not tickers_to_process:
        print("All tickers processed!")
        return

    # 3. Processing Loop
    batch_data = []
    BATCH_SIZE = 10 # Save every 10 tickers
    
    # Use tqdm for progress bar
    progress_bar = tqdm(tickers_to_process, desc="Processing Stocks", unit="ticker")
    
    for ticker in progress_bar:
        # Update progress bar description
        progress_bar.set_description(f"Processing {ticker}")
        
        # A. Fetch
        # Note: fetcher.fetch_financials handles exceptions and returns None on failure
        raw_data = fetcher.fetch_financials(ticker)
        
        if not raw_data:
            # Even if fetch failed, we might want to record it as "processed" to avoid infinite retries?
            # ideally yes, maybe add to a 'failed.csv' or just ignore. 
            # For now, let's NOT add to processed_tickers so it retries next time? 
            # Or if it's a permanent error (delisted), we are stuck.
            # safe option: just log and continue.
            continue
            
        # B. Process
        processed_data = processor.process_ticker_data(ticker, raw_data)
        if not processed_data:
            continue
            
        # C. Compute Metrics
        try:
            metrics = compute_metrics.compute_all_metrics(processed_data)
        except Exception:
            metrics = {}
            
        combined_row = {**processed_data, **metrics}
        batch_data.append(combined_row)
        
        # D. Batch Save
        if len(batch_data) >= BATCH_SIZE:
            save_batch(batch_data, output_path)
            batch_data = [] # Clear buffer

    # Save remaining
    if batch_data:
        save_batch(batch_data, output_path)
        
    print("Pipeline completed.")

def save_batch(new_data, path):
    """
    Appends a batch of data to the CSV file.
    Reads existing headers if file exists to ensure column order.
    """
    if not new_data:
        return
        
    df_batch = pd.DataFrame(new_data)
    
    # Standardize columns order based on existing file or settings
    # If file exists, align columns
    if os.path.exists(path):
        # We append mode='a', no header
        # Need to ensure columns match the existing file's order
        existing_header = pd.read_csv(path, nrows=0).columns.tolist()
        
        # Add missing cols to batch with NaN
        for col in existing_header:
            if col not in df_batch.columns:
                df_batch[col] = pd.NA
                
        # Reorder batch to match existing
        df_batch = df_batch[existing_header]
        
        df_batch.to_csv(path, mode='a', header=False, index=False)
    else:
        # New file
        # Put ticker first
        cols = ['ticker'] + [c for c in df_batch.columns if c != 'ticker']
        df_batch = df_batch[cols]
        df_batch.to_csv(path, mode='w', header=True, index=False)

if __name__ == "__main__":
    run()
