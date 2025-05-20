import streamlit as st
import plotly.graph_objects as go
import numpy as np
import pandas as pd
from utils import fit_power_law, load_data

st.set_page_config(layout="wide")
st.title("Kaspa Hashrate Analysis")

# Data loading and processing (unchanged)
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

# Controls (unchanged)
col1, col2 = st.columns(2)
with col1:
    show_fit = st.checkbox("Show Power-Law Fit", True)
    show_bands = st.checkbox("Show Deviation Bands", True)
with col2:
    y_scale = st.radio("Y-axis Scale", ["Linear", "Log"], index=1)
    x_scale = st.radio("X-axis Scale", ["Linear", "Log"], index=0)

# Create figure with enhanced grid
fig = go.Figure()

# Main trace (now with hover improvements)
fig.add_trace(go.Scatter(
    x=df['days_from_genesis'] if x_scale == "Log" else df['Date'],
    y=df['Hashrate_PH'],
    mode='lines',
    name='Hashrate (PH/s)',
    line=dict(color='#00FFCC', width=2),
    hovertemplate='<b>Date</b>: %{text|%Y-%m-%d}<br><b>Hashrate</b>: %{y:.2f} PH/s<extra></extra>',
    text=df['Date']  # Shows dates in hover even in log mode
))

# Power-law fit (unchanged)
if show_fit:
    x_fit = np.linspace(df['days_from_genesis'].min(), df['days_from_genesis'].max(), 100)
    y_fit = a * np.power(x_fit, b)
    
    fit_x = x_fit if x_scale == "Log" else [genesis_date + pd.Timedelta(days=int(d)) for d in x_fit]
    
    fig.add_trace(go.Scatter(
        x=fit_x,
        y=y_fit,
        mode='lines',
        name=f'Power-Law Fit (R²={r2:.3f})',
        line=dict(color='orange', dash='dot', width=1)
    ))
    
    if show_bands:
        fig.add_trace(go.Scatter(
            x=fit_x,
            y=y_fit * 0.4,
            mode='lines',
            name='-60% Band',
            line=dict(color='rgba(255,165,0,0.3)'),
            fill=None
        ))
        fig.add_trace(go.Scatter(
            x=fit_x,
            y=y_fit * 2.2,
            mode='lines',
            name='+120% Band',
            line=dict(color='rgba(255,165,0,0.3)'),
            fill='tonexty'
        ))

# Enhanced layout with proper grid lines
fig.update_layout(
    template='plotly_dark',
    hovermode='x unified',
    height=700,
    title="Kaspa Hashrate Growth",
    yaxis_title='Hashrate (PH/s)',
    xaxis=dict(
        title='Days Since Genesis' if x_scale == "Log" else 'Date',
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
        showgrid=True,
        gridwidth=1,
        gridcolor='rgba(100,100,100,0.2)',
        minor=dict(
            ticklen=6,
            gridcolor='rgba(100,100,100,0.1)',
            gridwidth=0.5
        )
    )
)

# Advanced log scaling configuration
if x_scale == "Log":
    fig.update_xaxes(
        type="log",
        tickmode='auto',
        nticks=10,
        minor=dict(
            ticklen=4,
            tickcolor='rgba(200,200,200,0.5)',
            tickmode='auto',
            nticks=8
        )
    )

if y_scale == "Log":
    fig.update_yaxes(
        type="log",
        tickmode='auto',
        nticks=10,
        minor=dict(
            ticklen=4,
            tickcolor='rgba(200,200,200,0.5)',
            tickmode='auto',
            nticks=8
        )
    )

# Show the figure
st.plotly_chart(fig, use_container_width=True)

# Stats (unchanged)
st.subheader("Model Statistics")
cols = st.columns(3)
cols[0].metric("Power-Law Slope", f"{b:.3f}")
cols[1].metric("Model Fit (R²)", f"{r2:.3f}")
cols[2].metric("Current Hashrate", f"{df['Hashrate_PH'].iloc[-1]:.2f} PH/s")
