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
        
        /* Beautiful Sidebar Styling - GitHub/File Explorer Style */
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
            padding: 16px 8px !important;
        }
        
        /* Section Headers - Always visible like folder names */
        .sidebar-section-header {
            display: flex !important;
            align-items: center !important;
            gap: 8px !important;
            padding: 8px 12px !important;
            font-size: 13px !important;
            font-weight: 600 !important;
            color: #94a3b8 !important;
            text-transform: uppercase !important;
            letter-spacing: 0.5px !important;
            margin: 16px 0 8px 0 !important;
            border-bottom: 1px solid rgba(255, 255, 255, 0.05) !important;
            cursor: pointer !important;
            transition: all 0.3s ease !important;
        }
        
        .sidebar-section-header:hover {
            color: #cbd5e1 !important;
        }
        
        .section-icon {
            color: #64748b !important;
            font-size: 12px !important;
            width: 14px !important;
            text-align: center !important;
        }
        
        .section-chevron {
            font-size: 10px !important;
            color: #64748b !important;
            transition: transform 0.3s ease !important;
            margin-left: auto !important;
        }
        
        .section-chevron.expanded {
            transform: rotate(90deg) !important;
        }
        
        /* Navigation Items Container - Like file tree */
        .nav-items-container {
            margin-left: 16px !important;
            border-left: 1px solid rgba(255, 255, 255, 0.05) !important;
            padding-left: 8px !important;
        }
        
        /* Individual Navigation Items - Like files */
        .nav-item-row {
            display: flex !important;
            align-items: center !important;
            margin: 2px 0 !important;
        }
        
        /* Remove all button styling to make it look like file explorer */
        .stButton > button {
            background: transparent !important;
            border: none !important;
            border-radius: 6px !important;
            padding: 6px 8px !important;
            width: 100% !important;
            text-align: left !important;
            font-size: 13px !important;
            font-weight: 500 !important;
            color: #94a3b8 !important;
            transition: all 0.2s ease !important;
            margin: 0 !important;
            box-shadow: none !important;
        }
        
        .stButton > button:hover {
            background: rgba(0, 212, 255, 0.08) !important;
            color: #cbd5e1 !important;
            transform: none !important;
        }
        
        .stButton > button:focus {
            background: rgba(0, 212, 255, 0.12) !important;
            color: #00d4ff !important;
            outline: none !important;
            box-shadow: none !important;
        }
        
        /* Active button styling - like selected file */
        .active-nav-item .stButton > button {
            background: rgba(0, 212, 255, 0.15) !important;
            color: #00d4ff !important;
            font-weight: 600 !important;
        }
        
        .active-nav-item .stButton > button:hover {
            background: rgba(0, 212, 255, 0.2) !important;
        }
        
        /* File/nav item icons */
        .nav-item-icon {
            color: #64748b !important;
            font-size: 11px !important;
            width: 16px !important;
            text-align: center !important;
            margin-right: 4px !important;
        }
        
        .nav-item-icon.active {
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
    """Render clean file explorer/GitHub style sidebar navigation"""
    
    # Define navigation structure
    nav_structure = {
        "Market Metrics": {
            "icon": "chart-area",
            "expanded": True,  # Market Metrics always expanded by default
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
    
    # Check which sections should be expanded based on current page
    for section_name, section_data in nav_structure.items():
        if any(item["page"] == current_page for item in section_data["items"]):
            section_data["expanded"] = True
    
    with st.sidebar:
        # Add some spacing at the top
        st.markdown("")
        
        for section_name, section_data in nav_structure.items():
            # Section header - always visible like folder name
            chevron_direction = "expanded" if section_data["expanded"] else ""
            st.markdown(f'''
            <div class="sidebar-section-header" onclick="toggleSection('{section_name.replace(' ', '')}')">
                <i class="fas fa-chevron-right section-chevron {chevron_direction}" id="chevron-{section_name.replace(' ', '')}"></i>
                <i class="fas fa-{section_data['icon']} section-icon"></i>
                <span>{section_name}</span>
            </div>
            ''', unsafe_allow_html=True)
            
            # Navigation items container - only show if expanded
            if section_data["expanded"]:
                st.markdown('<div class="nav-items-container">', unsafe_allow_html=True)
                
                for item in section_data["items"]:
                    # Create a row for each navigation item
                    st.markdown('<div class="nav-item-row">', unsafe_allow_html=True)
                    
                    # Icon + Button in columns
                    col_icon, col_button = st.columns([1, 6])
                    
                    with col_icon:
                        icon_class = "active" if item["page"] == current_page else ""
                        st.markdown(f'<i class="fas fa-{item["icon"]} nav-item-icon {icon_class}"></i>', unsafe_allow_html=True)
                    
                    with col_button:
                        # Apply active styling if this is the current page
                        container_class = "active-nav-item" if item["page"] == current_page else ""
                        st.markdown(f'<div class="{container_class}">', unsafe_allow_html=True)
                        
                        if st.button(
                            item["name"], 
                            key=f"nav_{item['page']}", 
                            use_container_width=True
                        ):
                            st.write(f"Navigate to {item['name']}")
                            # st.switch_page(f"pages/{item['page']}.py")
                        
                        st.markdown('</div>', unsafe_allow_html=True)
                    
                    st.markdown('</div>', unsafe_allow_html=True)
                
                st.markdown('</div>', unsafe_allow_html=True)
        
        # JavaScript for section toggle functionality
        st.markdown('''
        <script>
        function toggleSection(sectionId) {
            const chevron = document.getElementById('chevron-' + sectionId);
            if (chevron.classList.contains('expanded')) {
                chevron.classList.remove('expanded');
            } else {
                chevron.classList.add('expanded');
            }
            // Note: In a real implementation, you'd also toggle the section visibility
            // For now, sections are controlled by Python logic
        }
        </script>
        ''', unsafe_allow_html=True)

def render_simple_page_header(title, subtitle=None):
    """Simple page header without breadcrumbs"""
    
    subtitle_html = f'<p style="color: #94a3b8; font-size: 16px; margin: 8px 0 0 0;">{subtitle}</p>' if subtitle else ""
    
    page_header_html = f'<div style="padding: 0 0 32px 0;"><h1 style="color: #f1f5f9; font-size: 36px; font-weight: 800; margin: 0;">{title}</h1>{subtitle_html}</div>'
    
    st.markdown(page_header_html, unsafe_allow_html=True)
