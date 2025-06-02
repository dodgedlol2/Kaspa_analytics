# Add this to your shared_components.py file

def render_custom_css_with_sidebar_fix():
    """
    Enhanced CSS that ensures header stays above sidebar
    """
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
        @import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css');
        
        /* ========== SIDEBAR Z-INDEX FIXES ========== */
        
        /* Streamlit sidebar has z-index of 999999, so we need to go higher */
        .professional-header {
            background: rgba(15, 20, 25, 0.98) !important;
            backdrop-filter: blur(25px) !important;
            border-bottom: 1px solid rgba(0, 212, 255, 0.2) !important;
            padding: 16px 40px !important;
            position: fixed !important;  /* Changed from sticky to fixed */
            top: 0 !important;
            left: 0 !important;
            right: 0 !important;
            width: 100% !important;
            z-index: 9999999 !important;  /* Higher than sidebar's 999999 */
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4) !important;
            margin: 0 !important;
        }
        
        /* Ensure header content is also high z-index */
        .header-content {
            position: relative !important;
            z-index: 9999999 !important;
            display: flex !important;
            align-items: center !important;
            justify-content: space-between !important;
            max-width: 1400px !important;
            margin: 0 auto !important;
        }
        
        /* Push main content down to account for fixed header */
        .main .block-container {
            padding-top: 90px !important;  /* Adjust based on your header height */
            padding-left: 0 !important;
            padding-right: 0 !important;
            max-width: 100% !important;
        }
        
        /* Sidebar adjustments */
        .css-1d391kg {  /* Streamlit sidebar */
            z-index: 999998 !important;  /* Lower than header */
            margin-top: 80px !important;  /* Push sidebar below header */
        }
        
        .css-1dp5vir {  /* Another sidebar selector */
            z-index: 999998 !important;
            margin-top: 80px !important;
        }
        
        /* Sidebar content */
        .css-17eq0hr {
            margin-top: 20px !important;
        }
        
        /* Alternative: Hide sidebar completely if you don't need it */
        /* 
        section[data-testid="stSidebar"] {
            display: none !important;
        }
        */
        
        /* ========== ORIGINAL STYLES ========== */
        
        html, body, .stApp {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            background: linear-gradient(135deg, #0a0e1a 0%, #1a1f2e 50%, #0f1419 100%);
            color: #e2e8f0;
            overflow-x: hidden;
        }
        
        .stApp {
            background-attachment: fixed;
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
        
        /* Brand section styles */
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
        
        /* Responsive design */
        @media (max-width: 768px) {
            .professional-header {
                padding: 12px 20px !important;
            }
            
            .header-content {
                flex-direction: column !important;
                gap: 15px !important;
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
            
            .main .block-container {
                padding-top: 140px !important;  /* More space on mobile */
            }
        }
        
        /* Hide Streamlit default elements */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        .stDeployButton {display: none;}
        
        /* Additional sidebar fixes for different Streamlit versions */
        .css-1d391kg, .css-1dp5vir, .css-17eq0hr, .css-1v3fvcr {
            z-index: 999998 !important;
        }
        
        /* If sidebar is collapsed, adjust accordingly */
        .css-1rs6os.edgvbvh3 {
            z-index: 999998 !important;
        }
        
    </style>
    """, unsafe_allow_html=True)

# Alternative approach: Completely hide sidebar if not needed
def render_custom_css_no_sidebar():
    """
    CSS that completely hides the sidebar for a cleaner look
    """
    st.markdown("""
    <style>
        /* Hide sidebar completely */
        section[data-testid="stSidebar"] {
            display: none !important;
        }
        
        .css-1d391kg {
            display: none !important;
        }
        
        /* Adjust main content to use full width */
        .main .block-container {
            padding-left: 0 !important;
            max-width: 100% !important;
            padding-top: 90px !important;
        }
        
        /* Your existing header styles here... */
        .professional-header {
            background: rgba(15, 20, 25, 0.98) !important;
            backdrop-filter: blur(25px) !important;
            border-bottom: 1px solid rgba(0, 212, 255, 0.2) !important;
            padding: 16px 40px !important;
            position: fixed !important;
            top: 0 !important;
            left: 0 !important;
            right: 0 !important;
            width: 100% !important;
            z-index: 9999999 !important;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4) !important;
        }
        
        /* Rest of your existing styles... */
        
    </style>
    """, unsafe_allow_html=True)

# Option 3: Smart sidebar handling
def render_header_with_sidebar_detection():
    """
    Detect if sidebar is being used and adjust header accordingly
    """
    # Check if any sidebar elements exist
    sidebar_check = """
    <script>
        function adjustHeaderForSidebar() {
            const sidebar = document.querySelector('section[data-testid="stSidebar"]');
            const header = document.querySelector('.professional-header');
            
            if (sidebar && header) {
                const sidebarWidth = sidebar.offsetWidth;
                if (sidebarWidth > 0) {
                    // Sidebar is open, adjust header
                    header.style.marginLeft = sidebarWidth + 'px';
                    header.style.width = `calc(100% - ${sidebarWidth}px)`;
                } else {
                    // Sidebar is closed, full width header
                    header.style.marginLeft = '0px';
                    header.style.width = '100%';
                }
            }
        }
        
        // Run on load and when sidebar changes
        window.addEventListener('load', adjustHeaderForSidebar);
        setTimeout(adjustHeaderForSidebar, 100);
        setTimeout(adjustHeaderForSidebar, 500);
    </script>
    """
    
    st.components.v1.html(sidebar_check, height=0)
