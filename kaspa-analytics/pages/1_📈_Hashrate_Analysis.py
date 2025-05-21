import streamlit as st
import plotly.graph_objects as go
import numpy as np
import pandas as pd
from utils import fit_power_law, load_data

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

# Custom CSS for enhanced spacing
st.markdown("""
<style>
    .control-block {
        padding: 8px 12px;
        border-radius: 8px;
        border: 1px solid #2b3137;
        background-color: #2b2117;
        background-color: #0e1117;
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

    /* ===== METRIC CARD ENHANCEMENTS ===== */
    div[data-testid="stMetric"] {
        background-color: #1a1e25 !important;
        border: 1px solid #2b3137 !important;
        border-radius: 8px !important;
        padding: 15px 20px !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1) !important;
    }
    
    /* Metric value styling */
    div[data-testid="stMetricValue"] > div {
        font-size: 24px !important;
        font-weight: 600 !important;
        color: #00FFCC !important;
    }
    
    /* Metric label styling */
    div[data-testid="stMetricLabel"] > div {
        font-size: 14px !important;
        opacity: 0.8 !important;
        color: #e0e0e0 !important;
    }
    
    /* Hover effect for cards */
    div[data-testid="stMetric"]:hover {
        background-color: #1e222a !important;
        transition: background-color 0.2s ease;
    }
    
    /* Container spacing */
    .stMetric {
        margin: 5px !important;
        height: 100% !important;
    }
    
    /* Responsive adjustments */
    @media (max-width: 768px) {
        div[data-testid="stMetric"] {
            padding: 12px 15px !important;
        }
        div[data-testid="stMetricValue"] > div {
            font-size: 20px !important;
        }
    }
</style>
""", unsafe_allow_html=True)

# ====== ENHANCED CHART CONTAINER ======
with st.container():
    with st.container(border=True):
        # Create columns for title and controls
        title_col, control_col = st.columns([2, 8])

        with title_col:
            st.markdown('<div class="title-spacing"><h2>Kaspa Hashrate</h2></div>', unsafe_allow_html=True)

        with control_col:
            st.markdown('<div class="controls-wrapper">', unsafe_allow_html=True)
            cols = st.columns([1.5, 1.5, 1.5, 4])

            with cols[0]:
                with st.container(border=True):
                    st.markdown('<div class="control-label">Hashrate Scale</div>', unsafe_allow_html=True)
                    y_scale = st.toggle("Linear/Log", value=True, key="y_scale")
                    y_scale = "Log" if y_scale else "Linear"

            with cols[1]:
                with st.container(border=True):
                    st.markdown('<div class="control-label">Time Scale</div>', unsafe_allow_html=True)
                    x_scale_type = st.toggle("Linear/Log", value=False, key="x_scale")
                    x_scale_type = "Log" if x_scale_type else "Linear"

            with cols[2]:
                with st.container(border=True):
                    st.markdown('<div class="control-label">Deviation Bands</div>', unsafe_allow_html=True)
                    show_bands = st.toggle("Hide/Show", value=False, key="bands_toggle")

            st.markdown('</div>', unsafe_allow_html=True)

        # Create figure with enhanced grid
        fig = go.Figure()

        # Determine x-axis values based on scale type
        max_days = df['days_from_genesis'].max() + 300  # Extend by 300 days
        if x_scale_type == "Log":
            x_values = df['days_from_genesis']
            x_title = "Days Since Genesis (Log Scale)"
            tickformat = None
            hoverformat = None
        else:
            x_values = df['Date']
            x_title = "Date"
            tickformat = "%b %Y"
            hoverformat = "%b %d, %Y"

        # Main trace
        fig.add_trace(go.Scatter(
            x=x_values,
            y=df['Hashrate_PH'],
            mode='lines',
            name='Hashrate (PH/s)',
            line=dict(color='#00FFCC', width=2),
            hovertemplate='<b>Date</b>: %{text|%Y-%m-%d}<br><b>Hashrate</b>: %{y:.2f} PH/s<extra></extra>',
            text=df['Date']
        ))

        # Power-law fit extended 300 days into future (single continuous line)
        x_fit = np.linspace(df['days_from_genesis'].min(), max_days, 300)
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
            line=dict(color='orange', dash='dot', width=1.5)
        ))

        # Deviation bands (extended 300 days into future)
        if show_bands:
            fig.add_trace(go.Scatter(
                x=fit_x,
                y=y_fit * 0.4,
                mode='lines',
                name='-60% Deviation',
                line=dict(color='rgba(150, 150, 150, 0.8)', dash='dot', width=1),
                hoverinfo='skip',
                fill=None
            ))
            fig.add_trace(go.Scatter(
                x=fit_x,
                y=y_fit * 2.2,
                mode='lines',
                name='+120% Deviation',
                line=dict(color='rgba(150, 150, 150, 0.8)', dash='dot', width=1),
                hoverinfo='skip',
                fill='tonexty',
                fillcolor='rgba(100, 100, 100, 0.1)'
            ))

        # Enhanced layout with custom slider color
        fig.update_layout(
            template='plotly_dark',
            hovermode='x unified',
            height=700,
            margin=dict(l=20, r=20, t=60, b=100),
            yaxis_title='Hashrate (PH/s)',
            xaxis_title=x_title,
            xaxis=dict(
                rangeslider=dict(
                    visible=True,
                    thickness=0.1,
                    bgcolor='#0e1117',  # Match the main line color
                    bordercolor="#2b3137",
                    borderwidth=1
                ),
                type="log" if x_scale_type == "Log" else None,
                showgrid=True,
                gridwidth=1,
                gridcolor='rgba(100,100,100,0.2)',
                minor=dict(
                    ticklen=6,
                    gridcolor='rgba(100,100,100,0.1)',
                    gridwidth=0.5
                ),
                tickformat=tickformat,
                range=[None, max_days] if x_scale_type == "Log" else 
                      [df['Date'].min(), genesis_date + pd.Timedelta(days=max_days)]
            ),
            yaxis=dict(
                type="log" if y_scale == "Log" else "linear",
                showgrid=True,
                gridwidth=1,
                gridcolor='rgba(100,100,100,0.2)',
                minor=dict(
                    ticklen=6,
                    gridcolor='rgba(100,100,100,0.1)',
                    gridwidth=0.5
                )
            ),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            )
        )

        # Show the figure with more vertical space
        st.plotly_chart(fig, use_container_width=True)

# Stats in minimal cards with more spacing
st.markdown("<div style='margin-top: 30px;'></div>", unsafe_allow_html=True)
cols = st.columns(3)
with cols[0].container(border=True):
    st.metric("Power-Law Slope", f"{b:.3f}")
with cols[1].container(border=True):
    st.metric("Model Fit (R²)", f"{r2:.3f}")
with cols[2].container(border=True):
    st.metric("Current Hashrate", f"{df['Hashrate_PH'].iloc[-1]:.2f} PH/s")
