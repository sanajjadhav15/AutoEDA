import streamlit as st
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns

def show_basic_visualizations(df):
    st.subheader("📈 Numeric Column Distributions")
    num_cols = df.select_dtypes(include='number').columns.tolist()
    for col in num_cols:
        st.markdown(f"**{col}**")

        # Histogram
        fig1 = px.histogram(df, x=col, nbins=30, title=f"Histogram of {col}")
        st.plotly_chart(fig1, use_container_width=True)

        # Boxplot
        fig2 = px.box(df, y=col, title=f"Boxplot of {col}")
        st.plotly_chart(fig2, use_container_width=True)

    st.subheader("🔠 Categorical Column Distributions")
    cat_cols = df.select_dtypes(include='object').columns.tolist()
    for col in cat_cols:
        if df[col].nunique() < 30:
            st.markdown(f"**{col}**")

            # Bar chart
            fig1 = px.bar(df[col].value_counts().reset_index(),
                          x='index', y=col,
                          labels={'index': col, col: 'Count'},
                          title=f"Bar Chart of {col}")
            st.plotly_chart(fig1, use_container_width=True)

            # Pie chart (if low cardinality)
            if df[col].nunique() <= 10:
                fig2 = px.pie(df, names=col, title=f"Pie Chart of {col}")
                st.plotly_chart(fig2, use_container_width=True)

    st.subheader("🕒 Time Series Trends")
    dt_cols = df.select_dtypes(include='datetime').columns.tolist()
    for col in dt_cols:
        df_time = df[[col]].dropna()
        df_time['count'] = 1
        df_time = df_time.groupby(col).count().reset_index()

        fig = px.line(df_time, x=col, y='count', title=f"Time Trend of {col}")
        st.plotly_chart(fig, use_container_width=True)
