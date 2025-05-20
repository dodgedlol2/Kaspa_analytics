import streamlit as st
import plotly.graph_objects as go
import numpy as np
import pandas as pd
from utils import fit_power_law, load_data

st.set_page_config(layout="wide")

# Custom CSS for professional styling
st.markdown("""
<style>
    .chart-wrapper {
        position: relative;
    }
    .scale-controls {
        position: absolute;
        z-index: 100;
        background: rgba(30, 30, 30, 0.7);
        border-radius: 4px;
        padding: 4px;
        display: flex;
        gap: 4px;
    }
    .y-scale-controls {
        top: 10px;
        left: 10px;
    }
    .x-scale-controls {
        bottom: 10px;
        right: 10px;
    }
    .scale-btn {
        border: 1px solid #636e72 !important;
        border-radius: 4px !important;
        padding: 0.15rem 0.5rem !important;
        font-size: 0.8rem !important;
        background-color: transparent !important;
        color: white !important;
        min-width: 24px !important;
        height: 24px !important;
        margin: 0 !important;
        cursor: pointer;
    }
    .scale-btn:hover {
        background-color: rgba(45, 52, 54, 0.9) !important;
        border-color: #00FFCC !important;
    }
    .scale-btn.active {
        background-color: rgba(0, 255, 204, 0.2) !important;
        border-color: #00FFCC !important;
    }
    .scale-btn-tooltip {
        visibility: hidden;
        width: 120px;
        background-color: #2d3436;
        color: #fff;
        text-align: center;
        border-radius: 4px;
        padding: 4px;
        position: absolute;
        z-index: 1;
        bottom: 125%;
        left: 50%;
        transform: translateX(-50%);
        opacity: 0;
        transition: opacity 0.3s;
        font-size: 12px;
    }
    .scale-btn-container {
        position: relative;
        display: inline-block;
    }
    .scale-btn-container:hover .scale-btn-tooltip {
        visibility: visible;
        opacity: 1;
    }
</style>
""", unsafe_allow_html=True)

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

# Initialize session state for scale toggles
if 'y_scale' not in st.session_state:
    st.session_state.y_scale = "log"
if 'x_scale' not in st.session_state:
    st.session_state.x_scale = "linear"
if 'show_bands' not in st.session_state:
    st.session_state.show_bands = False

# Create columns for the scale toggles
col1, col2 = st.columns(2)
with col1:
    y_scale = st.radio(
        "Y-axis scale:",
        ["Linear", "Log"],
        index=1 if st.session_state.y_scale == "log" else 0,
        key="y_scale_radio",
        horizontal=True,
        label_visibility="collapsed"
    )
    st.session_state.y_scale = y_scale.lower()

with col2:
    x_scale = st.radio(
        "X-axis scale:",
        ["Linear", "Log"],
        index=1 if st.session_state.x_scale == "log" else 0,
        key="x_scale_radio",
        horizontal=True,
        label_visibility="collapsed"
    )
    st.session_state.x_scale = x_scale.lower()

# ====== PROFESSIONAL CHART CONTAINER ======
with st.container(border=True):
    st.markdown("### Kaspa Hashrate")
    
    # Create figure with enhanced grid
    fig = go.Figure()

    # Determine x-axis values based on scale type
    if st.session_state.x_scale == "log":
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
        line=dict(color='#00FFCC', width=2.5),
        hovertemplate='<b>Date</b>: %{text|%Y-%m-%d}<br><b>Hashrate</b>: %{y:.2f} PH/s<extra></extra>',
        text=df['Date']
    ))

    # Power-law fit (always shown)
    x_fit = np.linspace(df['days_from_genesis'].min(), df['days_from_genesis'].max(), 100)
    y_fit = a * np.power(x_fit, b)
    
    if st.session_state.x_scale == "log":
        fit_x = x_fit
    else:
        fit_x = [genesis_date + pd.Timedelta(days=int(d)) for d in x_fit]
    
    fig.add_trace(go.Scatter(
        x=fit_x,
        y=y_fit,
        mode='lines',
        name=f'Power-Law Fit (R²={r2:.3f})',
        line=dict(color='orange', dash='dot', width=1.8)
    ))
    
    # Deviation bands (only shown when toggled)
    if st.session_state.show_bands:
        fig.add_trace(go.Scatter(
            x=fit_x,
            y=y_fit * 0.4,
            mode='lines',
            name='-60%',
            line=dict(color='rgba(255,165,0,0.8)', dash='dot', width=1.2),
            hoverinfo='skip'
        ))
        fig.add_trace(go.Scatter(
            x=fit_x,
            y=y_fit * 2.2,
            mode='lines',
            name='+120%',
            line=dict(color='rgba(255,165,0,0.8)', dash='dot', width=1.2),
            hoverinfo='skip'
        ))

    # Enhanced layout
    fig.update_layout(
        template='plotly_dark',
        hovermode='x unified',
        height=600,
        margin=dict(l=20, r=20, t=40, b=40),
        yaxis_title='PH/s',
        xaxis_title=x_title,
        xaxis=dict(
            type=st.session_state.x_scale if st.session_state.x_scale == "log" else "date",
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
            type=st.session_state.y_scale,
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
            x=1,
            font=dict(size=10)
        )
    )

    # Display the chart
    st.plotly_chart(fig, use_container_width=True)

    # Floating buttons (visual only - functionality handled by the radio buttons)
    st.markdown(f"""
    <div class="chart-wrapper">
        <div class="scale-controls y-scale-controls">
            <div class="scale-btn-container">
                <button class="scale-btn {'active' if st.session_state.y_scale == 'linear' else ''}">A</button>
                <span class="scale-btn-tooltip">Autoscale/Linear</span>
            </div>
            <div class="scale-btn-container">
                <button class="scale-btn {'active' if st.session_state.y_scale == 'log' else ''}">L</button>
                <span class="scale-btn-tooltip">Logarithmic Scale</span>
            </div>
        </div>
        <div class="scale-controls x-scale-controls">
            <div class="scale-btn-container">
                <button class="scale-btn {'active' if st.session_state.x_scale == 'linear' else ''}">A</button>
                <span class="scale-btn-tooltip">Autoscale/Linear</span>
            </div>
            <div class="scale-btn-container">
                <button class="scale-btn {'active' if st.session_state.x_scale == 'log' else ''}">L</button>
                <span class="scale-btn-tooltip">Logarithmic Scale</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Stats in minimal cards
cols = st.columns(3)
with cols[0].container(border=True):
    st.metric("Power-Law Slope", f"{b:.3f}")
with cols[1].container(border=True):
    st.metric("Model Fit (R²)", f"{r2:.3f}")
with cols[2].container(border=True):
    st.metric("Current Hashrate", f"{df['Hashrate_PH'].iloc[-1]:.2f} PH/s")
