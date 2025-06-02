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

def render_custom_css_with_sidebar():
    """Enhanced CSS with beautiful sidebar dropdowns and glow effects"""
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
        
        /* Beautiful Sidebar Styling */
        section[data-testid="stSidebar"] {
            background: rgba(10, 14, 26, 0.95) !important;
            border-right: 1px solid rgba(0, 212, 255, 0.15) !important;
            margin-top: 80px !important;
            backdrop-filter: blur(25px) !important;
            box-shadow: 8px 0 32px rgba(0, 0, 0, 0.4) !important;
        }
        
        /* Hide default Streamlit sidebar content */
        section[data-testid="stSidebar"] > div {
            background: transparent !important;
        }
        
        /* Sidebar Section Containers */
        .sidebar-section {
            margin: 12px 8px !important;
            background: rgba(15, 20, 25, 0.6) !important;
            backdrop-filter: blur(25px) !important;
            border: 1px solid rgba(255, 255, 255, 0.08) !important;
            border-radius: 16px !important;
            overflow: hidden !important;
            transition: all 0.5s cubic-bezier(0.4, 0, 0.2, 1) !important;
        }
        
        .sidebar-section:hover {
            border-color: rgba(0, 212, 255, 0.2) !important;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3) !important;
        }
        
        /* Dropdown Header */
        .dropdown-header {
            display: flex !important;
            align-items: center !important;
            justify-content: space-between !important;
            padding: 16px 20px !important;
            cursor: pointer !important;
            transition: all 0.3s ease !important;
            border-bottom: 1px solid rgba(255, 255, 255, 0.05) !important;
        }
        
        .dropdown-header:hover {
            background: rgba(0, 212, 255, 0.05) !important;
        }
        
        .dropdown-header.active {
            background: rgba(0, 212, 255, 0.1) !important;
            border-bottom-color: rgba(0, 212, 255, 0.2) !important;
        }
        
        .dropdown-title {
            display: flex !important;
            align-items: center !important;
            gap: 12px !important;
            font-size: 14px !important;
            font-weight: 600 !important;
            color: #cbd5e1 !important;
        }
        
        .dropdown-icon {
            width: 16px !important;
            text-align: center !important;
            color: #00d4ff !important;
        }
        
        .dropdown-chevron {
            font-size: 12px !important;
            color: #64748b !important;
            transition: transform 0.3s ease !important;
        }
        
        .dropdown-chevron.expanded {
            transform: rotate(90deg) !important;
        }
        
        /* Dropdown Content */
        .dropdown-content {
            max-height: 0 !important;
            overflow: hidden !important;
            transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
            background: rgba(10, 14, 20, 0.4) !important;
        }
        
        .dropdown-content.expanded {
            max-height: 500px !important;
            padding-bottom: 8px !important;
        }
        
        /* Navigation Items */
        .nav-item {
            display: flex !important;
            align-items: center !important;
            gap: 12px !important;
            padding: 10px 20px 10px 48px !important;
            margin: 2px 8px !important;
            border-radius: 8px !important;
            color: #94a3b8 !important;
            font-size: 13px !important;
            font-weight: 500 !important;
            cursor: pointer !important;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
            border: 1px solid transparent !important;
        }
        
        .nav-item:hover {
            background: rgba(0, 212, 255, 0.08) !important;
            color: #00d4ff !important;
            transform: translateX(4px) !important;
            border-color: rgba(0, 212, 255, 0.2) !important;
            box-shadow: 0 2px 8px rgba(0, 212, 255, 0.1) !important;
        }
        
        .nav-item.active {
            background: rgba(0, 212, 255, 0.15) !important;
            color: #00d4ff !important;
            border-color: rgba(0, 212, 255, 0.4) !important;
            box-shadow: 0 4px 16px rgba(0, 212, 255, 0.2) !important;
        }
        
        .nav-item-icon {
            width: 14px !important;
            text-align: center !important;
            font-size: 12px !important;
        }
        
        /* Live Stats Section */
        .live-stats {
            padding: 16px !important;
        }
        
        .stats-title {
            font-size: 12px !important;
            font-weight: 600 !important;
            color: #64748b !important;
            text-transform: uppercase !important;
            letter-spacing: 1px !important;
            margin-bottom: 12px !important;
            display: flex !important;
            align-items: center !important;
            gap: 8px !important;
        }
        
        .live-dot {
            width: 6px !important;
            height: 6px !important;
            background: #00ff88 !important;
            border-radius: 50% !important;
            animation: pulse 2s infinite !important;
            box-shadow: 0 0 8px #00ff88 !important;
        }
        
        @keyframes pulse {
            0%, 100% { opacity: 1; transform: scale(1); }
            50% { opacity: 0.7; transform: scale(1.1); }
        }
        
        .stat-item {
            display: flex !important;
            justify-content: space-between !important;
            align-items: center !important;
            padding: 8px 0 !important;
            border-bottom: 1px solid rgba(255, 255, 255, 0.05) !important;
        }
        
        .stat-item:last-child {
            border-bottom: none !important;
        }
        
        .stat-label {
            font-size: 11px !important;
            color: #94a3b8 !important;
            font-weight: 500 !important;
        }
        
        .stat-value {
            font-size: 12px !important;
            font-weight: 600 !important;
            color: #f1f5f9 !important;
        }
        
        .stat-change {
            font-size: 10px !important;
            font-weight: 600 !important;
            margin-left: 4px !important;
        }
        
        .stat-change.positive {
            color: #10b981 !important;
        }
        
        .stat-change.negative {
            color: #ef4444 !important;
        }
        
        /* Main content adjustments */
        .main .block-container {
            padding-top: 100px !important;
            padding-left: 20px !important;
            padding-right: 20px !important;
            max-width: 100% !important;
        }
        
        /* Hide Streamlit elements */
        #MainMenu {visibility: hidden !important;}
        footer {visibility: hidden !important;}
        header {visibility: hidden !important;}
        .stDeployButton {display: none !important;}
        
        /* Mobile responsive */
        @media (max-width: 768px) {
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

def render_clean_header(user_name=None, user_role=None, show_auth=True):
    """Render a clean header with just branding and auth"""
    
    # Build auth section
    if user_name:
        user_initials = "".join([name[0].upper() for name in user_name.split()[:2]])
        auth_html = f'<div style="display: flex; align-items: center; gap: 10px; background: rgba(30, 41, 59, 0.6); border: 1px solid rgba(100, 116, 139, 0.3); border-radius: 12px; padding: 8px 12px;"><div style="width: 32px; height: 32px; border-radius: 8px; background: linear-gradient(135deg, #00d4ff 0%, #ff00a8 100%); display: flex; align-items: center; justify-content: center; color: white; font-weight: 700; font-size: 14px;">{user_initials}</div><div><div style="font-size: 13px; font-weight: 600; color: #f1f5f9;">{user_name}</div><div style="font-size: 11px; color: #64748b;">{user_role or "Free Plan"}</div></div></div>'
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
            {auth_html}
        </div>
    </div>
    '''
    
    st.markdown(header_html, unsafe_allow_html=True)

def render_beautiful_sidebar(current_page="Price"):
    """Render beautiful sidebar with dropdown navigation like Glassnode"""
    
    # Define navigation structure
    nav_structure = {
        "Market Metrics": {
            "icon": "fas fa-chart-area",
            "items": [
                {"name": "Price", "icon": "fas fa-dollar-sign", "page": "Price"},
                {"name": "Market Cap", "icon": "fas fa-coins", "page": "MarketCap"},
                {"name": "Trading Volume", "icon": "fas fa-chart-bar", "page": "Volume"},
                {"name": "Supply", "icon": "fas fa-layer-group", "page": "Supply"}
            ]
        },
        "Mining": {
            "icon": "fas fa-microchip",
            "items": [
                {"name": "Hashrate", "icon": "fas fa-tachometer-alt", "page": "Hashrate"},
                {"name": "Difficulty", "icon": "fas fa-puzzle-piece", "page": "Difficulty"},
                {"name": "Mining Revenue", "icon": "fas fa-money-bill-wave", "page": "Revenue"}
            ]
        },
        "Network": {
            "icon": "fas fa-network-wired",
            "items": [
                {"name": "Transactions", "icon": "fas fa-exchange-alt", "page": "Transactions"},
                {"name": "Addresses", "icon": "fas fa-wallet", "page": "Addresses"},
                {"name": "Blocks", "icon": "fas fa-cube", "page": "Blocks"}
            ]
        }
    }
    
    # Create sidebar navigation using Streamlit components
    with st.sidebar:
        # Navigation sections
        for section_name, section_data in nav_structure.items():
            # Check if any item in this section is active
            section_active = any(item["page"] == current_page for item in section_data["items"])
            
            # Create expander for each section
            with st.expander(f"{section_data['icon']} {section_name}", expanded=section_active):
                for item in section_data["items"]:
                    # Create columns for icon and text
                    col_icon, col_text = st.columns([1, 4])
                    
                    with col_icon:
                        if item["page"] == current_page:
                            st.markdown(f'<i class="{item["icon"]}" style="color: #00d4ff; font-size: 12px;"></i>', unsafe_allow_html=True)
                        else:
                            st.markdown(f'<i class="{item["icon"]}" style="color: #94a3b8; font-size: 12px;"></i>', unsafe_allow_html=True)
                    
                    with col_text:
                        # Use button for navigation
                        button_style = ""
                        if item["page"] == current_page:
                            button_style = "background-color: rgba(0, 212, 255, 0.15); color: #00d4ff; border: 1px solid rgba(0, 212, 255, 0.4);"
                        
                        if st.button(
                            item["name"], 
                            key=f"nav_{item['page']}", 
                            use_container_width=True,
                            help=f"Navigate to {item['name']}"
                        ):
                            st.switch_page(f"pages/{item['page']}.py")
        
        # Add separator
        st.markdown("---")
        
        # Live Stats Section
        st.markdown("### 🔴 Live Stats")
        
        # Create stats using metrics for clean look
        st.metric("KAS Price", "$0.0873", "2.4%")
        st.metric("Market Cap", "$2.1B", "1.8%") 
        st.metric("24h Volume", "$45.2M", "-5.1%")
        st.metric("Hashrate", "1.2 EH/s", "0.3%")

def render_simple_page_header(title, subtitle=None):
    """Simple page header without breadcrumbs"""
    
    subtitle_html = f'<p style="color: #94a3b8; font-size: 16px; margin: 8px 0 0 0;">{subtitle}</p>' if subtitle else ""
    
    page_header_html = f'<div style="padding: 0 0 32px 0;"><h1 style="color: #f1f5f9; font-size: 36px; font-weight: 800; margin: 0;">{title}</h1>{subtitle_html}</div>'
    
    st.markdown(page_header_html, unsafe_allow_html=True)
