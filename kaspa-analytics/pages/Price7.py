import streamlit as st
import plotly.graph_objects as go
import numpy as np
import pandas as pd
from utils import fit_power_law, load_price_data
from datetime import datetime, timedelta
from components.shared_components import (
    render_page_config,
    render_cohesive_css,
    render_styled_header,
    render_styled_sidebar_navigation
)

# MUST be first Streamlit command
render_page_config(page_title="Price Analysis - Kaspa Analytics Pro")

# Apply cohesive CSS that matches your existing design
render_cohesive_css()

# Render styled header that matches your chart sections
render_styled_header(
    user_name=None,  # Change to "John Doe" to test user menu
    show_auth=True
)

# Render styled sidebar navigation
render_styled_sidebar_navigation(current_page="Analytics")

# Data loading (with caching for performance)
@st.cache_data(ttl=300)  # Cache for 5 minutes
def get_price_data():
    try:
        return load_price_data()
    except Exception as e:
        st.error(f"Failed to load price data: {str(e)}")
        st.stop()

# Load data
if 'price_df' not in st.session_state or 'price_genesis_date' not in st.session_state:
    st.session_state.price_df, st.session_state.price_genesis_date = get_price_data()

price_df = st.session_state.price_df
genesis_date = st.session_state.price_genesis_date

# Calculate power law
try:
    a_price, b_price, r2_price = fit_power_law(price_df, y_col='Price')
except Exception as e:
    st.error(f"Failed to calculate price power law: {str(e)}")
    st.stop()

# Chart Section - Your existing styling preserved and enhanced
st.markdown("""
<div class="chart-section">
    <div class="chart-title-section">
        <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 0;">
            <div>
                <h2 style="font-size: 28px; font-weight: 800; background: linear-gradient(135deg, #f1f5f9 0%, #cbd5e1 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin: 0;">
                    Kaspa Price Analysis
                </h2>
            </div>
            <div class="live-indicator">
                <div class="live-dot"></div>
                <span>LIVE</span>
            </div>
        </div>
    </div>
    <div style="padding: 24px 48px; border-bottom: 1px solid rgba(255, 255, 255, 0.1);">
    </div>
</div>
""", unsafe_allow_html=True)

# Controls section with your existing styling
with st.container():
    col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
    
    with col1:
        st.markdown('<div style="color: #94a3b8; font-size: 12px; font-weight: 600; text-transform: uppercase; letter-spacing: 1.2px; margin-bottom: 6px;">Price Scale</div>', unsafe_allow_html=True)
        y_scale = st.selectbox("", ["Linear", "Log"], index=1, label_visibility="collapsed", key="price_y_scale_select")

    with col2:
        st.markdown('<div style="color: #94a3b8; font-size: 12px; font-weight: 600; text-transform: uppercase; letter-spacing: 1.2px; margin-bottom: 6px;">Time Scale</div>', unsafe_allow_html=True)
        x_scale_type = st.selectbox("", ["Linear", "Log"], index=0, label_visibility="collapsed", key="price_x_scale_select")

    with col3:
        st.markdown('<div style="color: #94a3b8; font-size: 12px; font-weight: 600; text-transform: uppercase; letter-spacing: 1.2px; margin-bottom: 6px;">Time Period</div>', unsafe_allow_html=True)
        time_range = st.selectbox("", ["1W", "1M", "3M", "6M", "1Y", "All"], index=5, label_visibility="collapsed", key="price_time_range_select")

    with col4:
        st.markdown('<div style="color: #94a3b8; font-size: 12px; font-weight: 600; text-transform: uppercase; letter-spacing: 1.2px; margin-bottom: 6px;">Power Law</div>', unsafe_allow_html=True)
        show_power_law = st.selectbox("", ["Hide", "Show"], index=1, label_visibility="collapsed", key="price_power_law_select")

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

# Create the enhanced chart with your existing styling
fig = go.Figure()

if x_scale_type == "Log":
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
    hovertemplate='<b>%{fullData.name}</b><br>Date: %{text}<br>Price: $%{y:.6f}<br><extra></extra>',
    text=[d.strftime('%Y-%m-%d') for d in filtered_df['Date']],
    showlegend=True,
    fillcolor='rgba(0, 212, 255, 0.1)'
))

