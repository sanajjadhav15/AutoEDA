# layout.py

import streamlit as st
from ui.styles import get_custom_css, feature_card, get_floating_shapes

def render_landing_page():
    # Inject custom CSS and background visuals
    st.markdown(get_custom_css(), unsafe_allow_html=True)
    st.markdown(get_floating_shapes(), unsafe_allow_html=True)

    # Hero Title and Subtitle in a centered container
    st.markdown("""
        <div class="hero-container">
            <h1 class="hero-title" style="color: #22c55e;">AutoEDA</h1>
            <p class="hero-subtitle">
                Transform raw datasets into <strong>stunning insights</strong> with our intelligent exploratory data analysis platform.<br>
                Upload, analyze, and export <strong>professional reports</strong> in just minutes.
            </p>
        </div>
    """, unsafe_allow_html=True)

    # Feature Cards
    features = [
        ("📁", "Smart Data Upload", "Seamlessly import CSV and Excel files with intelligent format detection and instant preview."),
        ("📊", "Dynamic Visualizations", "Auto-generate beautiful, interactive charts based on your data types."),
        ("🧠", "AI-Powered Insights", "Uncover patterns, anomalies, and trends with smart ML-powered analysis."),
        ("📋", "Interactive Metadata", "Get detailed column-wise summaries, missing values, and data types."),
        ("📤", "Professional Reports", "Export polished PDF or HTML reports with full visual summaries."),
        ("⚠️", "Data Quality Warnings", "Get automatic alerts for duplicates, nulls, outliers, and more.")
    ]

    cards = "".join([
        feature_card(icon, title, desc).strip() for icon, title, desc in features
    ])

    full_grid_html = f"""<div class="features-grid">{cards}</div>"""
    st.markdown(full_grid_html, unsafe_allow_html=True)
