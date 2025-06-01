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
            radial-gradient(circle at 20% 80%, rgba(120, 119, 198, 0.1) 0%, transparent 50%),
            radial-gradient(circle at 80% 20%, rgba(255, 119, 198, 0.1) 0%, transparent 50%),
            radial-gradient(circle at 40% 40%, rgba(120, 219, 255, 0.1) 0%, transparent 50%);
        pointer-events: none;
        z-index: -1;
    }
    
    /* Header Section */
    .header-container {
        background: rgba(15, 20, 25, 0.8);
        backdrop-filter: blur(20px);
        border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        padding: 20px 40px;
        position: sticky;
        top: 0;
        z-index: 100;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
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
        gap: 12px;
    }
    
    .brand h1 {
        font-size: 28px;
        font-weight: 800;
        background: linear-gradient(135deg, #00d4ff 0%, #ff00a8 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
    }
    
    .brand-subtitle {
        font-size: 12px;
        color: #64748b;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .header-stats {
        display: flex;
        gap: 30px;
        align-items: center;
    }
    
    .header-stat {
        text-align: center;
    }
    
    .header-stat-value {
        font-size: 18px;
        font-weight: 700;
        color: #00d4ff;
        display: block;
    }
    
    .header-stat-label {
        font-size: 11px;
        color: #64748b;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-top: 2px;
    }
    
    /* Control Panel */
    .control-panel {
        background: rgba(15, 20, 25, 0.6);
        backdrop-filter: blur(15px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        padding: 24px 32px;
        margin: 24px 40px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
    }
    
    .control-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
        gap: 24px;
        align-items: end;
    }
    
    .control-group {
        display: flex;
        flex-direction: column;
        gap: 8px;
    }
    
    .control-label {
        font-size: 12px;
        font-weight: 600;
        color: #94a3b8;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 4px;
    }
    
    /* Enhanced Selectbox Styling */
    .stSelectbox > div > div {
        background: rgba(30, 41, 59, 0.8) !important;
        border: 1px solid rgba(100, 116, 139, 0.3) !important;
        border-radius: 12px !important;
        backdrop-filter: blur(10px) !important;
        transition: all 0.3s ease !important;
    }
    
    .stSelectbox > div > div:hover {
        border-color: #00d4ff !important;
        box-shadow: 0 0 0 3px rgba(0, 212, 255, 0.1) !important;
    }
    
    .stSelectbox > div > div > div {
        color: #e2e8f0 !important;
        font-weight: 500 !important;
    }
    
    /* Chart Container */
    .chart-section {
        margin: 0 40px 40px 40px;
        background: rgba(15, 20, 25, 0.4);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        padding: 32px;
        box-shadow: 0 12px 48px rgba(0, 0, 0, 0.3);
    }
    
    .chart-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 24px;
        padding-bottom: 16px;
        border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .chart-title {
        font-size: 24px;
        font-weight: 700;
        color: #f1f5f9;
        margin: 0;
    }
    
    .chart-subtitle {
        font-size: 14px;
        color: #64748b;
        margin-top: 4px;
    }
    
    /* Enhanced Metrics Grid */
    .metrics-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
        gap: 24px;
        margin: 32px 40px;
    }
    
    .metric-card {
        background: rgba(15, 20, 25, 0.6);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        padding: 24px;
        position: relative;
        overflow: hidden;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        cursor: pointer;
    }
    
    .metric-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 2px;
        background: linear-gradient(90deg, #00d4ff, #ff00a8, #00ff88);
        opacity: 0;
        transition: opacity 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-4px);
        border-color: rgba(0, 212, 255, 0.3);
        box-shadow: 0 20px 60px rgba(0, 0, 0, 0.4), 0 0 0 1px rgba(0, 212, 255, 0.1);
    }
    
    .metric-card:hover::before {
        opacity: 1;
    }
    
    /* Streamlit Metric Overrides */
    div[data-testid="stMetric"] {
        background: transparent !important;
        border: none !important;
        padding: 0 !important;
        box-shadow: none !important;
    }
    
    div[data-testid="stMetric"] label {
        color: #94a3b8 !important;
        font-size: 12px !important;
        font-weight: 600 !important;
        text-transform: uppercase !important;
        letter-spacing: 1px !important;
        margin-bottom: 8px !important;
    }
    
    div[data-testid="stMetric"] div[data-testid="metric-container"] > div:first-child {
        color: #f1f5f9 !important;
        font-size: 32px !important;
        font-weight: 800 !important;
        line-height: 1.2 !important;
        margin-bottom: 4px !important;
    }
    
    div[data-testid="stMetric"] div[data-testid="metric-container"] div[data-testid="metric-delta"] {
        color: #00ff88 !important;
        font-size: 14px !important;
        font-weight: 600 !important;
    }
    
    /* Plotly Chart Styling */
    .stPlotlyChart {
        border-radius: 12px;
        overflow: hidden;
    }
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(30, 41, 59, 0.3);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: rgba(100, 116, 139, 0.5);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: rgba(100, 116, 139, 0.7);
    }
    
    /* Responsive Design */
    @media (max-width: 768px) {
        .header-container {
            padding: 16px 20px;
        }
        
        .control-panel, .chart-section {
            margin: 16px 20px;
            padding: 20px;
        }
        
        .metrics-grid {
            margin: 24px 20px;
            grid-template-columns: 1fr;
        }
        
        .brand h1 {
            font-size: 24px;
        }
        
        .header-stats {
            display: none;
        }
    }
    
    /* Loading Animation */
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.5; }
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
            <div>
                <h1>Kaspa Analytics Pro</h1>
                <div class="brand-subtitle">Advanced Market Intelligence</div>
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
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Control Panel
st.markdown("""
<div class="control-panel">
    <div style="margin-bottom: 16px;">
        <h3 style="color: #f1f5f9; margin: 0; font-size: 18px; font-weight: 600;">Chart Configuration</h3>
        <p style="color: #64748b; margin: 4px 0 0 0; font-size: 14px;">Customize your analysis view</p>
    </div>
</div>
""", unsafe_allow_html=True)

