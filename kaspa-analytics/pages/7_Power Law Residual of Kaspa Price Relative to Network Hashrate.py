import streamlit as st
import plotly.graph_objects as go
import numpy as np
import pandas as pd
from utils import load_data, load_price_data, fit_power_law
from datetime import datetime, timedelta

st.set_page_config(layout="wide")

# Data loading with aggressive caching
@st.cache_data(ttl=3600, show_spinner=False)
def load_all_data():
    try:
        df, genesis_date = load_data()
        price_df, _ = load_price_data()
        
        # Pre-process data immediately
        df['Date'] = pd.to_datetime(df['Date']).dt.normalize()
        price_df['Date'] = pd.to_datetime(price_df['Date']).dt.normalize()
        price_df = price_df.drop_duplicates('Date', keep='last')
        
        return df, price_df, genesis_date
    except Exception as e:
        st.error(f"Failed to load data: {str(e)}")
        st.stop()

# Process data with caching
@st.cache_data(ttl=3600)
def process_data(_df, _price_df, genesis_date):
    merged_df = pd.merge(_df, _price_df[['Date', 'Price']], on='Date', how='left')
    merged_df['days_from_genesis'] = (merged_df['Date'] - genesis_date).dt.days + 1
    
    analysis_df = merged_df.dropna(subset=['Hashrate_PH', 'Price']).copy()
    analysis_df['Days_Since_Genesis'] = (analysis_df['Date'] - genesis_date).dt.days + 1
    
    # Calculate power law
    a_relation, b_relation, _ = fit_power_law(analysis_df, x_col='Hashrate_PH', y_col='Price')
    analysis_df['Expected_Price'] = a_relation * np.power(analysis_df['Hashrate_PH'], b_relation)
    analysis_df['Price_Deviation_Pct'] = ((analysis_df['Price'] - analysis_df['Expected_Price']) / 
                                         analysis_df['Expected_Price']) * 100
    
    return merged_df, analysis_df, b_relation

# Load data
df, price_df, genesis_date = load_all_data()
merged_df, analysis_df, b_relation = process_data(df, price_df, genesis_date)

# Simplified CSS (removed unnecessary styles)
st.markdown("""
<style>
    .stMetric { margin: 5px !important; }
    div[data-testid="stMetricValue"] > div { color: #00FFCC !important; }
    .metrics-container { margin: 10px 20px !important; }
</style>
""", unsafe_allow_html=True)

# UI Elements
st.markdown('<h2 style="color:#e0e0e0">Power Law Residual of Kaspa Price Relative to Network Hashrate</h2>', 
            unsafe_allow_html=True)
st.divider()

# Controls in columns
cols = st.columns([1,1,1,5])
with cols[0]:
    y_scale = st.selectbox("Hashrate Scale", ["Linear", "Log"], index=1, key="y_scale")
with cols[1]:
    x_scale_type = st.selectbox("Time Scale", ["Linear", "Log"], index=0, key="x_scale")
with cols[2]:
    time_range = st.selectbox("Period", ["1W", "1M", "3M", "6M", "1Y", "All"], index=5, key="time_range")

st.divider()

# Date filtering
date_ranges = {
    "1W": timedelta(days=7),
    "1M": timedelta(days=30),
    "3M": timedelta(days=90),
    "6M": timedelta(days=180),
    "1Y": timedelta(days=365),
    "All": None
}

last_date = merged_df['Date'].iloc[-1]
time_delta = date_ranges.get(time_range, None)
filtered_df = merged_df[merged_df['Date'] >= (last_date - time_delta)] if time_delta else merged_df
filtered_analysis_df = analysis_df[analysis_df['Date'] >= (last_date - time_delta)] if time_delta else analysis_df

# Create simplified figure
fig = go.Figure()

# Main traces
x_values = filtered_df['days_from_genesis'] if x_scale_type == "Log" else filtered_df['Date']

fig.add_trace(go.Scatter(
    x=x_values,
    y=filtered_df['Hashrate_PH'],
    name='Hashrate',
    line=dict(color='#00FFCC', width=2),
    hovertemplate='Hashrate: %{y:.2f} PH/s<extra></extra>'
))

fig.add_trace(go.Scatter(
    x=x_values,
    y=filtered_df['Price'],
    name='Price',
    line=dict(color='#888', width=1),
    yaxis='y2',
    hovertemplate='Price: $%{y:.4f}<extra></extra>'
))

# Oscillator
osc_x = filtered_analysis_df['Days_Since_Genesis'] if x_scale_type == "Log" else filtered_analysis_df['Date']
fig.add_trace(go.Bar(
    x=osc_x,
    y=filtered_analysis_df['Price_Deviation_Pct'],
    name='Deviation',
    marker_color=np.where(filtered_analysis_df['Price_Deviation_Pct'] >= 0, '#00FFCC80', '#FF505080'),
    yaxis='y3'
))

# Layout configuration
fig.update_layout(
    plot_bgcolor='#262730',
    paper_bgcolor='#262730',
    font_color='#e0e0e0',
    height=600,
    margin=dict(t=40, b=80),
    hovermode='x unified',
    showlegend=True,
    xaxis=dict(
        type="log" if x_scale_type == "Log" else None,
        showgrid=True,
        gridcolor='rgba(255,255,255,0.1)',
        rangeslider=dict(visible=False)  # Disabled for performance
    ),
    yaxis=dict(
        title='Hashrate (PH/s)',
        type="log" if y_scale == "Log" else "linear",
        gridcolor='rgba(255,255,255,0.1)',
        domain=[0.35, 1]
    ),
    yaxis2=dict(
        title='Price (USD)',
        overlaying='y',
        side='right',
        gridcolor='rgba(255,255,255,0.05)',
        showgrid=False
    ),
    yaxis3=dict(
        title='Deviation (%)',
        domain=[0, 0.3],
        gridcolor='rgba(255,255,255,0.1)'
    )
)

# Render chart
st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})  # Disable modebar for performance

# Metrics
st.markdown('<div class="metrics-container">', unsafe_allow_html=True)
current_data = merged_df.iloc[-1]
cols = st.columns(4)
cols[0].metric("Current Hashrate", f"{current_data['Hashrate_PH']:.2f} PH/s")
cols[1].metric("Current Price", f"${current_data['Price']:.4f}")
cols[2].metric("Power-Law Slope", f"{b_relation:.3f}")
cols[3].metric("Current Deviation", f"{analysis_df['Price_Deviation_Pct'].iloc[-1]:.1f}%")
st.markdown('</div>', unsafe_allow_html=True)
