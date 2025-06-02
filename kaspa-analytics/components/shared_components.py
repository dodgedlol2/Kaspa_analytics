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
        
        /* Ultra-simple clean text sidebar */
        section[data-testid="stSidebar"] {
            background: rgba(10, 14, 26, 0.95) !important;
            border-right: 1px solid rgba(0, 212, 255, 0.15) !important;
            margin-top: 100px !important;
            backdrop-filter: blur(25px) !important;
            box-shadow: 8px 0 32px rgba(0, 0, 0, 0.4) !important;
        }
        
        /* FORCE COLLAPSE BUTTON TO BE VISIBLE */
        button[data-testid="collapsedControl"] {
            display: block !important;
            position: fixed !important;
            top: 110px !important;
            left: 16px !important;
            z-index: 999999999 !important; /* Higher than header */
            background: rgba(0, 212, 255, 0.8) !important;
            border: 2px solid rgba(0, 212, 255, 1) !important;
            border-radius: 6px !important;
            width: 28px !important;
            height: 28px !important;
            color: white !important;
            box-shadow: 0 4px 12px rgba(0, 212, 255, 0.4) !important;
        }
        
        button[data-testid="collapsedControl"]:hover {
            background: rgba(0, 212, 255, 1) !important;
            transform: scale(1.1) !important;
        }
        
        /* Alternative selectors for collapse button */
        .css-1rs6os {
            display: block !important;
            position: fixed !important;
            top: 110px !important;
            left: 16px !important;
            z-index: 999999999 !important;
        }
        
        /* Ensure sidebar toggle button is always there */
        div[data-testid="stSidebarCollapse"] {
            display: block !important;
            position: fixed !important;
            top: 110px !important;
            left: 16px !important;
            z-index: 999999999 !important;
        }
        
        /* Hide default Streamlit sidebar content */
        section[data-testid="stSidebar"] > div {
            background: transparent !important;
            padding: 16px 12px !important;
        }
        
        /* AGGRESSIVE HIDING OF VIEW MORE/LESS BUTTONS */
        section[data-testid="stSidebar"] button[data-testid="baseButton-minimal"] {
            display: none !important;
        }
        
        section[data-testid="stSidebar"] button:contains("View") {
            display: none !important;
        }
        
        section[data-testid="stSidebar"] .css-1vq4p4l {
            display: none !important;
        }
        
        section[data-testid="stSidebar"] .css-1rs6os.edgvbvh3 {
            display: none !important;
        }
        
        section[data-testid="stSidebar"] button[title*="View"] {
            display: none !important;
        }
        
        section[data-testid="stSidebar"] button[aria-label*="View"] {
            display: none !important;
        }
        
        /* Nuclear option - hide ALL buttons except collapse button */
        section[data-testid="stSidebar"] button:not([data-testid="collapsedControl"]) {
            display: none !important;
        }
        
        /* HIDE ALL STREAMLIT DEFAULT NAVIGATION */
        nav[data-testid="stSidebarNav"] { display: none !important; }
        .css-1d391kg .css-1v3fvcr { display: none !important; }
        .css-1d391kg .css-17eq0hr { display: none !important; }
        .css-1dp5vir { display: none !important; }
        section[data-testid="stSidebar"] nav { display: none !important; }
        section[data-testid="stSidebar"] ul { display: none !important; }
        section[data-testid="stSidebar"] .css-17eq0hr { display: none !important; }
        .stRadio { display: none !important; }
        .stSelectbox { display: none !important; }
        
        /* Head metrics styling */
        .head-metric {
            font-size: 12px !important;
            font-weight: 600 !important;
            color: #94a3b8 !important;
            text-transform: uppercase !important;
            letter-spacing: 0.5px !important;
            margin: 16px 0 8px 0 !important;
            cursor: pointer !important;
            transition: color 0.2s ease !important;
            display: flex !important;
            align-items: center !important;
            gap: 6px !important;
        }
        
        .head-metric:hover {
            color: #cbd5e1 !important;
        }
        
        .head-metric:first-child {
            margin-top: 8px !important;
        }
        
        /* Sub metrics styling */
        .sub-metric {
            font-size: 12px !important;
            font-weight: 600 !important;
            color: #64748b !important;
            text-transform: uppercase !important;
            letter-spacing: 0.5px !important;
            margin: 4px 0 4px 16px !important;
            cursor: pointer !important;
            transition: color 0.2s ease !important;
            display: flex !important;
            align-items: center !important;
            gap: 6px !important;
        }
        
        .sub-metric:hover {
            color: #94a3b8 !important;
        }
        
        .sub-metric.active {
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
    """Super simple clean text sidebar - no complex functionality"""
    
    # Simple navigation structure
    navigation = [
        {
            "head": "📊 MARKET METRICS",
            "items": [
                "💰 PRICE",
                "🪙 MARKET CAP", 
                "📈 TRADING VOLUME",
                "📦 SUPPLY"
            ]
        },
        {
            "head": "⛏️ MINING",
            "items": [
                "⚡ HASHRATE",
                "🧩 DIFFICULTY", 
                "💰 MINING REVENUE"
            ]
        },
        {
            "head": "🌐 NETWORK",
            "items": [
                "🔄 TRANSACTIONS",
                "👛 ADDRESSES",
                "🧊 BLOCKS"
            ]
        }
    ]
    
    # Build simple HTML
    sidebar_html = ""
    
    for section in navigation:
        # Head metric
        sidebar_html += f'<div class="head-metric">{section["head"]}</div>'
        
        # Sub metrics
        for item in section["items"]:
            active_class = "active" if "PRICE" in item and current_page == "Price" else ""
            sidebar_html += f'<div class="sub-metric {active_class}">{item}</div>'
    
    # Render in sidebar
    with st.sidebar:
        st.markdown(sidebar_html, unsafe_allow_html=True)

def render_simple_page_header(title, subtitle=None):
    """Simple page header without breadcrumbs"""
    
    subtitle_html = f'<p style="color: #94a3b8; font-size: 16px; margin: 8px 0 0 0;">{subtitle}</p>' if subtitle else ""
    
    page_header_html = f'<div style="padding: 0 0 32px 0;"><h1 style="color: #f1f5f9; font-size: 36px; font-weight: 800; margin: 0;">{title}</h1>{subtitle_html}</div>'
    
    st.markdown(page_header_html, unsafe_allow_html=True)
