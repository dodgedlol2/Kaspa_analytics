import streamlit as st
import plotly.graph_objects as go
import numpy as np
import pandas as pd
from utils import fit_power_law, load_data
from datetime import datetime, timedelta

st.set_page_config(layout="wide")

# Data loading and processing
if 'df' not in st.session_state or 'genesis_date' not in st.session_state:
    try:
        st.session_state.df, st.session_state.genesis_date = load_data()
    except Exception as e:
        st.error(f"Failed to load data: {str(e)}")
        st.stop()

df = st.session_state.df
genesis_date = st.session_state.genesis_date

try:
    a, b, r2 = fit_power_law(df)
except Exception as e:
    st.error(f"Failed to calculate power law: {str(e)}")
    st.stop()

# Custom CSS for unified styling
st.markdown("""
<style>
    /* Main background color */
    .stApp {
        background-color: #0E1117;
    }
    
    /* Correct sidebar grey color */
    .st-emotion-cache-6qob1r, .sidebar-content {
        background-color: #262730 !important;
    }
    
    /* Control block styling */
    .control-block {
        padding: 8px 12px;
        border-radius: 8px;
        border: 1px solid #3A3C4A;
        background-color: #262730;
        margin-right: 15px;
        min-width: 160px;
        height: 85px;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    
    .title-spacing {
        padding-left: 40px;
        margin-bottom: 15px;
    }
    
    .control-label {
        font-size: 13px !important;
        margin-bottom: 6px !important;
        white-space: nowrap;
        font-weight: 500;
        color: #e0e0e0 !important;
    }
    
    .stToggle {
        width: 100%;
    }
    
    .stToggle button {
        width: 100% !important;
        font-size: 12px !important;
    }
    
    .controls-wrapper {
        padding-top: 11px;
    }
    
    .main-container {
        padding: 25px;
    }
    
    .plotly-rangeslider {
        height: 80px !important;
    }
    
    /* Main chart container styling */
    div[data-testid="stVerticalBlock"] > div[data-testid="stVerticalBlockBorderWrapper"] {
        background-color: #262730 !important;
        border-radius: 10px !important;
        border: 1px solid #3A3C4A !important;
        padding: 15px !important;
    }
    
    /* Metric cards styling */
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
    
    .stMetric {
        margin: 5px !important;
        height: 100% !important;
    }
    
    /* Title styling */
    h2 {
        color: #e0e0e0 !important;
    }
    
    /* Toggle button styling */
    .st-bd {
        background-color: #262730 !important;
    }
    
    .st-cg {
        background-color: #00FFCC !important;
    }
    
    /* Plotly tooltip styling */
    .hovertext text.hovertext {
        fill: #e0e0e0 !important;
    }
    
    /* Range slider handle color */
    .range-slider .handle:after {
        background-color: #00FFCC !important;
    }
    
    /* Metrics container styling */
    .metrics-container {
        width: calc(100% - 40px) !important;
        margin-left: 20px !important;
        margin-right: 20px !important;
        margin-top: 10px !important;
        margin-bottom: 0px !important;
    }
    
    /* Time range selector styling */
    .time-range-selector {
        position: absolute;
        right: 30px;
        top: 20px;
        z-index: 100;
        background-color: #262730 !important;
        border-radius: 8px !important;
        padding: 4px !important;
        border: 1px solid #3A3C4A !important;
    }
    
    .time-range-button {
        width: 100% !important;
        font-size: 12px !important;
        padding: 6px 12px !important;
        border-radius: 6px !important;
        transition: all 0.2s ease !important;
        background-color: #262730 !important;
        color: #e0e0e0 !important;
        border: 1px solid #3A3C4A !important;
        margin: 0 !important;
    }
    
    .time-range-button:hover {
        background-color: #3A3C4A !important;
        color: #00FFCC !important;
    }
    
    .time-range-button:active,
    .time-range-button:focus {
        background-color: #00FFCC !important;
        color: #262730 !important;
        border-color: #00FFCC !important;
    }
    
    .time-range-button.active {
        background-color: #00FFCC !important;
        color: #262730 !important;
        border-color: #00FFCC !important;
        font-weight: 500 !important;
    }
    
    div[data-testid="stHorizontalBlock"] {
        gap: 0.25rem !important;
    }
</style>
""", unsafe_allow_html=True)

