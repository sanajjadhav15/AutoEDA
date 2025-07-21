# eda/missing_values.py

import pandas as pd
import plotly.express as px

def get_missing_value_report(df: pd.DataFrame) -> pd.DataFrame:
    missing = df.isnull().sum()
    missing_percent = df.isnull().mean() * 100
    report = pd.DataFrame({
        "Missing Count": missing,
        "Missing (%)": missing_percent
    })
    report = report[report["Missing Count"] > 0]
    return report.sort_values("Missing (%)", ascending=False).round(2)

def plot_missing_bar(missing_df: pd.DataFrame):
    if missing_df.empty:
        return None
    fig = px.bar(
        missing_df,
        x=missing_df.index,
        y="Missing (%)",
        title="Missing Data by Column",
        labels={"index": "Column"},
        text="Missing (%)"
    )
    fig.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
    fig.update_layout(yaxis_range=[0, 100])
    return fig
