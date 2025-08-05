import pandas as pd
from io import BytesIO

def get_summary_statistics(df: pd.DataFrame) -> pd.DataFrame:
    return df.describe(include='all').transpose()

def convert_summary_to_csv(summary_df: pd.DataFrame) -> BytesIO:
    output = BytesIO()
    summary_df.to_csv(output)
    output.seek(0)
    return output
