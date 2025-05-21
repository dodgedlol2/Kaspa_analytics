import streamlit as st
from utils import load_data

st.set_page_config(
    page_title="Kaspa Network Analytics",
    page_icon="🔍",
    layout="wide"
)

# Force dark mode on first visit
if 'dark_mode' not in st.session_state:
    st.session_state.dark_mode = True
    st.markdown("""
    <style>
        .stApp {
            background-color: #3b1117;
        }
    </style>
    """, unsafe_allow_html=True)

st.title("Kaspa Network Analytics Dashboard")
st.markdown("""
Welcome to the Kaspa network analytics dashboard. Use the sidebar to navigate between different metrics.
""")

# Sidebar navigation
st.sidebar.title("Navigation")
st.sidebar.markdown("Select a page to view different analytics")

# Load data (will be cached and shared across pages)
df, genesis_date = load_data()
st.session_state.df = df
st.session_state.genesis_date = genesis_date
