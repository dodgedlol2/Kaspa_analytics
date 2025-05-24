import streamlit as st
import plotly.graph_objects as go
import numpy as np
import pandas as pd
from utils import fit_power_law, load_price_data, load_data
from datetime import datetime, timedelta

# Set page config first
st.set_page_config(layout="wide")

# Data loading and processing
@st.cache_data
def load_all_data():
    try:
        price_df, genesis_date = load_price_data()
        hashrate_df, _ = load_data()
        return price_df, hashrate_df, genesis_date
    except Exception as e:
        st.error(f"Failed to load data: {str(e)}")
        st.stop()

price_df, hashrate_df, genesis_date = load_all_data()

# Data processing
def process_data(price_df, hashrate_df, genesis_date):
    # Merge data
    hashrate_df['Date'] = pd.to_datetime(hashrate_df['Date']).dt.normalize()
    price_df['Date'] = pd.to_datetime(price_df['Date']).dt.normalize()
    merged_df = pd.merge(price_df, hashrate_df[['Date', 'Hashrate_PH']], on='Date', how='left')
    merged_df = merged_df.dropna(subset=['Price', 'Hashrate_PH']).copy()
    
    # Calculate power laws
    a_price, b_price, r2_price = fit_power_law(price_df, y_col='Price')
    
    # Calculate ratio metrics
    merged_df['Price_Hashrate_Ratio'] = merged_df['Price'] / merged_df['Hashrate_PH']
    merged_df['Days_Since_Genesis'] = (merged_df['Date'] - genesis_date).dt.days + 1
    a_ratio, b_ratio, r2_ratio = fit_power_law(merged_df, x_col='Days_Since_Genesis', y_col='Price_Hashrate_Ratio')
    
    # Calculate deviations
    merged_df['Expected_Ratio'] = a_ratio * np.power(merged_df['Days_Since_Genesis'], b_ratio)
    merged_df['Ratio_Deviation_Pct'] = ((merged_df['Price_Hashrate_Ratio'] - merged_df['Expected_Ratio']) / 
                                       merged_df['Expected_Ratio']) * 100
    
    return merged_df, a_price, b_price, r2_price, a_ratio, b_ratio, r2_ratio

try:
    merged_df, a_price, b_price, r2_price, a_ratio, b_ratio, r2_ratio = process_data(price_df, hashrate_df, genesis_date)
except Exception as e:
    st.error(f"Data processing error: {str(e)}")
    st.stop()

# Custom CSS
st.markdown("""
<style>
    /* Your existing CSS styles */
    .oscillator-container {
        height: 150px !important;
        margin-top: -30px !important;
    }
    .combined-chart {
        height: 700px !important;
    }
    /* Fix for URI issues */
    .stApp a {
        all: unset !important;
    }
    .stApp a:hover {
        all: unset !important;
    }
</style>
""", unsafe_allow_html=True)

