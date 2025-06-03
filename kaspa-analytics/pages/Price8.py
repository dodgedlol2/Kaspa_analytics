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

# Enhanced Custom CSS - Cleaner without dropdown controls
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
    
    .chart-section {
        margin: 20px 40px 28px 40px;
        background: rgba(30, 41, 59, 0.4);
        backdrop-filter: blur(25px);
        border: none;
        border-radius: 16px;
        overflow: hidden;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.25);
        position: relative;
        transition: all 0.3s ease;
    }
    
    .header-section {
        padding: 24px 40px 16px 40px;
        background: transparent;
        text-align: center;
    }
    
    .main-title {
        font-size: 32px;
        font-weight: 800;
        color: #ffffff;
        margin: 0;
        letter-spacing: -0.5px;
        text-shadow: 0 0 20px rgba(255, 255, 255, 0.3);
        background: linear-gradient(135deg, #ffffff 0%, #00d4ff 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .chart-content {
        padding: 8px 28px 24px 28px;
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

# Clean header section - just the title
st.markdown('<div class="header-section">', unsafe_allow_html=True)
st.markdown('<h1 class="main-title">Kaspa Price Analytics</h1>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Chart content section
st.markdown('<div class="chart-content">', unsafe_allow_html=True)

# Prepare data for different time ranges
def get_filtered_data(time_range):
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
    
    return price_df[price_df['Date'] >= start_date]

# Custom Y-axis tick formatting function
def format_currency(value):
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

def generate_log_ticks(data_min, data_max):
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

# Create the enhanced chart with Plotly controls
fig = go.Figure()

# Create data for all time ranges
time_ranges = ["1W", "1M", "3M", "6M", "1Y", "All"]
all_data = {}
for tr in time_ranges:
    all_data[tr] = get_filtered_data(tr)

# Start with "All" data
current_data = all_data["All"]

# Add main price trace
fig.add_trace(go.Scatter(
    x=current_data['Date'],
    y=current_data['Price'],
    mode='lines',
    name='Kaspa Price (USD)',
    line=dict(color='#00d4ff', width=3, shape='spline', smoothing=0.3),
    hovertemplate='<b>%{fullData.name}</b><br>Date: %{text}<br>Price: $%{y:.6f}<br><extra></extra>',
    text=[d.strftime('%Y-%m-%d') for d in current_data['Date']],
    showlegend=True,
    visible=True
))

# Add power law traces (initially visible)
x_fit = current_data['days_from_genesis']
y_fit = a_price * np.power(x_fit, b_price)

fig.add_trace(go.Scatter(
    x=current_data['Date'],
    y=y_fit,
    mode='lines',
    name=f'Power Law Fit (R²={r2_price:.3f})',
    line=dict(color='#ff8c00', width=3, dash='solid'),
    showlegend=True,
    hovertemplate='<b>Power Law Fit</b><br>R² = %{customdata:.3f}<br>Value: $%{y:.6f}<br><extra></extra>',
    customdata=[r2_price] * len(x_fit),
    visible=True
))

fig.add_trace(go.Scatter(
    x=current_data['Date'],
    y=y_fit * 0.4,
    mode='lines',
    name='Support (-60%)',
    line=dict(color='rgba(255, 255, 255, 0.7)', width=1.5, dash='dot'),
    showlegend=True,
    hoverinfo='skip',
    visible=True
))

fig.add_trace(go.Scatter(
    x=current_data['Date'],
    y=y_fit * 2.2,
    mode='lines',
    name='Resistance (+120%)',
    line=dict(color='rgba(255, 255, 255, 0.7)', width=1.5, dash='dot'),
    fill='tonexty',
    fillcolor='rgba(100, 100, 100, 0.05)',
    showlegend=True,
    hoverinfo='skip',
    visible=True
))

# Enhanced chart layout with Plotly controls
fig.update_layout(
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    font=dict(family='Inter', color='#e2e8f0'),
    hovermode='x unified',
    height=700,
    margin=dict(l=30, r=30, t=80, b=40),
    
    # Add range selector buttons for time periods
    xaxis=dict(
        title=dict(text="Date", font=dict(size=13, color='#cbd5e1', weight=600), standoff=25),
        showgrid=True,
        gridwidth=1.2,
        gridcolor='rgba(255, 255, 255, 0.08)',
        linecolor='rgba(255, 255, 255, 0.15)',
        tickfont=dict(size=11, color='#94a3b8'),
        rangeselector=dict(
            buttons=list([
                dict(count=7, label="1W", step="day", stepmode="backward"),
                dict(count=30, label="1M", step="day", stepmode="backward"),
                dict(count=90, label="3M", step="day", stepmode="backward"),
                dict(count=180, label="6M", step="day", stepmode="backward"),
                dict(count=365, label="1Y", step="day", stepmode="backward"),
                dict(step="all", label="All")
            ]),
            bgcolor='rgba(30, 41, 59, 0.8)',
            bordercolor='rgba(255, 255, 255, 0.2)',
            borderwidth=1,
            font=dict(color='#e2e8f0', size=11),
            activecolor='rgba(0, 212, 255, 0.3)',
            x=0,
            y=1.12,
            xanchor='left',
            yanchor='top'
        ),
        rangeslider=dict(visible=False)
    ),
    
    yaxis=dict(
        title=None,
        showgrid=True,
        gridwidth=1.2,
        gridcolor='rgba(255, 255, 255, 0.08)',
        linecolor='rgba(255, 255, 255, 0.15)',
        tickfont=dict(size=11, color='#94a3b8'),
        type="linear"
    ),
    
    # Add update menus for scale controls
    updatemenus=[
        # Y-axis scale toggle
        dict(
            type="buttons",
            direction="right",
            x=0,
            y=1.08,
            xanchor='left',
            yanchor='top',
            bgcolor='rgba(30, 41, 59, 0.8)',
            bordercolor='rgba(255, 255, 255, 0.2)',
            borderwidth=1,
            font=dict(color='#e2e8f0', size=11),
            buttons=list([
                dict(label="Linear", method="relayout", args=[{"yaxis.type": "linear"}]),
                dict(label="Log", method="relayout", args=[{"yaxis.type": "log"}]),
            ]),
            showactive=True,
            active=0,
        ),
        # X-axis scale toggle
        dict(
            type="buttons",
            direction="right",
            x=0.15,
            y=1.08,
            xanchor='left',
            yanchor='top',
            bgcolor='rgba(30, 41, 59, 0.8)',
            bordercolor='rgba(255, 255, 255, 0.2)',
            borderwidth=1,
            font=dict(color='#e2e8f0', size=11),
            buttons=list([
                dict(label="Date", method="relayout", args=[{"xaxis.title.text": "Date"}]),
                dict(label="Log Days", method="relayout", args=[{"xaxis.title.text": "Days Since Genesis (Log)", "xaxis.type": "log"}]),
            ]),
            showactive=True,
            active=0,
        ),
        # Power Law toggle
        dict(
            type="buttons",
            direction="right",
            x=0.35,
            y=1.08,
            xanchor='left',
            yanchor='top',
            bgcolor='rgba(30, 41, 59, 0.8)',
            bordercolor='rgba(255, 255, 255, 0.2)',
            borderwidth=1,
            font=dict(color='#e2e8f0', size=11),
            buttons=list([
                dict(
                    label="Show Power Law",
                    method="restyle",
                    args=[{"visible": [True, True, True, True]}]
                ),
                dict(
                    label="Hide Power Law",
                    method="restyle",
                    args=[{"visible": [True, False, False, False]}]
                ),
            ]),
            showactive=True,
            active=0,
        ),
    ],
    
    # Add annotations for button labels
    annotations=[
        dict(text="Y-Scale:", x=0, y=1.14, xref="paper", yref="paper", 
             showarrow=False, font=dict(size=11, color='#94a3b8'), xanchor='left'),
        dict(text="X-Scale:", x=0.15, y=1.14, xref="paper", yref="paper", 
             showarrow=False, font=dict(size=11, color='#94a3b8'), xanchor='left'),
        dict(text="Power Law:", x=0.35, y=1.14, xref="paper", yref="paper", 
             showarrow=False, font=dict(size=11, color='#94a3b8'), xanchor='left'),
    ],
    
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1,
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
            'height': 750,
            'width': 1400,
            'scale': 2
        }
    })

st.markdown('</div>', unsafe_allow_html=True)

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
