import streamlit as st
from datetime import datetime
import os

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

def load_css_safely():
    """Load CSS for hover tabs component safely"""
    try:
        # Try to find style.css in the current directory
        css_path = './style.css'
        if os.path.exists(css_path):
            with open(css_path, 'r') as f:
                css_content = f.read()
            st.markdown(f'<style>{css_content}</style>', unsafe_allow_html=True)
        else:
            # Provide inline CSS as fallback
            st.markdown("""
            <style>
            @import url('https://fonts.googleapis.com/icon?family=Material+Icons');
            
            .css-1d391kg {
                background-color: #1e293b !important;
            }
            
            .stSidebar {
                background-color: #1e293b !important;
            }
            
            .material-icons {
                font-family: 'Material Icons';
                font-weight: normal;
                font-style: normal;
                font-size: 18px;
                line-height: 1;
                letter-spacing: normal;
                text-transform: none;
                display: inline-block;
                white-space: nowrap;
                word-wrap: normal;
                direction: ltr;
                -webkit-font-feature-settings: 'liga';
                -webkit-font-smoothing: antialiased;
            }
            
            .on-hover-tab {
                transition: all 0.3s ease;
                padding: 12px 16px;
                border-radius: 8px;
                margin: 4px 0;
                display: flex;
                align-items: center;
                gap: 12px;
            }
            
            .on-hover-tab:hover {
                background-color: rgba(0, 212, 255, 0.1);
                color: #00d4ff;
                cursor: pointer;
            }
            </style>
            """, unsafe_allow_html=True)
    except Exception as e:
        st.error(f"CSS loading error: {e}")

def render_hover_tabs_sidebar():
    """Render navigation using hover tabs component if available"""
    
    # Load CSS first
    load_css_safely()
    
    if not HOVER_TABS_AVAILABLE:
        st.sidebar.error("streamlit-on-Hover-tabs not installed properly.")
        return render_fallback_sidebar()
    
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
        
        try:
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
        except Exception as e:
            st.sidebar.error(f"Hover tabs error: {e}")
            return render_fallback_sidebar()
        
        # Add some info at the bottom
        st.markdown("---")
        st.markdown("**Kaspa Analytics**")
        st.markdown("Select a page from above to navigate")
    
    return selected_tab

def render_fallback_sidebar():
    """Fallback sidebar if hover tabs not available"""
    with st.sidebar:
        st.markdown("### 🔍 Navigation")
        st.markdown("---")
        
        # Simple selectbox as fallback
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
        
        selected = st.selectbox("Select Page:", pages, index=0)
        
        st.markdown("---")
        st.markdown("**Kaspa Analytics**")
        st.markdown("Fallback navigation")
        
        return selected

def render_simple_page_header(title, subtitle=None):
    """Simple page header without breadcrumbs"""
    
    subtitle_html = f'<p style="color: #94a3b8; font-size: 16px; margin: 8px 0 0 0;">{subtitle}</p>' if subtitle else ""
    
    page_header_html = f'<div style="padding: 0 0 32px 0;"><h1 style="color: #f1f5f9; font-size: 36px; font-weight: 800; margin: 0;">{title}</h1>{subtitle_html}</div>'
    
    st.markdown(page_header_html, unsafe_allow_html=True)

def render_basic_css():
    """Basic CSS for the application"""
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
        
        /* Basic hover effects */
        .hover-element {
            transition: all 0.3s ease !important;
        }
        
        .hover-element:hover {
            transform: translateY(-2px) !important;
        }
    </style>
    """, unsafe_allow_html=True)

# Keep your existing functions from the original file
def render_custom_css_with_sidebar():
    """Your existing CSS function"""
    # Keep all your existing CSS here
    pass

def render_clean_header(user_name=None, user_role=None, show_auth=True):
    """Your existing header function"""
    # Keep your existing header code here
    pass

def render_beautiful_sidebar(current_page="Price"):
    """Your existing sidebar function"""
    # Keep your existing sidebar code here
    pass
