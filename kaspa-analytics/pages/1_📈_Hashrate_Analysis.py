import streamlit as st
import plotly.graph_objects as go
import numpy as np
import pandas as pd  # Added missing import
from utils import fit_power_law, load_data  # Added load_data import

st.set_page_config(layout="wide")  # Ensures consistency

st.title("Kaspa Hashrate Analysis")

# Initialize or load data
if 'df' not in st.session_state or 'genesis_date' not in st.session_state:
    try:
        st.session_state.df, st.session_state.genesis_date = load_data()
    except Exception as e:
        st.error(f"Failed to load data: {str(e)}")
        st.stop()

# Get data from session state
df = st.session_state.df
genesis_date = st.session_state.genesis_date

# Fit power law
try:
    a, b, r2 = fit_power_law(df)
except Exception as e:
    st.error(f"Failed to calculate power law: {str(e)}")
    st.stop()

# Controls
col1, col2 = st.columns(2)
with col1:
    show_fit = st.checkbox("Show Power-Law Fit", True)
    show_bands = st.checkbox("Show Deviation Bands", True)
    
with col2:
    y_scale = st.radio("Y-axis Scale", ["Linear", "Log"], index=1)
    x_scale = st.radio("X-axis Scale", ["Linear", "Log"], index=0)

# Create figure
fig = go.Figure()

# Main trace
fig.add_trace(go.Scatter(
    x=df['Date'],
    y=df['Hashrate_PH'],
    mode='lines',
    name='Hashrate (PH/s)',
    line=dict(color='#00FFCC', width=2)
))

# Power-law fit
if show_fit:
    try:
        x_fit = np.linspace(df['days_from_genesis'].min(), df['days_from_genesis'].max(), 100)
        y_fit = a * np.power(x_fit, b)
        
        fig.add_trace(go.Scatter(
            x=[genesis_date + pd.Timedelta(days=int(d)) for d in x_fit],
            y=y_fit,
            mode='lines',
            name=f'Power-Law Fit (R²={r2:.3f})',
            line=dict(color='orange', dash='dot', width=1)
        ))
        
        if show_bands:
            fig.add_trace(go.Scatter(
                x=[genesis_date + pd.Timedelta(days=int(d)) for d in x_fit],
                y=y_fit * 0.4,
                mode='lines',
                name='-60% Band',
                line=dict(color='rgba(255,165,0,0.3)'),
                fill=None
            ))
            
            fig.add_trace(go.Scatter(
                x=[genesis_date + pd.Timedelta(days=int(d)) for d in x_fit],
                y=y_fit * 2.2,
                mode='lines',
                name='+120% Band',
                line=dict(color='rgba(255,165,0,0.3)'),
                fill='tonexty'
            ))
    except Exception as e:
        st.warning(f"Couldn't display power law fit: {str(e)}")

# Update layout
fig.update_layout(
    template='plotly_dark',
    hovermode='x unified',
    height=700,
    title="Kaspa Hashrate Growth",
    xaxis_title='Date',
    yaxis_title='Hashrate (PH/s)'
)

# Apply scale selections
if y_scale == "Log":
    fig.update_yaxes(type="log")
if x_scale == "Log":
    fig.update_xaxes(type="log")

# Show the figure
st.plotly_chart(fig, use_container_width=True)

# Show stats
st.subheader("Model Statistics")
col1, col2, col3 = st.columns(3)
col1.metric("Power-Law Slope", f"{b:.3f}")
col2.metric("Model Fit (R²)", f"{r2:.3f}")
col3.metric("Current Hashrate", f"{df['Hashrate_PH'].iloc[-1]:.2f} PH/s")
