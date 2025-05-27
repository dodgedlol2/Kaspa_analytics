import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from utils import load_volume_data, fit_power_law
from datetime import datetime, timedelta

st.set_page_config(layout="wide")

# Custom CSS - matching the style of your other pages
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

# Data loading
if 'volume_df' not in st.session_state:
    try:
        st.session_state.volume_df = load_volume_data()
    except Exception as e:
        st.error(f"Failed to load volume data: {str(e)}")
        st.stop()

volume_df = st.session_state.volume_df
volume_df['Date'] = pd.to_datetime(volume_df['Date']).dt.normalize()

# Calculate power law fit for Price vs Volume
try:
    a, b, r2 = fit_power_law(volume_df, x_col='Volume_USD', y_col='Price')
except Exception as e:
    st.error(f"Failed to calculate power law: {str(e)}")
    st.stop()

# ====== MAIN CHART CONTAINER ======
with st.container():
    st.markdown('<div class="title-spacing"><h2>Kaspa Price vs Trading Volume Analysis</h2></div>', unsafe_allow_html=True)
    
    # First divider - under the title
    st.divider()
    
    # Dropdown container
    col_spacer_left, col1, col2, col3, col4, col_spacer_right = st.columns(
        [0.35, 1, 1, 1, 1, 1]
    )

    with col1:
        st.markdown('<div class="control-label">X-Axis Scale</div>', unsafe_allow_html=True)
        x_scale_options = ["Linear", "Log"]
        x_scale = st.selectbox("X-Axis Scale", x_scale_options,
                               index=1,
                               label_visibility="collapsed", key="x_scale_select")

    with col2:
        st.markdown('<div class="control-label">Y-Axis Scale</div>', unsafe_allow_html=True)
        y_scale_options = ["Linear", "Log"]
        y_scale = st.selectbox("Y-Axis Scale", y_scale_options,
                                index=1,
                                label_visibility="collapsed", key="y_scale_select")

    with col3:
        st.markdown('<div class="control-label">Period</div>', unsafe_allow_html=True)
        time_ranges = ["1W", "1M", "3M", "6M", "1Y", "All"]
        time_range = st.selectbox("Time Range", time_ranges,
                                  index=time_ranges.index("All"),
                                  label_visibility="collapsed", key="time_range_select")

    with col4:
        st.markdown('<div class="control-label">Power Law Fit</div>', unsafe_allow_html=True)
        power_law_options = ["Hide", "Show"]
        show_power_law = st.selectbox("Power Law Fit", power_law_options,
                                      index=1,  # Default to shown
                                      label_visibility="collapsed", key="power_law_select")
    
    # Second divider - under the dropdown menus
    st.divider()

    # Filter data based on time range
    last_date = volume_df['Date'].iloc[-1]
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
        start_date = volume_df['Date'].iloc[0]

    filtered_df = volume_df[volume_df['Date'] >= start_date]

    fig = go.Figure()

    # Add scatter plot of Price vs Volume
    fig.add_trace(go.Scatter(
        x=filtered_df['Volume_USD'],
        y=filtered_df['Price'],
        mode='markers',
        name='Daily Price vs Volume',
        marker=dict(
            color='#00FFCC',
            size=8,
            opacity=0.7,
            line=dict(width=1, color='DarkSlateGrey')
        ),
        hovertemplate='<b>Date</b>: %{text|%Y-%m-%d}<br><b>Volume</b>: $%{x:,.0f}<br><b>Price</b>: $%{y:.4f}<extra></extra>',
        text=filtered_df['Date']
    ))

    # Add power law fit if enabled
    if show_power_law == "Show":
        x_fit = np.linspace(filtered_df['Volume_USD'].min(), filtered_df['Volume_USD'].max(), 100)
        y_fit = a * np.power(x_fit, b)
        
        fig.add_trace(go.Scatter(
            x=x_fit,
            y=y_fit,
            mode='lines',
            name=f'Power-Law Fit (R²={r2:.3f})',
            line=dict(color='#FFA726', width=3),
            hovertemplate='<b>Volume</b>: $%{x:,.0f}<br><b>Predicted Price</b>: $%{y:.4f}<extra></extra>'
        ))

        # Add confidence bands
        fig.add_trace(go.Scatter(
            x=x_fit,
            y=y_fit * 0.5,
            mode='lines',
            name='-50% Deviation',
            line=dict(color='rgba(255, 255, 255, 0.5)', width=1, dash='dot'),
            hoverinfo='skip'
        ))
        fig.add_trace(go.Scatter(
            x=x_fit,
            y=y_fit * 1.5,
            mode='lines',
            name='+50% Deviation',
            line=dict(color='rgba(255, 255, 255, 0.5)', width=1, dash='dot'),
            hoverinfo='skip',
            fill='tonexty',
            fillcolor='rgba(100, 100, 100, 0.2)'
        ))

    fig.update_layout(
        plot_bgcolor='#262730',
        paper_bgcolor='#262730',
        font_color='#e0e0e0',
        hovermode='closest',
        height=700,
        margin=dict(l=20, r=20, t=60, b=100),
        xaxis_title='Trading Volume (USD)',
        yaxis_title='Price (USD)',
        xaxis=dict(
            type="log" if x_scale == "Log" else "linear",
            showgrid=True,
            gridwidth=1,
            gridcolor='rgba(255, 255, 255, 0.1)',
            minor=dict(
                ticklen=6,
                gridcolor='rgba(255, 255, 255, 0.05)',
                gridwidth=0.5
            ),
            linecolor='#3A3C4A',
            zerolinecolor='#3A3C4A'
        ),
        yaxis=dict(
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
            zerolinecolor='#3A3C4A'
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
    st.metric("Power-Law Slope", f"{b:.3f}")
with cols[1]:
    st.metric("Model Fit (R²)", f"{r2:.3f}")
with cols[2]:
    st.metric("Current Volume", f"${volume_df['Volume_USD'].iloc[-1]:,.0f}")
with cols[3]:
    st.metric("Current Price", f"${volume_df['Price'].iloc[-1]:.4f}")
st.markdown('</div>', unsafe_allow_html=True)
