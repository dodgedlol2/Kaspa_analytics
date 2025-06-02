import streamlit as st
from datetime import datetime

def render_page_config(page_title="Kaspa Analytics Pro", page_icon="💎"):
    """Set consistent page config across all pages"""
    st.set_page_config(
        page_title=page_title,
        page_icon=page_icon,
        layout="wide",
        initial_sidebar_state="collapsed"
    )

def render_custom_css():
    """Render all custom CSS styling for the application"""
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
        
        /* Force header above everything */
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
            padding: 16px 40px !important;
            z-index: 999999999 !important;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.6) !important;
            display: flex !important;
            align-items: center !important;
            justify-content: space-between !important;
        }
        
        /* Push main content down */
        .main .block-container {
            padding-top: 100px !important;
            padding-left: 0 !important;
            padding-right: 0 !important;
            max-width: 100% !important;
        }
        
        /* Hide sidebar completely for now */
        section[data-testid="stSidebar"] {
            display: none !important;
        }
        
        /* Header content styling */
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
            gap: 20px !important;
        }
        
        .logo-container {
            display: flex !important;
            align-items: center !important;
            gap: 12px !important;
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
            font-size: 28px !important;
            font-weight: 800 !important;
            background: linear-gradient(135deg, #00d4ff 0%, #ff00a8 100%) !important;
            -webkit-background-clip: text !important;
            -webkit-text-fill-color: transparent !important;
            margin: 0 !important;
            line-height: 1.1 !important;
        }
        
        .brand-subtitle {
            font-size: 12px !important;
            color: #64748b !important;
            font-weight: 500 !important;
            text-transform: uppercase !important;
            letter-spacing: 1.2px !important;
            margin-top: 2px !important;
        }
        
        .nav-section {
            display: flex !important;
            align-items: center !important;
            gap: 8px !important;
        }
        
        .nav-button {
            background: rgba(30, 41, 59, 0.6) !important;
            border: 1px solid rgba(100, 116, 139, 0.3) !important;
            border-radius: 12px !important;
            padding: 10px 16px !important;
            color: #cbd5e1 !important;
            font-size: 13px !important;
            font-weight: 600 !important;
            display: flex !important;
            align-items: center !important;
            gap: 8px !important;
            cursor: pointer !important;
            transition: all 0.3s ease !important;
        }
        
        .nav-button:hover {
            background: rgba(0, 212, 255, 0.1) !important;
            border-color: rgba(0, 212, 255, 0.4) !important;
            color: #00d4ff !important;
            transform: translateY(-1px) !important;
        }
        
        .nav-button.active {
            background: rgba(0, 212, 255, 0.15) !important;
            border-color: rgba(0, 212, 255, 0.5) !important;
            color: #00d4ff !important;
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
        }
        
        /* Hide Streamlit elements */
        #MainMenu {visibility: hidden !important;}
        footer {visibility: hidden !important;}
        header {visibility: hidden !important;}
        .stDeployButton {display: none !important;}
        
        /* Mobile responsive */
        @media (max-width: 768px) {
            .professional-header {
                height: 120px !important;
                padding: 12px 20px !important;
            }
            
            .header-content {
                flex-direction: column !important;
                gap: 10px !important;
            }
            
            .main .block-container {
                padding-top: 140px !important;
            }
        }
    </style>
    """, unsafe_allow_html=True)

def render_professional_header(
    current_page="Home",
    user_name=None,
    user_role=None,
    show_auth=True,
    custom_nav_items=None
):
    """Render a professional header with navigation and auth"""
    
    # Default navigation items
    default_nav_items = [
        {"name": "Dashboard", "icon": "fas fa-tachometer-alt"},
        {"name": "Analytics", "icon": "fas fa-chart-line"},
        {"name": "Portfolio", "icon": "fas fa-wallet"},
        {"name": "Research", "icon": "fas fa-microscope"},
        {"name": "Alerts", "icon": "fas fa-bell"},
    ]
    
    nav_items = custom_nav_items if custom_nav_items else default_nav_items
    
    # Build navigation buttons - Fixed HTML escaping
    nav_buttons_html = ""
    for item in nav_items:
        active_class = "active" if item["name"] == current_page else ""
        nav_buttons_html += f'<div class="nav-button {active_class}"><i class="{item["icon"]}"></i><span>{item["name"]}</span></div>'
    
    # Build auth section - Fixed HTML
    if user_name:
        # User is logged in - create user menu
        user_initials = "".join([name[0].upper() for name in user_name.split()[:2]])
        auth_html = f'<div style="display: flex; align-items: center; gap: 10px; background: rgba(30, 41, 59, 0.6); border: 1px solid rgba(100, 116, 139, 0.3); border-radius: 12px; padding: 8px 12px;"><div style="width: 32px; height: 32px; border-radius: 8px; background: linear-gradient(135deg, #00d4ff 0%, #ff00a8 100%); display: flex; align-items: center; justify-content: center; color: white; font-weight: 700; font-size: 14px;">{user_initials}</div><div><div style="font-size: 13px; font-weight: 600; color: #f1f5f9;">{user_name}</div><div style="font-size: 11px; color: #64748b;">{user_role or "Free Plan"}</div></div></div>'
    else:
        # User not logged in - Fixed HTML on single line
        auth_html = '<div class="auth-section"><button class="login-button"><i class="fas fa-sign-in-alt"></i> Login</button><button class="signup-button"><i class="fas fa-rocket"></i> Get Started</button></div>' if show_auth else ""
    
    # Complete header HTML - all on single lines to avoid Streamlit markdown issues
    header_html = f'''
    <div class="professional-header">
        <div class="header-content">
            <div class="brand-section">
                <div class="logo-container">
                    <div class="logo"><i class="fas fa-gem"></i></div>
                    <div class="brand-text">
                        <h1>KaspaMetrics</h1>
                        <div class="brand-subtitle">Advanced Market Intelligence Platform</div>
                    </div>
                </div>
            </div>
            <div class="nav-section">{nav_buttons_html}</div>
            {auth_html}
        </div>
    </div>
    '''
    
    st.markdown(header_html, unsafe_allow_html=True)

       {title}
        </h1>
        {subtitle_html}
    </div>
    """
    
    st.markdown(page_header_html, unsafe_allow_html=True)
