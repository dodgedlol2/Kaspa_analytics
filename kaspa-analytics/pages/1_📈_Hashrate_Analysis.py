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

# Custom CSS for precise alignment
st.markdown("""
<style>
    .control-block {
        padding: 8px 12px;
        border-radius: 8px;
        border: 1px solid #2b3137;
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
        padding-top: 12px;
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
    .controls-container {
        padding-top: 12px;
    }
</style>
""", unsafe_allow_html=True)

# ====== ENHANCED CHART CONTAINER ======
with st.container(border=True):
    # Create columns for title and controls
    title_col, control_col = st.columns([2, 8])
    
    with title_col:
        # Title with vertical alignment
        st.markdown('<div class="title-spacing"><h2>Kaspa Hashrate</h2></div>', unsafe_allow_html=True)
    
    with control_col:
        # Controls with matching vertical alignment
        with st.container():
            cols = st.columns([1.5, 1.5, 1.5, 4])
            
            with cols[0]:
                with st.container(border=True):
                    st.markdown('<div class="control-label">Hashrate Scale</div>', unsafe_allow_html=True)
                    y_scale = st.toggle("Log / Linear", value=True, key="y_scale")
                    y_scale = "Log" if y_scale else "Linear"
            
            with cols[1]:
                with st.container(border=True):
                    st.markdown('<div class="control-label">Time Scale</div>', unsafe_allow_html=True)
                    x_scale_type = st.toggle("Log / Linear", value=False, key="x_scale")
                    x_scale_type = "Log" if x_scale_type else "Linear"
            
            with cols[2]:
                with st.container(border=True):
                    st.markdown('<div class="control-label">Deviation Bands</div>', unsafe_allow_html=True)
                    show_bands = st.toggle("Show / Hide", value=False)

    # Create figure with enhanced grid
    fig = go.Figure()

    # Determine x-axis values based on scale type
    if x_scale_type == "Log":
        x_values = df['days_from_genesis']
        x_title = "Days Since Genesis (Log Scale)"
    else:
        x_values = df['Date']
        x_title = "Date"

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

    # Power-law fit (always shown)
    x_fit = np.linspace(df['days_from_genesis'].min(), df['days_from_genesis'].max(), 100)
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
    
    # Deviation bands (only shown when toggled)
    if show_bands:
        fig.add_trace(go.Scatter(
            x=fit_x,
            y=y_fit * 0.4,
            mode='lines',
            name='-60% Deviation',
            line=dict(color='rgba(255,165,0,0.8)', dash='dot', width=1),
            hoverinfo='skip'
        ))
        fig.add_trace(go.Scatter(
            x=fit_x,
            y=y_fit * 2.2,
            mode='lines',
            name='+120% Deviation',
            line=dict(color='rgba(255,165,0,0.8)', dash='dot', width=1),
            hoverinfo='skip'
        ))

    # Enhanced layout
    fig.update_layout(
        template='plotly_dark',
        hovermode='x unified',
        height=600,
        margin=dict(l=20, r=20, t=60, b=20),
        yaxis_title='Hashrate (PH/s)',
        xaxis_title=x_title,
        xaxis=dict(
            type="log" if x_scale_type == "Log" else None,
            showgrid=True,
            gridwidth=1,
            gridcolor='rgba(100,100,100,0.2)',
            minor=dict(
                ticklen=6,
                gridcolor='rgba(100,100,100,0.1)',
                gridwidth=0.5
            )
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

    # Show the figure
    st.plotly_chart(fig, use_container_width=True)

# Stats in minimal cards
cols = st.columns(3)
with cols[0].container(border=True):
    st.metric("Power-Law Slope", f"{b:.3f}")
with cols[1].container(border=True):
    st.metric("Model Fit (R²)", f"{r2:.3f}")
with cols[2].container(border=True):
    st.metric("Current Hashrate", f"{df['Hashrate_PH'].iloc[-1]:.2f} PH/s")
