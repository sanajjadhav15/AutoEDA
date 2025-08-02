# insights/skewness_checker.py

import pandas as pd

def detect_skewness(df: pd.DataFrame, threshold: float = 1.0) -> pd.DataFrame:
    """
    Computes skewness for numeric columns and flags those with |skew| > threshold.
    Returns a DataFrame with skew values and an indicator.
    """
    numeric = df.select_dtypes(include='number')
    skew_series = numeric.skew().dropna()
    flagged = skew_series[skew_series.abs() > threshold].sort_values(ascending=False)

    result = pd.DataFrame({
        "Column": skew_series.index,
        "Skewness": skew_series.values
    })
    result["Flagged"] = result["Skewness"].abs() > threshold
    result = result.sort_values(by="Skewness", key=lambda x: x.abs(), ascending=False).reset_index(drop=True)
    return result

def generate_skewness_insights(skew_df: pd.DataFrame, threshold: float = 1.0):
    """
    Returns list of human-readable insight strings for flagged skewed columns.
    """
    insights = []
    for _, row in skew_df.iterrows():
        if row["Flagged"]:
            direction = "right" if row["Skewness"] > 0 else "left"
            insights.append(
                f"📌 Column `{row['Column']}` is {direction}-skewed (skewness={row['Skewness']:.2f}), "
                f"which may affect mean-based analyses."
            )
    return insights
