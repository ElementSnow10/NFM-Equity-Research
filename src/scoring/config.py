"""
Scoring configuration for NFM Equity Research
"""

METRIC_DIRECTION = {
    # Profitability
    "roe": "higher",
    "roce": "higher",
    "net_profit_margin": "higher",
    "operating_margin": "higher",

    # Growth
    "revenue_cagr": "higher",
    "profit_cagr": "higher",

    # Leverage
    "debt_to_equity": "lower",
    "interest_coverage": "higher",

    # Cash Flow
    "operating_cf_ratio": "higher",
    "free_cash_flow": "higher",
    "fcf_margin": "higher",

    # Efficiency
    "asset_turnover": "higher",

    # Stability
    "earnings_volatility": "lower",
}


WEIGHTS = {
    # Profitability (40%)
    "roe": 0.12,
    "roce": 0.12,
    "net_profit_margin": 0.08,
    "operating_margin": 0.08,

    # Growth (25%)
    "revenue_cagr": 0.13,
    "profit_cagr": 0.12,

    # Leverage (10%)
    "debt_to_equity": 0.06,
    "interest_coverage": 0.04,

    # Cash Flow (15%)
    "operating_cf_ratio": 0.06,
    "free_cash_flow": 0.05,
    "fcf_margin": 0.04,

    # Efficiency (5%)
    "asset_turnover": 0.05,

    # Stability (5%)
    "earnings_volatility": 0.05,
}
