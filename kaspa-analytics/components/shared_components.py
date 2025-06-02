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
        
        /* Ultra-clean sidebar - just text */
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
            padding: 12px 8px !important;
        }
        
        /* Hide ALL button styling completely */
        .stButton {
            display: none !important;
        }
        
        /* Custom clickable text styling */
        .sidebar-text-item {
            padding: 2px 4px !important;
            margin: 1px 0 !important;
            cursor: pointer !important;
            transition: all 0.2s ease !important;
            font-size: 12px !important;
            user-select: none !important;
            display: flex !important;
            align-items: center !important;
            gap: 6px !important;
        }
        
        .sidebar-text-item:hover {
            background: rgba(255, 255, 255, 0.02) !important;
        }
        
        .sidebar-section-text {
            font-weight: 600 !important;
            color: #94a3b8 !important;
            text-transform: uppercase !important;
            letter-spacing: 0.5px !important;
            margin: 8px 0 4px 0 !important;
        }
        
        .sidebar-nav-text {
            font-weight: 400 !important;
            color: #94a3b8 !important;
            margin-left: 12px !important;
            border-left: 1px solid rgba(255, 255, 255, 0.03) !important;
            padding-left: 8px !important;
        }
        
        .sidebar-nav-text:hover {
            color: #cbd5e1 !important;
        }
        
        .sidebar-nav-text.active {
            color: #00d4ff !important;
            font-weight: 500 !important;
        }
        
        .sidebar-icon {
            font-size: 9px !important;
            width: 12px !important;
            text-align: center !important;
        }
        
        .section-icon {
            color: #64748b !important;
        }
        
        .nav-icon {
            color: #64748b !important;
        }
        
        .nav-icon.active {
            color: #00d4ff !important;
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
    """Ultra-lean sidebar with just clickable text - no buttons or borders"""
    
    # Navigation structure
    nav_structure = {
        "Market Metrics": {
            "icon": "chart-area",
            "expanded": True,
            "items": [
                {"name": "Price", "icon": "dollar-sign", "page": "Price"},
                {"name": "Market Cap", "icon": "coins", "page": "MarketCap"},
                {"name": "Trading Volume", "icon": "chart-bar", "page": "Volume"},
                {"name": "Supply", "icon": "layer-group", "page": "Supply"}
            ]
        },
        "Mining": {
            "icon": "microchip", 
            "expanded": False,
            "items": [
                {"name": "Hashrate", "icon": "tachometer-alt", "page": "Hashrate"},
                {"name": "Difficulty", "icon": "puzzle-piece", "page": "Difficulty"},
                {"name": "Mining Revenue", "icon": "money-bill-wave", "page": "Revenue"}
            ]
        },
        "Network": {
            "icon": "network-wired",
            "expanded": False, 
            "items": [
                {"name": "Transactions", "icon": "exchange-alt", "page": "Transactions"},
                {"name": "Addresses", "icon": "wallet", "page": "Addresses"},
                {"name": "Blocks", "icon": "cube", "page": "Blocks"}
            ]
        }
    }
    
    # Auto-expand section containing current page
    for section_name, section_data in nav_structure.items():
        if any(item["page"] == current_page for item in section_data["items"]):
            section_data["expanded"] = True
    
    # Initialize session state
    if 'sidebar_expanded' not in st.session_state:
        st.session_state.sidebar_expanded = {k: v["expanded"] for k, v in nav_structure.items()}
    
    # Build pure HTML sidebar
    sidebar_html = '<div style="padding: 8px;">'
    
    for section_name, section_data in nav_structure.items():
        is_expanded = st.session_state.sidebar_expanded.get(section_name, section_data["expanded"])
        chevron = "▼" if is_expanded else "▶"
        
        # Section header - clickable text only
        sidebar_html += f'''
        <div class="sidebar-text-item sidebar-section-text" onclick="toggleSection('{section_name}')">
            <span style="color: #64748b; font-size: 10px;">{chevron}</span>
            <i class="fas fa-{section_data['icon']} sidebar-icon section-icon"></i>
            <span>{section_name}</span>
        </div>
        '''
        
        # Navigation items - only if expanded
        if is_expanded:
            for item in section_data["items"]:
                active_class = "active" if item["page"] == current_page else ""
                icon_class = "active" if item["page"] == current_page else ""
                
                sidebar_html += f'''
                <div class="sidebar-text-item sidebar-nav-text {active_class}" onclick="navigateTo('{item['page']}')">
                    <i class="fas fa-{item['icon']} sidebar-icon nav-icon {icon_class}"></i>
                    <span>{item['name']}</span>
                </div>
                '''
        
        sidebar_html += '<div style="height: 4px;"></div>'
    
    sidebar_html += '</div>'
    
    # JavaScript for functionality
    js_code = '''
    <script>
    function toggleSection(sectionName) {
        // This would need to communicate back to Streamlit
        // For now, just log
        console.log('Toggle:', sectionName);
    }
    
    function navigateTo(page) {
        console.log('Navigate to:', page);
        // st.switch_page implementation would go here
    }
    </script>
    '''
    
    # Use st.components.v1.html for better HTML rendering
    with st.sidebar:
        st.components.v1.html(sidebar_html + js_code, height=400, scrolling=False)
        
        # Add hidden buttons for Streamlit functionality
        st.markdown("---")
        st.markdown("**Quick Actions**")
        
        # Simple expand/collapse buttons
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("📊", help="Toggle Market Metrics"):
                st.session_state.sidebar_expanded["Market Metrics"] = not st.session_state.sidebar_expanded.get("Market Metrics", True)
                st.rerun()
        with col2:
            if st.button("⛏️", help="Toggle Mining"):
                st.session_state.sidebar_expanded["Mining"] = not st.session_state.sidebar_expanded.get("Mining", False)
                st.rerun()
        with col3:
            if st.button("🌐", help="Toggle Network"):
                st.session_state.sidebar_expanded["Network"] = not st.session_state.sidebar_expanded.get("Network", False)
                st.rerun()
        
        # Navigation buttons
        st.markdown("**Navigate**")
        if st.button("💰 Price", use_container_width=True):
            st.write("Navigate to Price")
        if st.button("🪙 Market Cap", use_container_width=True):
            st.write("Navigate to Market Cap")
        if st.button("📈 Trading Volume", use_container_width=True):
            st.write("Navigate to Trading Volume")

def render_simple_page_header(title, subtitle=None):
    """Simple page header without breadcrumbs"""
    
    subtitle_html = f'<p style="color: #94a3b8; font-size: 16px; margin: 8px 0 0 0;">{subtitle}</p>' if subtitle else ""
    
    page_header_html = f'<div style="padding: 0 0 32px 0;"><h1 style="color: #f1f5f9; font-size: 36px; font-weight: 800; margin: 0;">{title}</h1>{subtitle_html}</div>'
    
    st.markdown(page_header_html, unsafe_allow_html=True)
