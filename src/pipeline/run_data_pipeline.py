
import pandas as pd
import os
import sys

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from config import settings
from src.data_ingestion import fetcher, processor
from src.metrics import compute_metrics

# Sample Tickers for Phase 1 MVP
SAMPLE_TICKERS = ["RELIANCE", "TCS", "HDFCBANK", "INFY", "ITC"]

def run():
    print("Starting Data Pipeline...")
    all_data = []
    
    for ticker in SAMPLE_TICKERS:
        print(f"Processing {ticker}...")
        
        # 1. Fetch
        raw_data = fetcher.fetch_financials(ticker)
        if not raw_data:
            print(f"Skipping {ticker} (Fetch failed)")
            continue
            
        # 2. Process / Normalize
        processed_data = processor.process_ticker_data(ticker, raw_data)
        if not processed_data:
            print(f"Skipping {ticker} (Processing failed)")
            continue
            
        # 3. Compute Metrics
        # compute_all_metrics expects a dict/row.
        try:
            metrics = compute_metrics.compute_all_metrics(processed_data)
        except Exception as e:
            print(f"Error computing metrics for {ticker}: {e}")
            metrics = {}
            
        # Merge processed raw data + metrics
        # (Optional: do we want to keep raw numbers? Yes, usually good for debugging)
        combined_row = {**processed_data, **metrics}
        all_data.append(combined_row)
        
    if not all_data:
        print("No data collected.")
        return
        
    # 4. Save
    df = pd.DataFrame(all_data)
    
    # Reorder columns: ticker first, then metrics, then raw
    cols = ['ticker'] + [c for c in df.columns if c != 'ticker']
    df = df[cols]
    
    output_path = settings.PROCESSED_DATA_PATH
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"Pipeline completed. Data saved to {output_path}")
    print(f"Total companies processed: {len(df)}")
    print(df.head())

if __name__ == "__main__":
    run()