# Controls in the panel
with st.container():
    col1, col2, col3, col4, col5 = st.columns([1, 1, 1, 1, 2])
    
    with col1:
        st.markdown('<div class="control-label">Price Scale</div>', unsafe_allow_html=True)
        y_scale_options = ["Linear", "Log"]
        y_scale = st.selectbox("Price Scale", y_scale_options,
                             index=1, label_visibility="collapsed", key="price_y_scale_select")

    with col2:
        st.markdown('<div class="control-label">Time Scale</div>', unsafe_allow_html=True)
        x_scale_options = ["Linear", "Log"]
        x_scale_type = st.selectbox("Time Scale", x_scale_options,
                                  index=0, label_visibility="collapsed", key="price_x_scale_select")

    with col3:
        st.markdown('<div class="control-label">Time Period</div>', unsafe_allow_html=True)
        time_ranges = ["1W", "1M", "3M", "6M", "1Y", "All"]
        time_range = st.selectbox("Time Range", time_ranges,
                                index=5, label_visibility="collapsed", key="price_time_range_select")

    with col4:
        st.markdown('<div class="control-label">Power Law</div>', unsafe_allow_html=True)
        power_law_options = ["Hide", "Show"]
        show_power_law = st.selectbox("Power Law Fit", power_law_options,
                                    index=1, label_visibility="collapsed", key="price_power_law_select")

