import streamlit as st
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from utils import fit_power_law, load_price_data
from lightweight_charts import Chart

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

# Custom CSS with top padding adjustment
st.markdown("""
<style>
    /* Reset all margins and padding */
    html, body, .stApp, .main, .block-container {
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
    .lightweight-charts {
        width: 100% !important;
        height: 700px !important;
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
        padding-left: 60px !important; 
        margin-bottom: 10px !important;
    }
    
    /* Metrics styling */
    div[data-testid="stMetric"] {
        background-color: #1A1D26 !important;
        border: 1px solid #3A3C4A !important;
        border-radius: 8px !important;
        padding: 15px 20px !important;
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
    
    /* Lightweight Charts specific styling */
    .tv-lightweight-charts {
        border: none !important;
    }
</style>
""", unsafe_allow_html=True)

# ====== MAIN CHART CONTAINER ======
with st.container():
    st.markdown('<div class="title-spacing"><h2>Kaspa Price</h2></div>', unsafe_allow_html=True)
    
    # Dropdown container
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

    filtered_df = price_df[price_df['Date'] >= start_date].copy()
    
    # Convert dates to timestamps for Lightweight Charts
    filtered_df['timestamp'] = filtered_df['Date'].astype(np.int64) // 10**9
    
    # Create chart data
    chart_data = filtered_df[['timestamp', 'Price']].rename(columns={'Price': 'close'})
    chart_data['open'] = chart_data['close']
    chart_data['high'] = chart_data['close']
    chart_data['low'] = chart_data['close']
    
    # Create the chart
    chart = Chart()
    
    # Set chart options
    chart.set_options({
        'layout': {
            'background_color': '#1A1D26',
            'text_color': '#e0e0e0',
        },
        'right_price_scale': {
            'scale_mode': 2 if y_scale == "Log" else 1,  # 2 = Log, 1 = Linear
            'border_color': '#3A3C4A',
        },
        'time_scale': {
            'time_visible': True,
            'seconds_visible': False,
            'border_color': '#3A3C4A',
        },
        'grid': {
            'vert_lines': {
                'color': 'rgba(255, 255, 255, 0.1)',
            },
            'horz_lines': {
                'color': 'rgba(255, 255, 255, 0.1)',
            },
        },
        'crosshair': {
            'mode': 1,  # Normal mode
        },
        'handle_scroll': {
            'mouse_wheel': True,
            'pressed_mouse_move': True,
            'horz_touch_drag': True,
            'vert_touch_drag': True,
        },
    })
    
    # Add the main price line
    line = chart.line(chart_data)
    line.set_options({
        'color': '#00FFCC',
        'lineWidth': 2,
        'priceLineVisible': False,
        'lastValueVisible': False,
        'crosshairMarkerVisible': True,
        'crosshairMarkerRadius': 4,
    })
    
    # Add power law fit if enabled
    if show_power_law == "Show":
        filtered_df['power_law'] = a_price * np.power(filtered_df['days_from_genesis'], b_price)
        power_law_data = filtered_df[['timestamp', 'power_law']].rename(columns={'power_law': 'close'})
        power_law_data['open'] = power_law_data['close']
        power_law_data['high'] = power_law_data['close']
        power_law_data['low'] = power_law_data['close']
        
        power_law_line = chart.line(power_law_data)
        power_law_line.set_options({
            'color': '#FFA726',
            'lineWidth': 2,
            'lineStyle': 1,  # Dashed line
            'priceLineVisible': False,
            'lastValueVisible': False,
            'crosshairMarkerVisible': True,
            'crosshairMarkerRadius': 4,
        })
        
        # Add deviation bands
        filtered_df['upper_band'] = filtered_df['power_law'] * 2.2
        filtered_df['lower_band'] = filtered_df['power_law'] * 0.4
        
        upper_band_data = filtered_df[['timestamp', 'upper_band']].rename(columns={'upper_band': 'close'})
        lower_band_data = filtered_df[['timestamp', 'lower_band']].rename(columns={'lower_band': 'close'})
        
        upper_band = chart.line(upper_band_data)
        upper_band.set_options({
            'color': 'rgba(255, 255, 255, 0.5)',
            'lineWidth': 1,
            'lineStyle': 1,  # Dashed line
            'priceLineVisible': False,
            'lastValueVisible': False,
            'crosshairMarkerVisible': False,
        })
        
        lower_band = chart.line(lower_band_data)
        lower_band.set_options({
            'color': 'rgba(255, 255, 255, 0.5)',
            'lineWidth': 1,
            'lineStyle': 1,  # Dashed line
            'priceLineVisible': False,
            'lastValueVisible': False,
            'crosshairMarkerVisible': False,
        })
        
        # Add area between bands
        band_data = filtered_df[['timestamp', 'upper_band', 'lower_band']].copy()
        band_data['value'] = band_data['upper_band'] - band_data['lower_band']
        
        band_area = chart.area(band_data)
        band_area.set_options({
            'topColor': 'rgba(100, 100, 100, 0.2)',
            'bottomColor': 'rgba(100, 100, 100, 0)',
            'lineColor': 'rgba(100, 100, 100, 0)',
            'priceLineVisible': False,
            'lastValueVisible': False,
            'crosshairMarkerVisible': False,
        })
    
    # Display the chart
    chart_html = chart.get_script()
    st.components.v1.html(chart_html, height=700)

# Stats
st.markdown('<div class="metrics-container">', unsafe_allow_html=True)
cols = st.columns(3)
with cols[0]:
    st.metric("Power-Law Slope", f"{b_price:.3f}")
with cols[1]:
    st.metric("Model Fit (R²)", f"{r2_price:.3f}")
with cols[2]:
    st.metric("Current Price", f"${price_df['Price'].iloc[-1]:.4f}")
st.markdown('</div>', unsafe_allow_html=True)
