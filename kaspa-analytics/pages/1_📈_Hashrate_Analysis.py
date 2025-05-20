import streamlit as st
import plotly.graph_objects as go
import numpy as np
import pandas as pd
from utils import fit_power_law, load_data

st.set_page_config(layout="wide")

# Custom CSS to position the buttons
st.markdown("""
<style>
    .scale-button {
        position: absolute;
        z-index: 1000;
        font-size: 12px !important;
        padding: 0.15em 0.4em !important;
        min-width: 0 !important;
    }
    #y-scale-btn {
        left: 70px;
        top: 80px;
    }
    #x-scale-btn {
        right: 70px;
        bottom: 80px;
    }
    .stPlotlyChart {
        position: relative;
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

# Initialize session state for toggles
if 'y_log' not in st.session_state:
    st.session_state.y_log = True
if 'x_log' not in st.session_state:
    st.session_state.x_log = False
if 'show_bands' not in st.session_state:
    st.session_state.show_bands = False

# Callback functions
def toggle_y_scale():
    st.session_state.y_log = not st.session_state.y_log

def toggle_x_scale():
    st.session_state.x_log = not st.session_state.x_log

# ====== CHART CONTAINER ======
with st.container(border=True):
    st.markdown("### Kaspa Hashrate Analysis")
    
    # Create figure
    fig = go.Figure()

    # Determine x-axis values
    if st.session_state.x_log:
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

    # Power-law fit
    x_fit = np.linspace(df['days_from_genesis'].min(), df['days_from_genesis'].max(), 100)
    y_fit = a * np.power(x_fit, b)
    
    if st.session_state.x_log:
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
    
    # Deviation bands
    if st.session_state.show_bands:
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

    # Chart layout
    fig.update_layout(
        template='plotly_dark',
        hovermode='x unified',
        height=600,
        margin=dict(l=80, r=80, t=80, b=80),  # Extra margin for buttons
        yaxis_title='Hashrate (PH/s)',
        xaxis_title=x_title,
        xaxis=dict(
            type="log" if st.session_state.x_log else None,
            showgrid=True,
            gridwidth=1,
            gridcolor='rgba(100,100,100,0.2)'
        ),
        yaxis=dict(
            type="log" if st.session_state.y_log else "linear",
            showgrid=True,
            gridwidth=1,
            gridcolor='rgba(100,100,100,0.2)'
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )

    # Display the chart
    chart_container = st.plotly_chart(fig, use_container_width=True)

    # Add the scale buttons (using columns as containers)
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.button("Y: L" if st.session_state.y_log else "Y: A",
                on_click=toggle_y_scale,
                key="y_scale_btn",
                help="Toggle Y-axis scale (Log/Linear)",
                kwargs={'class': 'scale-button'},
                )
    
    with col2:
        st.button("X: L" if st.session_state.x_log else "X: A",
                on_click=toggle_x_scale,
                key="x_scale_btn",
                help="Toggle X-axis scale (Log/Linear)",
                kwargs={'class': 'scale-button'},
                )

# Controls below the chart
with st.container():
    st.toggle("Show Deviation Bands", 
             value=st.session_state.show_bands,
             key="show_bands",
             help="Show ± deviation bands around the fit")

# Stats cards
cols = st.columns(3)
with cols[0].container(border=True):
    st.metric("Power-Law Slope", f"{b:.3f}")
with cols[1].container(border=True):
    st.metric("Model Fit (R²)", f"{r2:.3f}")
with cols[2].container(border=True):
    st.metric("Current Hashrate", f"{df['Hashrate_PH'].iloc[-1]:.2f} PH/s")
