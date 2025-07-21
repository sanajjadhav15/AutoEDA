import pandas as pd
import numpy as np

def preprocess_data(df):
    df = df.copy()

    # Handle missing values
    for col in df.columns:
        if df[col].dtype in ["float64", "int64"]:
            df[col].fillna(df[col].median(), inplace=True)
        elif df[col].dtype == "object":
            df[col].fillna("Unknown", inplace=True)

    # Identify low-cardinality categoricals (less than 30 unique values)
    cat_cols = df.select_dtypes(include="object").columns
    low_cardinality = [col for col in cat_cols if df[col].nunique() < 30]

    # Encode low-cardinality categorical columns only
    for col in low_cardinality:
        df[col] = df[col].astype("category").cat.codes

    # Optional: Standardize numeric features
    # from sklearn.preprocessing import StandardScaler
    # scaler = StandardScaler()
    # num_cols = df.select_dtypes(include=["float64", "int64"]).columns
    # df[num_cols] = scaler.fit_transform(df[num_cols])

    return df
