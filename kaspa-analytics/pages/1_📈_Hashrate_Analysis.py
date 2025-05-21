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

# Updated CSS with deep dark grey and blue-toned accents
st.markdown("""
<style>
    .stApp {
        background-color: #1A1F2E;
    }
    [data-testid="stSidebar"] {
        background-color: #222837 !important;
    }
    [data-testid="stVerticalBlockBorderWrapper"] {
        background-color: #222837;
        border: 1px solid #2C3449;
        border-radius: 10px;
    }
    .control-block {
        padding: 8px 12px;
        border-radius: 10px;
        border: 1px solid #2C3449;
        background-color: #222837;
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
        color: #D0D8EA !important;
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
        background-color: #222837;
    }
    .plotly-rangeslider {
        height: 80px !important;
    }
    [data-testid="metric-container"] {
        background-color: #222837 !important;
        border: 1px solid #2C3449 !important;
        border-radius: 10px !important;
    }
    h1, h2, h3, h4, h5, h6, p, div, span {
        color: #D0D8EA !important;
    }
    .stSlider, .stSelectbox, .stTextInput {
        background-color: #222837 !important;
        border-color: #2C3449 !important;
    }
    .hovertext {
        background-color: #1A1F2E !important;
        border: 1px solid #2C3449 !important;
        color: #D0D8EA !important;
    }
</style>
""", unsafe_allow_html=True)

# ====== ENHANCED CHART CONTAINER ======
with st.container():
    with st.container(border=True):
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

        fig = go.Figure()
        max_days = df['days_from_genesis'].max() + 300
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

        fig.add_trace(go.Scatter(
            x=x_values,
            y=df['Hashrate_PH'],
            mode='lines',
            name='Hashrate (PH/s)',
            line=dict(color='#00BFFF', width=2),
            hovertemplate='<b>Date</b>: %{text|%Y-%m-%d}<br><b>Hashrate</b>: %{y:.2f} PH/s<extra></extra>',
            text=df['Date']
        ))

        x_fit = np.linspace(df['days_from_genesis'].min(), max_days, 300)
        y_fit = a * np.power(x_fit, b)
        fit_x = x_fit if x_scale_type == "Log" else [genesis_date + pd.Timedelta(days=int(d)) for d in x_fit]

        fig.add_trace(go.Scatter(
            x=fit_x,
            y=y_fit,
            mode='lines',
            name=f'Power-Law Fit (R²={r2:.3f})',
            line=dict(color='orange', dash='dot', width=1.5)
        ))

        if show_bands:
            fig.add_trace(go.Scatter(
                x=fit_x,
                y=y_fit * 0.4,
                mode='lines',
                name='-60% Deviation',
                line=dict(color='rgba(150, 180, 220, 0.8)', dash='dot', width=1),
                hoverinfo='skip',
                fill=None
            ))
            fig.add_trace(go.Scatter(
                x=fit_x,
                y=y_fit * 2.2,
                mode='lines',
                name='+120% Deviation',
                line=dict(color='rgba(150, 180, 220, 0.8)', dash='dot', width=1),
                hoverinfo='skip',
                fill='tonexty',
                fillcolor='rgba(100, 150, 255, 0.15)'
            ))

        fig.update_layout(
            plot_bgcolor='#222837',
            paper_bgcolor='#222837',
            font_color='#D0D8EA',
            hovermode='x unified',
            height=700,
            margin=dict(l=20, r=20, t=60, b=100),
            yaxis_title='Hashrate (PH/s)',
            xaxis_title=x_title,
            xaxis=dict(
                rangeslider=dict(
                    visible=True,
                    thickness=0.1,
                    bgcolor='rgba(0,191,255,0.2)',
                    bordercolor="#00BFFF",
                    borderwidth=1
                ),
                type="log" if x_scale_type == "Log" else None,
                showgrid=True,
                gridwidth=1,
                gridcolor='rgba(120,120,160,0.3)',
                minor=dict(
                    ticklen=6,
                    gridcolor='rgba(120,120,160,0.15)',
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
                gridcolor='rgba(120,120,160,0.3)',
                minor=dict(
                    ticklen=6,
                    gridcolor='rgba(120,120,160,0.15)',
                    gridwidth=0.5
                )
            ),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1,
                bgcolor='rgba(26, 31, 46, 0.8)'
            )
        )

        st.plotly_chart(fig, use_container_width=True)

st.markdown("<div style='margin-top: 30px;'></div>", unsafe_allow_html=True)
cols = st.columns(3)
with cols[0].container(border=True):
    st.metric("Power-Law Slope", f"{b:.3f}")
with cols[1].container(border=True):
    st.metric("Model Fit (R²)", f"{r2:.3f}")
with cols[2].container(border=True):
    st.metric("Current Hashrate", f"{df['Hashrate_PH'].iloc[-1]:.2f} PH/s")
