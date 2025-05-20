import streamlit as st
import plotly.graph_objects as go
import numpy as np
import pandas as pd
from utils import fit_power_law, load_data

st.set_page_config(layout="wide")

# Custom CSS for button styling
st.markdown("""
<style>
    .scale-toggle {
        background-color: rgba(0, 255, 204, 0.2) !important;
        border: 1px solid #00FFCC !important;
        border-radius: 12px !important;
        padding: 0.15rem 0.75rem !important;
        font-size: 0.8rem !important;
        color: white !important;
        height: 28px !important;
        min-width: 60px !important;
    }
    .scale-toggle:hover {
        background-color: rgba(0, 255, 204, 0.3) !important;
        border-color: #00FFCC !important;
    }
    .scale-toggle.st-emotion-cache-1gj0q5z {
        background-color: rgba(0, 255, 204, 0.4) !important;
    }
    .y-scale-container {
        position: absolute;
        top: 40px;
        left: 10px;
        z-index: 100;
    }
    .x-scale-container {
        position: absolute;
        bottom: 10px;
        right: 10px;
        z-index: 100;
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
    st.session_state.y_scale = False  # False = Linear, True = Log
if 'x_scale' not in st.session_state:
    st.session_state.x_scale = False  # False = Linear, True = Log

# ====== CHART CONTAINER ======
with st.container(border=True):
    st.markdown("### Kaspa Hashrate")
    
    # Create columns for the chart and controls
    chart_col, _ = st.columns([20, 1])
    
    with chart_col:
        # Create figure
        fig = go.Figure()

        # Determine x-axis values based on scale type
        if st.session_state.x_scale:
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

        # Power-law fit
        x_fit = np.linspace(df['days_from_genesis'].min(), df['days_from_genesis'].max(), 100)
        y_fit = a * np.power(x_fit, b)
        
        if st.session_state.x_scale:
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

        # Layout configuration
        fig.update_layout(
            template='plotly_dark',
            hovermode='x unified',
            height=600,
            margin=dict(l=20, r=20, t=40, b=40),
            yaxis_title='PH/s',
            xaxis_title=x_title,
            xaxis=dict(
                type='log' if st.session_state.x_scale else 'date',
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
                type='log' if st.session_state.y_scale else 'linear',
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

        # Display the chart
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

        # Y-axis scale toggle (left side)
        with st.container():
            st.markdown('<div class="y-scale-container">', unsafe_allow_html=True)
            st.session_state.y_scale = st.toggle(
                "Y Scale",
                value=st.session_state.y_scale,
                key="y_toggle",
                label_visibility="collapsed",
                help="Toggle between Linear (A) and Logarithmic (L) scale",
                format_func=lambda x: "L" if x else "A"
            )
            st.markdown('</div>', unsafe_allow_html=True)

        # X-axis scale toggle (right side)
        with st.container():
            st.markdown('<div class="x-scale-container">', unsafe_allow_html=True)
            st.session_state.x_scale = st.toggle(
                "X Scale",
                value=st.session_state.x_scale,
                key="x_toggle",
                label_visibility="collapsed",
                help="Toggle between Linear (A) and Logarithmic (L) scale",
                format_func=lambda x: "L" if x else "A"
            )
            st.markdown('</div>', unsafe_allow_html=True)

# Stats in minimal cards
cols = st.columns(3)
with cols[0].container(border=True):
    st.metric("Power-Law Slope", f"{b:.3f}")
with cols[1].container(border=True):
    st.metric("Model Fit (R²)", f"{r2:.3f}")
with cols[2].container(border=True):
    st.metric("Current Hashrate", f"{df['Hashrate_PH'].iloc[-1]:.2f} PH/s")
