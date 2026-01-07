import os

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')
RAW_DATA_PATH = os.path.join(DATA_DIR, 'raw')

# Market Config
# PROCESSED DATA PATH
PROCESSED_DATA_PATH = os.path.join(DATA_DIR, 'processed', 'features.csv')
MARKET_SUFFIX = '.NS'  # NSE stocks
START_DATE = '2020-01-01'

# Metrics Schema (Required Fields for NFM Model)
REQUIRED_FIELDS = [
    # Profitability
    "net_income",
    "equity",
    "ebit",
    "capital_employed",
    "revenue",
    "gross_profit", # New
    "eps", # New
    
    # Growth (Historical)
    "revenue_3y_ago",
    "profit_3y_ago",
    
    # Leverage
    "total_debt",
    "interest_expense",
    "total_liabilities", # New for SH/Liability
    
    # Cash Flow
    "cfo",       # Operating Cash Flow
    "capex",     # Capital Expenditure
    "cfi",       # Investing Cash Flow (New)
    
    # Efficiency
    "total_assets",
    
    # Market / Valuation
    "market_cap", # New
    "price_current", # New
    "price_1y_ago", # New
    
    # Receivables (New)
    "receivables"
]

# Yahoo Finance Field Mapping
# Key: Internal Field, Value: Yahoo Finance DataFrame Index (row literal)
YAHOO_MAPPING = {
    "net_income": ["Net Income", "Net Income Common Stockholders"],
    "equity": ["Stockholders Equity", "Total Stockholder Equity"],
    "ebit": ["EBIT", "Operating Income", "EBITDA"], 
    "revenue": ["Total Revenue", "Operating Revenue"],
    "gross_profit": ["Gross Profit"],
    "eps": ["Basic EPS", "Diluted EPS"], # Usually in financials
    "total_debt": ["Total Debt"],
    "interest_expense": ["Interest Expense", "Interest Paid"],
    "total_liabilities": ["Total Liabilities Net Minority Interest", "Total Liabilities"],
    "cfo": ["Operating Cash Flow", "Total Cash From Operating Activities"],
    "capex": ["Capital Expenditure", "Total Capitalization"],
    "cfi": ["Investing Cash Flow", "Total Cashflows From Investing Activities"],
    "total_assets": ["Total Assets"],
    "current_liabilities": ["Current Liabilities", "Total Current Liabilities"],
    "receivables": ["Receivables", "Net Receivables", "Accounts Receivable"]
}

# Scoring Weights
# Based on user request. 
# Note: Sum is > 100%, but Scorer normalizes logic per metric then sums.
# We will use these as relative weights.
SCORING_WEIGHTS = {
    "pe_ratio": 5.0,
    "fcf_to_net_profit": 8.0,
    "revenue_growth_latest": 5.0,
    "revenue_growth_10y": 5.0,
    "profit_growth_10y": 5.0, # Assumed "10Y Compounded Growth"
    "roce_latest": 5.0,
    "roce_10y": 5.0,
    "roe_10y": 5.0,
    "eps_10y_avg": 5.0,
    "eps_growth": 5.0,
    "fcf_to_revenue": 5.0,
    "inv_cf_to_op_cf": 5.0,
    "gp_margin_10y": 5.0,
    "np_margin_10y": 5.0,
    "debt_to_equity": 5.0,
    "capex_to_net_earnings": 3.0,
    "price_growth_1y": 3.0,
    "peg_ratio": 3.0,
    "m_score": 3.0,
    "sh_to_liability": 3.0,
    "coc_roce_check": 3.0, # Boolean logic (1 or 0) * 3
    "mkt_retained_growth": 8.0, # Market growth and Retained earnings growth ? Assumed Mkt Cap Growth vs Retained Earnings Growth
    "net_rec_sales_comparison": 8.0, # Placeholder for competitor comparison
    "mkt_cap_retained_val": 8.0, # "Market cap — (retained earnings * annual growth)"
    "market_share": 3.0 # Placeholder
}

# Metrics where lower values are better (Rank Inversion)
# Updated based on standard interpretation unless user implied otherwise
LOWER_IS_BETTER = [
    "debt_to_equity",
    "pe_ratio",
    "peg_ratio",
    "capex_to_net_earnings", # Usually less capital intensive is better
    "m_score", # Higher M-Score = Higher probability of manipulation. Be careful with sign.
               # Beneish: M > -2.22 suggests manipulation. 
               # So Lower (more negative) is Better.
    "net_rec_sales_comparison" # High receivables relative to sales usually bad (channel stuffing)
]

