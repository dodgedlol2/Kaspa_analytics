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
fig.update_
