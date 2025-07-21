# eda/basic_viz.py

import streamlit as st
import plotly.express as px
import pandas as pd
from ui import styles

def show_basic_visualizations(df: pd.DataFrame):
    num_cols = df.select_dtypes(include='number').columns.tolist()
    cat_cols = df.select_dtypes(include='object').columns.tolist()
    dt_cols = df.select_dtypes(include='datetime').columns.tolist()

    # -------------------
    # 📈 Numeric Columns
    # -------------------
    if num_cols:
        # st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown(f"### 📈 Numeric Column Distributions ({len(num_cols)})")

        for col in num_cols:
            with st.expander(f"🔢 {col}"):
                col1, col2 = st.columns(2)
                with col1:
                    fig1 = px.histogram(df, x=col, nbins=30, title=f"Histogram of {col}")
                    st.plotly_chart(fig1, use_container_width=True)
                with col2:
                    fig2 = px.box(df, y=col, title=f"Boxplot of {col}")
                    st.plotly_chart(fig2, use_container_width=True)
        # st.markdown('</div>', unsafe_allow_html=True)

    # -------------------
    # 🔠 Categorical Columns
    # -------------------
    if cat_cols:
        # st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown(f"### 🔠 Categorical Column Distributions ({len(cat_cols)})")

        for col in cat_cols:
            if df[col].nunique() < 30:
                with st.expander(f"🏷️ {col}"):
                    fig1 = px.bar(df[col].value_counts().reset_index(),
                                  x='index', y=col,
                                  labels={'index': col, col: 'Count'},
                                  title=f"Bar Chart of {col}")
                    st.plotly_chart(fig1, use_container_width=True)

                    if df[col].nunique() <= 10:
                        fig2 = px.pie(df, names=col, title=f"Pie Chart of {col}")
                        st.plotly_chart(fig2, use_container_width=True)
        # st.markdown('</div>', unsafe_allow_html=True)

    # -------------------
    # 🕒 Datetime Columns
    # -------------------
    if dt_cols:
        # st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown(f"### 🕒 Time Series Trends ({len(dt_cols)})")

        for col in dt_cols:
            with st.expander(f"📅 {col}"):
                df_time = df[[col]].dropna()
                df_time['count'] = 1
                df_time = df_time.groupby(col).count().reset_index()

                fig = px.line(df_time, x=col, y='count', title=f"Time Trend of {col}")
                st.plotly_chart(fig, use_container_width=True)
        # st.markdown('</div>', unsafe_allow_html=True)

    # -------------------
    # Empty state
    # -------------------
    if not num_cols and not cat_cols and not dt_cols:
        st.info("No visualizable columns found in the cleaned dataset.")
