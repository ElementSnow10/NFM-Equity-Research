"""
Metric computation module for NFM Equity Research.

All metrics are pure functions.
They take primitive numeric inputs (scalar or list) and return floats.
Missing / invalid inputs are handled safely.

"""
import numpy as np

# ------------------------
# Helper utilities
# ------------------------

def safe_div(numerator, denominator):
    """Safely divide two numbers, returning NaN if invalid."""
    try:
        if denominator == 0 or denominator is None or pd.isna(denominator) or pd.isna(numerator):
            return np.nan
        return numerator / denominator
    except Exception:
        return np.nan

def calculate_cagr(start_val, end_val, years):
    """Calculate CAGR given start, end, and years."""
    if years <= 0 or start_val <= 0 or end_val <= 0 or pd.isna(start_val) or pd.isna(end_val):
        return np.nan
    return (end_val / start_val) ** (1 / years) - 1

def list_avg(data_list):
    """Computes average of a list, handling NaNs/empty."""
    if not data_list:
        return np.nan
    clean = [x for x in data_list if not pd.isna(x)]
    if not clean:
        return np.nan
    return sum(clean) / len(clean)

import pandas as pd # Needed for pd.isna

# ------------------------
# CORE METRICS (UPDATED)
# ------------------------

# 1. P/E Ratio
def pe_ratio(price, eps):
    return safe_div(price, eps)

# 2. FCF/NP
def fcf_to_net_profit(fcf, net_profit):
    return safe_div(fcf, net_profit)

# 3. Revenue Growth Latest Year
def revenue_growth_latest(rev_current, rev_prev):
    if pd.isna(rev_current) or pd.isna(rev_prev) or rev_prev == 0:
        return np.nan
    return (rev_current - rev_prev) / rev_prev

# 4. 10Y Revenue Growth Rate (CAGR)
def revenue_cagr_10y(hist_revenue):
    # Expects list of [Current, -1Y, -2Y, ... -NY] or yfinance often gives [Current, -1Y, -2Y, -3Y]
    # We will use max available span.
    if not hist_revenue or len(hist_revenue) < 2:
        return np.nan
    start_val = hist_revenue[-1] # Oldest
    end_val = hist_revenue[0]    # Newest
    years = len(hist_revenue) - 1
    return calculate_cagr(start_val, end_val, years)

# 5. 10Y Compounded Growth (Assumed Profit CAGR)
def profit_cagr_10y(hist_profit):
    if not hist_profit or len(hist_profit) < 2:
        return np.nan
    start_val = hist_profit[-1]
    end_val = hist_profit[0]
    years = len(hist_profit) - 1
    # Profit can be negative, standard CAGR formula fails.
    # If negative, we usually return NaN or a custom metric (absolute growth).
    # Standard methodology: NaN if start or end is negative.
    return calculate_cagr(start_val, end_val, years)

# 6. ROCE Latest 
def roce(ebit, capital_employed):
    return safe_div(ebit, capital_employed)

# 7. 10Y ROCE (Avg)
def roce_10y_avg(hist_ebit, hist_cap_employed):
    if not hist_ebit or not hist_cap_employed:
        return np.nan
    # Compute per year then avg
    roces = []
    # Zip assumed aligned (both from yfinance columns)
    for e, c in zip(hist_ebit, hist_cap_employed):
        val = safe_div(e, c)
        if not pd.isna(val):
            roces.append(val)
    return list_avg(roces)

# 8. 10Y ROE (Avg)
def roe_10y_avg(hist_net_income, hist_equity):
    if not hist_net_income or not hist_equity:
        return np.nan
    roes = []
    for n, e in zip(hist_net_income, hist_equity):
        val = safe_div(n, e)
        if not pd.isna(val):
            roes.append(val)
    return list_avg(roes)

# 9. 10Y Avg EPS
def eps_10y_avg(hist_eps):
    return list_avg(hist_eps)

