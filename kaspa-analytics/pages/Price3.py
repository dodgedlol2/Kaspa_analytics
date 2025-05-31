import streamlit as st
from streamlit_lightweight_charts import renderLightweightCharts
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from utils import fit_power_law, load_price_data

st.set_page_config(layout="wide")

# Data loading and processing
@st.cache_data
def load_data():
    try:
        price_df, genesis_date = load_price_data()
        return price_df, genesis_date
    except Exception as e:
        st.error(f"Failed to load price data: {str(e)}")
        st.stop()

try:
    price_df, genesis_date = load_data()
except Exception as e:
    st.error(f"Data loading error: {str(e)}")
    st.stop()

try:
    a_price, b_price, r2_price = fit_power_law(price_df, y_col='Price')
except Exception as e:
    st.error(f"Failed to calculate price power law: {str(e)}")
    st.stop()

# Custom CSS with container fixes
st.markdown("""
<style>
    .stApp {
        background-color: #1A1D26;
        padding-top: 20px;
    }
    .st-emotion-cache-1kyxreq {
        padding: 0;
    }
    .stLightweightChart {
        border-radius: 0.5rem;
    }
    .stMetric {
        background-color: #1A1D26 !important;
        border: 1px solid #3A3C4A !important;
    }
    .stPlotlyChart {
        width: 100% !important;
    }
    .stContainer {
        padding: 0 !important;
    }
    .stMarkdown h2 {
        padding-left: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Main chart container
st.markdown('<h2>Kaspa Price</h2>', unsafe_allow_html=True)

# Controls
cols = st.columns([1, 1, 1, 1, 4])
with cols[0]:
    y_scale = st.selectbox("Price Scale", ["Linear", "Log"], index=1, label_visibility="collapsed")
with cols[1]:
    x_scale_type = st.selectbox("Time Scale", ["Linear", "Log"], index=0, label_visibility="collapsed")
with cols[2]:
    time_range = st.selectbox("Period", ["1W", "1M", "3M", "6M", "1Y", "All"], index=5, label_visibility="collapsed")
with cols[3]:
    show_power_law = st.selectbox("Power Law Fit", ["Hide", "Show"], index=0, label_visibility="collapsed")

# Filter data
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
filtered_df['timestamp'] = (filtered_df['Date'].astype(np.int64) // 10**6

# Prepare series
main_series = {
    'type': 'Line',
    'data': filtered_df[['timestamp', 'Price']].rename(columns={'Price': 'value'}).to_dict('records'),
    'options': {'color': '#00FFCC', 'lineWidth': 2}
}

series = [main_series]

if show_power_law == "Show":
    filtered_df['power_law'] = a_price * np.power(filtered_df['days_from_genesis'], b_price)
    filtered_df['upper_band'] = filtered_df['power_law'] * 2.2
    filtered_df['lower_band'] = filtered_df['power_law'] * 0.4
    
    power_law_series = {
        'type': 'Line',
        'data': filtered_df[['timestamp', 'power_law']].rename(columns={'power_law': 'value'}).to_dict('records'),
        'options': {'color': '#FFA726', 'lineWidth': 2, 'lineStyle': 1}
    }
    
    upper_band_series = {
        'type': 'Line',
        'data': filtered_df[['timestamp', 'upper_band']].rename(columns={'upper_band': 'value'}).to_dict('records'),
        'options': {'color': 'rgba(255, 255, 255, 0.5)', 'lineWidth': 1, 'lineStyle': 1}
    }
    
    lower_band_series = {
        'type': 'Line',
        'data': filtered_df[['timestamp', 'lower_band']].rename(columns={'lower_band': 'value'}).to_dict('records'),
        'options': {'color': 'rgba(255, 255, 255, 0.5)', 'lineWidth': 1, 'lineStyle': 1}
    }
    
    series.extend([power_law_series, upper_band_series, lower_band_series])

# Chart configuration
chart_config = {
    'chart': {
        'layout': {
            'background_color': '#1A1D26',
            'text_color': '#e0e0e0'
        },
        'rightPriceScale': {
            'scaleMode': 2 if y_scale == "Log" else 1,
            'borderColor': '#3A3C4A'
        },
        'timeScale': {
            'timeVisible': True,
            'borderColor': '#3A3C4A'
        },
        'grid': {
            'vertLines': {'color': 'rgba(255, 255, 255, 0.1)'},
            'horzLines': {'color': 'rgba(255, 255, 255, 0.1)'}
        },
        'height': 700
    },
    'series': series
}

# Render chart with error handling
try:
    renderLightweightCharts([chart_config], key='price_chart')
except Exception as e:
    st.error(f"Failed to render chart: {str(e)}")
    st.stop()

# Metrics
cols = st.columns(3)
with cols[0]:
    st.metric("Power-Law Slope", f"{b_price:.3f}")
with cols[1]:
    st.metric("Model Fit (R²)", f"{r2_price:.3f}")
with cols[2]:
    st.metric("Current Price", f"${price_df['Price'].iloc[-1]:.4f}")
