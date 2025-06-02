import streamlit as st
import plotly.graph_objects as go
import numpy as np
import pandas as pd
from utils import fit_power_law, load_price_data
from datetime import datetime, timedelta

st.set_page_config(
    page_title="Kaspa Analytics Pro",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="collapsed"
)

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

# Enhanced Custom CSS with Modern Design (Header removed)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    html, body, .stApp {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        background: linear-gradient(135deg, #0a0e1a 0%, #1a1f2e 50%, #0f1419 100%);
        color: #e2e8f0;
        overflow-x: hidden;
    }
    
    .stApp {
        background-attachment: fixed;
    }
    
    .main .block-container {
        padding: 2rem 1rem !important;
        max-width: 100% !important;
    }
    
    .stApp::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-image: 
            radial-gradient(circle at 20% 80%, rgba(120, 119, 198, 0.15) 0%, transparent 50%),
            radial-gradient(circle at 80% 20%, rgba(255, 119, 198, 0.15) 0%, transparent 50%),
            radial-gradient(circle at 40% 40%, rgba(120, 219, 255, 0.15) 0%, transparent 50%);
        pointer-events: none;
        z-index: -1;
        animation: backgroundShift 20s ease-in-out infinite;
    }
    
    @keyframes backgroundShift {
        0%, 100% { opacity: 1; transform: translateX(0px) translateY(0px); }
        50% { opacity: 0.8; transform: translateX(20px) translateY(-20px); }
    }
    
    .chart-section {
        margin: 0 0 40px 0;
        background: rgba(15, 20, 25, 0.6);
        backdrop-filter: blur(25px);
        border: 1px solid rgba(255, 255, 255, 0.15);
        border-radius: 24px;
        overflow: hidden;
        box-shadow: 0 16px 64px rgba(0, 0, 0, 0.4);
        position: relative;
    }
    
    .chart-title-section {
        background: rgba(30, 41, 59, 0.4);
        backdrop-filter: blur(15px);
        border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        padding: 28px 48px 20px 48px;
        position: relative;
    }
    
    .chart-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 0;
    }
    
    .chart-title {
        font-size: 28px;
        font-weight: 800;
        background: linear-gradient(135deg, #f1f5f9 0%, #cbd5e1 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
    }
    
    .live-indicator {
        display: flex;
        align-items: center;
        gap: 8px;
        font-size: 13px;
        color: #00ff88;
        font-weight: 600;
    }
    
    .live-dot {
        width: 8px;
        height: 8px;
        background: #00ff88;
        border-radius: 50%;
        animation: pulse 2s infinite;
        box-shadow: 0 0 10px #00ff88;
    }
    
    .controls-section {
        padding: 24px 48px;
        border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .control-label {
        font-size: 12px;
        font-weight: 600;
        color: #94a3b8;
        text-transform: uppercase;
        letter-spacing: 1.2px;
        margin-bottom: 6px;
    }
    
    .stSelectbox > div > div {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.9) 0%, rgba(15, 23, 42, 0.9) 100%) !important;
        border: 2px solid rgba(100, 116, 139, 0.3) !important;
        border-radius: 16px !important;
        backdrop-filter: blur(15px) !important;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2) !important;
        min-height: 40px !important;
    }
    
    .stSelectbox > div > div:hover {
        border-color: #00d4ff !important;
        box-shadow: 0 8px 32px rgba(0, 212, 255, 0.2), 0 0 0 1px rgba(0, 212, 255, 0.3) !important;
        transform: translateY(-2px);
    }
    
    .stSelectbox > div > div > div {
        color: #f1f5f9 !important;
        font-weight: 600 !important;
        font-size: 14px !important;
        padding: 8px 16px !important;
    }
    
    .chart-content {
        padding: 32px 48px;
        position: relative;
    }
    
    .metric-card {
        background: rgba(15, 20, 25, 0.7) !important;
        backdrop-filter: blur(25px) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 20px !important;
        padding: 28px !important;
        position: relative !important;
        overflow: hidden !important;
        transition: all 0.5s cubic-bezier(0.4, 0, 0.2, 1) !important;
        cursor: pointer !important;
        margin-bottom: 20px !important;
        width: 100% !important;
        box-sizing: border-box !important;
    }
    
    .metric-card:hover {
        transform: translateY(-8px) scale(1.02) !important;
        box-shadow: 0 25px 80px rgba(0, 0, 0, 0.5) !important;
    }
    
    .metric-label {
        color: #94a3b8 !important;
        font-size: 13px !important;
        font-weight: 600 !important;
        text-transform: uppercase !important;
        letter-spacing: 1.2px !important;
        margin-bottom: 12px !important;
    }
    
    .metric-value {
        color: #f1f5f9 !important;
        font-size: 36px !important;
        font-weight: 800 !important;
        line-height: 1.1 !important;
        margin-bottom: 6px !important;
        text-shadow: 0 0 20px rgba(255, 255, 255, 0.1);
    }
    
    .metric-delta {
        font-size: 15px !important;
        font-weight: 700 !important;
        margin-bottom: 8px;
    }
    
    .metric-delta.positive {
        color: #00ff88 !important;
    }
    
    .metric-delta.negative {
        color: #ff4757 !important;
    }
    
    .stPlotlyChart {
        border-radius: 16px;
        overflow: hidden;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
    }
    
    .stPlotlyChart .modebar {
        background: transparent !important;
        transform: translateY(15px) !important;
    }
    
    .stPlotlyChart .modebar-group {
        background: transparent !important;
    }
    
    .status-badge {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: rgba(0, 255, 136, 0.1);
        border: 1px solid rgba(0, 255, 136, 0.3);
        border-radius: 20px;
        padding: 6px 12px;
        font-size: 11px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        color: #00ff88;
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 1; transform: scale(1); }
        50% { opacity: 0.7; transform: scale(1.05); }
    }
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display: none;}
</style>
""", unsafe_allow_html=True)

# Calculate current metrics
current_price = price_df['Price'].iloc[-1]
last_date = price_df['Date'].iloc[-1]
thirty_days_ago = last_date - timedelta(days=30)
df_30_days_ago = price_df[price_df['Date'] >= thirty_days_ago]

if len(df_30_days_ago) > 0:
    price_30_days_ago = df_30_days_ago['Price'].iloc[0]
    price_pct_change = ((current_price - price_30_days_ago) / price_30_days_ago) * 100
else:
    price_pct_change = 0

# Chart Section with title and integrated controls
st.markdown("""
<div class="chart-section">
    <div class="chart-title-section">
        <div class="chart-header">
            <div>
                <h2 class="chart-title">Kaspa Price Analysis</h2>
            </div>
            <div class="live-indicator">
                <div class="live-dot"></div>
                <span>LIVE</span>
            </div>
        </div>
    </div>
    <div class="controls-section">
    </div>
