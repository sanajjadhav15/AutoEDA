# eda/basic_viz.py

import streamlit as st
import plotly.express as px
import pandas as pd
from ui import styles
import matplotlib.pyplot as plt
import seaborn as sns

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


def generate_plots_for_export(df: pd.DataFrame):
    """
    Generate plots for export (PDF/Dashboard) instead of displaying them in Streamlit.
    Returns a dictionary of plot objects.
    """
    plots = {}
    num_cols = df.select_dtypes(include='number').columns.tolist()
    cat_cols = df.select_dtypes(include='object').columns.tolist()
    dt_cols = df.select_dtypes(include='datetime').columns.tolist()

    # -------------------
    # 📈 Numeric Columns
    # -------------------
    if num_cols:
        # Generate histograms and box plots for first few numeric columns (limit to avoid too many plots)
        for i, col in enumerate(num_cols[:3]):  # Limit to first 3 numeric columns
            # Histogram
            plots[f"Histogram - {col}"] = px.histogram(
                df, x=col, nbins=30, 
                title=f"Distribution of {col}"
            )
            
            # Box plot
            plots[f"Box Plot - {col}"] = px.box(
                df, y=col, 
                title=f"Box Plot of {col}"
            )

    # -------------------
    # 🔠 Categorical Columns
    # -------------------
    if cat_cols:
        # Generate bar charts for first few categorical columns
        for i, col in enumerate(cat_cols[:2]):  # Limit to first 2 categorical columns
            if df[col].nunique() < 30:  # Only if manageable number of categories
                value_counts = df[col].value_counts().reset_index()
                plots[f"Bar Chart - {col}"] = px.bar(
                    value_counts,
                    x='index', y=col,
                    labels={'index': col, col: 'Count'},
                    title=f"Distribution of {col}"
                )
                
                # Pie chart if <= 10 categories
                if df[col].nunique() <= 10:
                    plots[f"Pie Chart - {col}"] = px.pie(
                        df, names=col, 
                        title=f"Pie Chart of {col}"
                    )

    # -------------------
    # 🕒 Datetime Columns
    # -------------------
    if dt_cols:
        for i, col in enumerate(dt_cols[:2]):  # Limit to first 2 datetime columns
            df_time = df[[col]].dropna()
            df_time['count'] = 1
            df_time = df_time.groupby(col).count().reset_index()
            
            plots[f"Time Trend - {col}"] = px.line(
                df_time, x=col, y='count', 
                title=f"Time Trend of {col}"
            )

    return plots


def generate_matplotlib_plots_for_export(df: pd.DataFrame):
    """
    Generate matplotlib plots as fallback for export when Plotly fails.
    Returns a dictionary of matplotlib figure objects.
    """
    plots = {}
    num_cols = df.select_dtypes(include='number').columns.tolist()
    cat_cols = df.select_dtypes(include='object').columns.tolist()
    
    # Set style for better looking plots
    plt.style.use('default')
    sns.set_palette("husl")
    
    # -------------------
    # 📈 Numeric Columns
    # -------------------
    if num_cols:
        for i, col in enumerate(num_cols[:3]):  # Limit to first 3 numeric columns
            # Histogram
            fig, ax = plt.subplots(figsize=(8, 5))
            ax.hist(df[col].dropna(), bins=30, alpha=0.7, edgecolor='black')
            ax.set_title(f"Distribution of {col}")
            ax.set_xlabel(col)
            ax.set_ylabel("Frequency")
            plt.tight_layout()
            plots[f"Histogram - {col}"] = fig
            
            # Box plot
            fig, ax = plt.subplots(figsize=(8, 5))
            ax.boxplot(df[col].dropna())
            ax.set_title(f"Box Plot of {col}")
            ax.set_ylabel(col)
            plt.tight_layout()
            plots[f"Box Plot - {col}"] = fig

    # -------------------
    # 🔠 Categorical Columns
    # -------------------
    if cat_cols:
        for i, col in enumerate(cat_cols[:2]):  # Limit to first 2 categorical columns
            if df[col].nunique() < 30:  # Only if manageable number of categories
                value_counts = df[col].value_counts()
                
                # Bar chart
                fig, ax = plt.subplots(figsize=(10, 6))
                value_counts.plot(kind='bar', ax=ax)
                ax.set_title(f"Distribution of {col}")
                ax.set_xlabel(col)
                ax.set_ylabel("Count")
                plt.xticks(rotation=45)
                plt.tight_layout()
                plots[f"Bar Chart - {col}"] = fig
                
                # Pie chart if <= 10 categories
                if df[col].nunique() <= 10:
                    fig, ax = plt.subplots(figsize=(8, 8))
                    value_counts.plot(kind='pie', ax=ax, autopct='%1.1f%%')
                    ax.set_title(f"Pie Chart of {col}")
                    ax.set_ylabel('')  # Remove ylabel for pie charts
                    plt.tight_layout()
                    plots[f"Pie Chart - {col}"] = fig

    return plots
