import streamlit as st
import plotly.graph_objects as go
import numpy as np
import pandas as pd
from utils import fit_power_law, load_data
from datetime import datetime, timedelta

st.set_page_config(layout="wide")
st.title("Kaspa Hashrate Analysis Dashboard")

# Data loading and processing
@st.cache_data
def load_all_data():
    try:
        df, genesis_date = load_data()
        
        # Calculate additional metrics
        df['Daily_Growth'] = df['Hashrate_PH'].pct_change() * 100
        df['Weekly_Growth'] = df['Hashrate_PH'].pct_change(7) * 100
        df['Monthly_Growth'] = df['Hashrate_PH'].pct_change(30) * 100
        
        # Calculate 30-day moving averages
        df['MA_7'] = df['Hashrate_PH'].rolling(7).mean()
        df['MA_30'] = df['Hashrate_PH'].rolling(30).mean()
        
        return df, genesis_date
    except Exception as e:
        st.error(f"Failed to load data: {str(e)}")
        st.stop()

if 'df' not in st.session_state or 'genesis_date' not in st.session_state:
    st.session_state.df, st.session_state.genesis_date = load_all_data()

df = st.session_state.df
genesis_date = st.session_state.genesis_date

# Calculate power law fit
try:
    a, b, r2 = fit_power_law(df)
except Exception as e:
    st.error(f"Failed to calculate power law: {str(e)}")
    st.stop()

# ===== SIDEBAR CONTROLS =====
with st.sidebar:
    st.header("Dashboard Controls")
    
    # Date range selector
    min_date = df['Date'].min()
    max_date = df['Date'].max()
    selected_range = st.date_input(
        "Date Range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )
    
    # Analysis timeframe
    timeframe = st.selectbox(
        "Analysis Timeframe",
        options=["All Time", "Yearly", "Quarterly", "Monthly"],
        index=0
    )
    
    # Additional metrics toggles
    st.subheader("Metrics to Display")
    show_growth = st.checkbox("Show Growth Rates", True)
    show_moving_avg = st.checkbox("Show Moving Averages", True)
    show_forecast = st.checkbox("Show 30-Day Forecast", False)
    
    # Advanced settings
    with st
