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

# ====== CHART CONTAINER WITH INTEGRATED CONTROLS ======
with st.container(border=True):
    # Header row with title and integrated controls
    header_cols = st.columns([3, 1, 1, 1])
    with header_cols[0]:
        st.markdown("### Kaspa Hashrate Analysis", help="Network hashrate growth over time")
    
    # Integrated controls in the header
    with header_cols[1]:
        show_fit = st.toggle("Fit", value=True, 
                           help="Show power-law regression", 
                           label_visibility="collapsed")
        show_bands = st.toggle("Bands", value=True,
                             help="Show deviation bands", 
                             label_visibility="collapsed")
    
    with header_cols[2]:
        y_scale = st.radio("Hashrate scale:", ["Linear", "Log"], 
                          index=1, horizontal=True,
                          label_visibility="collapsed")
    
    with header_cols[3]:
        x_scale = st.radio("Time scale:", ["Date", "Days"], 
                          index=0, horizontal=True,
                          label_visibility="collapsed")

    # Create figure with enhanced grid
    fig = go.Figure()

    # Main trace
    fig.add_trace(go.Scatter(
        x=df['days_from_genesis'] if x_scale == "Days" else df['Date'],
        y=df['Hashrate_PH'],
        mode='lines',
        name='Hashrate (PH/s)',
        line=dict(color='#00FFCC', width=2),
        hovertemplate='<b>Date</b>: %{text|%Y-%m-%d}<br><b>Hashrate</b>: %{y:.2f} PH/s<extra></extra>',
        text=df['Date']
    ))

    # Power-law fit
    if show_fit:
        x_fit = np.linspace(df['days_from_genesis'].min(), df['days_from_genesis'].max(), 100)
        y_fit = a * np.power(x_fit, b)
        
        fit_x = x_fit if x_scale == "Days" else [genesis_date + pd.Timedelta(days=int(d)) for d in x_fit]
        
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

    # Enhanced layout
    fig.update_layout(
        template='plotly_dark',
        hovermode='x unified',
        height=600,
        margin=dict(l=20, r=20, t=60, b=20),
        yaxis_title='Hashrate (PH/s)',
        xaxis_title=x_scale,
        xaxis=dict(
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
