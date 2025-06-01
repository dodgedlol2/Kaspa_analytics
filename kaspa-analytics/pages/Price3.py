import streamlit as st
import plotly.graph_objects as go
import numpy as np
import pandas as pd
from utils import fit_power_law, load_price_data
from datetime import datetime, timedelta

st.set_page_config(layout="wide")

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

# Custom CSS with top padding adjustment and improved metric alignment
st.markdown("""
<style>
    /* Reset all margins and padding */
    html, body, .stApp, .main, .block-container, .stPlotlyChart {
        margin: 0 !important;
        padding: 0 !important;
    }
    
    .stApp { 
        background-color: #1A1D26;
        overflow: hidden;
        padding-top: 100px !important;
    }
    
    /* Main container adjustments */
    .main .block-container {
        padding-left: 0px !important;
        padding-right: 0px !important;
        max-width: 100% !important;
    }
    
    /* Chart container */
    .stPlotlyChart {
        width: 100% !important;
        padding-left: 0 !important;
        padding-right: 0 !important;
        margin-left: 0 !important;
        margin-right: 0 !important;
    }
    
    /* Remove all borders and spacing */
    .element-container, 
    .st-emotion-cache-1v0mbdj, 
    .st-emotion-cache-1wrcr25,
    .st-emotion-cache-1kyxreq {
        padding: 0 !important;
        margin: 0 !important;
        border: none !important;
    }
    
    /* Force full width for all elements */
    div[data-testid="stVerticalBlock"] > div[data-testid="stVerticalBlockBorderWrapper"] {
        padding: 0 !important;
        margin: 0 !important;
        border: none !important;
    }
    
    /* Title spacing */
    .title-spacing { 
        padding-top: 50px !important;
        padding-left: 50px !important; 
        margin-bottom: 10px !important;
    }
    
    /* Metrics styling - Updated with teal color scheme and improved alignment */
    div[data-testid="stMetric"] {
        background-color: #1A1D26 !important;
        border: 1px solid #00FFCC !important;
        border-radius: 12px !important;
        padding: 20px !important;
        text-align: left !important;
        box-shadow: 0 2px 8px rgba(0, 255, 204, 0.1) !important;
        transition: all 0.3s ease !important;
        display: flex !important;
        flex-direction: column !important;
        align-items: flex-start !important;
    }
    
    div[data-testid="stMetric"]:hover {
        border-color: #00E6B8 !important;
        box-shadow: 0 4px 16px rgba(0, 255, 204, 0.2) !important;
        transform: translateY(-2px) !important;
    }
    
    /* Metric label styling */
    div[data-testid="stMetric"] label {
        color: #e0e0e0 !important;
        font-size: 14px !important;
        font-weight: 500 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.5px !important;
        margin-bottom: 8px !important;
        text-align: left !important;
        width: 100% !important;
    }
    
    /* Metric value styling */
    div[data-testid="stMetric"] div[data-testid="metric-container"] > div {
        color: #00FFCC !important;
        font-size: 24px !important;
        font-weight: 900 !important;
        line-height: 1.2 !important;
        text-align: left !important;
        width: 100% !important;
    }
    
    /* Delta styling for percentage changes */
    div[data-testid="stMetric"] div[data-testid="metric-container"] div[data-testid="metric-delta"] {
        color: #00FFCC !important;
        font-size: 16px !important;
        font-weight: 600 !important;
        text-align: left !important;
        width: 100% !important;
        margin-top: 4px !important;
    }
    
    /* Ensure all metric content aligns left */
    div[data-testid="stMetric"] * {
        text-align: left !important;
        justify-content: flex-start !important;
    }
    
    /* Make modebar always visible */
    .modebar {
        opacity: 1 !important;
        visibility: visible !important;
        background-color: rgba(26, 29, 38, 0.8) !important;
    }
    
    /* Additional aggressive resets */
    .st-emotion-cache-1kyxreq, 
    .st-emotion-cache-1wrcr25,
    .st-emotion-cache-1v0mbdj {
        padding: 0 !important;
        margin: 0 !important;
    }
    
    /* Remove any remaining Streamlit container padding */
    .st-emotion-cache-1n76uvr {
        padding-left: 0 !important;
        padding-right: 0 !important;
    }
    
    /* Metrics container styling for better alignment */
    .metrics-container {
        padding: 20px 50px !important;
        margin-top: 20px !important;
    }
</style>
""", unsafe_allow_html=True)

