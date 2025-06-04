import streamlit as st
import plotly.graph_objects as go
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import sys
import os

# Add the parent directory to the Python path to find components folder
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
components_dir = os.path.join(parent_dir, 'components')
sys.path.append(parent_dir)
sys.path.append(components_dir)

try:
    from components.shared_components import render_page_config, render_custom_css_with_sidebar, render_clean_header, render_beautiful_sidebar
except ImportError:
    try:
        # Alternative import if the above doesn't work
        import importlib.util
        spec = importlib.util.spec_from_file_location("shared_components", os.path.join(components_dir, "shared_components.py"))
        shared_components = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(shared_components)
        render_page_config = shared_components.render_page_config
        render_custom_css_with_sidebar = shared_components.render_custom_css_with_sidebar
        render_clean_header = shared_components.render_clean_header
        render_beautiful_sidebar = shared_components.render_beautiful_sidebar
    except Exception as e:
        st.error(f"Cannot import shared_components from components folder. Error: {str(e)}")
        st.error(f"Looking in: {components_dir}")
        st.stop()

try:
    from utils import fit_power_law, load_price_data
except ImportError:
    st.error("Cannot import utils. Please ensure utils.py is available.")
    st.stop()

# Set page config
render_page_config(
    page_title="Kaspa Analytics Pro",
    page_icon="💎"
)

# Render the CSS (this now includes all the necessary styles)
render_custom_css_with_sidebar()

# Render header and sidebar
render_clean_header()
render_beautiful_sidebar(current_page="Price")

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

# Header section with title and controls on the same line
st.markdown('<div class="header-section">', unsafe_allow_html=True)

# Column structure with spacing controls:
# [Left Space] [Title] [Middle Space] [Controls: Price Scale | Time Scale | Time Period | Power Law]
left_space, title_col, middle_space, ctrl_col1, ctrl_col2, ctrl_col3, ctrl_col4 = st.columns([0.1, 1, 5, 1, 1, 1, 1])

# Left invisible spacing column
with left_space:
    st.empty()  # Creates invisible space to the left of title

# Title column
with title_col:
    st.markdown('<div class="title-container"><h1 class="main-title">Kaspa Price</h1></div>', unsafe_allow_html=True)

# Middle invisible spacing column
with middle_space:
    st.empty()  # Creates invisible space between title and controls

# Control columns
with ctrl_col1:
    st.markdown('<div class="control-group"><div class="control-label">Price Scale</div>', unsafe_allow_html=True)
    y_scale = st.selectbox("", ["Linear", "Log"], index=1, label_visibility="collapsed", key="price_y_scale_select")
    st.markdown('</div>', unsafe_allow_html=True)

# Add JavaScript to force selectbox styling after Streamlit renders
st.markdown("""
<script>
setTimeout(function() {
    // Target all selectbox containers
    const selectboxes = document.querySelectorAll('.stSelectbox, [data-baseweb="select"]');
    
    selectboxes.forEach(selectbox => {
        // Apply styling to the selectbox and its children
        const applyStyles = (element) => {
            if (element && element.style) {
                element.style.background = 'linear-gradient(135deg, rgba(30, 41, 59, 0.9) 0%, rgba(15, 23, 42, 0.9) 100%)';
                element.style.border = '2px solid rgba(100, 116, 139, 0.3)';
                element.style.borderRadius = '12px';
                element.style.backdropFilter = 'blur(15px)';
                element.style.boxShadow = '0 4px 16px rgba(0, 0, 0, 0.2)';
                element.style.color = '#f1f5f9';
                element.style.fontWeight = '600';
                element.style.fontSize = '13px';
                element.style.transition = 'all 0.4s cubic-bezier(0.4, 0, 0.2, 1)';
                element.style.minHeight = '40px';
            }
        };
        
        // Apply to the selectbox itself
        applyStyles(selectbox);
        
        // Apply to child elements
        const children = selectbox.querySelectorAll('div, button, span');
        children.forEach(child => {
            if (child.getAttribute('role') === 'button' || child.closest('[role="button"]')) {
                applyStyles(child);
            }
        });
        
        // Add hover effects
        selectbox.addEventListener('mouseenter', () => {
            selectbox.style.borderColor = '#00d4ff';
            selectbox.style.boxShadow = '0 8px 32px rgba(0, 212, 255, 0.2), 0 0 0 1px rgba(0, 212, 255, 0.3)';
            selectbox.style.transform = 'translateY(-2px)';
        });
        
        selectbox.addEventListener('mouseleave', () => {
            selectbox.style.borderColor = 'rgba(100, 116, 139, 0.3)';
            selectbox.style.boxShadow = '0 4px 16px rgba(0, 0, 0, 0.2)';
            selectbox.style.transform = 'translateY(0)';
        });
    });
}, 500);
</script>
""", unsafe_allow_html=True)

