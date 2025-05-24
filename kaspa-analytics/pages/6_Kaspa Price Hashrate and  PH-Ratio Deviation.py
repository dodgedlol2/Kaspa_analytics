import streamlit as st
import plotly.graph_objects as go
import numpy as np
import pandas as pd
from scipy.optimize import curve_fit
from utils import load_data, load_price_data
from datetime import datetime, timedelta

st.set_page_config(layout="wide")

# Define power law fitting function (using log-log space for better fit)
def fit_power_law_loglog(df, x_col='days_from_genesis', y_col='Price_Hashrate_Ratio'):
    """Fit power law y = a*x^b to data in log-log space"""
    x_data = np.log(df[x_col].values)
    y_data = np.log(df[y_col].values)
    
    # Linear function for log-log space
    def linear_func(x, a, b):
        return a * x + b
    
    try:
        params, _ = curve_fit(linear_func, x_data, y_data)
        a_log, b_log = params
        
        # Convert back to power law parameters
        a = np.exp(b_log)
        b = a_log
        
        # Calculate R-squared in log space
        y_pred = linear_func(x_data, a_log, b_log)
        residuals = y_data - y_pred
        ss_res = np.sum(residuals**2)
        ss_tot = np.sum((y_data - np.mean(y_data))**2)
        r_squared = 1 - (ss_res / ss_tot)
        
        return a, b, r_squared
    except Exception as e:
        st.error(f"Power law fitting failed: {str(e)}")
        return None, None, None

# Data loading and processing
if 'df' not in st.session_state or 'genesis_date' not in st.session_state:
    try:
        st.session_state.df, st.session_state.genesis_date = load_data()
        st.session_state.price_df, _ = load_price_data()
    except Exception as e:
        st.error(f"Failed to load data: {str(e)}")
        st.stop()

df = st.session_state.df
price_df = st.session_state.price_df
genesis_date = st.session_state.genesis_date

# Normalize timestamps to daily resolution
df['Date'] = pd.to_datetime(df['Date']).dt.normalize()
price_df['Date'] = pd.to_datetime(price_df['Date']).dt.normalize()

# Remove duplicate dates (keep last)
price_df = price_df.drop_duplicates('Date', keep='last')

# Merge data
merged_df = pd.merge(df, price_df[['Date', 'Price']], on='Date', how='left')

# Calculate price/hashrate ratio and days since genesis
analysis_df = merged_df.dropna(subset=['Hashrate_PH', 'Price']).copy()
analysis_df['Price_Hashrate_Ratio'] = analysis_df['Price'] / analysis_df['Hashrate_PH']
analysis_df['Days_Since_Genesis'] = (analysis_df['Date'] - genesis_date).dt.days + 1  # +1 to avoid log(0)

# Calculate power law fit for the ratio in log-log space
try:
    # Fit power law to the ratio vs time in log-log space
    a_ratio, b_ratio, r2_ratio = fit_power_law_loglog(analysis_df, x_col='Days_Since_Genesis', y_col='Price_Hashrate_Ratio')
    if None in [a_ratio, b_ratio, r2_ratio]:
        st.error("Failed to calculate ratio power law fit")
        st.stop()
        
    # Calculate expected ratio values based on power law
    analysis_df['Expected_Ratio'] = a_ratio * np.power(analysis_df['Days_Since_Genesis'], b_ratio)
    
    # Calculate percentage deviation from expected ratio
    analysis_df['Ratio_Deviation_Pct'] = ((analysis_df['Price_Hashrate_Ratio'] - analysis_df['Expected_Ratio']) / analysis_df['Expected_Ratio']) * 100
    
    # Calculate standard deviation bands
    rolling_window = min(30, len(analysis_df))  # Use 30-day window or all data if less
    analysis_df['Deviation_MA'] = analysis_df['Ratio_Deviation_Pct'].rolling(rolling_window).mean()
    analysis_df['Deviation_Std'] = analysis_df['Ratio_Deviation_Pct'].rolling(rolling_window).std()
    analysis_df['Upper_Band'] = analysis_df['Deviation_MA'] + (2 * analysis_df['Deviation_Std'])
    analysis_df['Lower_Band'] = analysis_df['Deviation_MA'] - (2 * analysis_df['Deviation_Std'])
    
