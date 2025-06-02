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

# Enhanced Custom CSS with Modern Design
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    /* Global Reset and Base Styles */
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }
    
    html, body, .stApp {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        background: linear-gradient(135deg, #0a0e1a 0%, #1a1f2e 50%, #0f1419 100%);
        color: #e2e8f0;
        overflow-x: hidden;
    }
    
    .stApp {
        background-attachment: fixed;
    }
    
    /* Remove Streamlit defaults */
    .main .block-container {
        padding: 0 !important;
        max-width: 100% !important;
    }
    
    /* Animated Background Pattern */
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
    
    /* Header Section */
    .header-container {
        background: rgba(15, 20, 25, 0.9);
        backdrop-filter: blur(25px);
        border-bottom: 1px solid rgba(0, 212, 255, 0.2);
        padding: 24px 40px;
        position: sticky;
        top: 0;
        z-index: 100;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
    }
    
    .header-content {
        display: flex;
        align-items: center;
        justify-content: space-between;
        max-width: 1400px;
        margin: 0 auto;
    }
    
    .brand {
        display: flex;
        align-items: center;
        gap: 16px;
    }
    
    .brand-icon {
        width: 48px;
        height: 48px;
        background: linear-gradient(135deg, #00d4ff 0%, #ff00a8 100%);
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 24px;
        box-shadow: 0 4px 20px rgba(0, 212, 255, 0.3);
    }
    
    .brand h1 {
        font-size: 32px;
        font-weight: 800;
        background: linear-gradient(135deg, #00d4ff 0%, #ff00a8 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
        text-shadow: 0 0 30px rgba(0, 212, 255, 0.3);
    }
    
    .brand-subtitle {
        font-size: 13px;
        color: #64748b;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 1.2px;
        margin-top: 2px;
    }
    
    .header-stats {
        display: flex;
        gap: 40px;
        align-items: center;
    }
    
    .header-stat {
        text-align: center;
        position: relative;
    }
    
    .header-stat::after {
        content: '';
        position: absolute;
        bottom: -8px;
        left: 50%;
        transform: translateX(-50%);
        width: 0;
        height: 2px;
        background: linear-gradient(90deg, #00d4ff, #ff00a8);
        transition: width 0.3s ease;
    }
    
    .header-stat:hover::after {
        width: 100%;
    }
    
    .header-stat-value {
        font-size: 20px;
        font-weight: 700;
        color: #00d4ff;
        display: block;
        text-shadow: 0 0 20px rgba(0, 212, 255, 0.4);
    }
    
    .header-stat-label {
        font-size: 11px;
        color: #64748b;
        text-transform: uppercase;
        letter-spacing: 0.8px;
        margin-top: 4px;
    }
    
    /* Chart Section */
    .chart-section {
        margin: 32px 40px 40px 40px;
        background: rgba(15, 20, 25, 0.6);
        backdrop-filter: blur(25px);
        border: 1px solid rgba(255, 255, 255, 0.15);
        border-radius: 24px;
        overflow: hidden;
        box-shadow: 0 16px 64px rgba(0, 0, 0, 0.4);
        position: relative;
    }
    
    .chart-section::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 1px;
        background: linear-gradient(90deg, transparent, #00d4ff, #ff00a8, transparent);
        opacity: 0.6;
    }
    
    /* Chart Title Section */
    .chart-title-section {
        background: rgba(30, 41, 59, 0.4);
        backdrop-filter: blur(15px);
        border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        padding: 28px 32px 20px 32px;
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
    
    /* Controls Section */
    .controls-section {
        padding: 24px 32px;
        border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .control-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 32px;
        align-items: end;
    }
    
    .control-group {
        display: flex;
        flex-direction: column;
        gap: 10px;
        position: relative;
    }
    
    .control-label {
        font-size: 12px;
        font-weight: 600;
        color: #94a3b8;
        text-transform: uppercase;
        letter-spacing: 1.2px;
        margin-bottom: 6px;
        position: relative;
    }
    
    .control-label::after {
        content: '';
        position: absolute;
        bottom: -3px;
        left: 0;
        width: 20px;
        height: 2px;
        background: linear-gradient(90deg, #00d4ff, #ff00a8);
        border-radius: 1px;
    }
    
    /* Revolutionary Selectbox Styling */
    .stSelectbox {
        position: relative;
    }
    
    .stSelectbox > div {
        position: relative;
    }
    
    .stSelectbox > div > div {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.9) 0%, rgba(15, 23, 42, 0.9) 100%) !important;
        border: 2px solid rgba(100, 116, 139, 0.3) !important;
        border-radius: 16px !important;
        backdrop-filter: blur(15px) !important;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2) !important;
        position: relative;
        overflow: hidden;
    }
    
    .stSelectbox > div > div::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(0, 212, 255, 0.1), transparent);
        transition: left 0.5s ease;
        pointer-events: none;
    }
    
    .stSelectbox > div > div:hover {
        border-color: #00d4ff !important;
        box-shadow: 0 8px 32px rgba(0, 212, 255, 0.2), 0 0 0 1px rgba(0, 212, 255, 0.3) !important;
        transform: translateY(-2px);
    }
    
    .stSelectbox > div > div:hover::before {
        left: 100%;
    }
    
    .stSelectbox > div > div > div {
        color: #f1f5f9 !important;
        font-weight: 600 !important;
        font-size: 14px !important;
        padding: 12px 16px !important;
    }
    
    /* Selectbox dropdown styling */
    .stSelectbox [data-baseweb="popover"] {
        background: rgba(15, 23, 42, 0.95) !important;
        backdrop-filter: blur(20px) !important;
        border: 1px solid rgba(0, 212, 255, 0.3) !important;
        border-radius: 16px !important;
        box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5) !important;
    }
    
    .stSelectbox [role="option"] {
        background: transparent !important;
        color: #e2e8f0 !important;
        transition: all 0.2s ease !important;
        border-radius: 8px !important;
        margin: 4px !important;
    }
    
    .stSelectbox [role="option"]:hover {
        background: rgba(0, 212, 255, 0.15) !important;
        color: #00d4ff !important;
    }
    
    .stSelectbox [aria-selected="true"] {
        background: rgba(0, 212, 255, 0.2) !important;
        color: #00d4ff !important;
    }
    
    /* Chart Container */
    .chart-content {
        padding: 32px;
        position: relative;
    }
    
    /* Enhanced Metrics Grid */
    .metrics-grid {
        display: flex;
        flex-direction: row;
        gap: 28px;
        margin: 40px 40px;
        width: calc(100% - 80px);
        justify-content: space-between;
        align-items: stretch;
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
        flex: 1;
        min-width: 0;
    }
    
    .metric-card::before {
        content: '';
        position: absolute;
        top: -2px;
        left: -2px;
        right: -2px;
        bottom: -2px;
        background: linear-gradient(135deg, #00d4ff, #ff00a8, #00ff88, #00d4ff);
        border-radius: 22px;
        opacity: 0;
        z-index: -1;
        transition: opacity 0.3s ease;
    }
    
    .metric-card::after {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: rgba(15, 20, 25, 0.9);
        border-radius: 20px;
        z-index: -1;
    }
    
    .metric-card:hover {
        transform: translateY(-8px) scale(1.02) !important;
        box-shadow: 0 25px 80px rgba(0, 0, 0, 0.5) !important;
    }
    
    .metric-card:hover::before {
        opacity: 1;
    }
    
    /* Custom Metric Styling */
    .metric-label {
        color: #94a3b8 !important;
        font-size: 13px !important;
        font-weight: 600 !important;
        text-transform: uppercase !important;
        letter-spacing: 1.2px !important;
        margin-bottom: 12px !important;
        position: relative;
        z-index: 1;
    }
    
    .metric-value {
        color: #f1f5f9 !important;
        font-size: 36px !important;
        font-weight: 800 !important;
        line-height: 1.1 !important;
        margin-bottom: 6px !important;
        text-shadow: 0 0 20px rgba(255, 255, 255, 0.1);
        position: relative;
        z-index: 1;
    }
    
    .metric-delta {
        font-size: 15px !important;
        font-weight: 700 !important;
        margin-bottom: 8px;
        position: relative;
        z-index: 1;
    }
    
    .metric-delta.positive {
        color: #00ff88 !important;
    }
    
    .metric-delta.negative {
        color: #ff4757 !important;
    }
    
    .metric-delta.neutral {
        color: #64748b !important;
    }
    
    .metric-help {
        color: #64748b !important;
        font-size: 11px !important;
        font-weight: 400 !important;
        line-height: 1.4;
        position: relative;
        z-index: 1;
        opacity: 0.8;
    }
    
    /* Force metric containers to inherit card styling */
    .metric-card > div {
        background: transparent !important;
        border: none !important;
        padding: 0 !important;
        margin: 0 !important;
    }
    
    /* Streamlit Metric Overrides */
    .metric-card div[data-testid="stMetric"] {
        background: transparent !important;
        border: none !important;
        padding: 0 !important;
        box-shadow: none !important;
        margin: 0 !important;
    }
    
    .metric-card div[data-testid="stMetric"] label {
        color: #94a3b8 !important;
        font-size: 13px !important;
        font-weight: 600 !important;
        text-transform: uppercase !important;
        letter-spacing: 1.2px !important;
        margin-bottom: 12px !important;
    }
    
    .metric-card div[data-testid="stMetric"] div[data-testid="metric-container"] > div:first-child {
        color: #f1f5f9 !important;
        font-size: 36px !important;
        font-weight: 800 !important;
        line-height: 1.1 !important;
        margin-bottom: 6px !important;
        text-shadow: 0 0 20px rgba(255, 255, 255, 0.1);
    }
    
    .metric-card div[data-testid="stMetric"] div[data-testid="metric-container"] div[data-testid="metric-delta"] {
        color: #00ff88 !important;
        font-size: 15px !important;
        font-weight: 700 !important;
    }
    
    /* Plotly Chart Styling */
    .stPlotlyChart {
        border-radius: 16px;
        overflow: hidden;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
    }
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 10px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(30, 41, 59, 0.4);
        border-radius: 5px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #00d4ff, #ff00a8);
        border-radius: 5px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #ff00a8, #00d4ff);
    }
    
    /* Responsive Design */
    @media (max-width: 768px) {
        .header-container {
            padding: 20px;
        }
        
        .chart-section {
            margin: 20px;
        }
        
        .chart-title-section, .controls-section, .chart-content {
            padding: 24px;
        }
        
        .metrics-grid {
            margin: 24px 20px;
            grid-template-columns: 1fr;
        }
        
        .brand h1 {
            font-size: 28px;
        }
        
        .header-stats {
            display: none;
        }
        
        .control-grid {
            grid-template-columns: 1fr;
            gap: 20px;
        }
    }
    
    /* Loading Animation */
    @keyframes pulse {
        0%, 100% { opacity: 1; transform: scale(1); }
        50% { opacity: 0.7; transform: scale(1.05); }
    }
    
    .loading {
        animation: pulse 2s infinite;
    }
    
    /* Success/Error States */
    .success-indicator {
        color: #00ff88;
    }
    
    .error-indicator {
        color: #ff4757;
    }
    
    /* Hide Streamlit Elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display: none;}
    
    /* Status Badge */
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
</style>
""", unsafe_allow_html=True)

# Calculate current metrics for header
current_price = price_df['Price'].iloc[-1]
last_date = price_df['Date'].iloc[-1]
thirty_days_ago = last_date - timedelta(days=30)
df_30_days_ago = price_df[price_df['Date'] >= thirty_days_ago]

if len(df_30_days_ago) > 0:
    price_30_days_ago = df_30_days_ago['Price'].iloc[0]
    price_pct_change = ((current_price - price_30_days_ago) / price_30_days_ago) * 100
else:
    price_pct_change = 0

# Header Section
st.markdown(f"""
<div class="header-container">
    <div class="header-content">
        <div class="brand">
            <div class="brand-icon">💎</div>
            <div>
                <h1>Kaspa Analytics Pro</h1>
                <div class="brand-subtitle">Advanced Market Intelligence Platform</div>
            </div>
        </div>
        <div class="header-stats">
            <div class="header-stat">
                <span class="header-stat-value">${current_price:.4f}</span>
                <div class="header-stat-label">Current Price</div>
            </div>
            <div class="header-stat">
                <span class="header-stat-value" style="color: {'#00ff88' if price_pct_change >= 0 else '#ff4757'}">{price_pct_change:+.1f}%</span>
                <div class="header-stat-label">30D Change</div>
            </div>
            <div class="header-stat">
                <span class="header-stat-value">{r2_price:.3f}</span>
                <div class="header-stat-label">Model Fit</div>
            </div>
            <div class="header-stat">
                <div class="status-badge">
                    <div class="live-dot"></div>
                    <span>Live Data</span>
                </div>
            </div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

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
    # Create columns for the controls
    col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
    
    with col1:
        st.markdown('<div class="control-group"><div class="control-label">📈 Price Scale</div></div>', unsafe_allow_html=True)
        y_scale_options = ["Linear", "Log"]
        y_scale = st.selectbox("", y_scale_options,
                             index=1, label_visibility="collapsed", key="price_y_scale_select")

    with col2:
        st.markdown('<div class="control-group"><div class="control-label">⏱️ Time Scale</div></div>', unsafe_allow_html=True)
        x_scale_options = ["Linear", "Log"]
        x_scale_type = st.selectbox("", x_scale_options,
                                  index=0, label_visibility="collapsed", key="price_x_scale_select")

    with col3:
        st.markdown('<div class="control-group"><div class="control-label">📅 Time Period</div></div>', unsafe_allow_html=True)
        time_ranges = ["1W", "1M", "3M", "6M", "1Y", "All"]
        time_range = st.selectbox("", time_ranges,
                                index=5, label_visibility="collapsed", key="price_time_range_select")

    with col4:
        st.markdown('<div class="control-group"><div class="control-label">📊 Power Law</div></div>', unsafe_allow_html=True)
        power_law_options = ["Hide", "Show"]
        show_power_law = st.selectbox("", power_law_options,
                                    index=1, label_visibility="collapsed", key="price_power_law_select")

