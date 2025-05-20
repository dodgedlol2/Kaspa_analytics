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

# ====== ENHANCED CHART CONTAINER ======
with st.container(border=True):
    # Create columns for title and controls
    title_col, control_col = st.columns([3, 7])
    
    with title_col:
        # Smaller title
        st.markdown("## Kaspa Hashrate", help="Kaspa network hashrate over time")
    
    with control_col:
        # Compact controls in columns
        c1, c2, c3, _ = st.columns([1, 1, 2, 4])
        
        with c1:
            st.markdown("**Hashrate-scale**", help="Toggle between logarithmic and linear scale for hashrate")
            y_scale = st.toggle("L", value=True, key="y_scale", 
                              help="Logarithmic (L) or Linear (A) Y-axis scale",
                              label_visibility="collapsed")
            y_scale = "Log" if y_scale else "Linear"
        
        with c2:
            st.markdown("**Time-scale**", help="Toggle between logarithmic and linear scale for time")
            x_scale_type = st.toggle("L", value=False, key="x_scale", 
                                    help="Logarithmic (L) or Linear (A) X-axis scale",
                                    label_visibility="collapsed")
            x_scale_type = "Log" if x_scale_type else "Linear"
        
        with c3:
            st.markdown("**Deviations**", help="Show/hide deviation bands around the fit")
            show_bands = st.toggle("", value=False,
                                  help="Show ± deviation bands around the fit",
                                  label_visibility="collapsed")

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