# 10. EPS Growth Rate (CAGR or YoY Avg? Assumed CAGR)
def eps_growth(hist_eps):
    if not hist_eps or len(hist_eps) < 2:
        return np.nan
    start = hist_eps[-1]
    end = hist_eps[0]
    years = len(hist_eps) - 1
    return calculate_cagr(start, end, years)

# 11. FCF/Revenue
def fcf_to_revenue(fcf, revenue):
    return safe_div(fcf, revenue)

# 12. Investing CF / Operating CF
def inv_cf_to_op_cf(cfi, cfo):
    # Investing CF is usually negative (outflow).
    # Operating CF is usually positive.
    # Ratio: How much of OCF is used for Investing?
    # Expected result: If -100 CFI / 200 CFO = -0.5.
    # Usually we look at magnitude: abs(CFI) / CFO.
    # "Investing CF/Operating CF — 5%"
    # If CFI is negative (outflow), ratio is negative. 
    # Let's return raw ratio.
    return safe_div(cfi, cfo)

# 13. 10Y Avg GP Margin
def gp_margin_10y_avg(hist_gp, hist_rev):
    if not hist_gp or not hist_rev:
        return np.nan
    margins = []
    for g, r in zip(hist_gp, hist_rev):
        val = safe_div(g, r)
        if not pd.isna(val):
            margins.append(val)
    return list_avg(margins)

# 14. 10Y Avg NP Margin
def np_margin_10y_avg(hist_ni, hist_rev):
    if not hist_ni or not hist_rev:
        return np.nan
    margins = []
    for n, r in zip(hist_ni, hist_rev):
        val = safe_div(n, r)
        if not pd.isna(val):
            margins.append(val)
    return list_avg(margins)

# 15. D/E Ratio
def debt_to_equity(total_debt, equity):
    return safe_div(total_debt, equity)

# 16. CapEx/Net earnings
def capex_to_net_earnings(capex, net_income):
    return safe_div(capex, net_income)

# 17. 1Y Price Growth
def price_growth_1y(current, old):
    if pd.isna(current) or pd.isna(old) or old == 0:
        return np.nan
    return (current - old) / old

# 18. PEG
def peg_ratio(val):
    return val

# 19. M Score (Beneish)
# Simplified or Full? We have missing data issues for full.
# Placeholder calculation or based on limited available vars.
# We will return NaN currently as we lack detailed variables (Receivables index etc require 2 years of granular BS).
# Actually we have Receivables now.
# But we need COGS, Inventory, etc.
# Best effort: Return 0 (Safe) or NaN.
def m_score_proxy():
    # TODO: Implement full Beneish M-Score when granularity improves
    return np.nan

# 20. SH/Liability funds
def sh_to_liability(equity, total_liabilities):
    return safe_div(equity, total_liabilities)

# 21. COC 10 year ROCE@30% yes no
def coc_roce_check(hist_ebit, hist_cap_employed):
    # Check if ROCE > 30% for ALL years (or most?)
    # "yes no" implies boolean.
    # We'll return 1.0 (Yes) or 0.0 (No).
    if not hist_ebit or not hist_cap_employed:
        return 0.0
    
    count = 0
    valid = 0
    for e, c in zip(hist_ebit, hist_cap_employed):
        r = safe_div(e, c)
        if not pd.isna(r):
            valid += 1
            if r > 0.30:
                count += 1
    
    # Strict "Yes/No" -> All valid years > 30%?
    if valid == 0:
        return 0.0
    return 1.0 if (count == valid) else 0.0

# ------------------------
# Master function
# ------------------------

