# insights/insight_panel.py

from insights.outlier_detector import aggregate_outlier_flags
from insights.skewness_checker import detect_skewness, generate_skewness_insights
from insights.cardinality_checker import flag_high_cardinality
from insights.correlation_warner import high_correlation_pairs, generate_correlation_insights

def generate_all_insights(df):
    """
    Runs all smart insight checks and returns a dictionary with
    lists of bullet-point insights grouped by category.
    """
    all_insights = {}

    # 1️⃣ Outlier detection
    outlier_info = aggregate_outlier_flags(df)
    all_insights["Outliers"] = outlier_info["insights"]

    # 2️⃣ Skewness detection
    skew_df = detect_skewness(df, threshold=1.0)
    all_insights["Skewness"] = generate_skewness_insights(skew_df)

    # 3️⃣ Cardinality check
    high_card = flag_high_cardinality(df, threshold=0.95)
    card_insights = []
    for _, row in high_card.iterrows():
        card_insights.append(
            f"⚠️ Column `{row['Column']}` has {row['Uniqueness %']}% unique values — may behave like an identifier."
        )
    all_insights["Cardinality"] = card_insights

    # 4️⃣ High correlation
    high_corr_df = high_correlation_pairs(df, threshold=0.85)
    all_insights["Correlation"] = generate_correlation_insights(high_corr_df)

    return all_insights
