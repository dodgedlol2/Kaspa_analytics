import streamlit as st
from datetime import datetime

# Try to import the hover tabs component
try:
    from st_on_hover_tabs import on_hover_tabs
    HOVER_TABS_AVAILABLE = True
except ImportError:
    HOVER_TABS_AVAILABLE = False

def render_page_config(page_title="Kaspa Analytics Pro", page_icon="💎"):
    """Set consistent page config across all pages"""
    st.set_page_config(
        page_title=page_title,
        page_icon=page_icon,
        layout="wide",
        initial_sidebar_state="expanded"
    )

def render_hover_tabs_sidebar():
    """Render navigation using hover tabs component if available"""
    
    if not HOVER_TABS_AVAILABLE:
        st.sidebar.error("streamlit-on-Hover-tabs not installed. Add 'streamlit-on-Hover-tabs==0.0.2' to requirements.txt")
        return "Home"  # Default fallback
    
    # Define your pages to match your actual page files
    tab_names = [
        'Home',
        'Price', 
        'Hashrate Analysis', 
        'Market Cap', 
        'Kaspa Price vs Trading Volume',
        'Kaspa Trading Volume', 
        'Kaspa Price vs Hashrate', 
        'Kaspa Price Hashrate and PH-Ratio Deviation',
        'Power Law Residual of Kaspa Price Relative to Network Hashrate',
        'Test Page', 
        'Wallet Tracker'
    ]
    
    # Material Icons (Google Material Icons)
    icon_names = [
        'home',                  # Home
        'trending_up',           # Price
        'flash_on',              # Hashrate Analysis  
        'account_balance',       # Market Cap
        'show_chart',            # Price vs Volume
        'bar_chart',             # Trading Volume
        'timeline',              # Price vs Hashrate
        'analytics',             # PH-Ratio Deviation
        'functions',             # Power Law Residual
        'science',               # Test Page
        'account_balance_wallet' # Wallet Tracker
    ]
    
    with st.sidebar:
        # Add some spacing from the top
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Simple title
        st.markdown("### 🔍 Navigation")
        st.markdown("---")
        
        selected_tab = on_hover_tabs(
            tabName=tab_names,
            iconName=icon_names,
            styles={
                'navtab': {
                    'background-color': 'transparent',
                    'color': '#ffffff',
                    'font-size': '14px',
                    'transition': '.3s',
                    'white-space': 'nowrap',
                    'font-weight': '500',
                    'padding': '10px 0'
                },
                'tabStyle': {
                    ':hover': {
                        'color': '#00d4ff',
                        'cursor': 'pointer',
                        'background-color': 'rgba(0, 212, 255, 0.1)'
                    }
                },
                'tabStyle': {
                    'list-style-type': 'none',
                    'margin-bottom': '8px',
                    'padding': '12px 16px',
                    'border-radius': '8px',
                    'transition': 'all 0.3s ease',
                    'display': 'flex',
                    'align-items': 'center'
                },
                'iconStyle': {
                    'position': 'relative',
                    'left': '0px',
                    'text-align': 'left',
                    'color': 'inherit',
                    'margin-right': '12px',
                    'font-size': '18px'
                },
                'labelName': {
                    'color': 'inherit',
                    'font-size': '14px',
                    'font-weight': '500'
                }
            },
            default_choice=0,
            key="main_navigation"
        )
        
        # Add some info at the bottom
        st.markdown("---")
        st.markdown("**Kaspa Analytics**")
        st.markdown("Select a page from above to navigate")
    
    return selected_tab

def render_basic_sidebar_fallback():
    """Basic fallback sidebar if hover tabs not available"""
    with st.sidebar:
        st.markdown("### 🔍 Navigation")
        st.markdown("---")
        
        # Simple radio buttons as fallback
        pages = [
            'Home',
            'Price', 
            'Hashrate Analysis', 
            'Market Cap', 
            'Kaspa Price vs Trading Volume',
            'Kaspa Trading Volume', 
            'Kaspa Price vs Hashrate', 
            'Kaspa Price Hashrate and PH-Ratio Deviation',
            'Power Law Residual of Kaspa Price Relative to Network Hashrate',
            'Test Page', 
            'Wallet Tracker'
        ]
        
        selected = st.radio("Select Page:", pages, index=0)
        
        st.markdown("---")
        st.markdown("**Kaspa Analytics**")
        st.markdown("Basic navigation fallback")
        
        return selected

def render_simple_page_header(title, subtitle=None):
    """Simple page header without breadcrumbs"""
    
    subtitle_html = f'<p style="color: #94a3b8; font-size: 16px; margin: 8px 0 0 0;">{subtitle}</p>' if subtitle else ""
    
    page_header_html = f'<div style="padding: 0 0 32px 0;"><h1 style="color: #f1f5f9; font-size: 36px; font-weight: 800; margin: 0;">{title}</h1>{subtitle_html}</div>'
    
    st.markdown(page_header_html, unsafe_allow_html=True)

# Basic CSS for minimal styling
def render_basic_css():
    """Basic CSS for the hover tabs"""
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/icon?family=Material+Icons');
        
        /* Basic sidebar styling */
        .stSidebar {
            background-color: #1e293b;
        }
        
        /* Material Icons support */
        .material-icons {
            font-size: 18px !important;
            color: inherit !important;
        }
        
        /* Basic hover effects for tabs */
        .on-hover-tab {
            transition: all 0.3s ease !important;
        }
        
        .on-hover-tab:hover {
            background-color: rgba(0, 212, 255, 0.1) !important;
            color: #00d4ff !important;
        }
    </style>
    """, unsafe_allow_html=True)