# ====== MAIN CHART CONTAINER ======
with st.container():
    st.markdown('<div class="title-spacing"><h2>Kaspa Price</h2></div>', unsafe_allow_html=True)
    
    # Dropdown container - Added spacers as requested
    spacer_left, col1, col2, col3, col4, spacer_right1, spacer_right2, spacer_right3 = st.columns([0.4, 1, 1, 1, 1, 0.5, 0.5, 7])

    with col1:
        st.markdown('<div class="control-label">Price Scale</div>', unsafe_allow_html=True)
        y_scale_options = ["Linear", "Log"]
        y_scale = st.selectbox("Price Scale", y_scale_options,
                             index=1 if st.session_state.get("price_y_scale", True) else 0,
                             label_visibility="collapsed", key="price_y_scale_select")

    with col2:
        st.markdown('<div class="control-label">Time Scale</div>', unsafe_allow_html=True)
        x_scale_options = ["Linear", "Log"]
        x_scale_type = st.selectbox("Time Scale", x_scale_options,
                                  index=0,
                                  label_visibility="collapsed", key="price_x_scale_select")

    with col3:
        st.markdown('<div class="control-label">Period</div>', unsafe_allow_html=True)
        time_ranges = ["1W", "1M", "3M", "6M", "1Y", "All"]
        if 'price_time_range' not in st.session_state:
            st.session_state.price_time_range = "All"
        time_range = st.selectbox("Time Range", time_ranges,
                                index=time_ranges.index(st.session_state.price_time_range),
                                label_visibility="collapsed", key="price_time_range_select")

    with col4:
        st.markdown('<div class="control-label">Power Law Fit</div>', unsafe_allow_html=True)
        power_law_options = ["Hide", "Show"]
        show_power_law = st.selectbox("Power Law Fit", power_law_options,
                                    index=0,
                                    label_visibility="collapsed", key="price_power_law_select")

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
        name='Price',
        line=dict(color='#00FFCC', width=2.5),
        hovertemplate='<b>Date</b>: %{text|%Y-%m-%d}<br><b>Price</b>: $%{y:.4f}<extra></extra>',
        text=filtered_df['Date'],
        showlegend=True
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

    # Display the chart
    st.plotly_chart(fig, use_container_width=True, config={
        'displayModeBar': True,
        'displaylogo': False,
        'modeBarButtonsToRemove': ['lasso2d', 'select2d'],
        'modeBarButtonsToAdd': ['hoverclosest', 'hovercompare'],
    })

# Calculate individual metric changes over 30 days
last_date = price_df['Date'].iloc[-1]
thirty_days_ago = last_date - timedelta(days=30)

# Get data from 30 days ago (or closest available)
df_30_days_ago = price_df[price_df['Date'] >= thirty_days_ago]
if len(df_30_days_ago) > 0:
    # Current values
    current_price = price_df['Price'].iloc[-1]
    current_slope = b_price
    current_r2 = r2_price
    
    # Values from 30 days ago - recalculate power law for 30 days ago data
    price_30_days_ago_data = price_df[price_df['Date'] <= thirty_days_ago]
    if len(price_30_days_ago_data) > 10:  # Need sufficient data for power law fit
        try:
            a_price_30d, b_price_30d, r2_price_30d = fit_power_law(price_30_days_ago_data, y_col='Price')
        except:
            # Fallback to current values if fit fails
            b_price_30d = current_slope
            r2_price_30d = current_r2
    else:
        b_price_30d = current_slope
        r2_price_30d = current_r2
    
    price_30_days_ago = df_30_days_ago['Price'].iloc[0]
    
    # Calculate percentage changes
    price_pct_change = ((current_price - price_30_days_ago) / price_30_days_ago) * 100
    slope_pct_change = ((current_slope - b_price_30d) / abs(b_price_30d)) * 100 if b_price_30d != 0 else 0
    r2_pct_change = ((current_r2 - r2_price_30d) / r2_price_30d) * 100 if r2_price_30d != 0 else 0
    
else:
    # Fallback if not enough historical data
    price_pct_change = 0
    slope_pct_change = 0
    r2_pct_change = 0
    current_price = price_df['Price'].iloc[-1]

# For the 30-day change metric, we show the price change again (as it's specifically about price change)
overall_30d_change = price_pct_change

# Stats - Updated with individual logic for each metric and left alignment
st.markdown('<div class="metrics-container">', unsafe_allow_html=True)
spacer1, col1, col2, col3, col4, spacer2 = st.columns([0.5, 2, 2, 2, 2, 0.5])

with col1:
    st.metric("Power-Law Slope", f"{b_price:.3f}", delta=f"{slope_pct_change:+.1f}%")

with col2:
    st.metric("Model Fit (R²)", f"{r2_price:.3f}", delta=f"{r2_pct_change:+.1f}%")

with col3:
    st.metric("Current Price", f"${current_price:.4f}", delta=f"{price_pct_change:+.1f}%")

with col4:
    st.metric("30D Change", f"{overall_30d_change:+.1f}%", delta=f"{price_pct_change:+.1f}%")

st.markdown('</div>', unsafe_allow_html=True)