# Chart content section
st.markdown("""
<div class="chart-content">
</div>
""", unsafe_allow_html=True)

# Data filtering based on time range
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

# Create the enhanced chart
fig = go.Figure()

if x_scale_type == "Log":
    x_values = filtered_df['days_from_genesis']
    x_title = "Days Since Genesis (Log Scale)"
else:
    x_values = filtered_df['Date']
    x_title = "Date"

# Add price trace with standard styling
fig.add_trace(go.Scatter(
    x=x_values,
    y=filtered_df['Price'],
    mode='lines',
    name='Kaspa Price',
    line=dict(
        color='#00d4ff',
        width=3,
        shape='spline',
        smoothing=0.3
    ),
    hovertemplate='<b>%{fullData.name}</b><br>' +
                  'Date: %{text}<br>' +
                  'Price: $%{y:.6f}<br>' +
                  '<extra></extra>',
    text=[d.strftime('%Y-%m-%d') for d in filtered_df['Date']],
    showlegend=True,
    fill='tonexty' if len(fig.data) > 0 else None,
    fillcolor='rgba(0, 212, 255, 0.1)'
))

# Add power law if enabled
if show_power_law == "Show":
    x_fit = filtered_df['days_from_genesis']
    y_fit = a_price * np.power(x_fit, b_price)
    fit_x = x_fit if x_scale_type == "Log" else filtered_df['Date']

    # Main power law line
    fig.add_trace(go.Scatter(
        x=fit_x,
        y=y_fit,
        mode='lines',
        name=f'Power Law Fit (R²={r2_price:.3f})',
        line=dict(color='#ff00a8', width=3, dash='solid'),
        showlegend=True,
        hovertemplate='<b>Power Law Fit</b><br>' +
                      'R² = %{customdata:.3f}<br>' +
                      'Value: $%{y:.6f}<br>' +
                      '<extra></extra>',
        customdata=[r2_price] * len(fit_x)
    ))

    # Support levels
    fig.add_trace(go.Scatter(
        x=fit_x,
        y=y_fit * 0.4,
        mode='lines',
        name='Support (-60%)',
        line=dict(color='rgba(0, 255, 136, 0.6)', width=1.5, dash='dot'),
        showlegend=True,
        hoverinfo='skip'
    ))
    
    # Resistance levels
    fig.add_trace(go.Scatter(
        x=fit_x,
        y=y_fit * 2.2,
        mode='lines',
        name='Resistance (+120%)',
        line=dict(color='rgba(255, 71, 87, 0.6)', width=1.5, dash='dot'),
        fill='tonexty',
        fillcolor='rgba(100, 100, 100, 0.1)',
        showlegend=True,
        hoverinfo='skip'
    ))

