import os

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')
RAW_DATA_PATH = os.path.join(DATA_DIR, 'raw')

# Market Config
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
