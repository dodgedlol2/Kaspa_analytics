import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from utils import load_volume_data, fit_power_law
from datetime import datetime, timedelta

st.set_page_config(layout="wide")

# Reuse the same CSS styling from your volume page
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

# Calculate moving averages
volume_df['MA_30_Volume'] = volume_df['Volume_USD'].rolling(30).mean()
volume_df['MA_30_Price'] = volume_df['Price'].rolling(30).mean()

# Calculate power law fits
try:
    # Volume power law
    a_vol, b_vol, r2_vol = fit_power_law(volume_df, y_col='Volume_USD')
    
    # Price power law
    a_price, b_price, r2_price = fit_power_law(volume_df, y_col='Price')
except Exception as e:
    st.error(f"Failed to calculate power law: {str(e)}")
    st.stop()

# ====== MAIN CHART CONTAINER ======
with st.container():
    st.markdown('<div class="title-spacing"><h2>Kaspa Price & Volume Power Law Analysis</h2></div>', unsafe_allow_html=True)
    
    # First divider - under the title
    st.divider()
    
    # Dropdown container
    col_spacer_left, col1, col2, col3, col4, col5, col6, spacer1, spacer2, spacer3, spacer4, spacer5, spacer6, spacer7 = st.columns(
        [0.35, 1, 1, 1, 1, 1, 1, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 1]
    )

    with col1:
        st.markdown('<div class="control-label">Scale</div>', unsafe_allow_html=True)
        scale_options = ["Linear", "Log"]
        scale_type = st.selectbox("Scale", scale_options,
                               index=1,
                               label_visibility="collapsed", key="scale_select")

    with col2:
        st.markdown('<div class="control-label">Time Scale</div>', unsafe_allow_html=True)
        x_scale_options = ["Linear", "Log"]
        x_scale_type = st.selectbox("Time Scale", x_scale_options,
                                index=0,
                                label_visibility="collapsed", key="x_scale_select")

    with col3:
        st.markdown('<div class="control-label">Period</div>', unsafe_allow_html=True)
        time_ranges = ["1W", "1M", "3M", "6M", "1Y", "All"]
        time_range = st.selectbox("Time Range", time_ranges,
                                  index=time_ranges.index("All"),
                                  label_visibility="collapsed", key="time_range_select")

    with col4:
        st.markdown('<div class="control-label">Volume Power Law</div>', unsafe_allow_html=True)
        vol_pl_options = ["Hide", "Show"]
        show_vol_pl = st.selectbox("Volume Power Law", vol_pl_options,
                                      index=0,
                                      label_visibility="collapsed", key="vol_pl_select")
    
    with col5:
        st.markdown('<div class="control-label">Price Power Law</div>', unsafe_allow_html=True)
        price_pl_options = ["Hide", "Show"]
        show_price_pl = st.selectbox("Price Power Law", price_pl_options,
                                 index=0,
                                 label_visibility="collapsed", key="price_pl_select")
    
    with col6:
        st.markdown('<div class="control-label">30D MA</div>', unsafe_allow_html=True)
        ma30_options = ["Hide", "Show"]
        show_ma30 = st.selectbox("30D MA", ma30_options,
                                 index=0,
                                 label_visibility="collapsed", key="ma30_select")
    
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

    # Add Volume trace (primary y-axis)
    fig.add_trace(go.Scatter(
        x=x_values,
        y=filtered_df['Volume_USD'],
        mode='lines',
        name='Volume (USD)',
        line=dict(color='#00FFCC', width=2),
        hovertemplate='<b>Date</b>: %{text|%Y-%m-%d}<br><b>Volume</b>: $%{y:,.0f}<extra></extra>',
        text=filtered_df['Date'],
        yaxis='y'
    ))

    # Add Price trace (secondary y-axis)
    fig.add_trace(go.Scatter(
        x=x_values,
        y=filtered_df['Price'],
        mode='lines',
        name='Price (USD)',
        line=dict(color='#FFA726', width=2),
        hovertemplate='<b>Date</b>: %{text|%Y-%m-%d}<br><b>Price</b>: $%{y:.4f}<extra></extra>',
        text=filtered_df['Date'],
        yaxis='y2'
    ))

    # Add moving averages if enabled
    if show_ma30 == "Show":
        fig.add_trace(go.Scatter(
            x=x_values,
            y=filtered_df['MA_30_Volume'],
            mode='lines',
            name='30D MA Volume',
            line=dict(color='#00FFCC', width=1.5, dash='dash'),
            hovertemplate='<b>Date</b>: %{text|%Y-%m-%d}<br><b>30D MA Volume</b>: $%{y:,.0f}<extra></extra>',
            text=filtered_df['Date']
        ))
        
        fig.add_trace(go.Scatter(
            x=x_values,
            y=filtered_df['MA_30_Price'],
            mode='lines',
            name='30D MA Price',
            line=dict(color='#FFA726', width=1.5, dash='dash'),
            hovertemplate='<b>Date</b>: %{text|%Y-%m-%d}<br><b>30D MA Price</b>: $%{y:.4f}<extra></extra>',
            text=filtered_df['Date'],
            yaxis='y2'
        ))

    # Add power law fits if enabled
    if show_vol_pl == "Show":
        x_fit = filtered_df['days_from_genesis']
        y_fit_vol = a_vol * np.power(x_fit, b_vol)
        fit_x = x_fit if x_scale_type == "Log" else filtered_df['Date']

        fig.add_trace(go.Scatter(
            x=fit_x,
            y=y_fit_vol,
            mode='lines',
            name=f'Volume Power-Law (R²={r2_vol:.3f})',
            line=dict(color='#00FFCC', dash='dot', width=1.5)
        ))

    if show_price_pl == "Show":
        x_fit = filtered_df['days_from_genesis']
        y_fit_price = a_price * np.power(x_fit, b_price)
        fit_x = x_fit if x_scale_type == "Log" else filtered_df['Date']

        fig.add_trace(go.Scatter(
            x=fit_x,
            y=y_fit_price,
            mode='lines',
            name=f'Price Power-Law (R²={r2_price:.3f})',
            line=dict(color='#FFA726', dash='dot', width=1.5),
            yaxis='y2'
        ))

    fig.update_layout(
        plot_bgcolor='#262730',
        paper_bgcolor='#262730',
        font_color='#e0e0e0',
        hovermode='x unified',
        height=700,
        margin=dict(l=20, r=20, t=60, b=100),
        yaxis_title='Volume (USD)',
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
            type="log" if scale_type == "Log" else "linear",
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
            type="log" if scale_type == "Log" else "linear",
            showgrid=False,
            linecolor='#FFA726',
            zeroline=False,
            color='#FFA726'
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
cols = st.columns(6)
with cols[0]:
    st.metric("Volume Power-Law Slope", f"{b_vol:.3f}")
with cols[1]:
    st.metric("Volume Model Fit (R²)", f"{r2_vol:.3f}")
with cols[2]:
    st.metric("Current Volume", f"${volume_df['Volume_USD'].iloc[-1]:,.0f}")
with cols[3]:
    st.metric("Price Power-Law Slope", f"{b_price:.3f}")
with cols[4]:
    st.metric("Price Model Fit (R²)", f"{r2_price:.3f}")
with cols[5]:
    st.metric("Current Price", f"${volume_df['Price'].iloc[-1]:.4f}")
st.markdown('</div>', unsafe_allow_html=True)
