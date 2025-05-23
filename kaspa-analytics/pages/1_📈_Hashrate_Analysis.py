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

# Custom CSS - optimized for tight vertical spacing
st.markdown("""
<style>
    .stApp { background-color: #0E1117; }
    .st-emotion-cache-6qob1r, .sidebar-content { background-color: #262730 !important; }
    
    /* Tighter title spacing */
    .title-spacing { 
        padding-left: 40px; 
        margin-bottom: 5px !important; 
        margin-top: 0px !important;
    }
    
    /* Compact container styling */
    div[data-testid="stVerticalBlock"] > div[data-testid="stVerticalBlockBorderWrapper"] {
        background-color: #262730 !important;
        border-radius: 10px !important;
        border: 1px solid #3A3C4A !important;
        padding: 10px 15px !important;
    }
    
    /* Metrics styling */
    div[data-testid="stMetric"] {
        background-color: #262730 !important;
        border: 1px solid #3A3C4A !important;
        border-radius: 8px !important;
        padding: 10px 15px !important;
        margin: 3px !important;
    }
    
    /* Tighter dividers */
    .st-emotion-cache-1dp5vir {
        border-top: 1px solid #3A3C4A !important;
        margin-top: 0px !important;
        margin-bottom: 5px !important;
    }
    
    /* Compact dropdown controls */
    .control-row {
        padding-top: 2px !important;
        padding-bottom: 2px !important;
    }
    .control-label {
        font-size: 11px !important;
        color: #e0e0e0 !important;
        margin-bottom: 1px !important;
        white-space: nowrap;
    }
    
    /* Chart area adjustments */
    .stPlotlyChart {
        margin-top: -15px !important;
    }
    
    /* Dropdown styling */
    [data-baseweb="select"] > div {
        padding: 2px 6px !important;
        min-height: 28px !important;
    }
    [role="option"] {
        padding: 6px 12px !important;
    }
    
    /* Metrics container */
    .metrics-container {
        width: calc(100% - 40px) !important;
        margin-left: 20px !important;
        margin-right: 20px !important;
        margin-top: 5px !important;
        margin-bottom: 0px !important;
    }
    
    /* Standard elements */
    h2 { 
        color: #e0e0e0 !important;
        margin-bottom: 5px !important;
    }
    .hovertext text.hovertext { fill: #e0e0e0 !important; }
    .range-slider .handle:after { background-color: #00FFCC !important; }
</style>
""", unsafe_allow_html=True)

# ====== MAIN CHART CONTAINER ======
with st.container():
    # Title with minimal spacing
    st.markdown('<div class="title-spacing"><h2>Kaspa Hashrate</h2></div>', unsafe_allow_html=True)
    
    # First divider - tight to title
    st.divider()
    
    # Dropdown container - compact row
    with st.container():
        col1, col2, col3, col4, col_spacer = st.columns([1, 1, 1, 1, 6])
        
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

        with col4:
            st.markdown('<div class="control-label">Power Law Fit</div>', unsafe_allow_html=True)
            power_law_options = ["Hide", "Show"]
            show_power_law = st.selectbox("Power Law Fit", power_law_options,
                                          index=0,
                                          label_visibility="collapsed", key="power_law_select")
    
    # Second divider - tight to dropdowns
    st.divider()

    # Date filtering
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
    else:
        start_date = df['Date'].iloc[0]

    filtered_df = df[df['Date'] >= start_date]

    # Create plot
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

    fig.add_trace(go.Scatter(
        x=x_values,
        y=filtered_df['Hashrate_PH'],
        mode='lines',
        name='Hashrate (PH/s)',
        line=dict(color='#00FFCC', width=2.5),
        hovertemplate='<b>Date</b>: %{text|%Y-%m-%d}<br><b>Hashrate</b>: %{y:.2f} PH/s<extra></extra>',
        text=filtered_df['Date']
    ))

    if show_power_law == "Show":
        x_fit = filtered_df['days_from_genesis']
        y_fit = a * np.power(x_fit, b)
        fit_x = x_fit if x_scale_type == "Log" else filtered_df['Date']

        fig.add_trace(go.Scatter(
            x=fit_x,
            y=y_fit,
            mode='lines',
            name=f'Power-Law Fit (R²={r2:.3f})',
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
        margin=dict(l=20, r=20, t=40, b=100),  # Reduced top margin
        yaxis_title='Hashrate (PH/s)',
        xaxis_title=x_title,
        xaxis=dict(
            rangeslider=dict(visible=True, thickness=0.1),
            type="log" if x_scale_type == "Log" else None,
            showgrid=True,
            gridwidth=1,
            gridcolor='rgba(255, 255, 255, 0.1)',
            tickformat=tickformat,
            linecolor='#3A3C4A',
            zerolinecolor='#3A3C4A'
        ),
        yaxis=dict(
            type="log" if y_scale == "Log" else "linear",
            showgrid=True,
            gridwidth=1,
            gridcolor='rgba(255, 255, 255, 0.1)',
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
        )
    )

    st.plotly_chart(fig, use_container_width=True)

# Stats - compact row
st.markdown('<div class="metrics-container">', unsafe_allow_html=True)
cols = st.columns(3)
with cols[0]:
    st.metric("Power-Law Slope", f"{b:.3f}")
with cols[1]:
    st.metric("Model Fit (R²)", f"{r2:.3f}")
with cols[2]:
    st.metric("Current Hashrate", f"{df['Hashrate_PH'].iloc[-1]:.2f} PH/s")
st.markdown('</div>', unsafe_allow_html=True)