def compute_all_metrics(row):
    """
    Compute all metrics for a single company row (dict).
    """
    metrics = {}
    
    # Base Values
    p_curr = row.get("price_current", np.nan)
    p_old = row.get("price_1y_ago", np.nan)
    eps = row.get("eps", np.nan)
    ni = row.get("net_income", np.nan)
    rev = row.get("revenue", np.nan)
    fcf = (row.get("cfo", 0) - row.get("capex", 0)) # FCF = CFO - Capex (Capex assumed positive magnitude)
    cfo = row.get("cfo", np.nan)
    cfi = row.get("cfi", np.nan)
    capex = row.get("capex", np.nan)
    equity = row.get("equity", np.nan)
    debt = row.get("total_debt", np.nan)
    ebit = row.get("ebit", np.nan)
    ce = row.get("capital_employed", np.nan)
    liab = row.get("total_liabilities", np.nan)
    peg = row.get("peg_ratio", np.nan)
    
    # Histories
    h_rev = row.get("hist_revenue", [])
    h_ni = row.get("hist_net_income", [])
    h_ebit = row.get("hist_ebit", [])
    h_eq = row.get("hist_equity", [])
    h_ce = row.get("hist_cap_employed", [])
    h_eps = row.get("hist_eps", [])
    h_gp = row.get("hist_gross_profit", [])
    
    # 1. PE
    metrics["pe_ratio"] = pe_ratio(p_curr, eps)
    
    # 2. FCF/NP
    metrics["fcf_to_net_profit"] = fcf_to_net_profit(fcf, ni)
    
    # 3. Rev Growth Latest
    rev_prev = h_rev[1] if len(h_rev) > 1 else np.nan
    metrics["revenue_growth_latest"] = revenue_growth_latest(rev, rev_prev)
    
    # 4. Rev Growth 10Y
    metrics["revenue_growth_10y"] = revenue_cagr_10y(h_rev)
    
    # 5. Profit Growth 10Y
    metrics["profit_growth_10y"] = profit_cagr_10y(h_ni)
    
    # 6. ROCE Latest
    metrics["roce_latest"] = roce(ebit, ce)
    
    # 7. ROCE 10Y
    metrics["roce_10y"] = roce_10y_avg(h_ebit, h_ce)
    
    # 8. ROE 10Y
    metrics["roe_10y"] = roe_10y_avg(h_ni, h_eq)
    
    # 9. EPS 10Y Avg
    metrics["eps_10y_avg"] = eps_10y_avg(h_eps)
    
    # 10. EPS Growth
    metrics["eps_growth"] = eps_growth(h_eps)
    
    # 11. FCF/Rev
    metrics["fcf_to_revenue"] = fcf_to_revenue(fcf, rev)
    
    # 12. Inv CF/ Op CF
    metrics["inv_cf_to_op_cf"] = inv_cf_to_op_cf(cfi, cfo)
    
    # 13. GP Margin 10Y
    metrics["gp_margin_10y"] = gp_margin_10y_avg(h_gp, h_rev)
    
    # 14. NP Margin 10Y
    metrics["np_margin_10y"] = np_margin_10y_avg(h_ni, h_rev)
    
    # 15. D/E
    metrics["debt_to_equity"] = debt_to_equity(debt, equity)
    
    # 16. Capex/Net Earnings
    metrics["capex_to_net_earnings"] = capex_to_net_earnings(capex, ni)
    
    # 17. 1Y Price Growth
    metrics["price_growth_1y"] = price_growth_1y(p_curr, p_old)
    
    # 18. PEG
    metrics["peg_ratio"] = peg_ratio(peg)
    
    # 19. M Score
    metrics["m_score"] = m_score_proxy()
    
    # 20. SH/Liab
    metrics["sh_to_liability"] = sh_to_liability(equity, liab)
    
    # 21. COC Check
    metrics["coc_roce_check"] = coc_roce_check(h_ebit, h_ce)
    
    # Placeholders for undefined/impossible items
    metrics["mkt_retained_growth"] = np.nan
    metrics["net_rec_sales_comparison"] = np.nan
    metrics["mkt_cap_retained_val"] = np.nan
    metrics["market_share"] = np.nan

    return metrics
