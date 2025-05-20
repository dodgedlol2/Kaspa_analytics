import streamlit as st
import plotly.graph_objects as go
import numpy as np
import pandas as pd
from utils import fit_power_law, load_data

st.set_page_config(layout="wide")

# Custom CSS for professional styling
st.markdown("""
<style>
    .header-section {
        border-bottom: 1px solid #2d3436;
        padding-bottom: 0.5rem;
        margin-bottom: 0.5rem;
    }
    .control-button {
        border: 1px solid #636e72 !important;
        border-radius: 6px !important;
        padding: 0.25rem 0.75rem !important;
        font-size: 0.9rem !important;
    }
    .control-button label {
        font-weight: 500 !important;
        margin-bottom: 0 !important;
    }
    .stRadio [role="radiogroup"] {
        gap: 0.5rem !important;
    }
    .stToggle button {
        border: 1px solid #636e72 !important;
        border-radius: 6px !important;
        padding: 0.25rem 0.75rem !important;
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

# ====== PROFESSIONAL CHART CONTAINER ======
with st.container(border=True):
    # Header section with dedicated border
    with st.container():
        st.markdown('<div class="header-section">', unsafe_allow_html=True)
        
        # Header columns
        header_cols = st.columns([3, 2, 2, 1.5])
        
        with header_cols[0]:
            st.markdown("### Kaspa Hashrate")
        
        with header_cols[1]:
            st.markdown("**Scale:**", help="Hashrate scale type")
            y_scale = st.radio(
                "Hashrate Scale",
                ["Linear", "Log"],
                index=1,
                horizontal=True,
                label_visibility="collapsed",
                key="y_scale"
            )
        
        with header_cols[2]:
            st.markdown("**Time:**", help="Time scale type")
            x_scale_type = st.radio(
                "Time Scale",
                ["Linear", "Log"],
                index=0,
                horizontal=True,
                label_visibility="collapsed",
                key="x_scale"
            )
        
        with header_cols[3]:
            st.markdown("**Bands:**", help="Deviation bands visibility")
            show_bands = st.toggle(
                "Show Bands",
                value=False,
                label_visibility="collapsed",
                key="bands_toggle"
            )
        
        st.markdown('</div>', unsafe_allow_html=True)

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
        line=dict(color='#00FFCC', width=2.5),
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
        line=dict(color='orange', dash='dot', width=1.8)
    ))
    
    # Deviation bands (only shown when toggled)
    if show_bands:
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
        margin=dict(l=20, r=20, t=20, b=20),
        yaxis_title='PH/s',
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
            x=1,
            font=dict(size=10)
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
