import pandas as pd

def detect_column_types(df: pd.DataFrame):
    numerical_cols = []
    categorical_cols = []
    datetime_cols = []
    other_cols = []

    for col in df.columns:
        if pd.api.types.is_numeric_dtype(df[col]):
            numerical_cols.append(col)
        elif pd.api.types.is_datetime64_any_dtype(df[col]):
            datetime_cols.append(col)
        elif pd.api.types.is_categorical_dtype(df[col]) or df[col].nunique() < 20:
            categorical_cols.append(col)
        else:
            other_cols.append(col)

    return {
        "numerical": numerical_cols,
        "categorical": categorical_cols,
        "datetime": datetime_cols,
        "others": other_cols
    }
