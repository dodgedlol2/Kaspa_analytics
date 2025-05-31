import streamlit as st
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from utils import fit_power_law, load_price_data

# Initialize session state
if 'price_df' not in st.session_state:
    try:
        st.session_state.price_df, st.session_state.price_genesis_date = load_price_data()
    except Exception as e:
        st.error(f"Failed to load price data: {str(e)}")
        st.stop()

# Set page config
st.set_page_config(layout="wide", page_title="Kaspa Price Analysis")

# CSS Styling
st.markdown("""
<style>
    .stApp {
        background-color: #1A1D26;
        padding-top: 1rem;
    }
    .metric-container {
        background-color: #1A1D26;
        border: 1px solid #3A3C4A;
        border-radius: 8px;
        padding: 15px 20px;
    }
    .chart-container {
        height: 700px;
        width: 100%;
    }
</style>
""", unsafe_allow_html=True)

# Title
st.title("Kaspa Price Analysis")

# Controls
col1, col2, col3, col4 = st.columns(4)
with col1:
    price_scale = st.selectbox("Price Scale", ["Linear", "Log"], index=1)
with col2:
    time_scale = st.selectbox("Time Scale", ["Linear", "Log"], index=0)
with col3:
    time_range = st.selectbox("Period", ["1W", "1M", "3M", "6M", "1Y", "All"], index=5)
with col4:
    show_fit = st.selectbox("Power Law Fit", ["Hide", "Show"], index=0)

# Data processing
price_df = st.session_state.price_df
last_date = price_df['Date'].iloc[-1]

time_deltas = {
    "1W": timedelta(days=7),
    "1M": timedelta(days=30),
    "3M": timedelta(days=90),
    "6M": timedelta(days=180),
    "1Y": timedelta(days=365),
    "All": None
}

start_date = last_date - time_deltas[time_range] if time_range != "All" else price_df['Date'].iloc[0]
filtered_df = price_df[price_df['Date'] >= start_date].copy()

# Calculate power law fit
try:
    a, b, r2 = fit_power_law(filtered_df, y_col='Price')
except Exception as e:
    st.error(f"Power law calculation failed: {str(e)}")
    st.stop()

# Create chart data
chart_data = filtered_df[['Date', 'Price']].copy()
chart_data['timestamp'] = (chart_data['Date'].astype(np.int64) // 10**6

# Display metrics
metric_col1, metric_col2, metric_col3 = st.columns(3)
with metric_col1:
    st.metric("Power-Law Slope", f"{b:.3f}")
with metric_col2:
    st.metric("Model Fit (R²)", f"{r2:.3f}")
with metric_col3:
    st.metric("Current Price", f"${price_df['Price'].iloc[-1]:.4f}")

# Simple Plotly fallback since lightweight-charts is problematic
try:
    import plotly.graph_objects as go
    
    fig = go.Figure()
    
    # Add price trace
    fig.add_trace(go.Scatter(
        x=filtered_df['Date'],
        y=filtered_df['Price'],
        mode='lines',
        name='Price',
        line=dict(color='#00FFCC', width=2)
    ))
    
    if show_fit == "Show":
        filtered_df['power_law'] = a * np.power(filtered_df['days_from_genesis'], b)
        fig.add_trace(go.Scatter(
            x=filtered_df['Date'],
            y=filtered_df['power_law'],
            mode='lines',
            name=f'Power Law Fit (R²={r2:.3f})',
            line=dict(color='#FFA726', dash='dot')
        ))
    
    fig.update_layout(
        height=700,
        plot_bgcolor='#1A1D26',
        paper_bgcolor='#1A1D26',
        font_color='white',
        xaxis=dict(type='log' if time_scale == "Log" else None),
        yaxis=dict(type='log' if price_scale == "Log" else None)
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
except Exception as e:
    st.error(f"Chart rendering failed: {str(e)}")
    st.write("Here's the raw data as a fallback:")
    st.dataframe(filtered_df)
