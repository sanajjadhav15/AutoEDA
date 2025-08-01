# insights/outlier_detector.py

import pandas as pd
import numpy as np
from scipy import stats

def detect_outliers_iqr(df: pd.DataFrame, multiplier: float = 1.5) -> pd.DataFrame:
    """
    IQR-based outlier detection. Returns DataFrame with count and percent of outliers per numeric column.
    """
    numeric = df.select_dtypes(include='number')
    results = []
    for col in numeric.columns:
        q1 = numeric[col].quantile(0.25)
        q3 = numeric[col].quantile(0.75)
        iqr = q3 - q1
        lower = q1 - multiplier * iqr
        upper = q3 + multiplier * iqr
        outliers = numeric[(numeric[col] < lower) | (numeric[col] > upper)][col]
        count = outliers.shape[0]
        total = numeric.shape[0]
        percent = (count / total) * 100 if total > 0 else 0
        results.append({
            "Column": col,
            "Method": "IQR",
            "Outlier Count": count,
            "Outlier %": round(percent, 2)
        })
    return pd.DataFrame(results).sort_values(by="Outlier %", ascending=False)

def detect_outliers_zscore(df: pd.DataFrame, threshold: float = 3.0) -> pd.DataFrame:
    """
    Z-score based outlier detection. Returns DataFrame with count and percent of outliers per numeric column.
    """
    numeric = df.select_dtypes(include='number')
    results = []
    for col in numeric.columns:
        col_z = np.abs(stats.zscore(numeric[col].dropna()))
        if len(col_z) == 0:
            continue
        outlier_mask = col_z > threshold
        count = int(np.sum(outlier_mask))
        total = numeric[col].dropna().shape[0]
        percent = (count / total) * 100 if total > 0 else 0
        results.append({
            "Column": col,
            "Method": "Z-score",
            "Outlier Count": count,
            "Outlier %": round(percent, 2)
        })
    return pd.DataFrame(results).sort_values(by="Outlier %", ascending=False)

def aggregate_outlier_flags(df: pd.DataFrame, iqr_multiplier: float = 1.5, z_thresh: float = 3.0):
    """
    Combine both methods into a summary. Returns a dict with dataframes and a concise insight list.
    """
    iqr_df = detect_outliers_iqr(df, multiplier=iqr_multiplier)
    z_df = detect_outliers_zscore(df, threshold=z_thresh)

    # Merge summaries for the same column if needed
    summary = pd.concat([iqr_df, z_df], ignore_index=True)
    summary = summary.sort_values(by=["Outlier %"], ascending=False).reset_index(drop=True)

    # Insights: columns with >5% outliers in either method
    flags = []
    for _, row in summary.iterrows():
        if row["Outlier %"] > 5:  # threshold for insight
            flags.append(f"⚠️ Column `{row['Column']}` has {row['Outlier %']}% outliers detected by {row['Method']}.")
    return {
        "summary": summary,
        "insights": flags
    }
