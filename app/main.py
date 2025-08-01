# main.py

import streamlit as st
from ui.layout import render_landing_page
from eda.data_loader import upload_file
from ui import styles
from eda.type_inference import detect_column_types
from eda.summary_stats import generate_summary
from eda.missing_values import get_missing_value_report, plot_missing_bar
from eda.preprocess import preprocess_data

st.set_page_config(page_title="AutoEDA", layout="wide")

# --------------------------
# Inject global CSS
# --------------------------
st.markdown(styles.get_custom_css(), unsafe_allow_html=True)

# --------------------------
# Track current page
# --------------------------
if "page" not in st.session_state:
    st.session_state.page = "Home"

# --------------------------
# Navigation (Styled Buttons)
# -------------------------- 
# Navigation section using real Streamlit buttons
st.markdown("<div style='text-align: center; margin-top: 1rem;'>", unsafe_allow_html=True)
nav_col1, nav_col2, nav_col3, nav_col4, nav_col5 = st.columns([1, 1, 1, 1, 1])
with nav_col1:
    if st.button("🏠 Home", use_container_width=True, key="home_button"):
        st.session_state.page = "Home"
with nav_col2:
    if st.button("📁 Upload Dataset", use_container_width=True, key="upload_button"):
        st.session_state.page = "Upload"
with nav_col3:
    if st.button("🧼 Preprocess Data", use_container_width=True, key="preprocess_button"):
        st.session_state.page = "Preprocess"
with nav_col4:
    if st.button("📊 Visualizations", use_container_width=True, key="visualizations_button"):
        st.session_state.page = "Visualizations"
with nav_col5:
    if st.button("🧠 Smart Insights", use_container_width=True, key="insights_button"):
        st.session_state.page = "Smart Insights"
st.markdown("</div><hr>", unsafe_allow_html=True)

# --------------------------
# Render Pages
# --------------------------
if st.session_state.page == "Home":
    render_landing_page()

elif st.session_state.page == "Upload":
    df = upload_file()

    if df is not None:
        st.session_state.df_raw = df
        st.markdown(styles.section_block("👀 Data Preview"), unsafe_allow_html=True)
        st.dataframe(df.head(), use_container_width=True)

        st.markdown(styles.section_block("📏 Dataset Dimensions"), unsafe_allow_html=True)
        st.write(f"Rows: {df.shape[0]} &nbsp;&nbsp;|&nbsp;&nbsp; Columns: {df.shape[1]}", unsafe_allow_html=True)

        st.markdown(styles.section_block("🧮 Column Data Types"), unsafe_allow_html=True)
        st.dataframe(df.dtypes.reset_index().rename(columns={"index": "Column", 0: "Data Type"}), use_container_width=True)
        col_types = detect_column_types(df)
        st.markdown(styles.section_block("🔍 Auto Column Type Detection"), unsafe_allow_html=True)
        # st.markdown('<div class="type-section">', unsafe_allow_html=True)

        type_labels = {
            "numerical": "🔢 Numerical Columns",
            "categorical": "🏷️ Categorical Columns",
            "datetime": "🗓️ Datetime Columns",
            "others": "📦 Other/Unclassified Columns"
        }

        for key, label in type_labels.items():
            cols = col_types.get(key, [])
            with st.expander(f"{label} ({len(cols)})", expanded=True if cols else False):
                if cols:
                    st.markdown("".join([f"<span class='type-badge'>{col}</span>" for col in cols]), unsafe_allow_html=True)
                else:
                    st.markdown("`No columns detected.`")

        # st.markdown('</div>', unsafe_allow_html=True)

        # --------------------------
        # Summary Statistics
        # --------------------------
        st.markdown(styles.section_block("📊 Summary Statistics"), unsafe_allow_html=True)
        summary_df = generate_summary(df)
        st.dataframe(summary_df, use_container_width=True)

        # --------------------------
        # Missing Value Report
        # --------------------------
        st.markdown(styles.section_block("❗ Missing Values"), unsafe_allow_html=True)
        null_df = get_missing_value_report(df)

        if null_df.empty:
            st.success("No missing values detected! 🎉")
        else:
            st.dataframe(null_df, use_container_width=True)
            fig = plot_missing_bar(null_df)
            if fig:
                st.plotly_chart(fig, use_container_width=True)


