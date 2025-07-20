import streamlit as st
from ui.layout import render_landing_page

st.set_page_config(page_title="AutoEDA", layout="wide",page_icon="📊")
render_landing_page()