except Exception as e:
    st.error(f"Failed to calculate ratio power law: {str(e)}")
    st.stop()

# Create color gradient for last 7 points (teal to purple)
last_7 = analysis_df.tail(7).copy()
purple_gradient = ['#00FFCC', '#40E0D0', '#80C0FF', '#A080FF', '#C040FF', '#E000FF', '#FF00FF']
last_7['color'] = purple_gradient

# Custom CSS to match other pages
st.markdown("""
<style>
    .stApp { background-color: #0E1117; }
    .st-emotion-cache-6qob1r, .sidebar-content { background-color: #262730 !important; }
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
    .stMetric { margin: 5px !important; height: 100% !important; }
    h2 { color: #e0e0e0 !important; }
    .hovertext text.hovertext { fill: #e0e0e0 !important; }
    .range-slider .handle:after { background-color: #00FFCC !important; }
    .metrics-container {
        width: calc(100% - 40px) !important;
        margin-left: 20px !important;
        margin-right: 20px !important;
        margin-top: 10px !important;
        margin-bottom: 0px !important;
    }
    .control-label {
        font-size: 11px !important;
        color: #e0e0e0 !important;
        margin-bottom: 2px !important;
        white-space: nowrap;
    }
    .st-emotion-cache-1dp5vir {
        border-top: 2px solid #3A3C4A !important;
        margin-top: 1px !important;
        margin-bottom: 2px !important;
    }
    [data-baseweb="select"] {
        font-size: 12px !important;
    }
    [data-baseweb="select"] > div {
        padding: 2px 6px !important;
        border-radius: 4px !important;
        border: 1px solid #3A3C4A !important;
        background-color: #262730 !important;
        transition: all 0.2s ease;
    }
    [data-baseweb="select"] > div:hover {
        border-color: #00FFCC !important;
    }
    [data-baseweb="select"] > div[aria-expanded="true"],
    [data-baseweb="select"] > div:focus-within {
        border-color: #00FFCC !important;
        box-shadow: 0 0 0 1px #00FFCC !important;
    }
    [role="option"] {
        font-size: 12px !important;
        padding: 8px 12px !important;
    }
    [role="option"]:hover {
        background-color: #3A3C4A !important;
    }
    [aria-selected="true"] {
        background-color: #00FFCC20 !important;
        color: #00FFCC !important;
    }
    div[role="combobox"] > div {
        font-size: 12px !important;
        color: #e0e0e0 !important;
    }
    .stSelectbox [data-baseweb="select"] > div:has(> div[aria-selected="true"]) {
        border-color: #00FFCC !important;
        background-color: #00FFCC10 !important;
    }
    .stSelectbox [data-baseweb="select"] > div:has(> div[aria-selected="true"]) > div {
        color: #00FFCC !important;
    }
</style>
""", unsafe_allow_html=True)