# Main app
def main():
    st.markdown('<div class="title-spacing"><h2>Kaspa Price with Hashrate Ratio Oscillator</h2></div>', unsafe_allow_html=True)
    st.divider()
    
    # Controls
    col1, col2, col3, col4, col5, _ = st.columns([1, 1, 1, 1, 1, 3])
    
    with col1:
        y_scale = st.selectbox("Price Scale", ["Linear", "Log"], index=1, key="price_y_scale")
    
    with col2:
        x_scale_type = st.selectbox("Time Scale", ["Linear", "Log"], index=0, key="time_scale")
    
    with col3:
        time_range = st.selectbox("Period", ["1W", "1M", "3M", "6M", "1Y", "All"], index=5, key="time_range")
    
    with col4:
        show_power_law = st.selectbox("Power Law Fit", ["Hide", "Show"], index=0, key="power_law")
    
    with col5:
        show_oscillator = st.selectbox("Show Oscillator", ["Hide", "Show"], index=1, key="oscillator")
    
    st.divider()

    # Filter data
    last_date = merged_df['Date'].iloc[-1]
    date_ranges = {
        "1W": last_date - timedelta(days=7),
        "1M": last_date - timedelta(days=30),
        "3M": last_date - timedelta(days=90),
        "6M": last_date - timedelta(days=180),
        "1Y": last_date - timedelta(days=365),
        "All": merged_df['Date'].iloc[0]
    }
    filtered_df = merged_df[merged_df['Date'] >= date_ranges[time_range]]

    # Create figure
    fig = go.Figure()

    # Price trace
    fig.add_trace(go.Scatter(
        x=filtered_df['Date'],
        y=filtered_df['Price'],
        mode='lines',
        name='Price (USD)',
        line=dict(color='#00FFCC', width=2.5),
        hovertemplate='<b>Date</b>: %{x|%Y-%m-%d}<br><b>Price</b>: $%{y:.4f}<extra></extra>'
    ))

    # Power law fit
    if show_power_law == "Show":
        x_fit = filtered_df['days_from_genesis']
        y_fit = a_price * np.power(x_fit, b_price)
        fig.add_trace(go.Scatter(
            x=filtered_df['Date'],
            y=y_fit,
            mode='lines',
            name=f'Power-Law Fit (R²={r2_price:.3f})',
            line=dict(color='#FFA726', dash='dot', width=2)
        ))

    # Oscillator
    if show_oscillator == "Show":
        fig.add_shape(
            type="line",
            x0=filtered_df['Date'].min(),
            y0=0,
            x1=filtered_df['Date'].max(),
            y1=0,
            line=dict(color="rgba(255,255,255,0.5)", width=1, dash="dot"),
            yref="y2"
        )

        colors = ['rgba(0, 255, 0, 0.7)' if x >= 0 else 'rgba(255, 0, 0, 0.7)' 
                 for x in filtered_df['Ratio_Deviation_Pct']]
        fig.add_trace(go.Bar(
            x=filtered_df['Date'],
            y=filtered_df['Ratio_Deviation_Pct'],
            name='Deviation %',
            marker_color=colors,
            hovertemplate='<b>Date</b>: %{x|%Y-%m-%d}<br><b>Deviation</b>: %{y:.1f}%<extra></extra>',
            yaxis="y2"
        ))

    # Layout
    layout = {
        "plot_bgcolor": '#262730',
        "paper_bgcolor": '#262730',
        "font_color": '#e0e0e0',
        "hovermode": 'x unified',
        "height": 700,
        "margin": dict(l=20, r=20, t=60, b=100),
        "yaxis": {
            "title": 'Price (USD)',
            "type": "log" if y_scale == "Log" else "linear",
            "showgrid": True,
            "gridcolor": 'rgba(255, 255, 255, 0.1)',
            "linecolor": '#3A3C4A'
        },
        "xaxis": {
            "title": "Date",
            "rangeslider": dict(visible=True, thickness=0.1, bgcolor='#262730'),
            "type": "log" if x_scale_type == "Log" else None,
            "showgrid": True,
            "gridcolor": 'rgba(255, 255, 255, 0.1)',
            "linecolor": '#3A3C4A'
        }
    }

    if show_oscillator == "Show":
        layout["yaxis2"] = {
            "title": "Deviation %",
            "overlaying": "y",
            "side": "right",
            "showgrid": False,
            "zeroline": True,
            "zerolinecolor": 'rgba(255,255,255,0.5)'
        }

    fig.update_layout(**layout)
    st.plotly_chart(fig, use_container_width=True)

    # Metrics
    cols = st.columns(5)
    with cols[0]:
        st.metric("Power-Law Slope", f"{b_price:.3f}")
    with cols[1]:
        st.metric("Model Fit (R²)", f"{r2_price:.3f}")
    with cols[2]:
        current_dev = merged_df['Ratio_Deviation_Pct'].iloc[-1]
        st.metric("Current Deviation", f"{current_dev:.1f}%", 
                 delta_color="inverse" if current_dev < 0 else "normal")
    with cols[3]:
        st.metric("Ratio Fit (R²)", f"{r2_ratio:.3f}")
    with cols[4]:
        st.metric("Current Price", f"${price_df['Price'].iloc[-1]:.4f}")

if __name__ == "__main__":
    main()