with ctrl_col2:
    st.markdown('<div class="control-group"><div class="control-label">Time Scale</div>', unsafe_allow_html=True)
    x_scale_type = st.selectbox("", ["Linear", "Log"], index=0, label_visibility="collapsed", key="price_x_scale_select")
    st.markdown('</div>', unsafe_allow_html=True)

with ctrl_col3:
    st.markdown('<div class="control-group"><div class="control-label">Time Period</div>', unsafe_allow_html=True)
    time_range = st.selectbox("", ["1W", "1M", "3M", "6M", "1Y", "All"], index=5, label_visibility="collapsed", key="price_time_range_select")
    st.markdown('</div>', unsafe_allow_html=True)

with ctrl_col4:
    st.markdown('<div class="control-group"><div class="control-label">Power Law</div>', unsafe_allow_html=True)
    show_power_law = st.selectbox("", ["Hide", "Show"], index=1, label_visibility="collapsed", key="price_power_law_select")
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Chart content section
st.markdown('<div class="chart-content"></div>', unsafe_allow_html=True)

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
    intermediate_ticks = []  # For 2 and 5
    minor_ticks = []
    
    for i in range(log_min, log_max + 1):
        base = 10**i
        
        # Major tick at 1 * 10^i
        if data_min <= base <= data_max:
            major_ticks.append(base)
        
        # Intermediate ticks at 2 and 5 * 10^i
        for factor in [2, 5]:
            intermediate_val = factor * base
            if data_min <= intermediate_val <= data_max:
                intermediate_ticks.append(intermediate_val)
        
        # Minor ticks at 3, 4, 6, 7, 8, 9 * 10^i
        for j in [3, 4, 6, 7, 8, 9]:
            minor_val = j * base
            if data_min <= minor_val <= data_max:
                minor_ticks.append(minor_val)
    
    return major_ticks, intermediate_ticks, minor_ticks

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

# Add power law if enabled - now with orange color and white dotted bands
if show_power_law == "Show":
    x_fit = filtered_df['days_from_genesis']
    y_fit = a_price * np.power(x_fit, b_price)
    fit_x = x_fit if x_scale_type == "Log" else filtered_df['Date']

    fig.add_trace(go.Scatter(
        x=fit_x,
        y=y_fit,
        mode='lines',
        name=f'Power Law Fit (R²={r2_price:.3f})',
        line=dict(color='#ff8c00', width=3, dash='solid'),  # Orange color
        showlegend=True,
        hovertemplate='<b>Power Law Fit</b><br>R² = %{customdata:.3f}<br>Value: $%{y:.6f}<br><extra></extra>',
        customdata=[r2_price] * len(fit_x)
    ))

    fig.add_trace(go.Scatter(
        x=fit_x,
        y=y_fit * 0.4,
        mode='lines',
        name='Support (-60%)',
        line=dict(color='rgba(255, 255, 255, 0.7)', width=1.5, dash='dot'),  # White dotted
        showlegend=True,
        hoverinfo='skip'
    ))
    
    fig.add_trace(go.Scatter(
        x=fit_x,
        y=y_fit * 2.2,
        mode='lines',
        name='Resistance (+120%)',
        line=dict(color='rgba(255, 255, 255, 0.7)', width=1.5, dash='dot'),  # White dotted
        fill='tonexty',
        fillcolor='rgba(100, 100, 100, 0.05)',
        showlegend=True,
        hoverinfo='skip'
    ))

