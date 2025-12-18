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
    
    # Growth (Historical)
    "revenue_3y_ago",
    "profit_3y_ago",
    
    # Leverage
    "total_debt",
    "interest_expense",
    
    # Cash Flow
    "cfo",       # Operating Cash Flow
    "capex",     # Capital Expenditure
    
    # Efficiency
    "total_assets"
]

# Yahoo Finance Field Mapping
# Key: Internal Field, Value: Yahoo Finance DataFrame Index (row literal)
YAHOO_MAPPING = {
    "net_income": ["Net Income", "Net Income Common Stockholders"],
    "equity": ["Stockholders Equity", "Total Stockholder Equity"],
    "ebit": ["EBIT", "Operating Income", "EBITDA"], # Fallback chain
    "revenue": ["Total Revenue", "Operating Revenue"],
    "total_debt": ["Total Debt"],
    "interest_expense": ["Interest Expense", "Interest Paid"],
    "cfo": ["Operating Cash Flow", "Total Cash From Operating Activities"],
    "capex": ["Capital Expenditure", "Total Capitalization"],
    "total_assets": ["Total Assets"],
    "current_liabilities": ["Current Liabilities", "Total Current Liabilities"] # For Capital Employed calc
}

# Scoring Weights
# Positive weights = higher is better.
# For metrics where lower is better (Debt/Equity), Scorer will handle inversion before applying weight.
SCORING_WEIGHTS = {
    # Profitability (Weight: 3.5 total)
    "roe": 2.0,
    "roce": 1.5,
    "operating_margin": 1.0,
    
    # Growth (Weight: 3.0 total)
    "revenue_cagr": 1.5,
    "profit_cagr": 2.0,
    
    # Efficiency (Weight: 0.5)
    "asset_turnover": 0.5,
    
    # Leverage (Weight: 1.5 total)
    # Note: These ranks will be inverted by the scorer
    "debt_to_equity": 1.5,
    
    # Cash Flow (Weight: 1.5 total)
    "fcf_margin": 1.5
}

