import streamlit as st
from datetime import datetime

def render_page_config(page_title="Kaspa Analytics Pro", page_icon="💎"):
    """Set consistent page config across all pages"""
    st.set_page_config(
        page_title=page_title,
        page_icon=page_icon,
        layout="wide",
        initial_sidebar_state="expanded"
    )

def render_minimal_sidebar_css():
    """Minimal CSS that adds simple sidebar while preserving your original design"""
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
        @import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css');
        
        /* Preserve ALL your original styling */
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
        
        /* Your original header styling - PRESERVED */
        .header-container {
            background: rgba(15, 20, 25, 0.9);
            backdrop-filter: blur(25px);
            border-bottom: 1px solid rgba(0, 212, 255, 0.2);
            padding: 24px 40px;
            position: sticky;
            top: 0;
            z-index: 100;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
        }
        
        .header-content {
            display: flex;
            align-items: center;
            justify-content: space-between;
            max-width: 1400px;
            margin: 0 auto;
        }
        
        .brand h1 {
            font-size: 32px;
            font-weight: 800;
            background: linear-gradient(135deg, #00d4ff 0%, #ff00a8 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin: 0;
            text-shadow: 0 0 30px rgba(0, 212, 255, 0.3);
        }
        
        .brand-subtitle {
            font-size: 13px;
            color: #64748b;
            font-weight: 500;
            text-transform: uppercase;
            letter-spacing: 1.2px;
            margin-top: 2px;
        }
        
        .header-stats {
            display: flex;
            gap: 40px;
            align-items: center;
        }
        
        .header-stat {
            text-align: center;
            position: relative;
        }
        
        .header-stat-value {
            font-size: 20px;
            font-weight: 700;
            color: #00d4ff;
            display: block;
            text-shadow: 0 0 20px rgba(0, 212, 255, 0.4);
        }
        
        .header-stat-label {
            font-size: 11px;
            color: #64748b;
            text-transform: uppercase;
            letter-spacing: 0.8px;
            margin-top: 4px;
        }
        
        .status-badge {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            background: rgba(0, 255, 136, 0.1);
            border: 1px solid rgba(0, 255, 136, 0.3);
            border-radius: 20px;
            padding: 6px 12px;
            font-size: 11px;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            color: #00ff88;
        }
        
        .live-dot {
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
        
        /* Your original chart section styling - PRESERVED */
        .chart-section {
            margin: 32px 40px 40px 40px;
            background: rgba(15, 20, 25, 0.6);
            backdrop-filter: blur(25px);
            border: 1px solid rgba(255, 255, 255, 0.15);
            border-radius: 24px;
            overflow: hidden;
            box-shadow: 0 16px 64px rgba(0, 0, 0, 0.4);
            position: relative;
        }
        
        .chart-title-section {
            background: rgba(30, 41, 59, 0.4);
            backdrop-filter: blur(15px);
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
            padding: 28px 48px 20px 48px;
            position: relative;
        }
        
        .chart-header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 0;
        }
        
        .chart-title {
            font-size: 28px;
            font-weight: 800;
            background: linear-gradient(135deg, #f1f5f9 0%, #cbd5e1 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin: 0;
        }
        
        .live-indicator {
            display: flex;
            align-items: center;
            gap: 8px;
            font-size: 13px;
            color: #00ff88;
            font-weight: 600;
        }
        
        .controls-section {
            padding: 24px 48px;
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        }
        
        .control-label {
            font-size: 12px;
            font-weight: 600;
            color: #94a3b8;
            text-transform: uppercase;
            letter-spacing: 1.2px;
            margin-bottom: 6px;
        }
        
        .chart-content {
            padding: 32px 48px;
            position: relative;
        }
        
        /* Your original selectbox styling - PRESERVED */
        .stSelectbox > div > div {
            background: linear-gradient(135deg, rgba(30, 41, 59, 0.9) 0%, rgba(15, 23, 42, 0.9) 100%) !important;
            border: 2px solid rgba(100, 116, 139, 0.3) !important;
            border-radius: 16px !important;
            backdrop-filter: blur(15px) !important;
            transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2) !important;
            min-height: 40px !important;
        }
        
        .stSelectbox > div > div:hover {
            border-color: #00d4ff !important;
            box-shadow: 0 8px 32px rgba(0, 212, 255, 0.2), 0 0 0 1px rgba(0, 212, 255, 0.3) !important;
            transform: translateY(-2px);
        }
        
        .stSelectbox > div > div > div {
            color: #f1f5f9 !important;
            font-weight: 600 !important;
            font-size: 14px !important;
            padding: 8px 16px !important;
        }
        
        /* Your original metric cards - PRESERVED */
        .metric-card {
            background: rgba(15, 20, 25, 0.7) !important;
            backdrop-filter: blur(25px) !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
            border-radius: 20px !important;
            padding: 28px !important;
            position: relative !important;
            overflow: hidden !important;
            transition: all 0.5s cubic-bezier(0.4, 0, 0.2, 1) !important;
            cursor: pointer !important;
            margin-bottom: 20px !important;
            width: 100% !important;
            box-sizing: border-box !important;
        }
        
        .metric-card:hover {
            transform: translateY(-8px) scale(1.02) !important;
            box-shadow: 0 25px 80px rgba(0, 0, 0, 0.5) !important;
        }
        
        .metric-label {
            color: #94a3b8 !important;
            font-size: 13px !important;
            font-weight: 600 !important;
            text-transform: uppercase !important;
            letter-spacing: 1.2px !important;
            margin-bottom: 12px !important;
        }
        
        .metric-value {
            color: #f1f5f9 !important;
            font-size: 36px !important;
            font-weight: 800 !important;
            line-height: 1.1 !important;
            margin-bottom: 6px !important;
            text-shadow: 0 0 20px rgba(255, 255, 255, 0.1);
        }
        
        .metric-delta {
            font-size: 15px !important;
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
            border-radius: 16px;
            overflow: hidden;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        }
        
        .stPlotlyChart .modebar {
            background: transparent !important;
            transform: translateY(15px) !important;
        }
        
        .stPlotlyChart .modebar-group {
            background: transparent !important;
        }
        
        /* MINIMAL SIDEBAR - Simple like Kaspalytics/Glassnode */
        section[data-testid="stSidebar"] {
            background: rgba(10, 14, 26, 0.95) !important;
            border-right: 1px solid rgba(255, 255, 255, 0.08) !important;
            backdrop-filter: blur(20px) !important;
        }
        
        /* Simple sidebar navigation */
        .sidebar-nav-item {
            display: flex !important;
            align-items: center !important;
            gap: 12px !important;
            padding: 10px 16px !important;
            margin: 2px 8px !important;
            border-radius: 8px !important;
            color: #94a3b8 !important;
            font-size: 14px !important;
            font-weight: 500 !important;
            transition: all 0.2s ease !important;
            cursor: pointer !important;
            text-decoration: none !important;
        }
        
        .sidebar-nav-item:hover {
            background: rgba(255, 255, 255, 0.05) !important;
            color: #cbd5e1 !important;
        }
        
        .sidebar-nav-item.active {
            background: rgba(0, 212, 255, 0.1) !important;
            color: #00d4ff !important;
            border-left: 3px solid #00d4ff !important;
            padding-left: 13px !important;
        }
        
        .sidebar-nav-icon {
            width: 16px !important;
            text-align: center !important;
            font-size: 14px !important;
        }
        
        /* Simple sidebar sections */
        .sidebar-section {
            padding: 16px 0 !important;
            border-bottom: 1px solid rgba(255, 255, 255, 0.05) !important;
        }
        
        .sidebar-section:last-child {
            border-bottom: none !important;
        }
        
        .sidebar-title {
            font-size: 11px !important;
            font-weight: 600 !important;
            color: #64748b !important;
            text-transform: uppercase !important;
            letter-spacing: 1px !important;
            margin-bottom: 12px !important;
            padding: 0 16px !important;
        }
        
        /* Minimal price display in sidebar */
        .sidebar-price {
            padding: 12px 16px !important;
            background: rgba(15, 20, 25, 0.5) !important;
            margin: 8px !important;
            border-radius: 8px !important;
            border: 1px solid rgba(255, 255, 255, 0.05) !important;
        }
        
        .sidebar-price-value {
            font-size: 18px !important;
            font-weight: 700 !important;
            color: #f1f5f9 !important;
            margin-bottom: 4px !important;
        }
        
        .sidebar-price-change {
            font-size: 12px !important;
            font-weight: 600 !important;
        }
        
        .sidebar-price-change.positive {
            color: #10b981 !important;
        }
        
        .sidebar-price-change.negative {
            color: #ef4444 !important;
        }
        
        /* Hide Streamlit elements */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        .stDeployButton {display: none;}
        
        /* Mobile responsive */
        @media (max-width: 768px) {
            .header-container {
                padding: 16px 20px;
            }
            
            .chart-section {
                margin: 20px;
            }
            
            .chart-title-section {
                padding: 20px 24px 16px 24px;
            }
            
            .controls-section {
                padding: 16px 24px;
            }
            
            .chart-content {
                padding: 20px 24px;
            }
        }
    </style>
    """, unsafe_allow_html=True)

def render_minimal_sidebar(current_page="Price Analysis"):
    """Minimal sidebar like Kaspalytics/Glassnode"""
    
    # Simple navigation
    nav_items = [
        {"name": "Dashboard", "icon": "fas fa-home", "page": "Dashboard"},
        {"name": "Price Analysis", "icon": "fas fa-chart-line", "page": "Price Analysis"},
        {"name": "On-Chain Metrics", "icon": "fas fa-link", "page": "OnChain"},
        {"name": "Mining Analytics", "icon": "fas fa-microchip", "page": "Mining"},
        {"name": "Portfolio", "icon": "fas fa-wallet", "page": "Portfolio"},
        {"name": "Alerts", "icon": "fas fa-bell", "page": "Alerts"},
    ]
    
    # Navigation section
    st.sidebar.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
    st.sidebar.markdown('<div class="sidebar-title">Analytics</div>', unsafe_allow_html=True)
    
    for item in nav_items:
        active_class = "active" if item["page"] == current_page else ""
        
        nav_html = f'''
        <div class="sidebar-nav-item {active_class}">
            <i class="{item['icon']} sidebar-nav-icon"></i>
            <span>{item['name']}</span>
        </div>
        '''
        st.sidebar.markdown(nav_html, unsafe_allow_html=True)
    
    st.sidebar.markdown('</div>', unsafe_allow_html=True)
    
    # Simple price display
    st.sidebar.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
    st.sidebar.markdown('<div class="sidebar-title">Live Price</div>', unsafe_allow_html=True)
    
    price_html = '''
    <div class="sidebar-price">
        <div class="sidebar-price-value">$0.08734</div>
        <div class="sidebar-price-change positive">+2.4% (24h)</div>
    </div>
    '''
    st.sidebar.markdown(price_html, unsafe_allow_html=True)
    st.sidebar.markdown('</div>', unsafe_allow_html=True)
    
    # Simple stats
    st.sidebar.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
    st.sidebar.markdown('<div class="sidebar-title">Quick Stats</div>', unsafe_allow_html=True)
    
    # Using simple Streamlit metrics for clean look
    st.sidebar.metric("Market Cap", "$2.1B", "1.8%")
    st.sidebar.metric("24h Volume", "$45.2M", "-5.1%")
    st.sidebar.metric("Circulating", "24.0B KAS", "")
    
    st.sidebar.markdown('</div>', unsafe_allow_html=True)
