# insights/correlation_warner.py

import pandas as pd
import numpy as np

def high_correlation_pairs(df: pd.DataFrame, threshold: float = 0.85):
    """
    Finds pairs of numeric columns with absolute correlation above threshold.
    Returns a DataFrame of pairs and their correlation.
    """
    numeric = df.select_dtypes(include='number')
    corr_matrix = numeric.corr().abs()

    # Mask self-correlations and duplicate pairs using NumPy
    upper_mask = np.triu(np.ones(corr_matrix.shape), k=1).astype(bool)
    upper = corr_matrix.where(upper_mask)

    high_corr = (
        upper.stack()
        .reset_index()
        .rename(columns={'level_0': 'Column A', 'level_1': 'Column B', 0: 'Correlation'})
    )
    high_corr = high_corr[high_corr['Correlation'] > threshold].sort_values(by='Correlation', ascending=False)
    return high_corr.reset_index(drop=True)

def generate_correlation_insights(high_corr_df: pd.DataFrame):
    """
    Produces human-readable warnings for highly correlated feature pairs.
    """
    insights = []
    for _, row in high_corr_df.iterrows():
        a = row['Column A']
        b = row['Column B']
        corr = row['Correlation']
        insights.append(f"🔗 Columns `{a}` and `{b}` have high correlation ({corr:.2f}); consider dropping one or combining them.")
    return insights
