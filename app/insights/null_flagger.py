import pandas as pd

def flag_nulls(df, threshold=0.3):
    null_percent = df.isnull().mean()
    flagged = null_percent[null_percent > threshold]
    if flagged.empty:
        return pd.DataFrame()
    return pd.DataFrame({
        "Column": flagged.index,
        "Missing %": (flagged * 100).round(2)
    }).reset_index(drop=True)