# main.py

import streamlit as st
from ui.layout import render_landing_page
from eda.data_loader import upload_file
from ui import styles

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
        