</div>
""", unsafe_allow_html=True)

# Controls integrated within the chart section
with st.container():
    col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
    
    with col1:
        st.markdown('<div class="control-label">Price Scale</div>', unsafe_allow_html=True)
        y_scale = st.selectbox("", ["Linear", "Log"], index=1, label_visibility="collapsed", key="price_y_scale_select")

    with col2:
        st.markdown('<div class="control-label">Time Scale</div>', unsafe_allow_html=True)
        x_scale_type = st.selectbox("", ["Linear", "Log"], index=0, label_visibility="collapsed", key="price_x_scale_select")

    with col3:
        st.markdown('<div class="control-label">Time Period</div>', unsafe_allow_html=True)
        time_range = st.selectbox("", ["1W", "1M", "3M", "6M", "1Y", "All"], index=5, label_visibility="collapsed", key="price_time_range_select")

    with col4:
        st.markdown('<div class="control-label">Power Law</div>', unsafe_allow_html=True)
        show_power_law = st.selectbox("", ["Hide", "Show"], index=1, label_visibility="collapsed", key="price_power_law_select")

# Chart content section
st.markdown('<div class="chart-content"></div>', unsafe_allow_html=True)

# Data filtering based on time range
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

# Create the enhanced chart with improved formatting
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

# Add price trace with improved formatting
fig.add_trace(go.Scatter(
    x=x_values,
    y=filtered_df['Price'],
    mode='lines',
    name='Kaspa Price (USD)',
    line=dict(color='#00FFCC', width=2.5),
    hovertemplate='<b>Date</b>: %{text|%Y-%m-%d}<br><b>Price</b>: $%{y:.4f}<extra></extra>',
    text=filtered_df['Date'],
    showlegend=True
))

# Add power law if enabled with improved formatting
if show_power_law == "Show":
    x_fit = filtered_df['days_from_genesis']
    y_fit = a_price * np.power(x_fit, b_price)
    fit_x = x_fit if x_scale_type == "Log" else filtered_df['Date']

    fig.add_trace(go.Scatter(
        x=fit_x,
        y=y_fit,
        mode='lines',
        name=f'Power-Law Fit (R²={r2_price:.3f})',
        line=dict(color='#FFA726', dash='dot', width=2),
        showlegend=True
    ))

    fig.add_trace(go.Scatter(
        x=fit_x,
        y=y_fit * 0.4,
        mode='lines',
        name='-60% Deviation',
        line=dict(color='rgba(255, 255, 255, 0.5)', dash='dot', width=1),
        hoverinfo='skip',
        fill=None,
        showlegend=True
    ))
    
    fig.add_trace(go.Scatter(
        x=fit_x,
        y=y_fit * 2.2,
        mode='lines',
        name='+120% Deviation',
        line=dict(color='rgba(255, 255, 255, 0.5)', dash='dot', width=1),
        hoverinfo='skip',
        fill='tonexty',
        fillcolor='rgba(100, 100, 100, 0.2)',
        showlegend=True
    ))

# Enhanced chart layout with improved formatting
fig.update_layout(
    plot_bgcolor='#1A1D26',
    paper_bgcolor='#1A1D26',
    font_color='#e0e0e0',
    hovermode='x unified',
    height=700,
    margin=dict(l=0, r=40, t=60, b=100),
    yaxis_title='',
    xaxis_title=x_title,
    xaxis=dict(
        rangeslider=dict(
            visible=True,
            thickness=0.1,
            bgcolor='#1A1D26',
            bordercolor="#3A3C4A",
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
        linecolor='#3A3C4A',
        zerolinecolor='#3A3C4A'
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
        linecolor='#3A3C4A',
        zerolinecolor='#3A3C4A'
    ),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="left",
        x=0,
        bgcolor='rgba(26, 29, 38, 0.8)'
    ),
    hoverlabel=dict(
        bgcolor='#1A1D26',
        bordercolor='#3A3C4A',
        font_color='#e0e0e0'
    ),
    modebar=dict(
        bgcolor='rgba(26, 29, 38, 0.8)',
        color='#e0e0e0',
        activecolor='#00FFCC'
    )
)

# Display chart
st.plotly_chart(fig, use_container_width=True, config={
    'displayModeBar': True,
    'displaylogo': False,
    'modeBarButtonsToRemove': ['lasso2d', 'select2d'],
    'modeBarButtonsToAdd': ['hoverclosest', 'hovercompare'],
})

# Calculate comprehensive metrics
if len(df_30_days_ago) > 0:
    price_30_days_ago_data = price_df[price_df['Date'] <= thirty_days_ago]
    if len(price_30_days_ago_data) > 10:
        try:
            a_price_30d, b_price_30d, r2_price_30d = fit_power_law(price_30_days_ago_data, y_col='Price')
        except:
            b_price_30d = b_price
            r2_price_30d = r2_price
    else:
        b_price_30d = b_price
        r2_price_30d = r2_price
    
    slope_pct_change = ((b_price - b_price_30d) / abs(b_price_30d)) * 100 if b_price_30d != 0 else 0
    r2_pct_change = ((r2_price - r2_price_30d) / r2_price_30d) * 100 if r2_price_30d != 0 else 0
else:
    slope_pct_change = 0
    r2_pct_change = 0

# Enhanced Metrics Section
col1, col2, col3, col4 = st.columns(4)

with col1:
    metric_html = f"""
    <div class="metric-card">
        <div class="metric-label">POWER-LAW SLOPE</div>
        <div class="metric-value">{b_price:.4f}</div>
        <div class="metric-delta {'positive' if slope_pct_change >= 0 else 'negative'}">{slope_pct_change:+.2f}%</div>
    </div>
    """
    st.markdown(metric_html, unsafe_allow_html=True)

with col2:
    metric_html = f"""
    <div class="metric-card">
        <div class="metric-label">MODEL ACCURACY (R²)</div>
        <div class="metric-value">{r2_price:.4f}</div>
        <div class="metric-delta {'positive' if r2_pct_change >= 0 else 'negative'}">{r2_pct_change:+.2f}%</div>
    </div>
    """
    st.markdown(metric_html, unsafe_allow_html=True)

with col3:
    # Improved price display formatting
    if current_price >= 1:
        price_display = f"${current_price:.2f}"
    elif current_price >= 0.01:
        price_display = f"${current_price:.4f}"
    elif current_price >= 0.0001:
        price_display = f"${current_price:.6f}"
    else:
        price_display = f"${current_price:.8f}"
    
    metric_html = f"""
    <div class="metric-card">
        <div class="metric-label">CURRENT PRICE</div>
        <div class="metric-value">{price_display}</div>
        <div class="metric-delta {'positive' if price_pct_change >= 0 else 'negative'}">{price_pct_change:+.2f}%</div>
    </div>
    """
    st.markdown(metric_html, unsafe_allow_html=True)

with col4:
    market_cap_estimate = current_price * 24e9
    metric_html = f"""
    <div class="metric-card">
        <div class="metric-label">EST. MARKET CAP</div>
        <div class="metric-value">${market_cap_estimate/1e9:.2f}B</div>
        <div class="metric-delta {'positive' if price_pct_change >= 0 else 'negative'}">{price_pct_change:+.2f}%</div>
    </div>
    """
    st.markdown(metric_html, unsafe_allow_html=True)

# Footer
footer_html = """
<div style="text-align: center; padding: 50px 40px; margin-top: 40px; 
     background: rgba(15, 20, 25, 0.4); backdrop-filter: blur(20px);
     border-top: 1px solid rgba(255, 255, 255, 0.1);">
    <div style="max-width: 1200px; margin: 0 auto;">
        <h3 style="color: #f1f5f9; margin-bottom: 16px; font-size: 20px; font-weight: 700;">
            KaspaMetrics
        </h3>
        <p style="color: #64748b; font-size: 14px; margin-bottom: 20px;">
            Professional-grade cryptocurrency market analysis • Real-time data processing • Advanced predictive modeling
        </p>
        <div style="color: #475569; font-size: 11px; text-transform: uppercase; letter-spacing: 1px;">
            Last Updated: """ + datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC') + """ • 
            Built for institutional-grade analysis
        </div>
    </div>
</div>
"""

st.markdown(footer_html, unsafe_allow_html=True)
