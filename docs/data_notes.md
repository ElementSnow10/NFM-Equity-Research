# Data Validation Notes

## 1. Data Sanity Checks

### Checks Performed
- **Negative Values**: Verified that `revenue`, `total_assets`, `equity`, `capital_employed` are non-negative.
- **Ratios**: Checked `roe`, `debt_to_equity`, `net_margin` for extreme outliers (e.g., ROE > 500% or < -100%).
- **Missing Values**: Scanned for missing data in critical columns (`ebit`, `roce`, `operating_margin`, `interest_coverage`).
- **Duplicates**: Checked for duplicate `ticker` entries.
- **Zero Values**: Ensured `revenue` and `total_assets` are non-zero.

### Observations
- **Negative Values**: PASS. No negative values found in core financial metrics for the sample set.
- **Ratios**: PASS. All ratios appear within realistic bounds for the sample companies.
  - TCS ROE is ~51%, which is high but valid for IT services.
  - ITC Debt/Equity is remarkably low (~0.004), consistent with its cash-rich status.
- **Missing Values**: FAIL (Warning).
  - **HDFCBANK**: Missing values detected for `ebit`, `roce`, `operating_margin`, and `interest_coverage`. This is expected for banking stocks where EBIT/ROCE are often not standard metrics (Banks use Net Interest Income/ROA), but represents a gap in the standardized schema.
- **Duplicates**: PASS. All tickers are unique.
- **Zero Values**: PASS. All companies have non-zero Revenue and Assets.

