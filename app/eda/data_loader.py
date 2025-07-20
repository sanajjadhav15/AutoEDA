# eda/data_loader.py

import pandas as pd
import streamlit as st

def upload_file():
    st.markdown("""
        <div style="text-align: center; margin-top: 1rem; margin-bottom: 2rem;">
            <h2 style="color: #22c55e; font-weight: 600; font-size: 1.75rem;">📁 Upload Your Dataset</h2>
            <p style="color: #cbd5e1; font-size: 1rem;">
                Supported formats: <strong>.csv</strong> and <strong>.xlsx</strong><br>
                Upload your dataset to begin exploring insights.
            </p>
        </div>
    """, unsafe_allow_html=True)

    file = st.file_uploader(
        "Choose a file",
        type=['csv', 'xlsx'],
        label_visibility="collapsed",
        help="Supported formats: .csv and .xlsx"
    )

    if file is not None:
        try:
            if file.name.endswith('.csv'):
                df = pd.read_csv(file)
            else:
                df = pd.read_excel(file)
            st.success("✅ File uploaded and loaded successfully.")
            return df
        except Exception as e:
            st.error(f"❌ Error reading file: {e}")
            return None

    return None
