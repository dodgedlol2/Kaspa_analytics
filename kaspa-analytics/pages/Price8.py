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

# Enhanced Custom CSS with Modern Design and Animated Title
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
        padding: 0 !important;
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
    
    @keyframes shimmer {
        0% {
            background-position: -200% center;
            text-shadow: 0 0 10px rgba(241, 245, 249, 0.3);
        }
        50% {
            text-shadow: 
                0 0 20px rgba(0, 212, 255, 0.6),
                0 0 30px rgba(0, 212, 255, 0.4),
                0 0 40px rgba(0, 212, 255, 0.2);
        }
        100% {
            background-position: 200% center;
            text-shadow: 0 0 10px rgba(241, 245, 249, 0.3);
        }
    }
    
    @keyframes glow {
        0%, 100% {
            text-shadow: 
                0 0 10px rgba(241, 245, 249, 0.3),
                0 0 20px rgba(0, 212, 255, 0.2),
                0 0 30px rgba(0, 212, 255, 0.1);
        }
        50% {
            text-shadow: 
                0 0 20px rgba(241, 245, 249, 0.5),
                0 0 30px rgba(0, 212, 255, 0.4),
                0 0 40px rgba(0, 212, 255, 0.3),
                0 0 50px rgba(0, 212, 255, 0.2);
        }
    }
    
    .chart-section {
        margin: 12px 40px 28px 40px;
        background: rgba(30, 41, 59, 0.4);
        backdrop-filter: blur(25px);
        border: none;
        border-radius: 16px;
        overflow: hidden;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.25);
        position: relative;
        transition: all 0.3s ease;
    }
    
    /* Simplified header section with just title */
    .header-section {
        padding: 20px 40px 20px 40px;
        background: transparent;
        display: flex;
        align-items: center;
        justify-content: flex-start;
        margin-bottom: 0px;
    }
    
    .title-container {
        flex: 0 0 auto;
    }
    
    .main-title {
        font-size: 16px;
        font-weight: 700;
        color: #ffffff;
        margin: 0;
        letter-spacing: 0.5px;
        text-align: left;
        text-shadow: 0 0 8px rgba(255, 255, 255, 0.3);
        position: relative;
        white-space: nowrap;
        line-height: 1.2;
    }
    
    .chart-content {
        padding: 8px 28px;
        position: relative;
    }
    
    .metric-card {
        background: rgba(30, 41, 59, 0.4) !important;
        backdrop-filter: blur(25px) !important;
        border: 1px solid rgba(255, 255, 255, 0.15) !important;
        border-radius: 16px !important;
        padding: 24px !important;
        position: relative !important;
        overflow: hidden !important;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
        cursor: pointer !important;
        margin-bottom: 16px !important;
        width: 100% !important;
        box-sizing: border-box !important;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2) !important;
    }
    
    .metric-card:hover {
        border-color: rgba(0, 212, 255, 0.4) !important;
        box-shadow: 0 8px 32px rgba(0, 212, 255, 0.15), 0 0 0 1px rgba(0, 212, 255, 0.2) !important;
        transform: translateY(-3px) !important;
        background: rgba(30, 41, 59, 0.6) !important;
    }
    
    .metric-label {
        color: #94a3b8 !important;
        font-size: 12px !important;
        font-weight: 600 !important;
        text-transform: uppercase !important;
        letter-spacing: 1px !important;
        margin-bottom: 10px !important;
    }
    
    .metric-value {
        color: #f1f5f9 !important;
        font-size: 28px !important;
        font-weight: 800 !important;
        line-height: 1.1 !important;
        margin-bottom: 6px !important;
        text-shadow: 0 0 15px rgba(255, 255, 255, 0.1);
    }
    
    .metric-delta {
        font-size: 14px !important;
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
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 6px 24px rgba(0, 0, 0, 0.2);
    }
    
    .stPlotlyChart .modebar {
        background: transparent !important;
        transform: translateY(10px) !important;
    }
    
    .stPlotlyChart .modebar-group {
        background: transparent !important;
    }
    
    /* Chart control styles */
    .chart-controls {
        display: flex;
        gap: 12px;
        margin-bottom: 12px;
        padding: 0 28px;
        flex-wrap: wrap;
    }
    
    .control-group {
        display: flex;
        align-items: center;
        gap: 8px;
        background: rgba(30, 41, 59, 0.6);
        padding: 6px 12px;
        border-radius: 8px;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .control-label {
        font-size: 12px;
        color: #94a3b8;
        font-weight: 600;
    }
    
    .control-option {
        font-size: 12px;
        padding: 4px 8px;
        border-radius: 6px;
        cursor: pointer;
        transition: all 0.2s ease;
    }
    
    .control-option:hover {
        background: rgba(255, 255, 255, 0.1);
    }
    
    .control-option.active {
        background: rgba(0, 212, 255, 0.2);
        color: #00d4ff;
        font-weight: 600;
    }
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display: none;}
</style>
""", unsafe_allow_html=True)

# Calculate current metrics for later use
current_price = price_df['Price'].iloc[-1]
last_date = price_df['Date'].iloc[-1]
thirty_days_ago = last_date - timedelta(days=30)
df_30_days_ago = price_df[price_df['Date'] >= thirty_days_ago]

if len(df_30_days_ago) > 0:
    price_30_days_ago = df_30_days_ago['Price'].iloc[0]
    price_pct_change = ((current_price - price_30_days_ago) / price_30_days_ago) * 100
else:
    price_pct_change = 0

# Simplified header section with just title
st.markdown('<div class="header-section">', unsafe_allow_html=True)
st.markdown('<div class="title-container"><h1 class="main-title">Kaspa Price</h1></div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Initialize session state for chart controls if not already set
if 'y_scale' not in st.session_state:
    st.session_state.y_scale = "log"
if 'x_scale' not in st.session_state:
    st.session_state.x_scale = "linear"
if 'time_range' not in st.session_state:
    st.session_state.time_range = "all"
if 'show_power_law' not in st.session_state:
    st.session_state.show_power_law = True

# Create controls above the chart
with st.container():
    st.markdown('<div class="chart-controls">', unsafe_allow_html=True)
    
    # Price Scale
    st.markdown('<div class="control-group"><span class="control-label">Price Scale:</span>', unsafe_allow_html=True)
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("Linear", key="linear_y"):
            st.session_state.y_scale = "linear"
    with col2:
        if st.button("Log", key="log_y"):
            st.session_state.y_scale = "log"
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Time Scale
    st.markdown('<div class="control-group"><span class="control-label">Time Scale:</span>', unsafe_allow_html=True)
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("Linear", key="linear_x"):
            st.session_state.x_scale = "linear"
    with col2:
        if st.button("Log", key="log_x"):
            st.session_state.x_scale = "log"
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Time Range
    st.markdown('<div class="control-group"><span class="control-label">Time Range:</span>', unsafe_allow_html=True)
    col1, col2, col3, col4, col5, col6 = st.columns([1, 1, 1, 1, 1, 1])
    with col1:
        if st.button("1W", key="1w"):
            st.session_state.time_range = "1w"
    with col2:
        if st.button("1M", key="1m"):
            st.session_state.time_range = "1m"
    with col3:
        if st.button("3M", key="3m"):
            st.session_state.time_range = "3m"
    with col4:
        if st.button("6M", key="6m"):
            st.session_state.time_range = "6m"
    with col5:
        if st.button("1Y", key="1y"):
            st.session_state.time_range = "1y"
    with col6:
        if st.button("All", key="all"):
            st.session_state.time_range = "all"
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Power Law Toggle
    st.markdown('<div class="control-group"><span class="control-label">Power Law:</span>', unsafe_allow_html=True)
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("Show", key="show_pl"):
            st.session_state.show_power_law = True
    with col2:
        if st.button("Hide", key="hide_pl"):
            st.session_state.show_power_law = False
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Filter data based on time range
last_date = price_df['Date'].iloc[-1]
if st.session_state.time_range == "1w":
    start_date = last_date - timedelta(days=7)
elif st.session_state.time_range == "1m":
    start_date = last_date - timedelta(days=30)
elif st.session_state.time_range == "3m":
    start_date = last_date - timedelta(days=90)
elif st.session_state.time_range == "6m":
    start_date = last_date - timedelta(days=180)
elif st.session_state.time_range == "1y":
    start_date = last_date - timedelta(days=365)
else:  # "all"
    start_date = price_df['Date'].iloc[0]

filtered_df = price_df[price_df['Date'] >= start_date]

# Create the figure
fig = go.Figure()

# Determine x-axis values based on scale
if st.session_state.x_scale == "log":
    x_values = filtered_df['days_from_genesis']
    x_title = "Days Since Genesis (Log Scale)"
else:
    x_values = filtered_df['Date']
    x_title = "Date"

# Add price trace
fig.add_trace(go.Scatter(
    x=x_values,
    y=filtered_df['Price'],
    mode='lines',
    name='Kaspa Price (USD)',
    line=dict(color='#00d4ff', width=3, shape='spline', smoothing=0.3),
    hovertemplate='<b>%{fullData.name}</b><br>%{text}<br>Price: $%{y:.6f}<br><extra></extra>',
    text=[d.strftime('%Y-%m-%d') for d in filtered_df['Date']],
    showlegend=True
))

# Add power law if enabled
if st.session_state.show_power_law:
    x_fit_days = filtered_df['days_from_genesis']
    y_fit = a_price * np.power(x_fit_days, b_price)
    
    fig.add_trace(go.Scatter(
        x=x_values,
        y=y_fit,
        mode='lines',
        name=f'Power Law Fit (R²={r2_price:.3f})',
        line=dict(color='#ff8c00', width=3, dash='solid'),
        hovertemplate='<b>Power Law Fit</b><br>R² = %{customdata:.3f}<br>Value: $%{y:.6f}<br><extra></extra>',
        customdata=[r2_price] * len(x_values),
        showlegend=True
    ))
    
    # Add support and resistance bands
    fig.add_trace(go.Scatter(
        x=x_values,
        y=y_fit * 0.4,
        mode='lines',
        name='Support (-60%)',
        line=dict(color='rgba(255, 255, 255, 0.7)', width=1.5, dash='dot'),
        hoverinfo='skip',
        showlegend=True
    ))
    
    fig.add_trace(go.Scatter(
        x=x_values,
        y=y_fit * 2.2,
        mode='lines',
        name='Resistance (+120%)',
        line=dict(color='rgba(255, 255, 255, 0.7)', width=1.5, dash='dot'),
        fill='tonexty',
        fillcolor='rgba(100, 100, 100, 0.05)',
        hoverinfo='skip',
        showlegend=True
    ))

# Custom Y-axis tick formatting function
def format_currency(value):
    """Format currency values for clean display"""
    if value >= 1:
        if value >= 1000:
            return f"${value/1000:.1f}k"
        elif value >= 100:
            return f"${value:.0f}"
        elif value >= 10:
            return f"${value:.1f}"
        else:
            return f"${value:.2f}"
    elif value >= 0.01:
        return f"${value:.3f}"
    elif value >= 0.001:
        return f"${value:.4f}"
    elif value >= 0.0001:
        return f"${value:.5f}"
    else:
        return f"${value:.1e}"

# Generate custom tick values for log scale Y-axis
def generate_log_ticks(data_min, data_max):
    """Generate physics-style log tick marks with 1, 2, 5 pattern"""
    import math
    log_min = math.floor(math.log10(data_min))
    log_max = math.ceil(math.log10(data_max))
    
    major_ticks = []
    intermediate_ticks = []
    minor_ticks = []
    
    for i in range(log_min, log_max + 1):
        base = 10**i
        
        if data_min <= base <= data_max:
            major_ticks.append(base)
        
        for factor in [2, 5]:
            intermediate_val = factor * base
            if data_min <= intermediate_val <= data_max:
                intermediate_ticks.append(intermediate_val)
        
        for j in [3, 4, 6, 7, 8, 9]:
            minor_val = j * base
            if data_min <= minor_val <= data_max:
                minor_ticks.append(minor_val)
    
    return major_ticks, intermediate_ticks, minor_ticks

# Setup Y-axis ticks based on scale
y_min, y_max = filtered_df['Price'].min(), filtered_df['Price'].max()
if st.session_state.y_scale == "log":
    y_major_ticks, y_intermediate_ticks, y_minor_ticks = generate_log_ticks(y_min, y_max)
    y_tick_vals = sorted(y_major_ticks + y_intermediate_ticks)
    y_tick_text = [format_currency(val) for val in y_tick_vals]
else:
    y_tick_vals = None
    y_tick_text = None
    y_minor_ticks = []

# Update layout
fig.update_layout(
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    font=dict(family='Inter', color='#e2e8f0'),
    hovermode='x unified',
    height=700,
    margin=dict(l=30, r=30, t=30, b=10),
    xaxis=dict(
        title=dict(text=x_title, font=dict(size=13, color='#cbd5e1', weight=600), standoff=35),
        type=st.session_state.x_scale,
        showgrid=True,
        gridwidth=1.2,
        gridcolor='rgba(255, 255, 255, 0.08)',
        linecolor='rgba(255, 255, 255, 0.15)',
        tickfont=dict(size=11, color='#94a3b8'),
    ),
    yaxis=dict(
        title=None,
        type=st.session_state.y_scale,
        showgrid=True,
        gridwidth=1.2,
        gridcolor='rgba(255, 255, 255, 0.12)',
        linecolor='rgba(255, 255, 255, 0.15)',
        tickfont=dict(size=11, color='#94a3b8'),
        tickmode='array',
        tickvals=y_tick_vals,
        ticktext=y_tick_text,
        minor=dict(
            showgrid=True,
            gridwidth=0.5,
            gridcolor='rgba(255, 255, 255, 0.04)',
            tickmode='array',
            tickvals=y_minor_ticks
        )
    ),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="left",
        x=0,
        bgcolor='rgba(0,0,0,0)',
        bordercolor='rgba(0,0,0,0)',
        borderwidth=0,
        font=dict(size=11)
    ),
    hoverlabel=dict(
        bgcolor='rgba(15, 20, 25, 0.95)',
        bordercolor='rgba(0, 212, 255, 0.5)',
        font=dict(color='#e2e8f0', size=11),
        align='left'
    )
)

# Display chart
with st.container():
    st.plotly_chart(fig, use_container_width=True, config={
        'displayModeBar': True,
        'displaylogo': False,
        'modeBarButtonsToRemove': ['lasso2d', 'select2d'],
        'modeBarButtonsToAdd': ['hoverclosest', 'hovercompare'],
        'toImageButtonOptions': {
            'format': 'png',
            'filename': f'kaspa_analysis_{datetime.now().strftime("%Y%m%d_%H%M")}',
            'height': 650,
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

# Enhanced Metrics Section with improved styling and hover effects
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
    metric_html = f"""
    <div class="metric-card">
        <div class="metric-label">CURRENT PRICE</div>
        <div class="metric-value">${current_price:.6f}</div>
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
<div style="text-align: center; padding: 40px 40px; margin-top: 32px; 
     background: rgba(15, 20, 25, 0.3); backdrop-filter: blur(20px);
     border-top: 1px solid rgba(255, 255, 255, 0.08);">
    <div style="max-width: 1200px; margin: 0 auto;">
        <p style="color: #64748b; font-size: 13px; margin-bottom: 16px;">
            Professional-grade cryptocurrency market analysis • Real-time data processing • Advanced predictive modeling
        </p>
        <div style="color: #475569; font-size: 10px; text-transform: uppercase; letter-spacing: 1px;">
            Last Updated: """ + datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC') + """ • 
            Built for institutional-grade analysis
        </div>
    </div>
</div>
"""

st.markdown(footer_html, unsafe_allow_html=True)
