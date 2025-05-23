import streamlit as st
import plotly.graph_objects as go
import numpy as np
import pandas as pd
from utils import fit_power_law, load_data
from datetime import datetime, timedelta

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

# Minimal CSS focusing only on essential spacing
st.markdown("""
<style>
    /* Remove all unnecessary padding/margins */
    .stApp > div:first-child {
        padding-top: 0rem !important;
    }
    
    /* Compact title */
    h2 {
        color: #e0e0e0 !important;
        margin: 0 !important;
        padding: 0 !important;
    }
    
    /* Ultra-thin dividers */
    .st-emotion-cache-1dp5vir {
        border-top: 1px solid #3A3C4A !important;
        margin: 0 !important;
        padding: 0 !important;
    }
    
    /* Tight dropdown row */
    .stHorizontalBlock {
        padding-top: 2px !important;
        padding-bottom: 2px !important;
    }
    
    /* Compact dropdown labels */
    .control-label {
        font-size: 11px !important;
        margin: 0 0 1px 0 !important;
        padding: 0 !important;
    }
    
    /* Keep existing styling for other elements */
    div[data-testid="stVerticalBlock"] > div[data-testid="stVerticalBlockBorderWrapper"] {
        background-color: #262730 !important;
        border: 1px solid #3A3C4A !important;
        padding: 10px !important;
    }
    [data-testid="stMetric"] {
        background-color: #262730 !important;
        border: 1px solid #3A3C4A !important;
        padding: 15px 20px !important;
    }
</style>
""", unsafe_allow_html=True)

# ====== MAIN CHART ======
# Title with no container
st.markdown("<h2>Kaspa Hashrate</h2>", unsafe_allow_html=True)

# First divider - immediately after title
st.divider()

# Dropdowns in a single tight row
cols = st.columns([1,1,1,1,6])  # Last column is spacer

with cols[0]:
    st.markdown('<div class="control-label">Hashrate Scale</div>', unsafe_allow_html=True)
    y_scale = st.selectbox("Hashrate Scale", ["Linear", "Log"],
                         index=1, label_visibility="collapsed")

with cols[1]:
    st.markdown('<div class="control-label">Time Scale</div>', unsafe_allow_html=True)
    x_scale_type = st.selectbox("Time Scale", ["Linear", "Log"],
                              index=0, label_visibility="collapsed")

with cols[2]:
    st.markdown('<div class="control-label">Period</div>', unsafe_allow_html=True)
    time_range = st.selectbox("Time Range", ["1W", "1M", "3M", "6M", "1Y", "All"],
                            index=5, label_visibility="collapsed")

with cols[3]:
    st.markdown('<div class="control-label">Power Law Fit</div>', unsafe_allow_html=True)
    show_power_law = st.selectbox("Power Law Fit", ["Hide", "Show"],
                                index=0, label_visibility="collapsed")

# Second divider - immediately after dropdowns
st.divider()

# Rest of the code remains exactly the same...
last_date = df['Date'].iloc[-1]
if time_range == "1W":
    start_date = last_date - timedelta(days=7)
elif time_range == "1M":
    start_date = last_date - timedelta(days=30)
elif time_range == "3M":
    start_date = last_date - timedelta(days=90)
elif time_range == "6M":
    start_date = last_date - timedelta(days=180)
elif time_range == "1Y":
    start_date = last_date - timedelta(days=365)
else:
    start_date = df['Date'].iloc[0]

filtered_df = df[df['Date'] >= start_date]

fig = go.Figure()

if x_scale_type == "Log":
    x_values = filtered_df['days_from_genesis']
    x_title = "Days Since Genesis (Log Scale)"
    tickformat = None
    hoverformat = None
else:
    x_values = filtered_df['Date']
    x_title = "Date"
    tickformat = "%b %Y"
    hoverformat = "%b %d, %Y"

fig.add_trace(go.Scatter(
    x=x_values,
    y=filtered_df['Hashrate_PH'],
    mode='lines',
    name='Hashrate (PH/s)',
    line=dict(color='#00FFCC', width=2.5),
    hovertemplate='<b>Date</b>: %{text|%Y-%m-%d}<br><b>Hashrate</b>: %{y:.2f} PH/s<extra></extra>',
    text=filtered_df['Date']
))

if show_power_law == "Show":
    x_fit = filtered_df['days_from_genesis']
    y_fit = a * np.power(x_fit, b)
    fit_x = x_fit if x_scale_type == "Log" else filtered_df['Date']

    fig.add_trace(go.Scatter(
        x=fit_x,
        y=y_fit,
        mode='lines',
        name=f'Power-Law Fit (R²={r2:.3f})',
        line=dict(color='#FFA726', dash='dot', width=2)
    ))

    fig.add_trace(go.Scatter(
        x=fit_x,
        y=y_fit * 0.4,
        mode='lines',
        name='-60% Deviation',
        line=dict(color='rgba(255, 255, 255, 0.5)', dash='dot', width=1),
        hoverinfo='skip',
        fill=None
    ))
    fig.add_trace(go.Scatter(
        x=fit_x,
        y=y_fit * 2.2,
        mode='lines',
        name='+120% Deviation',
        line=dict(color='rgba(255, 255, 255, 0.5)', dash='dot', width=1),
        hoverinfo='skip',
        fill='tonexty',
        fillcolor='rgba(100, 100, 100, 0.2)'
    ))

fig.update_layout(
    plot_bgcolor='#262730',
    paper_bgcolor='#262730',
    font_color='#e0e0e0',
    hovermode='x unified',
    height=700,
    margin=dict(l=20, r=20, t=10, b=100),  # Minimal top margin
    yaxis_title='Hashrate (PH/s)',
    xaxis_title=x_title,
    xaxis=dict(
        rangeslider=dict(
            visible=True,
            thickness=0.1,
            bgcolor='#262730',
            bordercolor="#3A3C4A",
            borderwidth=1
        ),
        type="log" if x_scale_type == "Log" else None,
        showgrid=True,
        gridwidth=1,
        gridcolor='rgba(255, 255, 255, 0.1)',
        tickformat=tickformat,
        linecolor='#3A3C4A',
        zerolinecolor='#3A3C4A'
    ),
    yaxis=dict(
        type="log" if y_scale == "Log" else "linear",
        showgrid=True,
        gridwidth=1,
        gridcolor='rgba(255, 255, 255, 0.1)',
        linecolor='#3A3C4A',
        zerolinecolor='#3A3C4A'
    ),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1,
        bgcolor='rgba(38, 39, 48, 0.8)'
    )
)

st.plotly_chart(fig, use_container_width=True)

# Stats
cols = st.columns(3)
with cols[0]:
    st.metric("Power-Law Slope", f"{b:.3f}")
with cols[1]:
    st.metric("Model Fit (R²)", f"{r2:.3f}")
with cols[2]:
    st.metric("Current Hashrate", f"{df['Hashrate_PH'].iloc[-1]:.2f} PH/s")
