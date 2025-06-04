import streamlit as st
import sys
import os

# Add the components directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'components'))

from shared_components import render_hover_tabs_sidebar, render_basic_css, render_simple_page_header
from utils import load_data
import plotly.graph_objects as go
import pandas as pd

# Page config
st.set_page_config(
    page_title="Price Analysis - Kaspa Analytics",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply basic CSS
render_basic_css()

# Navigation
selected_page = render_hover_tabs_sidebar()

# Handle navigation
if selected_page != "Price":
    if selected_page == "Home":
        st.switch_page("streamlit/app.py")
    else:
        # Map to correct page files
        page_mapping = {
            "Hashrate Analysis": "2_Hashrate_Analysis.py",
            "Market Cap": "3_MarketCap.py",
            "Kaspa Price vs Trading Volume": "41_Kaspa price vs Trading volume.py",
            "Kaspa Trading Volume": "4_Kaspa Trading Volume.py",
            "Kaspa Price vs Hashrate": "5_Kaspa Price vs Hashrate.py",
            "Kaspa Price Hashrate and PH-Ratio Deviation": "6_Kaspa Price Hashrate and PH-Ratio Deviation.py",
            "Power Law Residual of Kaspa Price Relative to Network Hashrate": "7_Power Law Residual of Kaspa Price Relative to Network Hashrate.py",
            "Test Page": "8_Test Page.py",
            "Wallet Tracker": "9_Wallet Tracker.py"
        }
        
        if selected_page in page_mapping:
            st.switch_page(f"pages/{page_mapping[selected_page]}")

# Main content for Price page
render_simple_page_header("💎 Price Analysis", "Advanced Kaspa price analytics and modeling")

# Your existing price analysis content goes here
try:
    df, genesis_date = load_data()
    
    # Example content - replace with your actual price analysis
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if 'Price' in df.columns:
            current_price = df['Price'].iloc[-1]
            st.metric("Current Price", f"${current_price:.6f}", "5.2%")
        else:
            st.metric("Current Price", "Loading...", "")
    
    with col2:
        st.metric("24h High", "$0.048", "2.1%")
    
    with col3:
        st.metric("24h Low", "$0.042", "-1.8%")
    
    # Add your existing price charts and analysis here
    st.subheader("Price Chart")
    
    if 'Price' in df.columns and 'Date' in df.columns:
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=df['Date'],
            y=df['Price'],
            mode='lines',
            name='Kaspa Price',
            line=dict(color='#00d4ff')
        ))
        
        fig.update_layout(
            title="Kaspa Price Over Time",
            xaxis_title="Date",
            yaxis_title="Price (USD)",
            template="plotly_dark",
            height=500
        )
        
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Price data not available. Check your data source.")
    
except Exception as e:
    st.error(f"Error loading data: {str(e)}")
    st.info("Please check your data connection and try again.")