# Add power law if enabled
if show_power_law == "Show":
    x_fit = filtered_df['days_from_genesis']
    y_fit = a_price * np.power(x_fit, b_price)
    fit_x = x_fit if x_scale_type == "Log" else filtered_df['Date']

    fig.add_trace(go.Scatter(
        x=fit_x,
        y=y_fit,
        mode='lines',
        name=f'Power Law Fit (R²={r2_price:.3f})',
        line=dict(color='#ff00a8', width=3, dash='solid'),
        showlegend=True,
        hovertemplate='<b>Power Law Fit</b><br>R² = %{customdata:.3f}<br>Value: $%{y:.6f}<br><extra></extra>',
        customdata=[r2_price] * len(fit_x)
    ))

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

# Enhanced chart layout matching your existing style
fig.update_layout(
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    font=dict(family='Inter', color='#e2e8f0'),
    hovermode='x unified',
    height=700,
    margin=dict(l=40, r=40, t=60, b=0),
    xaxis=dict(
        title=dict(text=x_title, font=dict(size=14, color='#cbd5e1', weight=600), standoff=30),
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
        title=None,
        type="log" if y_scale == "Log" else "linear",
        showgrid=True,
        gridwidth=1,
        gridcolor='rgba(255, 255, 255, 0.08)',
        linecolor='rgba(255, 255, 255, 0.2)',
        tickfont=dict(size=12, color='#94a3b8'),
        tickprefix="$"
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
        font=dict(size=12)
    ),
    hoverlabel=dict(
        bgcolor='rgba(15, 20, 25, 0.95)',
        bordercolor='rgba(0, 212, 255, 0.5)',
        font=dict(color='#e2e8f0', size=12),
        align='left'
    )
)

# Display chart with your existing container styling
st.markdown('<div style="padding: 32px 48px;">', unsafe_allow_html=True)

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

st.markdown('</div>', unsafe_allow_html=True)

# Close the chart section
st.markdown('</div>', unsafe_allow_html=True)

# Calculate comprehensive metrics for your existing metric cards
current_price = price_df['Price'].iloc[-1]
last_date = price_df['Date'].iloc[-1]
thirty_days_ago = last_date - timedelta(days=30)
df_30_days_ago = price_df[price_df['Date'] >= thirty_days_ago]

if len(df_30_days_ago) > 0:
    price_30_days_ago = df_30_days_ago['Price'].iloc[0]
    price_pct_change = ((current_price - price_30_days_ago) / price_30_days_ago) * 100
    
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
    price_pct_change = 0
    slope_pct_change = 0
    r2_pct_change = 0

# Enhanced Metrics Section - Using your existing metric card styling
col1, col2, col3, col4 = st.columns(4)

with col1:
    metric_html = f"""
    <div style="background: rgba(15, 20, 25, 0.7) !important; backdrop-filter: blur(25px) !important; 
         border: 1px solid rgba(255, 255, 255, 0.1) !important; border-radius: 20px !important; 
         padding: 28px !important; position: relative !important; overflow: hidden !important; 
         transition: all 0.5s cubic-bezier(0.4, 0, 0.2, 1) !important; cursor: pointer !important; 
         margin: 20px 20px 20px 0 !important;">
        <div style="color: #94a3b8 !important; font-size: 13px !important; font-weight: 600 !important; 
             text-transform: uppercase !important; letter-spacing: 1.2px !important; margin-bottom: 12px !important;">
            POWER-LAW SLOPE
        </div>
        <div style="color: #f1f5f9 !important; font-size: 36px !important; font-weight: 800 !important; 
             line-height: 1.1 !important; margin-bottom: 6px !important; text-shadow: 0 0 20px rgba(255, 255, 255, 0.1);">
            {b_price:.4f}
        </div>
        <div style="font-size: 15px !important; font-weight: 700 !important; margin-bottom: 8px; 
             color: {'#00ff88' if slope_pct_change >= 0 else '#ff4757'} !important;">
            {slope_pct_change:+.2f}%
        </div>
    </div>
    """
    st.markdown(metric_html, unsafe_allow_html=True)