# Enhanced chart layout with custom tick formatting
y_min, y_max = filtered_df['Price'].min(), filtered_df['Price'].max()

# Generate custom ticks for Y-axis if log scale
if y_scale == "Log":
    y_major_ticks, y_intermediate_ticks, y_minor_ticks = generate_log_ticks(y_min, y_max)
    # Combine major and intermediate ticks for display
    y_tick_vals = sorted(y_major_ticks + y_intermediate_ticks)
    y_tick_text = [format_currency(val) for val in y_tick_vals]
else:
    y_tick_vals = None
    y_tick_text = None
    y_minor_ticks = []

# Generate custom ticks for X-axis if log scale
if x_scale_type == "Log":
    x_min, x_max = filtered_df['days_from_genesis'].min(), filtered_df['days_from_genesis'].max()
    x_major_ticks, x_intermediate_ticks, x_minor_ticks = generate_log_ticks(x_min, x_max)
    # Combine major and intermediate ticks for display
    x_tick_vals = sorted(x_major_ticks + x_intermediate_ticks)
    x_tick_text = [f"{int(val)}" for val in x_tick_vals]
else:
    x_tick_vals = None
    x_tick_text = None
    x_minor_ticks = []

fig.update_layout(
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    font=dict(family='Inter', color='#e2e8f0'),
    hovermode='x unified',
    height=600,
    margin=dict(l=30, r=30, t=40, b=10),
    xaxis=dict(
        title=dict(text=x_title, font=dict(size=13, color='#cbd5e1', weight=600), standoff=35),
        type="log" if x_scale_type == "Log" else None,
        showgrid=True,
        gridwidth=1.2,
        gridcolor='rgba(255, 255, 255, 0.12)' if x_scale_type == "Log" else 'rgba(255, 255, 255, 0.08)',
        linecolor='rgba(255, 255, 255, 0.15)',
        tickfont=dict(size=11, color='#94a3b8'),
        # Physics-style log ticks with 1, 2, 5 pattern
        tickmode='array' if x_scale_type == "Log" else 'auto',
        tickvals=x_tick_vals,
        ticktext=x_tick_text,
        minor=dict(
            showgrid=True,
            gridwidth=0.5,
            gridcolor='rgba(255, 255, 255, 0.04)',
            tickmode='array',
            tickvals=x_minor_ticks if x_scale_type == "Log" else []
        ) if x_scale_type == "Log" else dict()
    ),
    yaxis=dict(
        title=None,
        type="log" if y_scale == "Log" else "linear",
        showgrid=True,
        gridwidth=1.2,
        gridcolor='rgba(255, 255, 255, 0.12)' if y_scale == "Log" else 'rgba(255, 255, 255, 0.08)',
        linecolor='rgba(255, 255, 255, 0.15)',
        tickfont=dict(size=11, color='#94a3b8'),
        # Physics-style log ticks with 1, 2, 5 pattern and custom formatting
        tickmode='array' if y_scale == "Log" else 'auto',
        tickvals=y_tick_vals,
        ticktext=y_tick_text,
        minor=dict(
            showgrid=True,
            gridwidth=0.5,
            gridcolor='rgba(255, 255, 255, 0.04)',
            tickmode='array',
            tickvals=y_minor_ticks if y_scale == "Log" else []
        ) if y_scale == "Log" else dict()
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
