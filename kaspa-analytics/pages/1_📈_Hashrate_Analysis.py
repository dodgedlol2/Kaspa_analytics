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
    .stApp {
        background-color: #0E1117;
    }

    .st-emotion-cache-6qob1r, .sidebar-content {
        background-color: #262730 !important;
    }

    .title-spacing {
        padding-left: 40px;
        margin-bottom: 15px;
    }

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

    .metrics-container {
        width: calc(100% - 40px) !important;
        margin-left: 20px !important;
        margin-right: 20px !important;
        margin-top: 10px !important;
        margin-bottom: 0px !important;
    }

    .controls-container {
        display: flex;
        justify-content: flex-start;
        gap: 12px;
        margin-left: 40px;
        margin-bottom: 15px;
        flex-wrap: wrap;
    }

    .control-group {
        display: flex;
        flex-direction: column;
        width: 110px;
        padding: 6px;
        border: 1px solid #3A3C4A;
        border-radius: 6px;
        background-color: #1E1F25;
    }

    .control-label {
        font-size: 11px !important;
        color: #e0e0e0 !important;
        margin-bottom: 2px !important;
    }

    .stSelectbox select {
        font-size: 12px !important;
        padding: 2px 4px !important;
        background-color: #262730 !important;
        border: 1px solid #3A3C4A !important;
        color: #e0e0e0 !important;
        height: 24px !important;
    }

    .stSelectbox svg {
        color: #e0e0e0 !important;
    }
</style>
""", unsafe_allow_html=True)

# ====== MAIN CHART CONTAINER ======
with st.container():
    # Title
    st.markdown('<div class="title-spacing"><h2>Kaspa Hashrate</h2></div>', unsafe_allow_html=True)

    # Controls in horizontal layout
    st.markdown('<div class="controls-container">', unsafe_allow_html=True)

    for label, key, options, default_index in [
        ("Period", "time_range_select", ["1W", "1M", "3M", "6M", "1Y", "All"], 5),
        ("Hashrate Scale", "y_scale_select", ["Linear", "Log"], 1 if st.session_state.get("y_scale", True) else 0),
        ("Time Scale", "x_scale_select", ["Linear", "Log"], 0 if st.session_state.get("x_scale", False) else 1),
        ("Power Law Fit", "power_law_select", ["Hide", "Show"], 1 if st.session_state.get("power_law_toggle", False) else 0),
    ]:
        st.markdown('<div class="control-group">', unsafe_allow_html=True)
        st.markdown(f'<div class="control-label">{label}</div>', unsafe_allow_html=True)
        st.selectbox(label, options, index=default_index, label_visibility="collapsed", key=key)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    # Date range selection
    time_range = st.session_state["time_range_select"]
    y_scale = st.session_state["y_scale_select"]
    x_scale_type = st.session_state["x_scale_select"]
    show_power_law = st.session_state["power_law_select"]

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

    fig = go.Figure()

    max_days = filtered_df['days_from_genesis'].max() + 300
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
        x_fit = np.linspace(filtered_df['days_from_genesis'].min(), max_days, 300)
        y_fit = a * np.power(x_fit, b)
        fit_x = x_fit if x_scale_type == "Log" else [genesis_date + pd.Timedelta(days=int(d)) for d in x_fit]

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
        margin=dict(l=20, r=20, t=60, b=100),
        yaxis_title='Hashrate (PH/s)',
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
    st.metric("Power-Law Slope", f"{b:.3f}")
with cols[1]:
    st.metric("Model Fit (R²)", f"{r2:.3f}")
with cols[2]:
    st.metric("Current Hashrate", f"{df['Hashrate_PH'].iloc[-1]:.2f} PH/s")
st.markdown('</div>', unsafe_allow_html=True)
