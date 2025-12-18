import numpy as np
import pandas as pd
from .config import METRIC_DIRECTION, WEIGHTS


def min_max_normalize(series, direction):
    """
    Normalize a pandas Series to [0, 1].
    Handles missing values and constant columns safely.
    """
    s = series.astype(float)

    min_v = s.min(skipna=True)
    max_v = s.max(skipna=True)

    # Edge case: all values same or missing
    if pd.isna(min_v) or pd.isna(max_v) or min_v == max_v:
        return pd.Series(0.5, index=s.index)

    if direction == "higher":
        return (s - min_v) / (max_v - min_v)
    else:
        return (max_v - s) / (max_v - min_v)


def compute_nfm_score(df):
    """
    Compute final NFM score for each company.
    Returns a pandas Series.
    """
    score = pd.Series(0.0, index=df.index)

    for metric, weight in WEIGHTS.items():
        if metric not in df.columns:
            raise ValueError(f"Missing required metric: {metric}")

        norm_metric = min_max_normalize(
            df[metric], METRIC_DIRECTION[metric]
        )

        score += weight * norm_metric

    return score


def rank_companies(df):
    """
    Add NFM score and rank to the dataframe.
    """
    df = df.copy()

    df["nfm_score"] = compute_nfm_score(df)

    df["rank"] = df["nfm_score"].rank(
        ascending=False,
        method="dense"
    )

    return df.sort_values("rank")
