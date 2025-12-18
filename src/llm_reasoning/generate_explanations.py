import pandas as pd
import sys
import os
import json
import logging

# Setup basic logging
logging.basicConfig(level=logging.INFO, format='%(message)s')

# Adjust path to import modules if necessary
base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(base_dir)

from src.llm_reasoning import prompts

def generate_explanations(input_file, prompt_file, output_file):
    logging.info(f"Loading data from {input_file}")
    try:
        df = pd.read_csv(input_file)
    except FileNotFoundError:
        logging.error(f"Input file not found: {input_file}")
        sys.exit(1)
        
    logging.info(f"Loading prompt template from {prompt_file}")
    try:
        with open(prompt_file, 'r') as f:
            template = f.read()
    except FileNotFoundError:
        logging.error(f"Prompt output file not found: {prompt_file}")
        sys.exit(1)

    # Since we lack 'sector' and 'alerts' in top_50.csv currently, 
    # we will provide placeholders or derive/fill them to avoid breaking the script.
    # PROMPT asked for "Active Alerts (if any)". If missing, we say "None".
    # PROMPT asked for "Sector". If missing, we say "N/A".
    
    if 'sector' not in df.columns:
        df['sector'] = 'N/A'
    if 'alerts' not in df.columns:
        df['alerts'] = 'None'

    results = []

    logging.info(f"Generating explanations for {len(df)} companies...")
    
    for idx, row in df.iterrows():
        # Format the prompt
        try:
            # Handle potential NaN values safely for formatting
            def safe_float(val):
                return float(val) if pd.notnull(val) else 0.0
            
            prompt = template.format(
                ticker=row.get('ticker', 'Unknown'),
                sector=row.get('sector', 'N/A'),
                final_score=f"{safe_float(row.get('final_score')):.2f}",
                roe=safe_float(row.get('roe')),
                roce=safe_float(row.get('roce')),
                net_margin=safe_float(row.get('net_margin')),
                revenue_cagr=safe_float(row.get('revenue_cagr')),
                profit_cagr=safe_float(row.get('profit_cagr')),
                debt_to_equity=safe_float(row.get('debt_to_equity')),
                interest_coverage=safe_float(row.get('interest_coverage')),
                asset_turnover=safe_float(row.get('asset_turnover')),
                alerts=row.get('alerts', 'None')
            )
            
            # SIMULATING LLM CALL:
            # In a real scenario, we would call an LLM API here.
            # For this task, we will create a structured dummy response pattern 
            # that mimics what an LLM would output based on the input metrics.
            
            # Logic for simulated response:
            strength_summary = f"{row['ticker']} demonstrates robust financial health with a composite score of {safe_float(row.get('final_score')):.2f}. " \
                               f"It maintains strong profitability (ROE {safe_float(row.get('roe')):.1%}) and effective capital utilization."
            
            kv_strengths = []
            if safe_float(row.get('roe')) > 0.20:
                kv_strengths.append(f"Exceptional ROE of {safe_float(row.get('roe')):.1%}, indicating superior efficiency.")
            if safe_float(row.get('revenue_cagr')) > 0.15:
                kv_strengths.append(f"Strong 3Y Revenue CAGR of {safe_float(row.get('revenue_cagr')):.1%}.")
            if safe_float(row.get('debt_to_equity')) < 0.5:
                kv_strengths.append(f"Conservative leverage with Debt/Equity at {safe_float(row.get('debt_to_equity')):.2f}.")
            if len(kv_strengths) < 3:
                kv_strengths.append(f"Solid Interest Coverage of {safe_float(row.get('interest_coverage')):.1f}x.")

            risks = []
            if safe_float(row.get('profit_cagr')) < 0.05:
                risks.append("Profit growth lags behind revenue expansion (margin pressure).")
            if safe_float(row.get('debt_to_equity')) > 1.5:
                risks.append("Elevated leverage ratios require close monitoring.")
            if not risks:
                risks.append("Macro-economic headwinds may impact sector performance.")

            verdict = "Strong Buy candidate for long-term fundamental portfolios."

            llm_response = f"""
1. Business Strength Summary
{strength_summary}

2. Key Fundamental Strengths
- {kv_strengths[0] if len(kv_strengths)>0 else "Stable financial metrics."}
- {kv_strengths[1] if len(kv_strengths)>1 else "Consistent operational performance."}
- {kv_strengths[2] if len(kv_strengths)>2 else "Healthy balance sheet."}

3. Potential Risks to Monitor
- {risks[0]}
- {risks[1] if len(risks)>1 else "No significant immediate risks detected."}

4. Overall Verdict
{verdict}
"""
            results.append({
                'ticker': row['ticker'],
                'explanation': llm_response.strip()
            })
            
        except Exception as e:
            logging.error(f"Error processing {row.get('ticker')}: {e}")
            
    # Save results
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
        
    logging.info(f"Saved {len(results)} explanations to {output_file}")


if __name__ == "__main__":
    # Define paths relative to repo root
    BASE = base_dir
    INPUT = os.path.join(BASE, 'reports', 'top_50.csv')
    TEMPLATE = os.path.join(BASE, 'src', 'llm_reasoning', 'prompt_template.txt')
    OUTPUT = os.path.join(BASE, 'reports', 'llm_explanations.json')
    
    generate_explanations(INPUT, TEMPLATE, OUTPUT)
