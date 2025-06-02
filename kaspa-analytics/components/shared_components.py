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
        
        /* Header Styles */
        .professional-header {
            background: rgba(15, 20, 25, 0.95);
            backdrop-filter: blur(25px);
            border-bottom: 1px solid rgba(0, 212, 255, 0.2);
            padding: 16px 40px;
            position: sticky;
            top: 0;
            z-index: 1000;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
            margin-bottom: 2rem;
        }
        
        .header-content {
            display: flex;
            align-items: center;
            justify-content: space-between;
            max-width: 1400px;
            margin: 0 auto;
        }
        
        .brand-section {
            display: flex;
            align-items: center;
            gap: 20px;
        }
        
        .logo-container {
            display: flex;
            align-items: center;
            gap: 12px;
        }
        
        .logo {
            width: 45px;
            height: 45px;
            background: linear-gradient(135deg, #00d4ff 0%, #ff00a8 100%);
            border-radius: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 24px;
            color: white;
            font-weight: 800;
            box-shadow: 0 4px 15px rgba(0, 212, 255, 0.3);
        }
        
        .brand-text h1 {
            font-size: 28px;
            font-weight: 800;
            background: linear-gradient(135deg, #00d4ff 0%, #ff00a8 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin: 0;
            text-shadow: 0 0 30px rgba(0, 212, 255, 0.3);
            line-height: 1.1;
        }
        
        .brand-subtitle {
            font-size: 12px;
            color: #64748b;
            font-weight: 500;
            text-transform: uppercase;
            letter-spacing: 1.2px;
            margin-top: 2px;
        }
        
        .nav-section {
            display: flex;
            align-items: center;
            gap: 8px;
        }
        
        .nav-button {
            background: rgba(30, 41, 59, 0.6);
            border: 1px solid rgba(100, 116, 139, 0.3);
            border-radius: 12px;
            padding: 10px 16px;
            color: #cbd5e1;
            text-decoration: none;
            font-size: 13px;
            font-weight: 600;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            backdrop-filter: blur(10px);
            display: flex;
            align-items: center;
            gap: 8px;
            cursor: pointer;
        }
        
        .nav-button:hover {
            background: rgba(0, 212, 255, 0.1);
            border-color: rgba(0, 212, 255, 0.4);
            color: #00d4ff;
            transform: translateY(-1px);
            box-shadow: 0 4px 15px rgba(0, 212, 255, 0.2);
        }
        
        .nav-button.active {
            background: rgba(0, 212, 255, 0.15);
            border-color: rgba(0, 212, 255, 0.5);
            color: #00d4ff;
        }
        
        .auth-section {
            display: flex;
            align-items: center;
            gap: 12px;
        }
        
        .login-button {
            background: transparent;
            border: 1px solid rgba(100, 116, 139, 0.4);
            border-radius: 10px;
            padding: 8px 16px;
            color: #cbd5e1;
            font-size: 13px;
            font-weight: 600;
            transition: all 0.3s ease;
            cursor: pointer;
        }
        
        .login-button:hover {
            border-color: rgba(0, 212, 255, 0.6);
            color: #00d4ff;
        }
        
        .signup-button {
            background: linear-gradient(135deg, #00d4ff 0%, #0099cc 100%);
            border: none;
            border-radius: 10px;
            padding: 10px 20px;
            color: white;
            font-size: 13px;
            font-weight: 700;
            transition: all 0.3s ease;
            cursor: pointer;
            box-shadow: 0 4px 15px rgba(0, 212, 255, 0.3);
        }
        
        .signup-button:hover {
            transform: translateY(-1px);
            box-shadow: 0 6px 20px rgba(0, 212, 255, 0.4);
        }
        
        .user-menu {
            display: flex;
            align-items: center;
            gap: 10px;
            background: rgba(30, 41, 59, 0.6);
            border: 1px solid rgba(100, 116, 139, 0.3);
            border-radius: 12px;
            padding: 8px 12px;
            cursor: pointer;
            transition: all 0.3s ease;
        }
        
        .user-menu:hover {
            background: rgba(30, 41, 59, 0.8);
            border-color: rgba(0, 212, 255, 0.4);
        }
        
        .user-avatar {
            width: 32px;
            height: 32px;
            border-radius: 8px;
            background: linear-gradient(135deg, #00d4ff 0%, #ff00a8 100%);
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-weight: 700;
            font-size: 14px;
        }
        
        .user-info {
            display: flex;
            flex-direction: column;
            align-items: flex-start;
        }
        
        .user-name {
            font-size: 13px;
            font-weight: 600;
            color: #f1f5f9;
            line-height: 1;
        }
        
        .user-role {
            font-size: 11px;
            color: #64748b;
            line-height: 1;
        }
        
        /* Responsive Design */
        @media (max-width: 768px) {
            .professional-header {
                padding: 12px 20px;
            }
            
            .header-content {
                flex-direction: column;
                gap: 15px;
            }
            
            .nav-section {
                flex-wrap: wrap;
                justify-content: center;
            }
            
            .brand-text h1 {
                font-size: 24px;
            }
            
            .nav-button {
                padding: 8px 12px;
                font-size: 12px;
            }
        }
        
        /* Hide Streamlit elements */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        .stDeployButton {display: none;}
        
    </style>
    """, unsafe_allow_html=True)

def render_professional_header(
    current_page="Home",
    user_name=None,
    user_role=None,
    show_auth=True,
    custom_nav_items=None
):
    """
    Render a professional header with navigation and auth
    
    Args:
        current_page (str): Current active page name
        user_name (str): Logged in user name (None if not logged in)
        user_role (str): User role/subscription level
        show_auth (bool): Whether to show auth buttons
        custom_nav_items (list): Custom navigation items [{"name": "Page", "icon": "fas fa-icon"}]
    """
    
    # Default navigation items
    default_nav_items = [
        {"name": "Dashboard", "icon": "fas fa-tachometer-alt"},
        {"name": "Analytics", "icon": "fas fa-chart-line"},
        {"name": "Portfolio", "icon": "fas fa-wallet"},
        {"name": "Research", "icon": "fas fa-microscope"},
        {"name": "Alerts", "icon": "fas fa-bell"},
    ]
    
    nav_items = custom_nav_items if custom_nav_items else default_nav_items
    
    # Build navigation buttons
    nav_buttons_html = ""
    for item in nav_items:
        active_class = "active" if item["name"] == current_page else ""
        nav_buttons_html += f"""
        <div class="nav-button {active_class}">
            <i class="{item['icon']}"></i>
            <span>{item['name']}</span>
        </div>
        """
    
    # Build auth section
    if user_name:
        # User is logged in
        user_initials = "".join([name[0].upper() for name in user_name.split()[:2]])
        auth_html = f"""
        <div class="user-menu">
            <div class="user-avatar">{user_initials}</div>
            <div class="user-info">
                <div class="user-name">{user_name}</div>
                <div class="user-role">{user_role or 'Free Plan'}</div>
            </div>
            <i class="fas fa-chevron-down" style="color: #64748b; font-size: 12px;"></i>
        </div>
        """
    else:
        # User not logged in
        auth_html = """
        <div class="auth-section">
            <button class="login-button">
                <i class="fas fa-sign-in-alt"></i>
                Login
            </button>
            <button class="signup-button">
                <i class="fas fa-rocket"></i>
                Get Started
            </button>
        </div>
        """ if show_auth else ""
    
    # Complete header HTML
    header_html = f"""
    <div class="professional-header">
        <div class="header-content">
            <div class="brand-section">
                <div class="logo-container">
                    <div class="logo">
                        <i class="fas fa-gem"></i>
                    </div>
                    <div class="brand-text">
                        <h1>KaspaMetrics</h1>
                        <div class="brand-subtitle">Advanced Market Intelligence Platform</div>
                    </div>
                </div>
            </div>
            
            <div class="nav-section">
                {nav_buttons_html}
            </div>
            
            <div class="auth-section">
                {auth_html}
            </div>
        </div>
    </div>
    """
    
    st.markdown(header_html, unsafe_allow_html=True)

def render_page_header(title, subtitle=None, show_breadcrumb=False, breadcrumb_items=None):
    """
    Render a page-specific header section
    
    Args:
        title (str): Page title
        subtitle (str): Page subtitle/description
        show_breadcrumb (bool): Whether to show breadcrumb navigation
        breadcrumb_items (list): Breadcrumb items ["Home", "Analytics", "Price Analysis"]
    """
    
    breadcrumb_html = ""
    if show_breadcrumb and breadcrumb_items:
        breadcrumb_parts = []
        for i, item in enumerate(breadcrumb_items):
            if i == len(breadcrumb_items) - 1:
                # Last item (current page)
                breadcrumb_parts.append(f'<span style="color: #00d4ff;">{item}</span>')
            else:
                breadcrumb_parts.append(f'<span style="color: #64748b;">{item}</span>')
        
        breadcrumb_html = f"""
        <div style="margin-bottom: 16px;">
            <div style="font-size: 12px; color: #64748b; display: flex; align-items: center; gap: 8px;">
                {' <i class="fas fa-chevron-right" style="font-size: 10px;"></i> '.join(breadcrumb_parts)}
            </div>
        </div>
        """
    
    subtitle_html = f'<p style="color: #94a3b8; font-size: 16px; margin: 8px 0 0 0; font-weight: 400;">{subtitle}</p>' if subtitle else ""
    
    page_header_html = f"""
    <div style="padding: 0 40px 32px 40px;">
        {breadcrumb_html}
        <h1 style="color: #f1f5f9; font-size: 36px; font-weight: 800; margin: 0; line-height: 1.2;">
            {title}
        </h1>
        {subtitle_html}
    </div>
    """
    
    st.markdown(page_header_html, unsafe_allow_html=True)

# Utility function to easily update branding
def update_branding(
    app_name="KaspaMetrics",
    subtitle="Advanced Market Intelligence Platform",
    primary_color="#00d4ff",
    secondary_color="#ff00a8",
    logo_icon="fas fa-gem"
):
    """
    Utility function to easily update app branding
    Call this before render_custom_css() to customize colors and branding
    """
    # This could be expanded to dynamically update CSS variables
    # For now, it serves as a template for future customization
    return {
        "app_name": app_name,
        "subtitle": subtitle,
        "primary_color": primary_color,
        "secondary_color": secondary_color,
        "logo_icon": logo_icon
    }