elif st.session_state.page == "Preprocess":
    if "df_raw" not in st.session_state:
        st.warning("⚠️ Please upload a dataset first!")
    else:
        from eda.preprocess import preprocess_data  # ✅ updated function name

        st.markdown(styles.section_block("🧼 Data Preprocessing"), unsafe_allow_html=True)
        st.write("Click the button below to clean and standardize your dataset.")

        if st.button("✨ Run Preprocessing", use_container_width=True):
            df_cleaned = preprocess_data(st.session_state.df_raw)
            st.session_state.df_cleaned = df_cleaned
            st.success("✅ Dataset cleaned and stored as `df_cleaned` in memory.")

        if "df_cleaned" in st.session_state:
            st.markdown("### 🔍 Cleaned Data Preview")
            st.dataframe(st.session_state.df_cleaned.head(15), use_container_width=True)

    if "df_cleaned" in st.session_state:
        df_cleaned = st.session_state.df_cleaned

        col1, col2 = st.columns(2)
        with col1:
            st.metric("📐 Rows", df_cleaned.shape[0])
            st.metric("📏 Columns", df_cleaned.shape[1])
            st.metric("🧪 Missing Cells", df_cleaned.isnull().sum().sum())
        with col2:
            st.write("**🧬 Cleaned Data Types:**")
            st.dataframe(df_cleaned.dtypes.reset_index().rename(columns={"index": "Column", 0: "Data Type"}))

        st.markdown("### 👀 Preview Sample Rows")
        st.dataframe(df_cleaned.sample(5), use_container_width=True)

elif st.session_state.page == "Visualizations":
    if "df_cleaned" not in st.session_state:
        st.warning("⚠️ Please run preprocessing first!")
    else:
        from eda.basic_viz import show_basic_visualizations

        st.markdown(styles.section_block("📊 Auto Visualizations"), unsafe_allow_html=True)
        st.write("This section shows visualizations automatically.")

        show_basic_visualizations(st.session_state.df_cleaned)

elif st.session_state.page == "Smart Insights":
    st.markdown(styles.section_block("🧠 Smart Insights"), unsafe_allow_html=True)
    st.markdown(
        """
        <p style="color: #94a3b8; font-size: 1rem;">
        Get automatic data quality checks and smart warnings based on your dataset.
        These help identify potential issues before deeper analysis.
        </p>
        """,
        unsafe_allow_html=True
    )

    if "df_cleaned" not in st.session_state:
        st.warning("⚠️ Please upload and preprocess a dataset first.")
    else:
        from insights.null_flagger import flag_nulls
        df = st.session_state.df_cleaned

        # --- Section: Null Value Flags ---
        st.markdown("### <span style='color:#10b981'>🔍 Null Value Check</span>", unsafe_allow_html=True)
        st.info("Detects columns with more than **30% missing values**.")

        null_flags = flag_nulls(df)

        if not null_flags.empty:
            st.markdown("#### ⚠️ Columns With High Missing Values")

            col1, col2 = st.columns([3, 2])  # Wider for table, narrower for badges

            with col1:
                st.dataframe(
                    null_flags.style
                        .format({"Missing %": "{:.2f}"})
                        .background_gradient(cmap="OrRd")
                        .set_properties(**{'text-align': 'left'}),
                    use_container_width=True
                )

            with col2:
                st.markdown("**Flagged Columns:**", unsafe_allow_html=True)
                badges = "".join([f"<span class='null-flag-badge'>{col}</span><br>" for col in null_flags['Column']])
                st.markdown(badges, unsafe_allow_html=True)

        else:
            st.success("✅ Great! No columns have more than 30% missing values.")


        # --- Section: Outlier Detection Flags ---

        from insights.outlier_detector import aggregate_outlier_flags

        st.markdown("### <span style='color:#10b981'>🔎 Outlier Detection</span>", unsafe_allow_html=True)
        st.info("Detects potential outliers using both IQR and Z-score methods. Columns with >5% outliers are flagged.")

        outlier_info = aggregate_outlier_flags(st.session_state.df_cleaned)

        col1, col2 = st.columns([2, 1])  # Wider summary, narrower flags

        with col1:
            st.markdown("#### 📊 Outlier Summary")
            st.dataframe(outlier_info["summary"].head(15), use_container_width=True)

        with col2:
            # some padding for better alignment
            st.markdown("<div style='padding-top: 3.5rem;'></div>", unsafe_allow_html=True)
            st.markdown("**Flagged Columns:**")
            if outlier_info["insights"]:
                for insight in outlier_info["insights"]:
                    st.markdown(f"<div class='insight-flag'>{insight}</div>", unsafe_allow_html=True)
            else:
                st.success("✅ No significant outlier patterns detected (threshold: 5%).")





