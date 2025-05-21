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

# Kaspa Brand Color Scheme
COLORS = {
    'primary': '#17B2A7',     # Kaspa's signature teal
    'primary_dark': '#0E8C84', # Darker teal
    'background': '#0D1B2A',   # Deep navy-blue
    'panel': '#1B263B',        # Dark slate
    'border': '#2C3A58',       # Medium slate-blue
    'secondary': '#E9C46A',    # Golden yellow
    'accent': '#F4A261',       # Orange accent
    'text': '#E0E1DD',         # Off-white text
    'success': '#2ECC71',      # Emerald green
    'grid': 'rgba(200, 213, 219, 0.1)'
}

# Custom CSS
st.markdown(f"""
<style>
    .stApp {{
        background-color: {COLORS['background']};
        color: {COLORS['text']};
    }}
    .st-emotion-cache-6qob1r, .sidebar-content {{
        background-color: {COLORS['panel']} !important;
        border-right: 1px solid {COLORS['border']} !important;
    }}
    div[data-testid="stVerticalBlock"] > div[data-testid="stVerticalBlockBorderWrapper"] {{
        background-color: {COLORS['panel']} !important;
        border: 1px solid {COLORS['border']} !important;
        border-radius: 10px;
        padding: 20px !important;
    }}
    div[data-testid="stMetric"] {{
        background-color: {COLORS['panel']} !important;
        border: 1px solid {COLORS['border']} !important;
        border-radius: 8px;
        padding: 20px !important;
    }}
    div[data-testid="stMetricValue"] > div {{
        font-size: 26px !important;
        font-weight: 700 !important;
        color: {COLORS['primary']} !important;
    }}
    h2 {{
        color: {COLORS['primary']} !important;
    }}
</style>
""", unsafe_allow_html=True)

# Main chart
with st.container():
    header_col1, header_col2 = st.columns([2, 8])
    
    with header_col1:
        st.markdown(f"""
        <div style="padding-left: 15px; margin-bottom: 10px;">
            <h2>Kaspa Hashrate</h2>
            <div style="color: {COLORS['text']}; opacity: 0.8; font-size: 14px;">
                Power-law growth analysis
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with header_col2:
        controls = st.columns([1.5, 1.5, 1.5, 4])
        with controls[0]:
            y_scale = st.toggle("Linear/Log", value=True, key="y_scale")
            y_scale = "Log" if y_scale else "Linear"
        with controls[1]:
            x_scale_type = st.toggle("Linear/Log", value=False, key="x_scale")
            x_scale_type = "Log" if x_scale_type else "Linear"
        with controls[2]:
            show_bands = st.toggle("Hide/Show", value=False, key="bands_toggle")

    fig = go.Figure()

    max_days = df['days_from_genesis'].max() + 300
    if x_scale_type == "Log":
        x_values = df['days_from_genesis']
        x_title = "Days Since Genesis (Log Scale)"
    else:
        x_values = df['Date']
        x_title = "Date"

    fig.add_trace(go.Scatter(
        x=x_values,
        y=df['Hashrate_PH'],
        mode='lines',
        name='Hashrate (PH/s)',
        line=dict(color=COLORS['primary'], width=2.8),
        hovertemplate='<b>Date</b>: %{text|%Y-%m-%d}<br><b>Hashrate</b>: %{y:.2f} PH/s<extra></extra>',
        text=df['Date']
    ))

    x_fit = np.linspace(df['days_from_genesis'].min(), max_days, 300)
    y_fit = a * np.power(x_fit, b)
    fit_x = x_fit if x_scale_type == "Log" else [genesis_date + pd.Timedelta(days=int(d)) for d in x_fit]

    fig.add_trace(go.Scatter(
        x=fit_x,
        y=y_fit,
        mode='lines',
        name=f'Power-Law Fit (R²={r2:.3f})',
        line=dict(color=COLORS['secondary'], dash='dot', width=2.5)
    ))

    if show_bands:
        fig.add_trace(go.Scatter(
            x=fit_x,
            y=y_fit * 0.4,
            mode='lines',
            line=dict(color=f"rgba(244, 162, 97, 0.3)", width=1),
            hoverinfo='skip'
        ))
        fig.add_trace(go.Scatter(
            x=fit_x,
            y=y_fit * 2.2,
            mode='lines',
            line=dict(color=f"rgba(244, 162, 97, 0.3)", width=1),
            hoverinfo='skip',
            fill='tonexty',
            fillcolor=f"rgba(23, 178, 167, 0.1)"
        ))

    fig.update_layout(
        plot_bgcolor=COLORS['panel'],
        paper_bgcolor=COLORS['panel'],
        font_color=COLORS['text'],
        height=700,
        yaxis_title='Hashrate (PH/s)',
        xaxis_title=x_title,
        xaxis=dict(
            rangeslider=dict(visible=True),
            type="log" if x_scale_type == "Log" else None
        ),
        yaxis=dict(
            type="log" if y_scale == "Log" else "linear"
        )
    )

    st.plotly_chart(fig, use_container_width=True)

# Metrics
metrics = st.columns(3)
with metrics[0]:
    st.metric("POWER-LAW SLOPE", f"{b:.3f}")
with metrics[1]:
    st.metric("MODEL FIT (R²)", f"{r2:.3f}")
with metrics[2]:
    st.metric("CURRENT HASHRATE", f"{df['Hashrate_PH'].iloc[-1]:.2f} PH/s")
