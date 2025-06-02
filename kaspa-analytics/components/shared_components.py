import streamlit as st
from datetime import datetime

def render_page_config(page_title="Kaspa Analytics Pro", page_icon="💎"):
    """Set consistent page config across all pages"""
    st.set_page_config(
        page_title=page_title,
        page_icon=page_icon,
        layout="wide",
        initial_sidebar_state="expanded"  # Show sidebar by default
    )

def render_custom_css_with_sidebar():
    """Enhanced CSS with proper header layout and left sidebar"""
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
        @import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css');
        
        /* Base styles */
        html, body, .stApp {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
            background: linear-gradient(135deg, #0a0e1a 0%, #1a1f2e 50%, #0f1419 100%) !important;
            color: #e2e8f0 !important;
            overflow-x: hidden !important;
        }
        
        .stApp {
            background-attachment: fixed !important;
        }
        
        /* Professional Header - Clean layout */
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
        
        /* Brand section - Left side */
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
        
        /* Auth section - Right side */
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
        
        /* Hide the top navigation from header */
        .nav-section {
            display: none !important;
        }
        
        /* Sidebar Styling */
        section[data-testid="stSidebar"] {
            background: rgba(15, 20, 25, 0.95) !important;
            border-right: 1px solid rgba(0, 212, 255, 0.2) !important;
            margin-top: 80px !important;
            backdrop-filter: blur(25px) !important;
        }
        
        .sidebar-nav {
            padding: 20px 0 !important;
        }
        
        .sidebar-nav-item {
            display: flex !important;
            align-items: center !important;
            gap: 12px !important;
            padding: 12px 20px !important;
            margin: 4px 10px !important;
            border-radius: 12px !important;
            color: #cbd5e1 !important;
            text-decoration: none !important;
            font-size: 14px !important;
            font-weight: 500 !important;
            transition: all 0.3s ease !important;
            cursor: pointer !important;
            border: 1px solid transparent !important;
        }
        
        .sidebar-nav-item:hover {
            background: rgba(0, 212, 255, 0.1) !important;
            border-color: rgba(0, 212, 255, 0.3) !important;
            color: #00d4ff !important;
        }
        
        .sidebar-nav-item.active {
            background: rgba(0, 212, 255, 0.15) !important;
            border-color: rgba(0, 212, 255, 0.5) !important;
            color: #00d4ff !important;
        }
        
        .sidebar-nav-icon {
            width: 18px !important;
            text-align: center !important;
        }
        
        /* Main content adjustments */
        .main .block-container {
            padding-top: 100px !important;
            padding-left: 20px !important;
            padding-right: 20px !important;
            max-width: 100% !important;
        }
        
        /* Streamlit sidebar content styling */
        .css-1d391kg .css-1v3fvcr {
            background: transparent !important;
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
            
            .brand-subtitle {
                font-size: 10px !important;
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

def render_sidebar_navigation(current_page="Home"):
    """Render navigation in the sidebar"""
    
    nav_items = [
        {"name": "Dashboard", "icon": "fas fa-tachometer-alt", "page": "Dashboard"},
        {"name": "Price Analysis", "icon": "fas fa-chart-line", "page": "Analytics"},
        {"name": "Portfolio", "icon": "fas fa-wallet", "page": "Portfolio"},
        {"name": "Research", "icon": "fas fa-microscope", "page": "Research"},
        {"name": "Alerts", "icon": "fas fa-bell", "page": "Alerts"},
        {"name": "Settings", "icon": "fas fa-cog", "page": "Settings"},
    ]
    
    # Custom sidebar navigation
    st.sidebar.markdown("## Navigation")
    
    for item in nav_items:
        active_class = "active" if item["page"] == current_page else ""
        
        # Using columns for better layout
        col_icon, col_text = st.sidebar.columns([1, 4])
        
        with col_icon:
            if item["page"] == current_page:
                st.markdown(f'<i class="{item["icon"]}" style="color: #00d4ff;"></i>', unsafe_allow_html=True)
            else:
                st.markdown(f'<i class="{item["icon"]}" style="color: #cbd5e1;"></i>', unsafe_allow_html=True)
        
        with col_text:
            if st.button(item["name"], key=f"nav_{item['page']}", use_container_width=True):
                st.switch_page(f"pages/{item['page']}.py")
    
    # Add separator
    st.sidebar.markdown("---")
    
    # Add some quick stats or info
    st.sidebar.markdown("### Quick Stats")
    st.sidebar.metric("KAS Price", "$0.0873", "2.4%")
    st.sidebar.metric("24h Volume", "$45.2M", "-5.1%")

def render_simple_page_header(title, subtitle=None):
    """Simple page header without breadcrumbs"""
    
    subtitle_html = f'<p style="color: #94a3b8; font-size: 16px; margin: 8px 0 0 0;">{subtitle}</p>' if subtitle else ""
    
    page_header_html = f'<div style="padding: 0 0 32px 0;"><h1 style="color: #f1f5f9; font-size: 36px; font-weight: 800; margin: 0;">{title}</h1>{subtitle_html}</div>'
    
    st.markdown(page_header_html, unsafe_allow_html=True)
