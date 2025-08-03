# insights/cardinality_checker.py

import pandas as pd

def compute_cardinality(df: pd.DataFrame):
    """
    Returns DataFrame with unique count and uniqueness ratio for each column.
    """
    total = len(df)
    cardinality = []
    for col in df.columns:
        unique = df[col].nunique(dropna=False)
        ratio = unique / total if total > 0 else 0
        cardinality.append({
            "Column": col,
            "Unique Count": unique,
            "Uniqueness %": round(ratio * 100, 2)
        })
    return pd.DataFrame(cardinality).sort_values(by="Uniqueness %", ascending=False)

def flag_high_cardinality(df: pd.DataFrame, threshold: float = 0.95):
    """
    Flags columns where uniqueness (unique/total) exceeds threshold.
    """
    card_df = compute_cardinality(df)
    flagged = card_df[card_df["Uniqueness %"] > (threshold * 100)]
    return flagged.reset_index(drop=True)