with col2:
    metric_html = f"""
    <div style="background: rgba(15, 20, 25, 0.7) !important; backdrop-filter: blur(25px) !important; 
         border: 1px solid rgba(255, 255, 255, 0.1) !important; border-radius: 20px !important; 
         padding: 28px !important; position: relative !important; overflow: hidden !important; 
         transition: all 0.5s cubic-bezier(0.4, 0, 0.2, 1) !important; cursor: pointer !important; 
         margin: 20px 10px !important;">
        <div style="color: #94a3b8 !important; font-size: 13px !important; font-weight: 600 !important; 
             text-transform: uppercase !important; letter-spacing: 1.2px !important; margin-bottom: 12px !important;">
            MODEL ACCURACY (R²)
        </div>
        <div style="color: #f1f5f9 !important; font-size: 36px !important; font-weight: 800 !important; 
             line-height: 1.1 !important; margin-bottom: 6px !important; text-shadow: 0 0 20px rgba(255, 255, 255, 0.1);">
            {r2_price:.4f}
        </div>
        <div style="font-size: 15px !important; font-weight: 700 !important; margin-bottom: 8px; 
             color: {'#00ff88' if r2_pct_change >= 0 else '#ff4757'} !important;">
            {r2_pct_change:+.2f}%
        </div>
    </div>
    """
    st.markdown(metric_html, unsafe_allow_html=True)

with col3:
    metric_html = f"""
    <div style="background: rgba(15, 20, 25, 0.7) !important; backdrop-filter: blur(25px) !important; 
         border: 1px solid rgba(255, 255, 255, 0.1) !important; border-radius: 20px !important; 
         padding: 28px !important; position: relative !important; overflow: hidden !important; 
         transition: all 0.5s cubic-bezier(0.4, 0, 0.2, 1) !important; cursor: pointer !important; 
         margin: 20px 10px !important;">
        <div style="color: #94a3b8 !important; font-size: 13px !important; font-weight: 600 !important; 
             text-transform: uppercase !important; letter-spacing: 1.2px !important; margin-bottom: 12px !important;">
            CURRENT PRICE
        </div>
        <div style="color: #f1f5f9 !important; font-size: 36px !important; font-weight: 800 !important; 
             line-height: 1.1 !important; margin-bottom: 6px !important; text-shadow: 0 0 20px rgba(255, 255, 255, 0.1);">
            ${current_price:.6f}
        </div>
        <div style="font-size: 15px !important; font-weight: 700 !important; margin-bottom: 8px; 
             color: {'#00ff88' if price_pct_change >= 0 else '#ff4757'} !important;">
            {price_pct_change:+.2f}%
        </div>
    </div>
    """
    st.markdown(metric_html, unsafe_allow_html=True)

with col4:
    market_cap_estimate = current_price * 24e9
    metric_html = f"""
    <div style="background: rgba(15, 20, 25, 0.7) !important; backdrop-filter: blur(25px) !important; 
         border: 1px solid rgba(255, 255, 255, 0.1) !important; border-radius: 20px !important; 
         padding: 28px !important; position: relative !important; overflow: hidden !important; 
         transition: all 0.5s cubic-bezier(0.4, 0, 0.2, 1) !important; cursor: pointer !important; 
         margin: 20px 0 20px 10px !important;">
        <div style="color: #94a3b8 !important; font-size: 13px !important; font-weight: 600 !important; 
             text-transform: uppercase !important; letter-spacing: 1.2px !important; margin-bottom: 12px !important;">
            EST. MARKET CAP
        </div>
        <div style="color: #f1f5f9 !important; font-size: 36px !important; font-weight: 800 !important; 
             line-height: 1.1 !important; margin-bottom: 6px !important; text-shadow: 0 0 20px rgba(255, 255, 255, 0.1);">
            ${market_cap_estimate/1e9:.2f}B
        </div>
        <div style="font-size: 15px !important; font-weight: 700 !important; margin-bottom: 8px; 
             color: {'#00ff88' if price_pct_change >= 0 else '#ff4757'} !important;">
            {price_pct_change:+.2f}%
        </div>
    </div>
    """
    st.markdown(metric_html, unsafe_allow_html=True)

# Footer matching your existing style
footer_html = f"""
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
            Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')} • 
            Built for institutional-grade analysis
        </div>
    </div>
</div>
"""

st.markdown(footer_html, unsafe_allow_html=True)
