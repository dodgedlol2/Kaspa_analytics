import streamlit as st
import plotly.graph_objects as go
import numpy as np
import pandas as pd
from utils import fit_power_law, load_price_data
from datetime import datetime, timedelta
from components.shared_components import (
    render_page_config,
    render_clean_header,
    render_beautiful_sidebar
)

# MUST be first Streamlit command
render_page_config(page_title="Price Analysis - Kaspa Analytics Pro")

# Render clean header
render_clean_header(
    user_name=None,  # Set to user name if logged in
    show_auth=True
)

# Render beautiful dropdown sidebar
render_beautiful_sidebar(current_page="Price")

# Custom CSS that works WITH shared components but fixes selectbox visibility
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    @import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css');
    
    /* Base styles with background effects */
    html, body, .stApp {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
        background: linear-gradient(135deg, #0a0e1a 0%, #1a1f2e 50%, #0f1419 100%) !important;
        color: #e2e8f0 !important;
        overflow-x: hidden !important;
    }
    
    .stApp {
        background-attachment: fixed !important;
    }
    
    /* Background gradient effects */
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
    
    /* Professional Header */
    .professional-header {
        position: fixed !important;
        top: 0 !important;
        left: 0 !important;
        right: 0 !important;
        width: 100vw !important;
        height: 80px !important;
        background: rgba(15, 20, 25, 0.98) !important;
        backdrop-filter: blur(25px) !important;
        border-bottom: 1px solid rgba(0, 212, 255, 0.2) !important;
        padding: 0 40px !important;
        z-index: 999999999 !important;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.6) !important;
        display: flex !important;
        align-items: center !important;
        justify-content: space-between !important;
    }
    
    .header-content {
        display: flex !important;
        align-items: center !important;
        justify-content: space-between !important;
        width: 100% !important;
        max-width: 1400px !important;
        margin: 0 auto !important;
    }
    
    .brand-section {
        display: flex !important;
        align-items: center !important;
        gap: 15px !important;
    }
    
    .logo {
        width: 45px !important;
        height: 45px !important;
        background: linear-gradient(135deg, #00d4ff 0%, #ff00a8 100%) !important;
        border-radius: 12px !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        font-size: 24px !important;
        color: white !important;
        font-weight: 800 !important;
        box-shadow: 0 4px 15px rgba(0, 212, 255, 0.3) !important;
    }
    
    .brand-text h1 {
        font-size: 26px !important;
        font-weight: 800 !important;
        background: linear-gradient(135deg, #00d4ff 0%, #ff00a8 100%) !important;
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
        margin: 0 !important;
        line-height: 1.1 !important;
    }
    
    .brand-subtitle {
        font-size: 11px !important;
        color: #64748b !important;
        font-weight: 500 !important;
        text-transform: uppercase !important;
        letter-spacing: 1px !important;
        margin-top: 2px !important;
    }
    
    .auth-section {
        display: flex !important;
        align-items: center !important;
        gap: 12px !important;
    }
    
    .login-button {
        background: transparent !important;
        border: 1px solid rgba(100, 116, 139, 0.4) !important;
        border-radius: 10px !important;
        padding: 8px 16px !important;
        color: #cbd5e1 !important;
        font-size: 13px !important;
        font-weight: 600 !important;
        cursor: pointer !important;
        transition: all 0.3s ease !important;
    }
    
    .login-button:hover {
        border-color: rgba(0, 212, 255, 0.6) !important;
        color: #00d4ff !important;
    }
    
    .signup-button {
        background: linear-gradient(135deg, #00d4ff 0%, #0099cc 100%) !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 10px 20px !important;
        color: white !important;
        font-size: 13px !important;
        font-weight: 700 !important;
        cursor: pointer !important;
        box-shadow: 0 4px 15px rgba(0, 212, 255, 0.3) !important;
        transition: all 0.3s ease !important;
    }
    
    .signup-button:hover {
        transform: translateY(-1px) !important;
        box-shadow: 0 6px 20px rgba(0, 212, 255, 0.4) !important;
    }
    
    /* Ultra-simple clean text sidebar */
    section[data-testid="stSidebar"] {
        background: rgba(10, 14, 26, 0.95) !important;
        border-right: 1px solid rgba(0, 212, 255, 0.15) !important;
        margin-top: 100px !important;
        backdrop-filter: blur(25px) !important;
        box-shadow: 8px 0 32px rgba(0, 0, 0, 0.4) !important;
    }
    
    /* Fix sidebar collapse/expand button positioning */
    button[data-testid="collapsedControl"] {
        top: 110px !important;
        left: 8px !important;
        z-index: 999999998 !important;
        background: rgba(15, 20, 25, 0.9) !important;
        border: 1px solid rgba(0, 212, 255, 0.3) !important;
        border-radius: 8px !important;
        width: 32px !important;
        height: 32px !important;
    }
    
    /* Ensure collapse button is always visible */
    .css-1rs6os {
        top: 110px !important;
        left: 8px !important;
        z-index: 999999998 !important;
    }
    
    /* Hide default Streamlit sidebar content */
    section[data-testid="stSidebar"] > div {
        background: transparent !important;
        padding: 16px 12px !important;
    }
    
    /* AGGRESSIVE HIDING OF VIEW MORE/LESS BUTTONS */
    section[data-testid="stSidebar"] button[data-testid="baseButton-minimal"] {
        display: none !important;
    }
    
    section[data-testid="stSidebar"] button:contains("View") {
        display: none !important;
    }
    
    section[data-testid="stSidebar"] .css-1vq4p4l {
        display: none !important;
    }
    
    section[data-testid="stSidebar"] .css-1rs6os.edgvbvh3 {
        display: none !important;
    }
    
    section[data-testid="stSidebar"] button[title*="View"] {
        display: none !important;
    }
    
    section[data-testid="stSidebar"] button[aria-label*="View"] {
        display: none !important;
    }
    
    /* Nuclear option - hide ALL buttons except collapse button */
    section[data-testid="stSidebar"] button:not([data-testid="collapsedControl"]) {
        display: none !important;
    }
    
    /* But make sure collapse button stays visible */
    button[data-testid="collapsedControl"] {
        display: block !important;
    }
    
    /* HIDE ALL STREAMLIT DEFAULT NAVIGATION */
    .css-1d391kg .css-1v3fvcr {
        display: none !important;
    }
    
    .css-1d391kg .css-17eq0hr {
        display: none !important;
    }
    
    nav[data-testid="stSidebarNav"] {
        display: none !important;
    }
    
    .css-1dp5vir {
        display: none !important;
    }
    
    section[data-testid="stSidebar"] nav {
        display: none !important;
    }
    
    section[data-testid="stSidebar"] ul {
        display: none !important;
    }
    
    section[data-testid="stSidebar"] .css-17eq0hr {
        display: none !important;
    }
    
    .stRadio {
        display: none !important;
    }
    
    /* Head metrics styling */
    .head-metric {
        font-size: 12px !important;
        font-weight: 600 !important;
        color: #94a3b8 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.5px !important;
        margin: 16px 0 8px 0 !important;
        cursor: pointer !important;
        transition: color 0.2s ease !important;
        display: flex !important;
        align-items: center !important;
        gap: 8px !important;
    }
    
    .head-metric:hover {
        color: #cbd5e1 !important;
    }
    
    .head-metric:first-child {
        margin-top: 8px !important;
    }
    
    .head-metric i {
        color: #94a3b8 !important;
        font-size: 12px !important;
        width: 16px !important;
        text-align: center !important;
        transition: color 0.2s ease !important;
    }
    
    .head-metric:hover i {
        color: #cbd5e1 !important;
    }
    
    .sub-metric {
        font-size: 12px !important;
        font-weight: 600 !important;
        color: #64748b !important;
        text-transform: uppercase !important;
        letter-spacing: 0.5px !important;
        margin: 4px 0 4px 16px !important;
        cursor: pointer !important;
        transition: color 0.2s ease !important;
        display: flex !important;
        align-items: center !important;
        gap: 8px !important;
    }
    
    .sub-metric:hover {
        color: #94a3b8 !important;
    }
    
    .sub-metric.active {
        color: #00d4ff !important;
    }
    
    .sub-metric i {
        color: #64748b !important;
        font-size: 12px !important;
        width: 16px !important;
        text-align: center !important;
        transition: color 0.2s ease !important;
    }
    
    .sub-metric:hover i {
        color: #94a3b8 !important;
    }
    
    .sub-metric.active i {
        color: #00d4ff !important;
    }
    
    /* Main content adjustments */
    .main .block-container {
        padding-top: 100px !important;
        padding-left: 20px !important;
        padding-right: 20px !important;
        max-width: 100% !important;
    }
    
    /* Chart section styling */
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
    
    .header-section {
        padding: 15px 40px 15px 40px;
        background: transparent;
        display: flex;
        align-items: center;
        justify-content: space-between;
        flex-wrap: wrap;
        gap: 15px;
        margin-bottom: 20px;
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
    
    .control-group {
        display: flex !important;
        flex-direction: column !important;
        gap: 3px !important;
        min-width: 120px !important;
    }
    
    .control-label {
        font-size: 11px;
        font-weight: 600;
        color: #94a3b8;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 0;
        white-space: nowrap;
        line-height: 1;
    }
    
    /* FORCE CHART SELECTBOXES TO BE VISIBLE WITH BEAUTIFUL STYLING - ULTRA SPECIFIC */
    .chart-section .stSelectbox {
        display: block !important;
        visibility: visible !important;
        opacity: 1 !important;
    }
    
    .chart-section .stSelectbox > div {
        display: block !important;
        visibility: visible !important;
        opacity: 1 !important;
    }
    
    .chart-section .stSelectbox > div > div,
    .chart-section div[data-testid="stSelectbox"] > div > div,
    .chart-section .stSelectbox .st-emotion-cache-1s6koen,
    .chart-section .stSelectbox .st-emotion-cache-1mfa4h5 {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.9) 0%, rgba(15, 23, 42, 0.9) 100%) !important;
        border: 2px solid rgba(100, 116, 139, 0.3) !important;
        border-radius: 12px !important;
        backdrop-filter: blur(15px) !important;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: 
            0 4px 16px rgba(0, 0, 0, 0.2) !important,
            0 0 20px rgba(0, 212, 255, 0.1) !important,
            inset 0 1px 0 rgba(255, 255, 255, 0.1) !important;
        min-height: 26px !important;
        width: 150px !important;
        max-width: 250px !important;
        min-width: 100px !important;
        display: block !important;
        visibility: visible !important;
        opacity: 1 !important;
        position: relative !important;
    }
    
    .chart-section .stSelectbox > div > div:hover,
    .chart-section div[data-testid="stSelectbox"] > div > div:hover,
    .chart-section .stSelectbox .st-emotion-cache-1s6koen:hover,
    .chart-section .stSelectbox .st-emotion-cache-1mfa4h5:hover {
        border-color: #00d4ff !important;
        box-shadow: 
            0 8px 32px rgba(0, 212, 255, 0.2) !important, 
            0 0 0 1px rgba(0, 212, 255, 0.3) !important,
            0 0 40px rgba(0, 212, 255, 0.15) !important,
            inset 0 1px 0 rgba(255, 255, 255, 0.2) !important;
        transform: translateY(-2px) !important;
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.95) 0%, rgba(15, 23, 42, 0.95) 100%) !important;
    }
    
    .chart-section .stSelectbox > div > div > div,
    .chart-section div[data-testid="stSelectbox"] > div > div > div {
        color: #f1f5f9 !important;
        font-weight: 600 !important;
        font-size: 13px !important;
        padding: 8px 16px !important;
        text-shadow: 0 0 10px rgba(255, 255, 255, 0.1) !important;
        position: relative !important;
        z-index: 2 !important;
    }
    
    /* Additional override for any emotion cache classes */
    .chart-section [class*="st-emotion-cache"] {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.9) 0%, rgba(15, 23, 42, 0.9) 100%) !important;
        border: 2px solid rgba(100, 116, 139, 0.3) !important;
        border-radius: 12px !important;
        backdrop-filter: blur(15px) !important;
        box-shadow: 
            0 4px 16px rgba(0, 0, 0, 0.2) !important,
            0 0 20px rgba(0, 212, 255, 0.1) !important,
            inset 0 1px 0 rgba(255, 255, 255, 0.1) !important;
    }
    
    .chart-section [class*="st-emotion-cache"]:hover {
        border-color: #00d4ff !important;
        box-shadow: 
            0 8px 32px rgba(0, 212, 255, 0.2) !important, 
            0 0 0 1px rgba(0, 212, 255, 0.3) !important,
            0 0 40px rgba(0, 212, 255, 0.15) !important,
            inset 0 1px 0 rgba(255, 255, 255, 0.2) !important;
        transform: translateY(-2px) !important;
    }
    
    /* Force override any shared component styles */
    .chart-section .stSelectbox * {
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
    }
    
    /* Dropdown arrow styling with more specificity */
    .chart-section .stSelectbox svg,
    .chart-section div[data-testid="stSelectbox"] svg {
        color: #94a3b8 !important;
        transition: all 0.3s ease !important;
        filter: drop-shadow(0 0 5px rgba(0, 212, 255, 0.3)) !important;
    }
    
    .chart-section .stSelectbox:hover svg,
    .chart-section div[data-testid="stSelectbox"]:hover svg {
        color: #00d4ff !important;
        filter: drop-shadow(0 0 8px rgba(0, 212, 255, 0.5)) !important;
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
    
    /* Hide Streamlit elements */
    #MainMenu {visibility: hidden !important;}
    footer {visibility: hidden !important;}
    header {visibility: hidden !important;}
    .stDeployButton {display: none !important;}
    
    /* Responsive design for smaller screens */
    @media (max-width: 1200px) {
        .header-section {
            flex-direction: column;
            align-items: flex-start;
            gap: 12px;
        }
        
        .controls-container {
            width: 100%;
            justify-content: flex-start;
            gap: 16px;
        }
        
        .control-group {
            min-width: 100px;
        }
    }
    
    @media (max-width: 768px) {
        .controls-container {
            gap: 12px;
        }
        
        .control-group {
            min-width: 90px;
        }
        
        .professional-header {
            height: 70px !important;
            padding: 0 20px !important;
        }
        
        .brand-text h1 {
            font-size: 22px !important;
        }
        
        .main .block-container {
            padding-top: 90px !important;
        }
    }
</style>
""", unsafe_allow_html=True)

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
st.markdown('<div class="chart-section">', unsafe_allow_html=True)
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
st.markdown('<div class="chart-content">', unsafe_allow_html=True)

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

# Create the enhanced chart
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
        # Removed rangeslider configuration
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

st.markdown('</div>', unsafe_allow_html=True)
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