# Enhanced chart layout
fig.update_layout(
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    font=dict(family='Inter', color='#e2e8f0'),
    hovermode='x unified',
    height=700,
    margin=dict(l=0, r=0, t=60, b=0),
    xaxis=dict(
        title=dict(
            text=x_title,
            font=dict(size=14, color='#cbd5e1', weight=600)
        ),
        type="log" if x_scale_type == "Log" else None,
        showgrid=True,
        gridwidth=1,
        gridcolor='rgba(255, 255, 255, 0.08)',
        linecolor='rgba(255, 255, 255, 0.2)',
        tickfont=dict(size=12, color='#94a3b8'),
        rangeslider=dict(
            visible=True,
            thickness=0.08,
            bgcolor='rgba(15, 20, 25, 0.9)',
            bordercolor="rgba(0, 212, 255, 0.3)",
            borderwidth=2
        )
    ),
    yaxis=dict(
        title=dict(
            text='Price (USD)',
            font=dict(size=14, color='#cbd5e1', weight=600)
        ),
        type="log" if y_scale == "Log" else "linear",
        showgrid=True,
        gridwidth=1,
        gridcolor='rgba(255, 255, 255, 0.08)',
        linecolor='rgba(255, 255, 255, 0.2)',
        tickfont=dict(size=12, color='#94a3b8')
    ),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="left",
        x=0,
        bgcolor='rgba(15, 20, 25, 0.9)',
        bordercolor='rgba(0, 212, 255, 0.3)',
        borderwidth=1,
        font=dict(size=12)
    ),
    hoverlabel=dict(
        bgcolor='rgba(15, 20, 25, 0.95)',
        bordercolor='rgba(0, 212, 255, 0.5)',
        font=dict(color='#e2e8f0', size=12),
        align='left'
    )
)

