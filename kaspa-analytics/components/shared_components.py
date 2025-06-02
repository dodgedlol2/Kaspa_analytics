import streamlit as st

def render_aggressive_header_fix():
    """
    Ultra-aggressive CSS to force header above everything
    """
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
        @import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css');
        
        /* NUCLEAR OPTION - Override everything */
        * {
            box-sizing: border-box;
        }
        
        /* Force header to be absolutely positioned above everything */
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
            margin: 0 !important;
            display: flex !important;
            align-items: center !important;
            justify-content: space-between !important;
        }
        
        /* Override ALL Streamlit sidebar z-indexes */
        .css-1d391kg,
        .css-1dp5vir,
        .css-17eq0hr,
        .css-1v3fvcr,
        .css-12w0qpk,
        .css-163ttbj,
        .css-1rs6os,
        .css-1lcbmhc,
        .css-1y4p8pa,
        section[data-testid="stSidebar"],
        .stSidebar,
        div[data-testid="stSidebar"] {
            z-index: 999998 !important;
            margin-top: 80px !important;
        }
        
        /* Force main content below header */
        .main,
        .main .block-container,
        .css-k1vhr4,
        .css-18e3th9,
        .css-1d391kg,
        div[data-testid="stAppViewContainer"] {
            padding-top: 100px !important;
            margin-top: 0 !important;
        }
        
        /* Base app styles */
        html, body, .stApp {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
            background: linear-gradient(135deg, #0a0e1a 0%, #1a1f2e 50%, #0f1419 100%) !important;
            color: #e2e8f0 !important;
            overflow-x: hidden !important;
            margin: 0 !important;
            padding: 0 !important;
        }
        
        .stApp {
            background-attachment: fixed !important;
        }
        
        /* Header content styling */
        .header-content {
            display: flex !important;
            align-items: center !important;
            justify-content: space-between !important;
            width: 100% !important;
            max-width: 1400px !important;
            margin: 0 auto !important;
            position: relative !important;
            z-index: 999999999 !important;
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
            text-shadow: 0 0 30px rgba(0, 212, 255, 0.3) !important;
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
            text-decoration: none !important;
            font-size: 13px !important;
            font-weight: 600 !important;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
            backdrop-filter: blur(10px) !important;
            display: flex !important;
            align-items: center !important;
            gap: 8px !important;
            cursor: pointer !important;
        }
        
        .nav-button:hover {
            background: rgba(0, 212, 255, 0.1) !important;
            border-color: rgba(0, 212, 255, 0.4) !important;
            color: #00d4ff !important;
            transform: translateY(-1px) !important;
            box-shadow: 0 4px 15px rgba(0, 212, 255, 0.2) !important;
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
            transition: all 0.3s ease !important;
            cursor: pointer !important;
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
            transition: all 0.3s ease !important;
            cursor: pointer !important;
            box-shadow: 0 4px 15px rgba(0, 212, 255, 0.3) !important;
        }
        
        .signup-button:hover {
            transform: translateY(-1px) !important;
            box-shadow: 0 6px 20px rgba(0, 212, 255, 0.4) !important;
        }
        
        /* Hide Streamlit elements */
        #MainMenu {visibility: hidden !important;}
        footer {visibility: hidden !important;}
        header {visibility: hidden !important;}
        .stDeployButton {display: none !important;}
        
        /* Override any remaining z-index issues */
        div[role="dialog"],
        .css-1cpxqw2,
        .css-1y4p8pa {
            z-index: 999997 !important;
        }
        
        /* Mobile responsive */
        @media (max-width: 768px) {
            .professional-header {
                height: 120px !important;
                padding: 12px 20px !important;
            }
            
            .header-content {
                flex-direction: column !important;
                gap: 15px !important;
            }
            
            .main .block-container {
                padding-top: 140px !important;
            }
        }
        
    </style>
    """, unsafe_allow_html=True)

def render_debug_header():
    """
    Simple header with debug info to test z-index
    """
    debug_html = """
    <div class="professional-header" style="background: red !important; z-index: 999999999 !important;">
        <div class="header-content">
            <div class="brand-section">
                <div class="logo-container">
                    <div class="logo">
                        <i class="fas fa-gem"></i>
                    </div>
                    <div class="brand-text">
                        <h1>DEBUG HEADER - Should be on top!</h1>
                        <div class="brand-subtitle">Z-Index Test</div>
                    </div>
                </div>
            </div>
            
            <div class="nav-section">
                <div class="nav-button active">
                    <i class="fas fa-bug"></i>
                    <span>DEBUG MODE</span>
                </div>
            </div>
            
            <div class="auth-section">
                <button class="login-button">Test</button>
            </div>
        </div>
    </div>
    """
    
    st.markdown(debug_html, unsafe_allow_html=True)

def render_javascript_fix():
    """
    JavaScript solution to force header on top after page loads
    """
    js_code = """
    <script>
        function forceHeaderOnTop() {
            // Find the header
            const header = document.querySelector('.professional-header');
            
            // Find all sidebar elements
            const sidebarElements = document.querySelectorAll(`
                .css-1d391kg,
                .css-1dp5vir,
                .css-17eq0hr,
                .css-1v3fvcr,
                section[data-testid="stSidebar"],
                .stSidebar,
                div[data-testid="stSidebar"]
            `);
            
            if (header) {
                // Force header styles
                header.style.position = 'fixed';
                header.style.top = '0';
                header.style.left = '0';
                header.style.right = '0';
                header.style.width = '100vw';
                header.style.zIndex = '999999999';
                header.style.background = 'rgba(15, 20, 25, 0.98)';
                header.style.backdropFilter = 'blur(25px)';
                
                console.log('Header forced to top with z-index:', header.style.zIndex);
            }
            
            // Lower sidebar z-index
            sidebarElements.forEach((element, index) => {
                if (element) {
                    element.style.zIndex = '999998';
                    element.style.marginTop = '80px';
                    console.log(`Sidebar element ${index} z-index lowered`);
                }
            });
            
            // Push main content down
            const mainContent = document.querySelector('.main .block-container');
            if (mainContent) {
                mainContent.style.paddingTop = '100px';
                console.log('Main content pushed down');
            }
        }
        
        // Run immediately and on various events
        document.addEventListener('DOMContentLoaded', forceHeaderOnTop);
        window.addEventListener('load', forceHeaderOnTop);
        
        // Keep trying for a few seconds in case Streamlit is still loading
        setTimeout(forceHeaderOnTop, 100);
        setTimeout(forceHeaderOnTop, 500);
        setTimeout(forceHeaderOnTop, 1000);
        setTimeout(forceHeaderOnTop, 2000);
        
        // Watch for sidebar changes
        const observer = new MutationObserver(forceHeaderOnTop);
        observer.observe(document.body, { childList: true, subtree: true });
    </script>
    """
    
    st.components.v1.html(js_code, height=0)
