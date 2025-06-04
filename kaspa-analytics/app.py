import streamlit as st
import sys
import os

# Add the components directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'components'))

from shared_components import render_hover_tabs_sidebar
from utils import load_data
from datetime import datetime
import plotly.graph_objects as go
import numpy as np

st.set_page_config(
    page_title="Kaspa Network Analytics",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Force dark mode on first visit
if 'dark_mode' not in st.session_state:
    st.session_state.dark_mode = True

# Enhanced Custom CSS with Modern Design matching Price6 page
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    @import url('https://fonts.googleapis.com/icon?family=Material+Icons');
    
    /* Global Reset and Base Styles */
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }
    
    html, body, .stApp {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        background: linear-gradient(135deg, #0a0e1a 0%, #1a1f2e 50%, #0f1419 100%);
        color: #e2e8f0;
        overflow-x: hidden;
    }
    
    .stApp {
        background-attachment: fixed;
    }
    
    /* Remove Streamlit defaults */
    .main .block-container {
        padding: 2rem 1rem !important;
        max-width: 100% !important;
    }
    
    /* Animated Background Pattern */
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
    
    /* Hide default Streamlit title */
    h1[data-testid="stAppViewBlockContainer"] h1 {
        display: none;
    }
    
    /* Custom Hero Section */
    .hero-container {
        background: rgba(15, 20, 25, 0.9);
        backdrop-filter: blur(25px);
        border: 1px solid rgba(0, 212, 255, 0.2);
        border-radius: 24px;
        padding: 60px 40px;
        margin: 20px 0 40px 0;
        text-align: center;
        position: relative;
        overflow: hidden;
        box-shadow: 0 16px 64px rgba(0, 0, 0, 0.4);
    }
    
    .hero-container::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 1px;
        background: linear-gradient(90deg, transparent, #00d4ff, #ff00a8, transparent);
        opacity: 0.6;
    }
    
    .hero-title {
        font-size: 64px;
        font-weight: 900;
        background: linear-gradient(135deg, #00d4ff 0%, #ff00a8 50%, #00ff88 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 20px;
        text-shadow: 0 0 40px rgba(0, 212, 255, 0.3);
        line-height: 1.1;
    }
    
    .hero-subtitle {
        font-size: 24px;
        color: #cbd5e1;
        font-weight: 600;
        margin-bottom: 16px;
        opacity: 0.9;
    }
    
    .hero-description {
        font-size: 16px;
        color: #64748b;
        max-width: 600px;
        margin: 0 auto 40px auto;
        line-height: 1.6;
    }
    
    .hero-stats {
        display: flex;
        justify-content: center;
        gap: 60px;
        margin-top: 40px;
        flex-wrap: wrap;
    }
    
    .hero-stat {
        text-align: center;
        position: relative;
    }
    
    .hero-stat::after {
        content: '';
        position: absolute;
        bottom: -10px;
        left: 50%;
        transform: translateX(-50%);
        width: 0;
        height: 2px;
        background: linear-gradient(90deg, #00d4ff, #ff00a8);
        transition: width 0.3s ease;
    }
    
    .hero-stat:hover::after {
        width: 100%;
    }
    
    .hero-stat-value {
        font-size: 32px;
        font-weight: 800;
        color: #00d4ff;
        display: block;
        text-shadow: 0 0 20px rgba(0, 212, 255, 0.4);
    }
    
    .hero-stat-label {
        font-size: 12px;
        color: #64748b;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-top: 8px;
    }
    
    /* Navigation Cards */
    .nav-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
        gap: 32px;
        margin: 40px 0;
    }
    
    .nav-card {
        background: rgba(15, 20, 25, 0.7);
        backdrop-filter: blur(25px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 24px;
        padding: 40px;
        position: relative;
        overflow: hidden;
        transition: all 0.5s cubic-bezier(0.4, 0, 0.2, 1);
        cursor: pointer;
        text-decoration: none;
        color: inherit;
    }
    
    .nav-card::before {
        content: '';
        position: absolute;
        top: -2px;
        left: -2px;
        right: -2px;
        bottom: -2px;
        background: linear-gradient(135deg, #00d4ff, #ff00a8, #00ff88, #00d4ff);
        border-radius: 26px;
        opacity: 0;
        z-index: -1;
        transition: opacity 0.3s ease;
    }
    
    .nav-card::after {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: rgba(15, 20, 25, 0.9);
        border-radius: 24px;
        z-index: -1;
    }
    
    .nav-card:hover {
        transform: translateY(-12px) scale(1.03);
        box-shadow: 0 30px 100px rgba(0, 0, 0, 0.6);
        text-decoration: none;
        color: inherit;
    }
    
    .nav-card:hover::before {
        opacity: 1;
    }
    
    .nav-card-icon {
        font-size: 48px;
        margin-bottom: 24px;
        display: block;
        position: relative;
        z-index: 1;
    }
    
    .nav-card-title {
        font-size: 24px;
        font-weight: 700;
        color: #f1f5f9;
        margin-bottom: 16px;
        position: relative;
        z-index: 1;
    }
    
    .nav-card-description {
        font-size: 14px;
        color: #64748b;
        line-height: 1.6;
        margin-bottom: 20px;
        position: relative;
        z-index: 1;
    }
    
    .nav-card-features {
        list-style: none;
        padding: 0;
        position: relative;
        z-index: 1;
    }
    
    .nav-card-features li {
        font-size: 13px;
        color: #94a3b8;
        margin-bottom: 8px;
        padding-left: 16px;
        position: relative;
    }
    
    .nav-card-features li::before {
        content: '→';
        position: absolute;
        left: 0;
        color: #00d4ff;
        font-weight: bold;
    }
    
    /* Sidebar Styling - Minimal for now */
    .css-1d391kg {
        background: rgba(15, 20, 25, 0.95) !important;
        backdrop-filter: blur(20px) !important;
    }
    
    .css-1d391kg .stMarkdown {
        color: #e2e8f0 !important;
    }
    
    /* Status Section */
    .status-section {
        background: rgba(15, 20, 25, 0.6);
        backdrop-filter: blur(25px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        padding: 32px;
        margin: 40px 0;
        text-align: center;
    }
    
    .status-title {
        font-size: 20px;
        font-weight: 700;
        color: #f1f5f9;
        margin-bottom: 16px;
    }
    
    .status-indicator {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        background: rgba(0, 255, 136, 0.1);
        border: 1px solid rgba(0, 255, 136, 0.3);
        border-radius: 25px;
        padding: 8px 20px;
        font-size: 14px;
        font-weight: 600;
        color: #00ff88;
        margin-bottom: 20px;
    }
    
    .status-dot {
        width: 8px;
        height: 8px;
        background: #00ff88;
        border-radius: 50%;
        animation: pulse 2s infinite;
        box-shadow: 0 0 10px #00ff88;
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 1; transform: scale(1); }
        50% { opacity: 0.7; transform: scale(1.05); }
    }
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 10px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(30, 41, 59, 0.4);
        border-radius: 5px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #00d4ff, #ff00a8);
        border-radius: 5px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #ff00a8, #00d4ff);
    }
    
    /* Responsive Design */
    @media (max-width: 768px) {
        .hero-title {
            font-size: 48px;
        }
        
        .hero-subtitle {
            font-size: 20px;
        }
        
        .hero-stats {
            gap: 30px;
        }
        
        .nav-grid {
            grid-template-columns: 1fr;
            gap: 24px;
        }
        
        .nav-card {
            padding: 32px;
        }
    }
    
    /* Hide Streamlit Elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display: none;}
    
    /* Fix Streamlit title hiding */
    .main h1 {
        display: none !important;
    }
</style>
""", unsafe_allow_html=True)

# Load data (will be cached and shared across pages)
try:
    df, genesis_date = load_data()
    st.session_state.df = df
    st.session_state.genesis_date = genesis_date
    data_loaded = True
except Exception as e:
    data_loaded = False
    st.error(f"Failed to load data: {str(e)}")

# Use the hover tabs sidebar navigation
selected_page = render_hover_tabs_sidebar()

# Route to different pages based on selection
if selected_page and selected_page != "Home":
    # If a page is selected from the sidebar, navigate to it
    st.switch_page(f"pages/{selected_page}.py")
else:
    # Show the main landing page content
    
    # Sidebar navigation with enhanced styling
    st.sidebar.markdown("""
    <div style="text-align: center; padding: 20px 0; border-bottom: 1px solid rgba(255, 255, 255, 0.1); margin-bottom: 20px;">
        <h2 style="color: #00d4ff; font-weight: 800; margin: 0; font-size: 24px;">🔍 Navigation</h2>
        <p style="color: #64748b; font-size: 12px; margin: 8px 0 0 0; text-transform: uppercase; letter-spacing: 1px;">Analytics Suite</p>
    </div>
    """, unsafe_allow_html=True)

    st.sidebar.markdown("""
    <div style="color: #94a3b8; font-size: 14px; line-height: 1.6; margin-bottom: 20px;">
        Navigate through different analytics pages to explore comprehensive Kaspa network metrics and insights.
    </div>
    """, unsafe_allow_html=True)

    # Hero Section
    if data_loaded:
        current_price = df['Price'].iloc[-1] if 'Price' in df.columns else 0.0
        total_data_points = len(df)
        # Fix datetime subtraction issue
        if genesis_date:
            try:
                # Convert genesis_date to datetime if it's a pandas Timestamp
                if hasattr(genesis_date, 'to_pydatetime'):
                    genesis_dt = genesis_date.to_pydatetime()
                else:
                    genesis_dt = genesis_date
                days_since_genesis = (datetime.now() - genesis_dt).days
            except Exception:
                days_since_genesis = 0
        else:
            days_since_genesis = 0
    else:
        current_price = 0.0
        total_data_points = 0
        days_since_genesis = 0

    st.markdown(f"""
    <div class="hero-container">
        <h1 class="hero-title">Kaspa Network Analytics</h1>
        <h2 class="hero-subtitle">Advanced Blockchain Intelligence Platform</h2>
        <p class="hero-description">
            Comprehensive real-time analytics for the Kaspa network featuring advanced power-law modeling, 
            market analysis, and network metrics. Built for researchers, traders, and blockchain enthusiasts.
        </p>
        <div class="hero-stats">
            <div class="hero-stat">
                <span class="hero-stat-value">${current_price:.6f}</span>
                <div class="hero-stat-label">Current Price</div>
            </div>
            <div class="hero-stat">
                <span class="hero-stat-value">{total_data_points:,}</span>
                <div class="hero-stat-label">Data Points</div>
            </div>
            <div class="hero-stat">
                <span class="hero-stat-value">{days_since_genesis:,}</span>
                <div class="hero-stat-label">Days Active</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Navigation Cards Section
    st.markdown("""
    <div class="nav-grid">
        <div class="nav-card">
            <span class="nav-card-icon">💎</span>
            <h3 class="nav-card-title">Price Analysis</h3>
            <p class="nav-card-description">
                Advanced price analytics with power-law modeling, trend analysis, and predictive insights for Kaspa's market performance.
            </p>
            <ul class="nav-card-features">
                <li>Real-time price tracking</li>
                <li>Power-law regression modeling</li>
                <li>Support & resistance levels</li>
                <li>Historical trend analysis</li>
            </ul>
        </div>
        
        <div class="nav-card">
            <span class="nav-card-icon">⚡</span>
            <h3 class="nav-card-title">Hashrate Analysis</h3>
            <p class="nav-card-description">
                Comprehensive network security metrics including hashrate trends, mining difficulty, and network strength indicators.
            </p>
            <ul class="nav-card-features">
                <li>Network hashrate monitoring</li>
                <li>Mining difficulty tracking</li>
                <li>Security trend analysis</li>
                <li>Miner distribution metrics</li>
            </ul>
        </div>
        
        <div class="nav-card">
            <span class="nav-card-icon">📊</span>
            <h3 class="nav-card-title">Market Metrics</h3>
            <p class="nav-card-description">
                Market capitalization analysis, trading volume insights, and comprehensive market health indicators.
            </p>
            <ul class="nav-card-features">
                <li>Market cap calculations</li>
                <li>Volume analysis</li>
                <li>Liquidity metrics</li>
                <li>Market dominance tracking</li>
            </ul>
        </div>
        
        <div class="nav-card">
            <span class="nav-card-icon">📈</span>
            <h3 class="nav-card-title">Trading Volume</h3>
            <p class="nav-card-description">
                Detailed trading activity analysis including volume patterns, market momentum, and liquidity assessments.
            </p>
            <ul class="nav-card-features">
                <li>Volume trend analysis</li>
                <li>Market momentum indicators</li>
                <li>Liquidity depth analysis</li>
                <li>Trading pattern recognition</li>
            </ul>
        </div>
        
        <div class="nav-card">
            <span class="nav-card-icon">🔄</span>
            <h3 class="nav-card-title">Cross Correlations</h3>
            <p class="nav-card-description">
                Advanced correlation analysis between price, hashrate, and other network metrics to identify market relationships.
            </p>
            <ul class="nav-card-features">
                <li>Price-hashrate correlation</li>
                <li>Network metric relationships</li>
                <li>Predictive correlation modeling</li>
                <li>Multi-variate analysis</li>
            </ul>
        </div>
        
        <div class="nav-card">
            <span class="nav-card-icon">🔬</span>
            <h3 class="nav-card-title">Advanced Research</h3>
            <p class="nav-card-description">
                Cutting-edge analytics including power-law residuals, statistical modeling, and experimental features for deep insights.
            </p>
            <ul class="nav-card-features">
                <li>Power-law residual analysis</li>
                <li>Statistical modeling</li>
                <li>Experimental features</li>
                <li>Research-grade metrics</li>
            </ul>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Status Section
    st.markdown(f"""
    <div class="status-section">
        <h3 class="status-title">System Status</h3>
        <div class="status-indicator">
            <div class="status-dot"></div>
            <span>All Systems Operational</span>
        </div>
        <p style="color: #64748b; font-size: 14px; margin: 0;">
            Data updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')} • 
            Analytics engine running optimally
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Footer
    st.markdown(f"""
    <div style="text-align: center; padding: 40px 20px; margin-top: 60px; 
         background: rgba(15, 20, 25, 0.4); backdrop-filter: blur(20px);
         border-top: 1px solid rgba(255, 255, 255, 0.1); border-radius: 16px;">
        <h3 style="color: #f1f5f9; margin-bottom: 16px; font-size: 18px; font-weight: 700;">
            Kaspa Network Analytics
        </h3>
        <p style="color: #64748b; font-size: 14px; margin-bottom: 20px;">
            Professional-grade blockchain analytics • Real-time data processing • Advanced statistical modeling
        </p>
        <div style="color: #475569; font-size: 11px; text-transform: uppercase; letter-spacing: 1px;">
            Powered by advanced analytics • Built for the Kaspa community
        </div>
    </div>
    """, unsafe_allow_html=True)
