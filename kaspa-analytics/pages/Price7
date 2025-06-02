import streamlit as st
import plotly.graph_objects as go
import numpy as np
import pandas as pd
from utils import fit_power_law, load_price_data
from datetime import datetime, timedelta
from components.shared_components import (
    render_page_config, 
    render_custom_css, 
    render_professional_header,
    render_page_header
)

# MUST be first Streamlit command
render_page_config(page_title="Price Analysis - Kaspa Analytics Pro")

# Apply custom CSS
render_custom_css()

# Render professional header
render_professional_header(
    current_page="Analytics",
    user_name=None,  # Set to "John Doe" when user is logged in
    user_role=None,  # Set to "Pro Plan" etc. when user is logged in
    show_auth=True
)

# Render page-specific header
render_page_header(
    title="Price Analysis",
    subtitle="Advanced power-law modeling and price prediction for Kaspa cryptocurrency",
    show_breadcrumb=True,
    breadcrumb_items=["Dashboard", "Analytics", "Price Analysis"]
)

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

# Chart Section (your existing chart code, but with updated styling)
st.markdown("""
<div style="margin: 0 40px 40px 40px; background: rgba(15, 20, 25, 0.6); 
     backdrop-filter: blur(25px); border: 1px solid rgba(255, 255, 255, 0.15); 
     border-radius: 24px; overflow: hidden; box-shadow: 0 16px 64px rgba(0, 0, 0, 0.4);">
    <div style="background: rgba(30, 41, 59, 0.4); backdrop-filter: blur(15px); 
         border-bottom: 1px solid rgba(255, 255, 255, 0.1); padding: 28px 48px 20px 48px;">
        <div style="display: flex; align-items: center; justify-content: space-between;">
            <h2 style="font-size: 28px; font-weight: 800; color: #f1f5f9; margin: 0;">
                Live Price Chart
            </h2>
            <div style="display: flex; align-items: center; gap: 8px; color: #00ff88; font-size: 13px; font-weight: 600;">
                <div style="width: 8px; height: 8px; background: #00ff88; border-radius: 50%; 
                     animation: pulse 2s infinite; box-shadow: 0 0 10px #00ff88;"></div>
                <span>LIVE</span>
            </div>
        </div>
    </div>
    <div style="padding: 24px 48px; border-bottom: 1px solid rgba(255, 255, 255, 0.1);">
        <!-- Your controls here -->
    </div>
    <div style="padding: 32px 48px;">
        <!-- Your chart will go here -->
    </div>
</div>
""", unsafe_allow_html=True)

# Your existing chart controls and logic here
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

# Your existing chart creation and display code here...
# (I'll keep this shorter for the example, but you'd include all your chart logic)

# Display a simple message for now
st.info("🚀 **Header Updated!** Your chart logic goes here. The header is now modular and can be easily customized across all pages.")

# Example of how metrics could look with the new design
col1, col2, col3, col4 = st.columns(4)

current_price = price_df['Price'].iloc[-1]

with col1:
    st.markdown(f"""
    <div style="background: rgba(15, 20, 25, 0.7); backdrop-filter: blur(25px); 
         border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 20px; 
         padding: 28px; margin: 20px 20px 20px 0;">
        <div style="color: #94a3b8; font-size: 13px; font-weight: 600; 
             text-transform: uppercase; letter-spacing: 1.2px; margin-bottom: 12px;">
            CURRENT PRICE
        </div>
        <div style="color: #f1f5f9; font-size: 36px; font-weight: 800; 
             line-height: 1.1; margin-bottom: 6px;">
            ${current_price:.6f}
        </div>
        <div style="color: #00ff88; font-size: 15px; font-weight: 700;">
            +2.4% (24h)
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div style="background: rgba(15, 20, 25, 0.7); backdrop-filter: blur(25px); 
         border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 20px; 
         padding: 28px; margin: 20px 10px;">
        <div style="color: #94a3b8; font-size: 13px; font-weight: 600; 
             text-transform: uppercase; letter-spacing: 1.2px; margin-bottom: 12px;">
            MODEL ACCURACY
        </div>
        <div style="color: #f1f5f9; font-size: 36px; font-weight: 800; 
             line-height: 1.1; margin-bottom: 6px;">
            {r2_price:.3f}
        </div>
        <div style="color: #00d4ff; font-size: 15px; font-weight: 700;">
            R² Score
        </div>
    </div>
    """, unsafe_allow_html=True)

# Add similar metrics for col3 and col4...