# Chart Section
st.markdown("""
<div class="chart-section">
    <div class="chart-header">
        <div>
            <h2 class="chart-title">Kaspa Price Analysis</h2>
            <div class="chart-subtitle">Historical price data with power-law modeling</div>
        </div>
    </div>
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

# Create the chart
fig = go.Figure()

if x_scale_type == "Log":
    x_values = filtered_df['days_from_genesis']
    x_title = "Days Since Genesis (Log Scale)"
else:
    x_values = filtered_df['Date']
    x_title = "Date"

# Add price trace with enhanced styling
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
        line=dict(color='#ff00a8', width=2.5, dash='solid'),
        showlegend=True,
        hovertemplate='<b>Power Law Fit</b><br>' +
                      'R² = %{customdata:.3f}<br>' +
                      'Value: $%{y:.6f}<br>' +
                      '<extra></extra>',
        customdata=[r2_price] * len(fit_x)
    ))

    # Deviation bands
    fig.add_trace(go.Scatter(
        x=fit_x,
        y=y_fit * 0.4,
        mode='lines',
        name='Support (-60%)',
        line=dict(color='rgba(0, 255, 136, 0.6)', width=1.5, dash='dot'),
        showlegend=True,
        hoverinfo='skip'
    ))
    
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

# Enhanced chart layout with FIXED title configuration
fig.update_layout(
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    font=dict(family='Inter', color='#e2e8f0'),
    hovermode='x unified',
    height=650,
    margin=dict(l=0, r=0, t=40, b=0),
    xaxis=dict(
        title=dict(
            text=x_title,
            font=dict(size=14, color='#cbd5e1')
        ),
        type="log" if x_scale_type == "Log" else None,
        showgrid=True,
        gridwidth=1,
        gridcolor='rgba(255, 255, 255, 0.08)',
        linecolor='rgba(255, 255, 255, 0.2)',
        tickfont=dict(size=12, color='#94a3b8'),
        rangeslider=dict(
            visible=True,
            thickness=0.06,
            bgcolor='rgba(15, 20, 25, 0.8)',
            bordercolor="rgba(255, 255, 255, 0.1)",
            borderwidth=1
        )
    ),
    yaxis=dict(
        title=dict(
            text='Price (USD)',
            font=dict(size=14, color='#cbd5e1')
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
        bgcolor='rgba(15, 20, 25, 0.8)',
        bordercolor='rgba(255, 255, 255, 0.1)',
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
        'modeBarButtonsToRemove': ['lasso2d', 'select2d', 'autoScale2d'],
        'modeBarButtonsToAdd': ['hoverclosest', 'hovercompare'],
        'toImageButtonOptions': {
            'format': 'png',
            'filename': f'kaspa_price_analysis_{datetime.now().strftime("%Y%m%d")}',
            'height': 650,
            'width': 1200,
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

# Enhanced Metrics Section
st.markdown('<div class="metrics-grid">', unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.metric(
        "Power-Law Slope", 
        f"{b_price:.4f}", 
        delta=f"{slope_pct_change:+.2f}%",
        help="Indicates the growth trajectory strength"
    )
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.metric(
        "Model Accuracy (R²)", 
        f"{r2_price:.4f}", 
        delta=f"{r2_pct_change:+.2f}%",
        help="How well the power law fits the data (closer to 1.0 is better)"
    )
    st.markdown('</div>', unsafe_allow_html=True)

with col3:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.metric(
        "Current Price", 
        f"${current_price:.6f}", 
        delta=f"{price_pct_change:+.2f}%",
        help="Latest recorded price with 30-day change"
    )
    st.markdown('</div>', unsafe_allow_html=True)

with col4:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    market_cap_estimate = current_price * 24e9  # Rough estimate
    st.metric(
        "Est. Market Cap", 
        f"${market_cap_estimate/1e9:.2f}B", 
        delta=f"{price_pct_change:+.2f}%",
        help="Estimated market capitalization"
    )
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Footer info
st.markdown("""
<div style="text-align: center; padding: 40px 20px; color: #64748b; font-size: 12px;">
    <p>Kaspa Analytics Pro • Advanced cryptocurrency market analysis • Data updated in real-time</p>
    <p style="margin-top: 8px;">Built with professional-grade visualization tools for institutional analysis</p>
</div>
""", unsafe_allow_html=True)
