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

def render_cohesive_css():
    """CSS styled to perfectly match your price analysis page"""
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
        @import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css');
        
        /* Base App Styling - Matching your existing design */
        html, body, .stApp {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
            background: linear-gradient(135deg, #0a0e1a 0%, #1a1f2e 50%, #0f1419 100%) !important;
            color: #e2e8f0 !important;
            overflow-x: hidden !important;
        }
        
        .stApp {
            background-attachment: fixed !important;
        }
        
        /* Background effects matching your design */
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
        
        /* Professional Header - Matching your chart section styling */
        .professional-header {
            position: fixed !important;
            top: 0 !important;
            left: 0 !important;
            right: 0 !important;
            width: 100vw !important;
            height: 85px !important;
            background: rgba(15, 20, 25, 0.9) !important;
            backdrop-filter: blur(25px) !important;
            border-bottom: 1px solid rgba(0, 212, 255, 0.2) !important;
            padding: 0 40px !important;
            z-index: 999999999 !important;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4) !important;
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
        
        /* Brand Section - Enhanced to match your style */
        .brand-section {
            display: flex !important;
            align-items: center !important;
            gap: 16px !important;
        }
        
        .logo {
            width: 48px !important;
            height: 48px !important;
            background: linear-gradient(135deg, #00d4ff 0%, #ff00a8 100%) !important;
            border-radius: 16px !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
            font-size: 26px !important;
            color: white !important;
            font-weight: 800 !important;
            box-shadow: 0 8px 25px rgba(0, 212, 255, 0.3) !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
        }
        
        .brand-text h1 {
            font-size: 32px !important;
            font-weight: 800 !important;
            background: linear-gradient(135deg, #00d4ff 0%, #ff00a8 100%) !important;
            -webkit-background-clip: text !important;
            -webkit-text-fill-color: transparent !important;
            margin: 0 !important;
            line-height: 1.1 !important;
            text-shadow: 0 0 30px rgba(0, 212, 255, 0.3) !important;
        }
        
        .brand-subtitle {
            font-size: 13px !important;
            color: #64748b !important;
            font-weight: 500 !important;
            text-transform: uppercase !important;
            letter-spacing: 1.2px !important;
            margin-top: 2px !important;
        }
        
        /* Header Status Indicator */
        .header-status {
            display: flex !important;
            align-items: center !important;
            gap: 12px !important;
            background: rgba(30, 41, 59, 0.4) !important;
            backdrop-filter: blur(15px) !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
            border-radius: 16px !important;
            padding: 12px 20px !important;
        }
        
        .live-indicator {
            display: flex !important;
            align-items: center !important;
            gap: 8px !important;
            font-size: 13px !important;
            color: #00ff88 !important;
            font-weight: 600 !important;
        }
        
        .live-dot {
            width: 8px !important;
            height: 8px !important;
            background: #00ff88 !important;
            border-radius: 50% !important;
            animation: pulse 2s infinite !important;
            box-shadow: 0 0 10px #00ff88 !important;
        }
        
        @keyframes pulse {
            0%, 100% { opacity: 1; transform: scale(1); }
            50% { opacity: 0.7; transform: scale(1.05); }
        }
        
        /* Auth Section - Matching your metric card style */
        .auth-section {
            display: flex !important;
            align-items: center !important;
            gap: 12px !important;
        }
        
        .login-button {
            background: rgba(15, 20, 25, 0.7) !important;
            backdrop-filter: blur(25px) !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
            border-radius: 16px !important;
            padding: 12px 20px !important;
            color: #cbd5e1 !important;
            font-size: 13px !important;
            font-weight: 600 !important;
            cursor: pointer !important;
            transition: all 0.5s cubic-bezier(0.4, 0, 0.2, 1) !important;
        }
        
        .login-button:hover {
            transform: translateY(-2px) !important;
            border-color: rgba(0, 212, 255, 0.4) !important;
            color: #00d4ff !important;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3) !important;
        }
        
        .signup-button {
            background: linear-gradient(135deg, #00d4ff 0%, #0099cc 100%) !important;
            border: none !important;
            border-radius: 16px !important;
            padding: 12px 24px !important;
            color: white !important;
            font-size: 13px !important;
            font-weight: 700 !important;
            cursor: pointer !important;
            box-shadow: 0 8px 32px rgba(0, 212, 255, 0.3) !important;
            transition: all 0.5s cubic-bezier(0.4, 0, 0.2, 1) !important;
        }
        
        .signup-button:hover {
            transform: translateY(-3px) scale(1.02) !important;
            box-shadow: 0 15px 50px rgba(0, 212, 255, 0.4) !important;
        }
        
        /* Sidebar - Styled to match your chart sections */
        section[data-testid="stSidebar"] {
            background: rgba(15, 20, 25, 0.6) !important;
            backdrop-filter: blur(25px) !important;
            border-right: 1px solid rgba(255, 255, 255, 0.15) !important;
            margin-top: 85px !important;
            box-shadow: 8px 0 32px rgba(0, 0, 0, 0.4) !important;
        }
        
        .sidebar-section {
            background: rgba(15, 20, 25, 0.7) !important;
            backdrop-filter: blur(25px) !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
            border-radius: 20px !important;
            padding: 24px !important;
            margin: 16px !important;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3) !important;
        }
        
        .sidebar-title {
            font-size: 18px !important;
            font-weight: 800 !important;
            background: linear-gradient(135deg, #f1f5f9 0%, #cbd5e1 100%) !important;
            -webkit-background-clip: text !important;
            -webkit-text-fill-color: transparent !important;
            margin-bottom: 20px !important;
        }
        
        .nav-item {
            display: flex !important;
            align-items: center !important;
            gap: 12px !important;
            padding: 12px 16px !important;
            margin: 6px 0 !important;
            border-radius: 12px !important;
            color: #cbd5e1 !important;
            font-size: 14px !important;
            font-weight: 500 !important;
            transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
            cursor: pointer !important;
            border: 1px solid transparent !important;
        }
        
        .nav-item:hover {
            background: rgba(0, 212, 255, 0.1) !important;
            border-color: rgba(0, 212, 255, 0.3) !important;
            color: #00d4ff !important;
            transform: translateX(4px) !important;
        }
        
        .nav-item.active {
            background: rgba(0, 212, 255, 0.15) !important;
            border-color: rgba(0, 212, 255, 0.5) !important;
            color: #00d4ff !important;
        }
        
        .nav-icon {
            width: 18px !important;
            text-align: center !important;
        }
        
        /* Sidebar Metrics - Matching your metric card style */
        .sidebar-metric {
            background: rgba(15, 20, 25, 0.7) !important;
            backdrop-filter: blur(25px) !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
            border-radius: 16px !important;
            padding: 16px !important;
            margin: 8px 0 !important;
            transition: all 0.5s cubic-bezier(0.4, 0, 0.2, 1) !important;
        }
        
        .sidebar-metric:hover {
            transform: translateY(-2px) scale(1.02) !important;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4) !important;
        }
        
        .metric-label {
            color: #94a3b8 !important;
            font-size: 11px !important;
            font-weight: 600 !important;
            text-transform: uppercase !important;
            letter-spacing: 1.2px !important;
            margin-bottom: 8px !important;
        }
        
        .metric-value {
            color: #f1f5f9 !important;
            font-size: 20px !important;
            font-weight: 800 !important;
            line-height: 1.1 !important;
            margin-bottom: 4px !important;
        }
        
        .metric-delta {
            font-size: 12px !important;
            font-weight: 700 !important;
        }
        
        .metric-delta.positive {
            color: #00ff88 !important;
        }
        
        .metric-delta.negative {
            color: #ff4757 !important;
        }
        
        /* Main content adjustments */
        .main .block-container {
            padding-top: 105px !important;
            padding-left: 0 !important;
            padding-right: 0 !important;
            max-width: 100% !important;
        }
        
        /* Ensure your existing chart sections work perfectly */
        .chart-section {
            margin: 32px 40px 40px 40px !important;
            background: rgba(15, 20, 25, 0.6) !important;
            backdrop-filter: blur(25px) !important;
            border: 1px solid rgba(255, 255, 255, 0.15) !important;
            border-radius: 24px !important;
            overflow: hidden !important;
            box-shadow: 0 16px 64px rgba(0, 0, 0, 0.4) !important;
        }
        
        .chart-title-section {
            background: rgba(30, 41, 59, 0.4) !important;
            backdrop-filter: blur(15px) !important;
            border-bottom: 1px solid rgba(255, 255, 255, 0.1) !important;
            padding: 28px 48px 20px 48px !important;
        }
        
        /* Hide Streamlit elements */
        #MainMenu {visibility: hidden !important;}
        footer {visibility: hidden !important;}
        header {visibility: hidden !important;}
        .stDeployButton {display: none !important;}
        
        /* Mobile responsive */
        @media (max-width: 768px) {
            .professional-header {
                height: 75px !important;
                padding: 0 20px !important;
            }
            
            .brand-text h1 {
                font-size: 24px !important;
            }
            
            .main .block-container {
                padding-top: 95px !important;
            }
            
            .chart-section {
                margin: 20px !important;
            }
        }
    </style>
    """, unsafe_allow_html=True)

def render_styled_header(user_name=None, user_role=None, show_auth=True):
    """Header that perfectly matches your price analysis page style"""
    
    # Build auth section
    if user_name:
        user_initials = "".join([name[0].upper() for name in user_name.split()[:2]])
        auth_html = f'''
        <div style="display: flex; align-items: center; gap: 10px; background: rgba(15, 20, 25, 0.7); backdrop-filter: blur(25px); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 16px; padding: 12px 16px;">
            <div style="width: 36px; height: 36px; border-radius: 10px; background: linear-gradient(135deg, #00d4ff 0%, #ff00a8 100%); display: flex; align-items: center; justify-content: center; color: white; font-weight: 700; font-size: 16px;">{user_initials}</div>
            <div>
                <div style="font-size: 14px; font-weight: 600; color: #f1f5f9;">{user_name}</div>
                <div style="font-size: 11px; color: #64748b;">{user_role or "Free Plan"}</div>
            </div>
        </div>
        '''
    else:
        auth_html = '<div class="auth-section"><button class="login-button"><i class="fas fa-sign-in-alt"></i> Login</button><button class="signup-button"><i class="fas fa-rocket"></i> Get Started</button></div>' if show_auth else ""
    
    header_html = f'''
    <div class="professional-header">
        <div class="header-content">
            <div class="brand-section">
                <div class="logo"><i class="fas fa-gem"></i></div>
                <div class="brand-text">
                    <h1>KaspaMetrics</h1>
                    <div class="brand-subtitle">Advanced Market Intelligence Platform</div>
                </div>
            </div>
            <div class="header-status">
                <div class="live-indicator">
                    <div class="live-dot"></div>
                    <span>LIVE DATA</span>
                </div>
            </div>
            {auth_html}
        </div>
    </div>
    '''
    
    st.markdown(header_html, unsafe_allow_html=True)

def render_styled_sidebar_navigation(current_page="Dashboard"):
    """Sidebar navigation that matches your design perfectly"""
    
    # Navigation section
    nav_html = '''
    <div class="sidebar-section">
        <div class="sidebar-title">Navigation</div>
    '''
    
    nav_items = [
        {"name": "Dashboard", "icon": "fas fa-tachometer-alt", "page": "Dashboard"},
        {"name": "Price Analysis", "icon": "fas fa-chart-line", "page": "Analytics"},
        {"name": "Portfolio Tracker", "icon": "fas fa-wallet", "page": "Portfolio"},
        {"name": "Market Research", "icon": "fas fa-microscope", "page": "Research"},
        {"name": "Price Alerts", "icon": "fas fa-bell", "page": "Alerts"},
        {"name": "Settings", "icon": "fas fa-cog", "page": "Settings"},
    ]
    
    for item in nav_items:
        active_class = "active" if item["page"] == current_page else ""
        nav_html += f'<div class="nav-item {active_class}"><i class="{item["icon"]} nav-icon"></i><span>{item["name"]}</span></div>'
    
    nav_html += '</div>'
    
    # Quick metrics section
    metrics_html = '''
    <div class="sidebar-section">
        <div class="sidebar-title">Live Metrics</div>
        <div class="sidebar-metric">
            <div class="metric-label">KAS PRICE</div>
            <div class="metric-value">$0.08734</div>
            <div class="metric-delta positive">+2.4%</div>
        </div>
        <div class="sidebar-metric">
            <div class="metric-label">24H VOLUME</div>
            <div class="metric-value">$45.2M</div>
            <div class="metric-delta negative">-5.1%</div>
        </div>
        <div class="sidebar-metric">
            <div class="metric-label">MARKET CAP</div>
            <div class="metric-value">$2.1B</div>
            <div class="metric-delta positive">+1.8%</div>
        </div>
        <div class="sidebar-metric">
            <div class="metric-label">POWER LAW R²</div>
            <div class="metric-value">0.885</div>
            <div class="metric-delta positive">+0.12%</div>
        </div>
    </div>
    '''
    
    # Market status section
    status_html = '''
    <div class="sidebar-section">
        <div class="sidebar-title">Market Status</div>
        <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 12px;">
            <div style="width: 8px; height: 8px; background: #00ff88; border-radius: 50%; animation: pulse 2s infinite;"></div>
            <span style="color: #00ff88; font-size: 13px; font-weight: 600;">Markets Open</span>
        </div>
        <div style="color: #94a3b8; font-size: 12px; line-height: 1.4;">
            All systems operational<br>
            Last update: Just now<br>
            Next update: 30 seconds
        </div>
    </div>
    '''
    
    st.sidebar.markdown(nav_html + metrics_html + status_html, unsafe_allow_html=True)
