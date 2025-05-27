import streamlit as st
import plotly.graph_objects as go
import numpy as np
import pandas as pd
from utils import fit_power_law, load_price_data
from datetime import datetime, timedelta

st.set_page_config(layout="wide", page_title="Kaspa Analytics | Price")

# Data loading and processing
if 'price_df' not in st.session_state or 'price_genesis_date' not in st.session_state:
    try:
        st.session_state.price_df, st.session_state.price_genesis_date = load_price_data()
    except Exception as e:
        st.error(f"Failed to load price data: {str(e)}")
        st.stop()

price_df = st.session_state.price_df
genesis_date = st.session_state.price_genesis_date

try:
    a_price, b_price, r2_price = fit_power_law(price_df, y_col='Price')
except Exception as e:
    st.error(f"Failed to calculate price power law: {str(e)}")
    st.stop()

# Custom CSS - Glassnode-inspired styling with dark theme
st.markdown("""
<style>
    /* Main app styling */
    .stApp { 
        background-color: #0E1117;
    }
    
    /* Sidebar styling */
    .st-emotion-cache-6qob1r, .sidebar-content { 
        background-color: #1A1D26 !important;
        border-right: 1px solid #2A2E3C !important;
    }
    
    /* Title styling */
    .page-title {
        font-size: 24px;
        font-weight: 600;
        color: #FFFFFF;
        margin-bottom: 8px;
        padding-top: 8px;
    }
    
    /* Container styling */
    .glassnode-container {
        background-color: #1A1D26;
        border-radius: 8px;
        border: 1px solid #2A2E3C;
        padding: 16px;
        margin-bottom: 16px;
    }
    
    /* Metric styling */
    .metric-container {
        background-color: #1A1D26;
        border-radius: 8px;
        border: 1px solid #2A2E3C;
        padding: 12px 16px;
    }
    
    .metric-value {
        font-size: 24px !important;
        font-weight: 600 !important;
        color: #00FFCC !important;
    }
    
    .metric-label {
        font-size: 12px !important;
        color: #A0A4B8 !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    /* Button/select styling */
    .stSelectbox, .stRadio {
        margin-bottom: 8px;
    }
    
    [data-baseweb="select"] > div {
        background-color: #1A1D26 !important;
        border: 1px solid #2A2E3C !important;
        color: #FFFFFF !important;
    }
    
    [data-baseweb="select"] > div:hover {
        border-color: #00FFCC !important;
    }
    
    /* Chart styling */
    .plotly-chart {
        border-radius: 8px;
    }
    
    /* Divider styling */
    .st-emotion-cache-1dp5vir {
        border-top: 1px solid #2A2E3C !important;
    }
    
    /* Hover tooltip */
    .hovertext text.hovertext {
        fill: #FFFFFF !important;
        font-size: 12px !important;
    }
    
    /* Range slider */
    .rangeslider-bg {
        background-color: #2A2E3C !important;
    }
    
    /* Tabs styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 32px;
        padding: 0 16px;
        background-color: #1A1D26;
        border-radius: 6px;
        border: 1px solid #2A2E3C;
        color: #A0A4B8;
        font-size: 12px;
        font-weight: 500;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #00FFCC20 !important;
        color: #00FFCC !important;
        border-color: #00FFCC50 !important;
    }
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 6px;
        height: 6px;
    }
    
    ::-webkit-scrollbar-track {
        background: #1A1D26;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #2A2E3C;
        border-radius: 3px;
    }
    
    /* Custom date range picker */
    .stDateInput input {
        color: #FFFFFF !important;
    }
    
    /* Custom radio buttons */
    .stRadio [role="radiogroup"] {
        gap: 8px;
    }
    
    .stRadio [role="radio"] {
        margin: 0;
        padding: 6px 12px;
        background-color: #1A1D26;
        border: 1px solid #2A2E3C;
        border-radius: 6px;
        color: #A0A4B8;
        font-size: 12px;
    }
    
    .stRadio [role="radio"][aria-checked="true"] {
        background-color: #00FFCC20 !important;
        color: #00FFCC !important;
        border-color: #00FFCC50 !important;
    }
</style>
""", unsafe_allow_html=True)