# ====== MAIN CHART CONTAINER ======
with st.container():
    # Create columns for title and controls
    title_col, control_col = st.columns([2, 8])

    with title_col:
        st.markdown('<div class="title-spacing"><h2>Kaspa Hashrate</h2></div>', unsafe_allow_html=True)

    with control_col:
        st.markdown('<div class="controls-wrapper">', unsafe_allow_html=True)
        cols = st.columns([1.5, 1.5, 1.5, 4])

        with cols[0]:
            with st.container():
                st.markdown('<div class="control-label">Hashrate Scale</div>', unsafe_allow_html=True)
                y_scale = st.toggle("Linear/Log", value=True, key="y_scale")
                y_scale = "Log" if y_scale else "Linear"

        with cols[1]:
            with st.container():
                st.markdown('<div class="control-label">Time Scale</div>', unsafe_allow_html=True)
                x_scale_type = st.toggle("Linear/Log", value=False, key="x_scale")
                x_scale_type = "Log" if x_scale_type else "Linear"

        with cols[2]:
            with st.container():
                st.markdown('<div class="control-label">Deviation Bands</div>', unsafe_allow_html=True)
                show_bands = st.toggle("Hide/Show", value=False, key="bands_toggle")

        st.markdown('</div>', unsafe_allow_html=True)

    # Add professional time range selector in the top right
    with st.container():
        st.markdown('<div class="time-range-selector">', unsafe_allow_html=True)
        
        time_ranges = ["1W", "1M", "3M", "6M", "1Y", "All"]
        cols = st.columns(len(time_ranges))
        
        # Initialize time_range in session state if not exists
        if 'time_range' not in st.session_state:
            st.session_state.time_range = "All"
        
        for i, tr in enumerate(time_ranges):
            with cols[i]:
                # Use a button for each time range
                if st.button(
                    tr,
                    key=f"time_range_{tr}",
                    type="primary" if st.session_state.time_range == tr else "secondary"
                ):
                    st.session_state.time_range = tr
        
        st.markdown('</div>', unsafe_allow_html=True)

    # Get the selected time range
    time_range = st.session_state.time_range

    # Calculate date range based on selection
    last_date = df['Date'].iloc[-1]
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
    else:  # All
        start_date = df['Date'].iloc[0]

    # Filter data based on selected time range
    filtered_df = df[df['Date'] >= start_date]

    # Create figure with unified color scheme
    fig = go.Figure()

    # Determine x-axis values based on scale type
    max_days = filtered_df['days_from_genesis'].max() + 300  # Extend by 300 days
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

    # Main trace with updated colors
    fig.add_trace(go.Scatter(
        x=x_values,
        y=filtered_df['Hashrate_PH'],
        mode='lines',
        name='Hashrate (PH/s)',
        line=dict(color='#00FFCC', width=2.5),
        hovertemplate='<b>Date</b>: %{text|%Y-%m-%d}<br><b>Hashrate</b>: %{y:.2f} PH/s<extra></extra>',
        text=filtered_df['Date']
    ))

    # Power-law fit extended 300 days into future
    x_fit = np.linspace(filtered_df['days_from_genesis'].min(), max_days, 300)
    y_fit = a * np.power(x_fit, b)

    if x_scale_type == "Log":
        fit_x = x_fit
    else:
        fit_x = [genesis_date + pd.Timedelta(days=int(d)) for d in x_fit]

    fig.add_trace(go.Scatter(
        x=fit_x,
        y=y_fit,
        mode='lines',
        name=f'Power-Law Fit (R²={r2:.3f})',
        line=dict(color='#FFA726', dash='dot', width=2)
    ))

    # Deviation bands (extended 300 days into future)
    if show_bands:
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

    # Enhanced layout with matching background
    fig.update_layout(
        plot_bgcolor='#262730',  # Correct sidebar grey
        paper_bgcolor='#262730',  # Correct sidebar grey
        font_color='#e0e0e0',
        hovermode='x unified',
        height=700,
        margin=dict(l=20, r=20, t=60, b=100),
        yaxis_title='Hashrate (PH/s)',
        xaxis_title=x_title,
        xaxis=dict(
            rangeslider=dict(
                visible=True,
                thickness=0.1,
                bgcolor='#262730',  # Correct sidebar grey
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
            range=[None, max_days] if x_scale_type == "Log" else 
                  [filtered_df['Date'].min(), genesis_date + pd.Timedelta(days=max_days)],
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
            bgcolor='rgba(38, 39, 48, 0.8)'  # Semi-transparent sidebar grey
        ),
        hoverlabel=dict(
            bgcolor='#262730',  # Correct sidebar grey
            bordercolor='#3A3C4A',
            font_color='#e0e0e0'
        )
    )

    st.plotly_chart(fig, use_container_width=True)

# Stats in cards with matching styling - now aligned with main panel
st.markdown('<div class="metrics-container">', unsafe_allow_html=True)
cols = st.columns(3)
with cols[0]:
    st.metric("Power-Law Slope", f"{b:.3f}")
with cols[1]:
    st.metric("Model Fit (R²)", f"{r2:.3f}")
with cols[2]:
    st.metric("Current Hashrate", f"{df['Hashrate_PH'].iloc[-1]:.2f} PH/s")
st.markdown('</div>', unsafe_allow_html=True)
