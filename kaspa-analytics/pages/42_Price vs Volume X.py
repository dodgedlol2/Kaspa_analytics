import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from utils import load_volume_data, fit_power_law
from datetime import datetime, timedelta

st.set_page_config(layout="wide")

# Custom CSS - optimized version
st.markdown("""
<style>
    .stApp { background-color: #0E1117; }
    .st-emotion-cache-6qob1r { background-color: #262730 !important; }
    .title-spacing { padding-left: 40px; margin-bottom: 15px; }
    div[data-testid="stVerticalBlock"] > div[data-testid="stVerticalBlockBorderWrapper"] {
        background-color: #262730 !important;
        border-radius: 10px !important;
        border: 1px solid #3A3C4A !important;
        padding: 15px !important;
    }
    div[data-testid="stMetric"] {
        background-color: #262730 !important;
        border: 1px solid #3A3C4A !important;
        border-radius: 8px !important;
        padding: 15px 20px !important;
    }
    div[data-testid="stMetricValue"] > div {
        font-size: 24px !important;
        font-weight: 600 !important;
        color: #00FFCC !important;
    }
    div[data-testid="stMetricLabel"] > div {
        font-size: 14px !important;
        opacity: 0.8 !important;
        color: #e0e0e0 !important;
    }
    h2 { color: #e0e0e0 !important; }
    .metrics-container {
        width: calc(100% - 40px) !important;
        margin-left: 20px !important;
        margin-right: 20px !important;
        margin-top: 10px !important;
    }
    .control-label {
        font-size: 11px !important;
        color: #e0e0e0 !important;
        margin-bottom: 2px !important;
    }
</style>
""", unsafe_allow_html=True)

# Data loading with caching
@st.cache_data
def load_and_prepare_data():
    try:
        df = load_volume_data()
        df['Date'] = pd.to_datetime(df['Date']).dt.normalize()
        return df
    except Exception as e:
        st.error(f"Failed to load data: {str(e)}")
        st.stop()

volume_df = load_and_prepare_data()

# Calculate power law fit (cached)
@st.cache_data
def calculate_power_law(_df):
    try:
        return fit_power_law(_df, x_col='Volume_USD', y_col='Price')
    except Exception as e:
        st.error(f"Power law calculation failed: {str(e)}")
        return 1, 0, 0  # Default values if calculation fails

a, b, r2 = calculate_power_law(volume_df)

# ====== MAIN PAGE ======
with st.container():
    st.markdown('<div class="title-spacing"><h2>Kaspa Price vs Trading Volume Analysis</h2></div>', unsafe_allow_html=True)
    st.divider()
    
    # Simplified controls
    col1, col2, col3 = st.columns(3)
    with col1:
        time_ranges = ["1W", "1M", "3M", "6M", "1Y", "All"]
        time_range = st.selectbox("Time Range", time_ranges, index=len(time_ranges)-1)
    with col2:
        scale_options = ["Linear", "Log"]
        x_scale = st.selectbox("X-Axis Scale", scale_options, index=1)
    with col3:
        y_scale = st.selectbox("Y-Axis Scale", scale_options, index=1)
    st.divider()

    # Filter and downsample data based on time range
    last_date = volume_df['Date'].iloc[-1]
    if time_range == "1W":
        start_date = last_date - timedelta(days=7)
        df = volume_df[volume_df['Date'] >= start_date]
    elif time_range == "1M":
        start_date = last_date - timedelta(days=30)
        df = volume_df[volume_df['Date'] >= start_date]
    elif time_range == "3M":
        start_date = last_date - timedelta(days=90)
        df = volume_df[volume_df['Date'] >= start_date].iloc[::3]  # Sample every 3rd day
    elif time_range == "6M":
        start_date = last_date - timedelta(days=180)
        df = volume_df[volume_df['Date'] >= start_date].iloc[::5]  # Sample every 5th day
    elif time_range == "1Y":
        start_date = last_date - timedelta(days=365)
        df = volume_df[volume_df['Date'] >= start_date].iloc[::7]  # Sample weekly
    else:  # "All"
        df = volume_df.iloc[::10]  # Sample every 10th day for full history

    # Create the plot
    fig = go.Figure()

    # Main scatter plot with optimized markers
    fig.add_trace(go.Scatter(
        x=df['Volume_USD'],
        y=df['Price'],
        mode='markers',
        name='Daily Price vs Volume',
        marker=dict(
            color='#00FFCC',
            size=6,
            opacity=0.7,
            line=dict(width=0.5, color='DarkSlateGrey')
        ),
        hovertemplate='<b>Date</b>: %{text|%Y-%m-%d}<br><b>Volume</b>: $%{x:,.0f}<br><b>Price</b>: $%{y:.4f}<extra></extra>',
        text=df['Date']
    ))

    # Power law fit (calculated with full data but displayed with fewer points)
    x_fit = np.logspace(
        np.log10(df['Volume_USD'].min()), 
        np.log10(df['Volume_USD'].max()), 
        50  # Only 50 points for the fit line
    )
    y_fit = a * np.power(x_fit, b)
    
    fig.add_trace(go.Scatter(
        x=x_fit,
        y=y_fit,
        mode='lines',
        name=f'Power-Law Fit (R²={r2:.3f})',
        line=dict(color='#FFA726', width=2.5),
        hovertemplate='<b>Volume</b>: $%{x:,.0f}<br><b>Predicted Price</b>: $%{y:.4f}<extra></extra>'
    ))

    # Confidence bands (simplified)
    fig.add_trace(go.Scatter(
        x=x_fit,
        y=y_fit * 0.5,
        mode='lines',
        line=dict(width=0),
        showlegend=False,
        hoverinfo='skip'
    ))
    fig.add_trace(go.Scatter(
        x=x_fit,
        y=y_fit * 1.5,
        mode='lines',
        fill='tonexty',
        fillcolor='rgba(255, 165, 38, 0.1)',
        line=dict(width=0),
        name='±50% Confidence',
        hoverinfo='skip'
    ))

    # Optimized layout
    fig.update_layout(
        plot_bgcolor='#262730',
        paper_bgcolor='#262730',
        font=dict(color='#e0e0e0', size=12),
        hovermode='closest',
        height=600,  # Slightly reduced height
        margin=dict(l=50, r=50, t=50, b=50),
        xaxis_title='Trading Volume (USD)',
        yaxis_title='Price (USD)',
        xaxis_type="log" if x_scale == "Log" else "linear",
        yaxis_type="log" if y_scale == "Log" else "linear",
        xaxis=dict(
            gridcolor='rgba(100, 100, 100, 0.2)',
            linecolor='#3A3C4A'
        ),
        yaxis=dict(
            gridcolor='rgba(100, 100, 100, 0.2)',
            linecolor='#3A3C4A'
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        hoverlabel=dict(
            bgcolor='#262730',
            bordercolor='#3A3C4A',
            font_size=12
        )
    )

    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

# Stats - simplified metrics
st.markdown('<div class="metrics-container">', unsafe_allow_html=True)
cols = st.columns(3)
with cols[0]:
    st.metric("Power Law Slope", f"{b:.3f}", f"R² = {r2:.3f}")
with cols[1]:
    st.metric("Current Volume", f"${volume_df['Volume_USD'].iloc[-1]:,.0f}")
with cols[2]:
    st.metric("Current Price", f"${volume_df['Price'].iloc[-1]:.4f}")
st.markdown('</div>', unsafe_allow_html=True)
