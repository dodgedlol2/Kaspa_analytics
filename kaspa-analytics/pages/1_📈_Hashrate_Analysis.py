import streamlit as st
import plotly.graph_objects as go
import numpy as np
import pandas as pd
from utils import fit_power_law, load_data
from streamlit_plotly_events import plotly_events

st.set_page_config(layout="wide")

# Load data and compute model
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

# UI controls
y_scale = st.toggle("Log Y-scale", value=True)
x_scale = st.toggle("Log X-scale", value=False)
show_bands = st.toggle("Show Deviation Bands", value=False)

y_scale_type = "log" if y_scale else "linear"
x_scale_type = "log" if x_scale else "linear"

# Generate power-law fit
max_days = df['days_from_genesis'].max() + 300
x_fit = np.linspace(df['days_from_genesis'].min(), max_days, 300)
y_fit = a * np.power(x_fit, b)
fit_x = x_fit if x_scale_type == "log" else [genesis_date + pd.Timedelta(days=int(d)) for d in x_fit]

# Chart
fig = go.Figure()

# Main hashrate trace
fig.add_trace(go.Scatter(
    x=df['days_from_genesis'] if x_scale_type == "log" else df['Date'],
    y=df['Hashrate_PH'],
    mode='lines',
    name='Hashrate (PH/s)',
    line=dict(color='#00FFCC', width=2.5),
    text=df['Date'],
    hovertemplate='<b>Date</b>: %{text|%Y-%m-%d}<br><b>Hashrate</b>: %{y:.2f} PH/s<extra></extra>'
))

# Power-law fit trace
fig.add_trace(go.Scatter(
    x=fit_x,
    y=y_fit,
    mode='lines',
    name=f'Power-Law Fit (R²={r2:.3f})',
    line=dict(color='#FFA726', dash='dot', width=2)
))

# Deviation bands
if show_bands:
    fig.add_trace(go.Scatter(
        x=fit_x,
        y=y_fit * 0.4,
        mode='lines',
        name='-60% Deviation',
        line=dict(color='rgba(255,255,255,0.5)', dash='dot'),
        hoverinfo='skip'
    ))
    fig.add_trace(go.Scatter(
        x=fit_x,
        y=y_fit * 2.2,
        mode='lines',
        name='+120% Deviation',
        line=dict(color='rgba(255,255,255,0.5)', dash='dot'),
        fill='tonexty',
        fillcolor='rgba(100, 100, 100, 0.2)',
        hoverinfo='skip'
    ))

# Initial layout
fig.update_layout(
    height=700,
    margin=dict(l=10, r=10, t=40, b=40),
    paper_bgcolor='#1a1e25',
    plot_bgcolor='#1a1e25',
    font_color='#e0e0e0',
    hovermode='x unified',
    xaxis=dict(
        title='Days Since Genesis' if x_scale_type == "log" else 'Date',
        type=x_scale_type,
        linecolor='#2b3137',
        zerolinecolor='#2b3137',
    ),
    yaxis=dict(
        title='Hashrate (PH/s)',
        type=y_scale_type,
        linecolor='#2b3137',
        zerolinecolor='#2b3137',
        autorange=True  # Important for auto Y-scaling!
    ),
    legend=dict(
        orientation='h',
        yanchor='bottom',
        y=1.02,
        xanchor='right',
        x=1
    )
)

# Plot and capture zoom events
selected_points = plotly_events(fig, override_height=700, key="chart")

# Metrics below chart
st.markdown("### Model Metrics")
c1, c2, c3 = st.columns(3)
c1.metric("Power-Law Slope", f"{b:.3f}")
c2.metric("Model Fit (R²)", f"{r2:.3f}")
c3.metric("Current Hashrate", f"{df['Hashrate_PH'].iloc[-1]:.2f} PH/s")
