import streamlit as st
import plotly.graph_objects as go
import numpy as np
import pandas as pd
from utils import fit_power_law, load_marketcap_data
from datetime import datetime, timedelta

st.set_page_config(layout="wide")

# Data loading and processing with 0 values excluded
if 'mcap_df' not in st.session_state or 'mcap_genesis_date' not in st.session_state:
    try:
        # Load data and filter out 0 values
        mcap_df, genesis_date = load_marketcap_data()
        mcap_df = mcap_df[mcap_df['MarketCap_B'] > 0]  # Exclude 0 values
        st.session_state.mcap_df = mcap_df
        st.session_state.mcap_genesis_date = genesis_date
    except Exception as e:
        st.error(f"Failed to load market cap data: {str(e)}")
        st.stop()

mcap_df = st.session_state.mcap_df
genesis_date = st.session_state.mcap_genesis_date

try:
    a_mcap, b_mcap, r2_mcap = fit_power_law(mcap_df, y_col='MarketCap_B')
except Exception as e:
    st.error(f"Failed to calculate market cap power law: {str(e)}")
    st.stop()

# Custom CSS - same styling as other pages
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
    st.markdown('<div class="title-spacing"><h2>Kaspa Market Cap Analysis</h2></div>', unsafe_allow_html=True)
    
    # First divider - under the title
    st.divider()
    
    # Dropdown container
    col_spacer_left, col1, col2, col3, col4, spacer1, spacer2, spacer3, spacer4, spacer5, spacer6, spacer7, spacer8, spacer9 = st.columns(
        [0.35, 1, 1, 1, 1, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 3]
    )

    with col1:
        st.markdown('<div class="control-label">Market Cap Scale</div>', unsafe_allow_html=True)
        y_scale_options = ["Linear", "Log"]
        y_scale = st.selectbox("Market Cap Scale", y_scale_options,
                             index=1 if st.session_state.get("mcap_y_scale", True) else 0,
                             label_visibility="collapsed", key="mcap_y_scale_select")

    with col2:
        st.markdown('<div class="control-label">Time Scale</div>', unsafe_allow_html=True)
        x_scale_options = ["Linear", "Log"]
        x_scale_type = st.selectbox("Time Scale", x_scale_options,
                                  index=0,
                                  label_visibility="collapsed", key="mcap_x_scale_select")

    with col3:
        st.markdown('<div class="control-label">Period</div>', unsafe_allow_html=True)
        time_ranges = ["1W", "1M", "3M", "6M", "1Y", "All"]
        if 'mcap_time_range' not in st.session_state:
            st.session_state.mcap_time_range = "All"
        time_range = st.selectbox("Time Range", time_ranges,
                                index=time_ranges.index(st.session_state.mcap_time_range),
                                label_visibility="collapsed", key="mcap_time_range_select")

    with col4:
        st.markdown('<div class="control-label">Power Law Fit</div>', unsafe_allow_html=True)
        power_law_options = ["Hide", "Show"]
        show_power_law = st.selectbox("Power Law Fit", power_law_options,
                                    index=0,
                                    label_visibility="collapsed", key="mcap_power_law_select")
    
    # Second divider - under the dropdown menus
    st.divider()

    last_date = mcap_df['Date'].iloc[-1]
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
        start_date = mcap_df['Date'].iloc[0]

    filtered_df = mcap_df[mcap_df['Date'] >= start_date]

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

    # Add market cap trace
    fig.add_trace(go.Scatter(
        x=x_values,
        y=filtered_df['MarketCap_B'],
        mode='lines',
        name='Market Cap (Billions USD)',
        line=dict(color='#00FFCC', width=2.5),
        hovertemplate='<b>Date</b>: %{text|%Y-%m-%d}<br><b>Market Cap</b>: $%{y:.2f}B<extra></extra>',
        text=filtered_df['Date']
    ))

    if show_power_law == "Show":
        x_fit = filtered_df['days_from_genesis']
        y_fit = a_mcap * np.power(x_fit, b_mcap)
        fit_x = x_fit if x_scale_type == "Log" else filtered_df['Date']

        fig.add_trace(go.Scatter(
            x=fit_x,
            y=y_fit,
            mode='lines',
            name=f'Power-Law Fit (R²={r2_mcap:.3f})',
            line=dict(color='#FFA726', dash='dot', width=2)
        ))

        fig.add_trace(go.Scatter(
            x=fit_x,
            y=y_fit * 0.4,
            mode='lines',
            name='-60% Deviation',
            line=dict(color='rgba(255, 255, 255, 0.5)', dash='dot', width=1),
            hoverinfo='skip',
            fill=None
        ))
        fig.add_trace(go.Scatter(
            x=fit_x,
            y=y_fit * 2.2,
            mode='lines',
            name='+120% Deviation',
            line=dict(color='rgba(255, 255, 255, 0.5)', dash='dot', width=1),
            hoverinfo='skip',
            fill='tonexty',
            fillcolor='rgba(100, 100, 100, 0.2)'
        ))

    fig.update_layout(
        plot_bgcolor='#262730',
        paper_bgcolor='#262730',
        font_color='#e0e0e0',
        hovermode='x unified',
        height=700,
        margin=dict(l=20, r=20, t=60, b=100),
        yaxis_title='Market Cap (Billions USD)',
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
cols = st.columns(3)
with cols[0]:
    st.metric("Power-Law Slope", f"{b_mcap:.3f}")
with cols[1]:
    st.metric("Model Fit (R²)", f"{r2_mcap:.3f}")
with cols[2]:
    st.metric("Current Market Cap", f"${mcap_df['MarketCap_B'].iloc[-1]:.2f}B")
st.markdown('</div>', unsafe_allow_html=True)
