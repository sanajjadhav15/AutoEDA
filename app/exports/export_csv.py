import pandas as pd
from io import BytesIO

def convert_df_to_csv(df: pd.DataFrame) -> BytesIO:
    output = BytesIO()
    df.to_csv(output, index=False)
    output.seek(0)
    return output
