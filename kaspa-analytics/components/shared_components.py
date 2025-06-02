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
        
        /* Beautiful Sidebar Styling - Compact File Explorer Style */
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
        
        /* Section Headers - Compact folder style */
        .sidebar-section-header {
            display: flex !important;
            align-items: center !important;
            gap: 6px !important;
            padding: 6px 8px !important;
            font-size: 12px !important;
            font-weight: 600 !important;
            color: #94a3b8 !important;
            text-transform: uppercase !important;
            letter-spacing: 0.5px !important;
            margin: 8px 0 4px 0 !important;
            cursor: pointer !important;
            transition: all 0.2s ease !important;
            border-radius: 4px !important;
        }
        
        .sidebar-section-header:hover {
            background: rgba(255, 255, 255, 0.02) !important;
            color: #cbd5e1 !important;
        }
        
        .section-icon {
            color: #64748b !important;
            font-size: 10px !important;
            width: 12px !important;
            text-align: center !important;
        }
        
        .section-chevron {
            font-size: 8px !important;
            color: #64748b !important;
            transition: transform 0.2s ease !important;
        }
        
        .section-chevron.expanded {
            transform: rotate(90deg) !important;
        }
        
        /* Navigation Items Container - Compact tree */
        .nav-items-container {
            margin-left: 12px !important;
            border-left: 1px solid rgba(255, 255, 255, 0.03) !important;
            padding-left: 8px !important;
            margin-bottom: 8px !important;
        }
        
        /* Hide all Streamlit button styling completely */
        .stButton {
            margin: 0 !important;
            padding: 0 !important;
        }
        
        .stButton > button {
            background: transparent !important;
            border: none !important;
            border-radius: 0 !important;
            padding: 2px 4px !important;
            width: 100% !important;
            text-align: left !important;
            font-size: 12px !important;
            font-weight: 400 !important;
            color: #94a3b8 !important;
            transition: all 0.2s ease !important;
            margin: 0 !important;
            box-shadow: none !important;
            min-height: 20px !important;
            height: 20px !important;
        }
        
        .stButton > button:hover {
            background: transparent !important;
            color: #cbd5e1 !important;
            transform: none !important;
            box-shadow: none !important;
        }
        
        .stButton > button:focus {
            background: transparent !important;
            color: #00d4ff !important;
            outline: none !important;
            box-shadow: none !important;
        }
        
        .stButton > button:active {
            background: transparent !important;
            transform: none !important;
        }
        
        /* Active navigation item - like selected file */
        .active-nav-item .stButton > button {
            color: #00d4ff !important;
            font-weight: 500 !important;
        }
        
        .active-nav-item .stButton > button:hover {
            color: #00d4ff !important;
        }
        
        /* Navigation item row - very compact */
        .nav-item-row {
            display: flex !important;
            align-items: center !important;
            margin: 1px 0 !important;
            height: 20px !important;
        }
        
        /* File/nav item icons - very small */
        .nav-item-icon {
            color: #64748b !important;
            font-size: 9px !important;
            width: 12px !important;
            text-align: center !important;
            margin-right: 6px !important;
            margin-top: 0 !important;
        }
        
        .nav-item-icon.active {
            color: #00d4ff !important;
        }
        
        /* Streamlit columns - make them compact */
        .element-container {
            margin: 0 !important;
            padding: 0 !important;
        }
        
        .stColumn {
            padding: 0 !important;
            gap: 0 !important;
        }
        
        .stColumn > div {
            padding: 0 !important;
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
    """Render ultra-compact file explorer style sidebar with clean text headers"""
    
    # Define navigation structure
    nav_structure = {
        "Market Metrics": {
            "icon": "chart-area",
            "items": [
                {"name": "Price", "icon": "dollar-sign", "page": "Price"},
                {"name": "Market Cap", "icon": "coins", "page": "MarketCap"},
                {"name": "Trading Volume", "icon": "chart-bar", "page": "Volume"},
                {"name": "Supply", "icon": "layer-group", "page": "Supply"}
            ]
        },
        "Mining": {
            "icon": "microchip",
            "items": [
                {"name": "Hashrate", "icon": "tachometer-alt", "page": "Hashrate"},
                {"name": "Difficulty", "icon": "puzzle-piece", "page": "Difficulty"},
                {"name": "Mining Revenue", "icon": "money-bill-wave", "page": "Revenue"}
            ]
        },
        "Network": {
            "icon": "network-wired",
            "items": [
                {"name": "Transactions", "icon": "exchange-alt", "page": "Transactions"},
                {"name": "Addresses", "icon": "wallet", "page": "Addresses"},
                {"name": "Blocks", "icon": "cube", "page": "Blocks"}
            ]
        }
    }
    
    # Initialize session state for expanded sections
    if 'expanded_sections' not in st.session_state:
        st.session_state.expanded_sections = {
            "Market Metrics": True,  # Start with Market Metrics expanded
            "Mining": False,
            "Network": False
        }
    
    # Auto-expand section that contains current page
    for section_name, section_data in nav_structure.items():
        if any(item["page"] == current_page for item in section_data["items"]):
            st.session_state.expanded_sections[section_name] = True
    
    with st.sidebar:
        # Add minimal spacing
        st.markdown('<div style="height: 8px;"></div>', unsafe_allow_html=True)
        
        for section_name, section_data in nav_structure.items():
            is_expanded = st.session_state.expanded_sections.get(section_name, False)
            chevron_icon = "fa-chevron-down" if is_expanded else "fa-chevron-right"
            
            # Create clickable section header with clean HTML
            section_id = section_name.replace(' ', '_')
            
            # Use HTML for clean clickable header
            header_html = f'''
            <div class="sidebar-section-header" onclick="toggleSection_{section_id}()" style="cursor: pointer;">
                <i class="fas {chevron_icon} section-chevron"></i>
                <i class="fas fa-{section_data['icon']} section-icon"></i>
                <span>{section_name}</span>
            </div>
            
            <script>
            function toggleSection_{section_id}() {{
                // Use Streamlit's component communication
                window.parent.postMessage({{
                    type: 'streamlit:setComponentValue',
                    value: 'toggle_{section_id}'
                }}, '*');
            }}
            </script>
            '''
            
            st.markdown(header_html, unsafe_allow_html=True)
            
            # Hidden button to handle the toggle logic
            if st.button("", key=f"hidden_toggle_{section_id}", help="", label_visibility="hidden"):
                st.session_state.expanded_sections[section_name] = not st.session_state.expanded_sections[section_name]
                st.rerun()
            
            # Hide the button with CSS
            st.markdown(f'''
            <style>
            button[data-testid="baseButton-secondary"]:has-text("") {{
                display: none !important;
            }}
            div[data-testid="stButton"]:has(button[data-testid="baseButton-secondary"]:empty) {{
                display: none !important;
            }}
            </style>
            ''', unsafe_allow_html=True)
            
            # Show navigation items only if expanded
            if is_expanded:
                st.markdown('<div class="nav-items-container">', unsafe_allow_html=True)
                
                for item in section_data["items"]:
                    # Create compact row
                    col_icon, col_button = st.columns([1, 8])
                    
                    with col_icon:
                        icon_class = "active" if item["page"] == current_page else ""
                        st.markdown(f'<i class="fas fa-{item["icon"]} nav-item-icon {icon_class}"></i>', unsafe_allow_html=True)
                    
                    with col_button:
                        # Apply active styling
                        container_class = "active-nav-item" if item["page"] == current_page else ""
                        if container_class:
                            st.markdown(f'<div class="{container_class}">', unsafe_allow_html=True)
                        
                        # Compact navigation button
                        if st.button(
                            item["name"], 
                            key=f"nav_{item['page']}", 
                            use_container_width=True
                        ):
                            st.write(f"Navigate to {item['name']}")
                            # st.switch_page(f"pages/{item['page']}.py")
                        
                        if container_class:
                            st.markdown('</div>', unsafe_allow_html=True)
                
                st.markdown('</div>', unsafe_allow_html=True)
            
            # Minimal spacing between sections
            st.markdown('<div style="height: 4px;"></div>', unsafe_allow_html=True)
    
    # Alternative simpler approach - using clickable text with session state
    # This creates a much cleaner interface

def render_simple_page_header(title, subtitle=None):
    """Simple page header without breadcrumbs"""
    
    subtitle_html = f'<p style="color: #94a3b8; font-size: 16px; margin: 8px 0 0 0;">{subtitle}</p>' if subtitle else ""
    
    page_header_html = f'<div style="padding: 0 0 32px 0;"><h1 style="color: #f1f5f9; font-size: 36px; font-weight: 800; margin: 0;">{title}</h1>{subtitle_html}</div>'
    
    st.markdown(page_header_html, unsafe_allow_html=True)