# Display chart with container
with st.container():
    st.plotly_chart(fig, use_container_width=True, config={
        'displayModeBar': True,
        'displaylogo': False,
        'modeBarButtonsToRemove': ['lasso2d', 'select2d'],
        'modeBarButtonsToAdd': ['hoverclosest', 'hovercompare'],
        'toImageButtonOptions': {
            'format': 'png',
            'filename': f'kaspa_analysis_{datetime.now().strftime("%Y%m%d_%H%M")}',
            'height': 700,
            'width': 1400,
            'scale': 2
        }
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

# Calculate additional metrics
volatility_30d = filtered_df['Price'].pct_change().rolling(30).std().iloc[-1] * 100 if len(filtered_df) > 30 else 0
max_price = filtered_df['Price'].max()
min_price = filtered_df['Price'].min()
price_range_pct = ((max_price - min_price) / min_price) * 100

# Enhanced Metrics Section
st.markdown('<div class="metrics-grid">', unsafe_allow_html=True)

# Power-Law Slope
st.markdown(f"""
<div class="metric-card">
    <div class="metric-label">💎 POWER-LAW SLOPE</div>
    <div class="metric-value">{b_price:.4f}</div>
    <div class="metric-delta {'positive' if slope_pct_change >= 0 else 'negative'}">{slope_pct_change:+.2f}%</div>
    <div class="metric-help">Growth trajectory strength - higher values indicate steeper exponential growth</div>
</div>
""", unsafe_allow_html=True)

# Model Accuracy
st.markdown(f"""
<div class="metric-card">
    <div class="metric-label">🎯 MODEL ACCURACY (R²)</div>
    <div class="metric-value">{r2_price:.4f}</div>
    <div class="metric-delta {'positive' if r2_pct_change >= 0 else 'negative'}">{r2_pct_change:+.2f}%</div>
    <div class="metric-help">Power law fit quality - values closer to 1.0 indicate better model accuracy</div>
</div>
""", unsafe_allow_html=True)

# Current Price
st.markdown(f"""
<div class="metric-card">
    <div class="metric-label">📈 CURRENT PRICE</div>
    <div class="metric-value">${current_price:.6f}</div>
    <div class="metric-delta {'positive' if price_pct_change >= 0 else 'negative'}">{price_pct_change:+.2f}%</div>
    <div class="metric-help">Latest recorded price with 30-day percentage change</div>
</div>
""", unsafe_allow_html=True)

# Market Cap
market_cap_estimate = current_price * 24e9
st.markdown(f"""
<div class="metric-card">
    <div class="metric-label">💰 EST. MARKET CAP</div>
    <div class="metric-value">${market_cap_estimate/1e9:.2f}B</div>
    <div class="metric-delta {'positive' if price_pct_change >= 0 else 'negative'}">{price_pct_change:+.2f}%</div>
    <div class="metric-help">Estimated market capitalization based on circulating supply</div>
</div>
""", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Enhanced Footer with additional information
st.markdown(f"""
<div style="text-align: center; padding: 50px 40px; margin-top: 40px; 
     background: rgba(15, 20, 25, 0.4); backdrop-filter: blur(20px);
     border-top: 1px solid rgba(255, 255, 255, 0.1);">
    <div style="max-width: 1200px; margin: 0 auto;">
        <h3 style="color: #f1f5f9; margin-bottom: 16px; font-size: 20px; font-weight: 700;">
            Kaspa Analytics Pro
        </h3>
        <p style="color: #64748b; font-size: 14px; margin-bottom: 20px;">
            Professional-grade cryptocurrency market analysis • Real-time data processing • Advanced predictive modeling
        </p>
        <div style="display: flex; justify-content: center; gap: 40px; margin-bottom: 20px; flex-wrap: wrap;">
            <div style="text-align: center;">
                <div style="color: #00d4ff; font-weight: 700; font-size: 16px;">{len(filtered_df):,}</div>
                <div style="color: #64748b; font-size: 12px; text-transform: uppercase;">Data Points</div>
            </div>
            <div style="text-align: center;">
                <div style="color: #ff00a8; font-weight: 700; font-size: 16px;">Standard</div>
                <div style="color: #64748b; font-size: 12px; text-transform: uppercase;">Analysis Mode</div>
            </div>
            <div style="text-align: center;">
                <div style="color: #00ff88; font-weight: 700; font-size: 16px;">Live</div>
                <div style="color: #64748b; font-size: 12px; text-transform: uppercase;">Data Status</div>
            </div>
        </div>
        <div style="color: #475569; font-size: 11px; text-transform: uppercase; letter-spacing: 1px;">
            Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')} • 
            Built for institutional-grade analysis
        </div>
    </div>
</div>
""", unsafe_allow_html=True)
