# Direction: whether higher or lower values are better
METRIC_DIRECTION = {
    "roe": "higher",
    "roce": "higher",
    "net_margin": "higher",
    "operating_margin": "higher",
    "revenue_cagr": "higher",
    "profit_cagr": "higher",
    "debt_to_equity": "lower",
    "interest_coverage": "higher",
    "ocf_ratio": "higher",
    "fcf": "higher",
    "fcf_margin": "higher",
    "asset_turnover": "higher",
}

# Initial weights 
WEIGHTS = {
    "roe": 0.15,
    "roce": 0.15,
    "net_margin": 0.10,
    "operating_margin": 0.10,
    "revenue_cagr": 0.15,
    "profit_cagr": 0.10,
    "debt_to_equity": 0.10,
    "interest_coverage": 0.05,
    "ocf_ratio": 0.05,
    "fcf": 0.03,
    "fcf_margin": 0.01,
    "asset_turnover": 0.01,
}
