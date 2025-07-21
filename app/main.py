# main.py

import streamlit as st
from ui.layout import render_landing_page
from eda.data_loader import upload_file
from ui import styles
from eda.type_inference import detect_column_types
from eda.summary_stats import generate_summary
from eda.missing_values import get_missing_value_report, plot_missing_bar

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
nav_col1, nav_col2 = st.columns([1, 1])
with nav_col1:
    if st.button("🏠 Home", use_container_width=True, key="home_button"):
        st.session_state.page = "Home"
with nav_col2:
    if st.button("📁 Upload Dataset", use_container_width=True, key="upload_button"):
        st.session_state.page = "Upload"
st.markdown("</div><hr>", unsafe_allow_html=True)

# --------------------------
# Render Pages
# --------------------------
if st.session_state.page == "Home":
    render_landing_page()

elif st.session_state.page == "Upload":
    df = upload_file()

    if df is not None:
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