# ====== MAIN CHART CONTAINER ======
with st.container():
    st.markdown('<div class="title-spacing"><h2>Kaspa Hashrate with Price and Ratio Oscillator</h2></div>', unsafe_allow_html=True)
    
    # First divider - under the title
    st.divider()
    
    # Dropdown container
    col_spacer_left, col1, col2, col3, spacer1, spacer2, spacer3, spacer4, spacer5, spacer6, spacer7, spacer8, spacer9 = st.columns(
        [0.35, 1, 1, 1, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 3]
    )

    with col1:
        st.markdown('<div class="control-label">Hashrate Scale</div>', unsafe_allow_html=True)
        y_scale_options = ["Linear", "Log"]
        y_scale = st.selectbox("Hashrate Scale", y_scale_options,
                             index=1 if st.session_state.get("y_scale", True) else 0,
                             label_visibility="collapsed", key="y_scale_select")

    with col2:
        st.markdown('<div class="control-label">Time Scale</div>', unsafe_allow_html=True)
        x_scale_options = ["Linear", "Log"]
        x_scale_type = st.selectbox("Time Scale", x_scale_options,
                                  index=0,
                                  label_visibility="collapsed", key="x_scale_select")

    with col3:
        st.markdown('<div class="control-label">Period</div>', unsafe_allow_html=True)
        time_ranges = ["1W", "1M", "3M", "6M", "1Y", "All"]
        if 'time_range' not in st.session_state:
            st.session_state.time_range = "All"
        time_range = st.selectbox("Time Range", time_ranges,
                                index=time_ranges.index(st.session_state.time_range),
                                label_visibility="collapsed", key="time_range_select")
    
    # Second divider - under the dropdown menus
    st.divider()

    last_date = merged_df['Date'].iloc[-1]
    if time_range == "1W":
        start_date = last_date - timedelta(days=7)
    elif time_range == "1M":
        start_date = last_date - timedelta(days=30)
    elif time_range == "3M":
        start_date = last_date - timedelta(days=90)
    elif time_range == "6M":
        start_date = last_date - timedelta(days=180)
    elif time_range == "1Y":
        start_date = last_date - timedelta(days=365)
    else:
        start_date = merged_df['Date'].iloc[0]

    filtered_df = merged_df[merged_df['Date'] >= start_date]
    filtered_analysis_df = analysis_df[analysis_df['Date'] >= start_date]

    # Create figure with secondary y-axis for oscillator
    fig = go.Figure()

    if x_scale_type == "Log":
        x_values = filtered_df['days_from_genesis']
        x_title = "Days Since Genesis (Log Scale)"
        tickformat = None
        hoverformat = None
    else:
        x_values = filtered_df['Date']
        x_title = "Date"
        tickformat = "%b %Y"
        hoverformat = "%b %d, %Y"

    # Add hashrate trace (primary y-axis)
    fig.add_trace(go.Scatter(
        x=x_values,
        y=filtered_df['Hashrate_PH'],
        mode='lines',
        name='Hashrate (PH/s)',
        line=dict(color='#00FFCC', width=2.5),
        hovertemplate='<b>Date</b>: %{text|%Y-%m-%d}<br><b>Hashrate</b>: %{y:.2f} PH/s<extra></extra>',
        text=filtered_df['Date'],
        yaxis='y1'
    ))

    # Add price trace (secondary y-axis)
    fig.add_trace(go.Scatter(
        x=x_values,
        y=filtered_df['Price'],
        mode='lines',
        name='Price (USD)',
        line=dict(color='rgba(150, 150, 150, 0.7)', width=1.2),
        hovertemplate='<b>Date</b>: %{text|%Y-%m-%d}<br><b>Price</b>: $%{y:.4f}<extra></extra>',
        text=filtered_df['Date'],
        yaxis='y2'
    ))

    # Add oscillator trace (tertiary y-axis)
    fig.add_trace(go.Scatter(
        x=x_values,
        y=filtered_analysis_df['Ratio_Deviation_Pct'],
        mode='lines',
        name='Ratio Deviation %',
        line=dict(color='#FF00FF', width=2),
        hovertemplate='<b>Date</b>: %{text|%Y-%m-%d}<br><b>Deviation</b>: %{y:.1f}%<extra></extra>',
        text=filtered_analysis_df['Date'],
        yaxis='y3'
    ))

    # Add zero line for oscillator
    fig.add_shape(
        type="line",
        x0=x_values.iloc[0], x1=x_values.iloc[-1],
        y0=0, y1=0,
        line=dict(color="rgba(255,255,255,0.5)", width=1, dash="dot"),
        yref='y3'
    )

    # Add Bollinger-style bands for oscillator
    fig.add_trace(go.Scatter(
        x=x_values,
        y=filtered_analysis_df['Upper_Band'],
        mode='lines',
        line=dict(width=0),
        showlegend=False,
        hoverinfo='skip',
        yaxis='y3'
    ))
    
    fig.add_trace(go.Scatter(
        x=x_values,
        y=filtered_analysis_df['Lower_Band'],
        mode='lines',
        line=dict(width=0),
        fill='tonexty',
        fillcolor='rgba(100, 100, 100, 0.2)',
        name='±2σ Range',
        hoverinfo='skip',
        yaxis='y3'
    ))

    # Add colored markers for last 7 points on oscillator
    last_7_filtered = filtered_analysis_df.tail(7)
    for i, row in last_7_filtered.iterrows():
        x_val = row['Days_Since_Genesis'] if x_scale_type == "Log" else row['Date']
        fig.add_trace(go.Scatter(
            x=[x_val],
            y=[row['Ratio_Deviation_Pct']],
            mode='markers',
            marker=dict(
                color=purple_gradient[i % len(purple_gradient)],
                size=8,
                line=dict(width=1.5, color='DarkSlateGrey')
            ),
            showlegend=False,
            hoverinfo='skip',
            yaxis='y3'
        ))

    fig.update_layout(
        plot_bgcolor='#262730',
        paper_bgcolor='#262730',
        font_color='#e0e0e0',
        hovermode='x unified',
        height=700,
        margin=dict(l=20, r=20, t=60, b=100),
        xaxis_title=x_title,
        xaxis=dict(
            rangeslider=dict(
                visible=True,
                thickness=0.1,
                bgcolor='#262730',
                bordercolor="#3A3C4A",
                borderwidth=1
            ),
            type="log" if x_scale_type == "Log" else None,
            showgrid=True,
            gridwidth=1,
            gridcolor='rgba(255, 255, 255, 0.1)',
            minor=dict(
                ticklen=6,
                gridcolor='rgba(255, 255, 255, 0.05)',
                gridwidth=0.5
            ),
            tickformat=tickformat,
            linecolor='#3A3C4A',
            zerolinecolor='#3A3C4A'
        ),
        yaxis=dict(
            title='Hashrate (PH/s)',
            type="log" if y_scale == "Log" else "linear",
            showgrid=True,
            gridwidth=1,
            gridcolor='rgba(255, 255, 255, 0.1)',
            minor=dict(
                ticklen=6,
                gridcolor='rgba(255, 255, 255, 0.05)',
                gridwidth=0.5
            ),
            linecolor='#3A3C4A',
            zerolinecolor='#3A3C4A',
            color='#00FFCC'
        ),
        yaxis2=dict(
            title='Price (USD)',
            overlaying='y',
            side='right',
            type="log" if y_scale == "Log" else "linear",
            showgrid=False,
            linecolor='rgba(150, 150, 150, 0.5)',
            zeroline=False,
            color='rgba(150, 150, 150, 0.7)'
        ),
        yaxis3=dict(
            title='Deviation (%)',
            overlaying='y',
            side='right',
            position=0.85,
            showgrid=False,
            linecolor='#FF00FF',
            zeroline=False,
            color='#FF00FF'
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            bgcolor='rgba(38, 39, 48, 0.8)'
        ),
        hoverlabel=dict(
            bgcolor='#262730',
            bordercolor='#3A3C4A',
            font_color='#e0e0e0'
        )
    )

    st.plotly_chart(fig, use_container_width=True)

# Stats
st.markdown('<div class="metrics-container">', unsafe_allow_html=True)
cols = st.columns(4)
with cols[0]:
    st.metric("Current Hashrate", f"{df['Hashrate_PH'].iloc[-1]:.2f} PH/s")
with cols[1]:
    st.metric("Current Price", f"${price_df['Price'].iloc[-1]:.4f}")
with cols[2]:
    current_deviation = analysis_df['Ratio_Deviation_Pct'].iloc[-1]
    st.metric("Current Deviation", f"{current_deviation:.1f}%")
with cols[3]:
    st.metric("Ratio Trend (R²)", f"{r2_ratio:.3f}")
st.markdown('</div>', unsafe_allow_html=True)
