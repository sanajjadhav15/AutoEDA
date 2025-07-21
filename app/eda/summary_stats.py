# eda/summary_stats.py

import pandas as pd

def generate_summary(df: pd.DataFrame) -> pd.DataFrame:
    numeric_summary = df.describe().T
    numeric_summary["missing (%)"] = df.isnull().mean() * 100
    numeric_summary["dtype"] = df.dtypes
    return numeric_summary.round(2)