# ====== SIDEBAR ======
with st.sidebar:
    st.markdown("""
    <div style="padding: 16px 0 24px 0; border-bottom: 1px solid #2A2E3C;">
        <img src="https://assets-global.website-files.com/5f4ec532319820f7c2ccd7a3/5f55620b7b806770e6becea2_glassnode-logo.svg" width="160">
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div style="padding: 16px 0; border-bottom: 1px solid #2A2E3C;">
        <div style="font-size: 12px; color: #A0A4B8; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 12px;">Kaspa Analytics</div>
        <div style="display: flex; flex-direction: column; gap: 4px;">
            <div style="padding: 8px 12px; background-color: #00FFCC20; border-radius: 6px; color: #00FFCC; font-size: 14px; display: flex; align-items: center; gap: 8px;">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M12 2C6.48 2 2 6.48 2 12C2 17.52 6.48 22 12 22C17.52 22 22 17.52 22 12C22 6.48 17.52 2 12 2ZM12 20C7.59 20 4 16.41 4 12C4 7.59 7.59 4 12 4C16.41 4 20 7.59 20 12C20 16.41 16.41 20 12 20Z" fill="#00FFCC"/>
                    <path d="M12.5 7H11V13L16.2 16.2L17 14.9L12.5 12.2V7Z" fill="#00FFCC"/>
                </svg>
                <span>Price Analysis</span>
            </div>
            <div style="padding: 8px 12px; border-radius: 6px; color: #A0A4B8; font-size: 14px; display: flex; align-items: center; gap: 8px;">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M9 17H7V10H9V17ZM13 17H11V7H13V17ZM17 17H15V13H17V17ZM19 19H5V5H19V19.1V19ZM19 3H5C3.9 3 3 3.9 3 5V19C3 20.1 3.9 21 5 21H19C20.1 21 21 20.1 21 19V5C21 3.9 20.1 3 19 3Z" fill="#A0A4B8"/>
                </svg>
                <span>Hashrate Analysis</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div style="padding: 16px 0;">
        <div style="font-size: 12px; color: #A0A4B8; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 12px;">Time Range</div>
        <div style="display: flex; flex-direction: column; gap: 8px;">
            <div style="display: flex; gap: 8px;">
                <button style="flex: 1; padding: 8px; background-color: #00FFCC20; border: 1px solid #00FFCC50; border-radius: 6px; color: #00FFCC; font-size: 12px;">1W</button>
                <button style="flex: 1; padding: 8px; background-color: #1A1D26; border: 1px solid #2A2E3C; border-radius: 6px; color: #A0A4B8; font-size: 12px;">1M</button>
                <button style="flex: 1; padding: 8px; background-color: #1A1D26; border: 1px solid #2A2E3C; border-radius: 6px; color: #A0A4B8; font-size: 12px;">3M</button>
            </div>
            <div style="display: flex; gap: 8px;">
                <button style="flex: 1; padding: 8px; background-color: #1A1D26; border: 1px solid #2A2E3C; border-radius: 6px; color: #A0A4B8; font-size: 12px;">6M</button>
                <button style="flex: 1; padding: 8px; background-color: #1A1D26; border: 1px solid #2A2E3C; border-radius: 6px; color: #A0A4B8; font-size: 12px;">1Y</button>
                <button style="flex: 1; padding: 8px; background-color: #1A1D26; border: 1px solid #2A2E3C; border-radius: 6px; color: #A0A4B8; font-size: 12px;">ALL</button>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ====== MAIN CONTENT ======
st.markdown('<div class="page-title">Kaspa Price Analysis</div>', unsafe_allow_html=True)

# Metrics row
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown("""
    <div class="metric-container">
        <div class="metric-label">Current Price</div>
        <div class="metric-value">${price:.4f}</div>
    </div>
    """.format(price=price_df['Price'].iloc[-1]), unsafe_allow_html=True)
with col2:
    st.markdown("""
    <div class="metric-container">
        <div class="metric-label">Power-Law Slope</div>
        <div class="metric-value">{b_price:.3f}</div>
    </div>
    """.format(b_price=b_price), unsafe_allow_html=True)
with col3:
    st.markdown("""
    <div class="metric-container">
        <div class="metric-label">Model Fit (R²)</div>
        <div class="metric-value">{r2_price:.3f}</div>
    </div>
    """.format(r2_price=r2_price), unsafe_allow_html=True)
with col4:
    st.markdown("""
    <div class="metric-container">
        <div class="metric-label">Days Since Genesis</div>
        <div class="metric-value">{days:.0f}</div>
    </div>
    """.format(days=price_df['days_from_genesis'].iloc[-1]), unsafe_allow_html=True)

# Chart controls
with st.container():
    st.markdown('<div class="glassnode-container">', unsafe_allow_html=True)
    
    # Controls row
    col1, col2, col3, col4 = st.columns([2, 2, 2, 4])
    with col1:
        st.markdown('<div style="font-size: 12px; color: #A0A4B8; margin-bottom: 4px;">Price Scale</div>', unsafe_allow_html=True)
        y_scale = st.radio("Price Scale", ["Linear", "Log"], index=1, horizontal=True, label_visibility="collapsed")
    with col2:
        st.markdown('<div style="font-size: 12px; color: #A0A4B8; margin-bottom: 4px;">Time Scale</div>', unsafe_allow_html=True)
        x_scale_type = st.radio("Time Scale", ["Linear", "Log"], index=0, horizontal=True, label_visibility="collapsed")
    with col3:
        st.markdown('<div style="font-size: 12px; color: #A0A4B8; margin-bottom: 4px;">Power Law Fit</div>', unsafe_allow_html=True)
        show_power_law = st.radio("Power Law Fit", ["Hide", "Show"], index=0, horizontal=True, label_visibility="collapsed")
    
    st.markdown('</div>', unsafe_allow_html=True)

# Time range filter from sidebar
time_range = "1W"  # Default, would be set by sidebar interaction
last_date = price_df['Date'].iloc[-1]
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
    start_date = price_df['Date'].iloc[0]

filtered_df = price_df[price_df['Date'] >= start_date]

# Main chart
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

# Add price trace
fig.add_trace(go.Scatter(
    x=x_values,
    y=filtered_df['Price'],
    mode='lines',
    name='Price (USD)',
    line=dict(color='#00FFCC', width=2.5),
    hovertemplate='<b>Date</b>: %{text|%Y-%m-%d}<br><b>Price</b>: $%{y:.4f}<extra></extra>',
    text=filtered_df['Date']
))

if show_power_law == "Show":
    x_fit = filtered_df['days_from_genesis']
    y_fit = a_price * np.power(x_fit, b_price)
    fit_x = x_fit if x_scale_type == "Log" else filtered_df['Date']

    fig.add_trace(go.Scatter(
        x=fit_x,
        y=y_fit,
        mode='lines',
        name=f'Power-Law Fit (R²={r2_price:.3f})',
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
    plot_bgcolor='#1A1D26',
    paper_bgcolor='#1A1D26',
    font_color='#e0e0e0',
    hovermode='x unified',
    height=600,
    margin=dict(l=20, r=20, t=40, b=80),
    yaxis_title='Price (USD)',
    xaxis_title=x_title,
    xaxis=dict(
        rangeslider=dict(
            visible=True,
            thickness=0.08,
            bgcolor='#1A1D26',
            bordercolor="#2A2E3C",
            borderwidth=1
        ),
        type="log" if x_scale_type == "Log" else None,
        showgrid=True,
        gridwidth=1,
        gridcolor='rgba(255, 255, 255, 0.1)',
        minor=dict(
            ticklen=6,
            gridcolor='rgba(255, 255, 255, 0.05)',
            gridwidth=0.5
        ),
        tickformat=tickformat,
        linecolor='#2A2E3C',
        zerolinecolor='#2A2E3C'
    ),
    yaxis=dict(
        type="log" if y_scale == "Log" else "linear",
        showgrid=True,
        gridwidth=1,
        gridcolor='rgba(255, 255, 255, 0.1)',
        minor=dict(
            ticklen=6,
            gridcolor='rgba(255, 255, 255, 0.05)',
            gridwidth=0.5
        ),
        linecolor='#2A2E3C',
        zerolinecolor='#2A2E3C'
    ),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1,
        bgcolor='rgba(26, 29, 38, 0.8)'
    ),
    hoverlabel=dict(
        bgcolor='#1A1D26',
        bordercolor='#2A2E3C',
        font_color='#e0e0e0'
    )
)

st.plotly_chart(fig, use_container_width=True)

# Additional sections would go here
st.markdown("""
<div class="glassnode-container">
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px;">
        <div style="font-size: 16px; font-weight: 600; color: #FFFFFF;">Price Performance Metrics</div>
        <div style="display: flex; gap: 8px;">
            <button style="padding: 6px 12px; background-color: #1A1D26; border: 1px solid #2A2E3C; border-radius: 6px; color: #A0A4B8; font-size: 12px;">Daily</button>
            <button style="padding: 6px 12px; background-color: #1A1D26; border: 1px solid #2A2E3C; border-radius: 6px; color: #A0A4B8; font-size: 12px;">Weekly</button>
            <button style="padding: 6px 12px; background-color: #00FFCC20; border: 1px solid #00FFCC50; border-radius: 6px; color: #00FFCC; font-size: 12px;">Monthly</button>
        </div>
    </div>
    
    <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px;">
        <div style="padding: 12px; background-color: #1A1D26; border-radius: 6px; border: 1px solid #2A2E3C;">
            <div style="font-size: 12px; color: #A0A4B8; margin-bottom: 4px;">1M Return</div>
            <div style="font-size: 18px; font-weight: 600; color: #00FFCC;">+24.5%</div>
        </div>
        <div style="padding: 12px; background-color: #1A1D26; border-radius: 6px; border: 1px solid #2A2E3C;">
            <div style="font-size: 12px; color: #A0A4B8; margin-bottom: 4px;">3M Return</div>
            <div style="font-size: 18px; font-weight: 600; color: #00FFCC;">+56.2%</div>
        </div>
        <div style="padding: 12px; background-color: #1A1D26; border-radius: 6px; border: 1px solid #2A2E3C;">
            <div style="font-size: 12px; color: #A0A4B8; margin-bottom: 4px;">6M Return</div>
            <div style="font-size: 18px; font-weight: 600; color: #00FFCC;">+112.8%</div>
        </div>
        <div style="padding: 12px; background-color: #1A1D26; border-radius: 6px; border: 1px solid #2A2E3C;">
            <div style="font-size: 12px; color: #A0A4B8; margin-bottom: 4px;">YTD Return</div>
            <div style="font-size: 18px; font-weight: 600; color: #00FFCC;">+248.3%</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)
