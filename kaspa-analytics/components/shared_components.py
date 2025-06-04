def render_custom_css_with_sidebar():
    """Enhanced CSS with working auto-collapsing sidebar functionality using JavaScript"""
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
            background: linear-gradient(135deg, #0a0e1a 0%, #1a1f2e 50%, #0f1419 100%) !important;
            backdrop-filter: blur(25px) !important;
            border-bottom: 1px solid rgba(100, 116, 139, 0.2) !important;
            padding: 0 60px !important;
            z-index: 999999999 !important;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4) !important;
            display: flex !important;
            align-items: center !important;
            justify-content: space-between !important;
        }
        
        .header-content {
            display: flex !important;
            align-items: center !important;
            justify-content: space-between !important;
            width: 100% !important;
            max-width: none !important;
        }
        
        .brand-section {
            display: flex !important;
            align-items: center !important;
            gap: 15px !important;
            flex: 0 0 auto !important;
        }
        
        .logo {
            width: 45px !important;
            height: 45px !important;
            background: linear-gradient(135deg, #00d4ff 0%, #0099cc 50%, #006699 100%) !important;
            border-radius: 12px !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
            font-size: 24px !important;
            color: white !important;
            font-weight: 800 !important;
            box-shadow: 0 4px 15px rgba(0, 212, 255, 0.3) !important;
            position: relative !important;
            overflow: hidden !important;
        }
        
        .logo::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: radial-gradient(circle at 30% 30%, rgba(255, 255, 255, 0.2) 0%, transparent 60%);
            border-radius: 12px;
            pointer-events: none;
        }
        
        .brand-text {
            display: flex !important;
            flex-direction: column !important;
        }
        
        .brand-text h1 {
            font-size: 26px !important;
            font-weight: 800 !important;
            background: linear-gradient(135deg, #00d4ff 0%, #94a3b8 50%, #e2e8f0 100%) !important;
            -webkit-background-clip: text !important;
            -webkit-text-fill-color: transparent !important;
            margin: 0 !important;
            line-height: 1.1 !important;
            text-shadow: 0 0 20px rgba(0, 212, 255, 0.1) !important;
        }
        
        .auth-section {
            display: flex !important;
            align-items: center !important;
            gap: 12px !important;
            flex: 0 0 auto !important;
            margin-left: auto !important;
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
            background: rgba(0, 212, 255, 0.05) !important;
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
            background: linear-gradient(135deg, #00d4ff 0%, #00aadd 100%) !important;
        }
        
        /* AUTO-COLLAPSING SIDEBAR - Base styles */
        section[data-testid="stSidebar"] {
            background: linear-gradient(135deg, #0a0e1a 0%, #1a1f2e 50%, #0f1419 100%) !important;
            border-right: 1px solid rgba(100, 116, 139, 0.2) !important;
            margin-top: 80px !important;
            backdrop-filter: blur(25px) !important;
            box-shadow: 8px 0 32px rgba(0, 0, 0, 0.4) !important;
            position: relative !important;
            transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
            overflow: hidden !important;
        }
        
        /* Collapsed state - set by JavaScript */
        section[data-testid="stSidebar"].collapsed {
            width: 60px !important;
            min-width: 60px !important;
        }
        
        /* Expanded state - set by JavaScript */
        section[data-testid="stSidebar"].expanded {
            width: 280px !important;
            min-width: 280px !important;
        }
        
        /* Sidebar content container */
        section[data-testid="stSidebar"] > div {
            background: transparent !important;
            padding: 16px 12px !important;
            position: relative !important;
            z-index: 2 !important;
            transition: opacity 0.3s ease !important;
        }
        
        /* Content hidden when collapsed */
        section[data-testid="stSidebar"].collapsed > div {
            opacity: 0 !important;
            pointer-events: none !important;
        }
        
        /* Content visible when expanded */
        section[data-testid="stSidebar"].expanded > div {
            opacity: 1 !important;
            pointer-events: auto !important;
        }
        
        /* Collapse indicator overlay */
        .sidebar-collapse-indicator {
            position: absolute !important;
            top: 20px !important;
            left: 50% !important;
            transform: translateX(-50%) !important;
            font-size: 18px !important;
            line-height: 50px !important;
            z-index: 4 !important;
            opacity: 1 !important;
            transition: opacity 0.3s ease !important;
            text-align: center !important;
            pointer-events: none !important;
            white-space: pre !important;
        }
        
        /* Hide indicator when expanded */
        section[data-testid="stSidebar"].expanded .sidebar-collapse-indicator {
            opacity: 0 !important;
        }
        
        /* Hide Streamlit's default elements */
        nav[data-testid="stSidebarNav"] {
            display: none !important;
        }
        
        section[data-testid="stSidebar"] .stRadio {
            display: none !important;
        }
        
        button[data-testid="collapsedControl"] {
            display: none !important;
        }
        
        /* Navigation styles */
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
            gap: 8px !important;
            white-space: nowrap !important;
        }
        
        .head-metric:hover {
            color: #cbd5e1 !important;
        }
        
        .head-metric:first-child {
            margin-top: 8px !important;
        }
        
        .head-metric i {
            color: #94a3b8 !important;
            font-size: 12px !important;
            width: 16px !important;
            text-align: center !important;
            transition: color 0.2s ease !important;
            flex-shrink: 0 !important;
        }
        
        .head-metric:hover i {
            color: #cbd5e1 !important;
        }
        
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
            gap: 8px !important;
            white-space: nowrap !important;
        }
        
        .sub-metric:hover {
            color: #94a3b8 !important;
        }
        
        .sub-metric.active {
            color: #00d4ff !important;
        }
        
        .sub-metric i {
            color: #64748b !important;
            font-size: 12px !important;
            width: 16px !important;
            text-align: center !important;
            transition: color 0.2s ease !important;
            flex-shrink: 0 !important;
        }
        
        .sub-metric:hover i {
            color: #94a3b8 !important;
        }
        
        .sub-metric.active i {
            color: #00d4ff !important;
        }
        
        /* Main content adjustments */
        .main .block-container {
            padding-top: 100px !important;
            padding-left: 80px !important;
            padding-right: 20px !important;
            max-width: 100% !important;
            transition: padding-left 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
        }
        
        /* Adjusted main content when sidebar expanded */
        .main-content-expanded {
            padding-left: 300px !important;
        }
        
        /* Rest of your existing styles */
        .header-section {
            padding: 15px 40px 15px 40px;
            background: transparent;
            display: flex;
            align-items: center;
            justify-content: space-between;
            flex-wrap: wrap;
            gap: 15px;
            margin-bottom: 20px;
        }
        
        .title-container {
            flex: 0 0 auto;
        }
        
        .main-title {
            font-size: 16px;
            font-weight: 700;
            color: #ffffff;
            margin: 0;
            letter-spacing: 0.5px;
            text-align: left;
            text-shadow: 0 0 8px rgba(255, 255, 255, 0.3);
            position: relative;
            white-space: nowrap;
            line-height: 1.2;
        }
        
        .control-group {
            display: flex;
            flex-direction: column;
            gap: 3px;
            min-width: 120px;
        }
        
        .control-label {
            font-size: 11px;
            font-weight: 600;
            color: #94a3b8;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 0;
            white-space: nowrap;
            line-height: 1;
        }
        
        /* Selectbox styling */
        .stSelectbox > div > div {
            background: linear-gradient(135deg, rgba(30, 41, 59, 0.9) 0%, rgba(15, 23, 42, 0.9) 100%) !important;
            border: 2px solid rgba(100, 116, 139, 0.3) !important;
            border-radius: 12px !important;
            backdrop-filter: blur(15px) !important;
            transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
            box-shadow: 0 4px 16px rgba(0, 0, 0, 0.2) !important;
            min-height: 26px !important;
            width: 150px !important;
            max-width: 250px !important;
            min-width: 100px !important;
        }
        
        .stSelectbox > div > div:hover {
            border-color: #00d4ff !important;
            box-shadow: 0 8px 32px rgba(0, 212, 255, 0.2), 0 0 0 1px rgba(0, 212, 255, 0.3) !important;
            transform: translateY(-2px);
        }
        
        .stSelectbox > div > div > div {
            color: #f1f5f9 !important;
            font-weight: 600 !important;
            font-size: 13px !important;
            padding: 8px 16px !important;
            background: transparent !important;
        }
        
        /* Metric cards */
        .metric-card {
            background: rgba(30, 41, 59, 0.4) !important;
            backdrop-filter: blur(25px) !important;
            border: 1px solid rgba(255, 255, 255, 0.15) !important;
            border-radius: 16px !important;
            padding: 24px !important;
            position: relative !important;
            overflow: hidden !important;
            transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
            cursor: pointer !important;
            margin-bottom: 16px !important;
            width: 100% !important;
            box-sizing: border-box !important;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2) !important;
        }
        
        .metric-card:hover {
            border-color: rgba(0, 212, 255, 0.4) !important;
            box-shadow: 0 8px 32px rgba(0, 212, 255, 0.15), 0 0 0 1px rgba(0, 212, 255, 0.2) !important;
            transform: translateY(-3px) !important;
            background: rgba(30, 41, 59, 0.6) !important;
        }
        
        .metric-label {
            color: #94a3b8 !important;
            font-size: 12px !important;
            font-weight: 600 !important;
            text-transform: uppercase !important;
            letter-spacing: 1px !important;
            margin-bottom: 10px !important;
        }
        
        .metric-value {
            color: #f1f5f9 !important;
            font-size: 28px !important;
            font-weight: 800 !important;
            line-height: 1.1 !important;
            margin-bottom: 6px !important;
            text-shadow: 0 0 15px rgba(255, 255, 255, 0.1);
        }
        
        .metric-delta {
            font-size: 14px !important;
            font-weight: 700 !important;
            margin-bottom: 8px;
        }
        
        .metric-delta.positive {
            color: #00ff88 !important;
        }
        
        .metric-delta.negative {
            color: #ff4757 !important;
        }
        
        /* Hide Streamlit elements */
        #MainMenu {visibility: hidden !important;}
        footer {visibility: hidden !important;}
        header {visibility: hidden !important;}
        .stDeployButton {display: none !important;}
        
        /* Mobile responsive */
        @media (max-width: 768px) {
            section[data-testid="stSidebar"] {
                display: none !important;
            }
            
            .main .block-container {
                padding-left: 20px !important;
            }
        }
    </style>
    
    <script>
    function initAutoCollapsingSidebar() {
        const sidebar = document.querySelector('section[data-testid="stSidebar"]');
        const mainContainer = document.querySelector('.main .block-container');
        
        if (!sidebar) {
            console.log('Sidebar not found, retrying...');
            setTimeout(initAutoCollapsingSidebar, 500);
            return;
        }
        
        // Create collapse indicator
        let indicator = sidebar.querySelector('.sidebar-collapse-indicator');
        if (!indicator) {
            indicator = document.createElement('div');
            indicator.className = 'sidebar-collapse-indicator';
            indicator.innerHTML = '📊\\n📈\\n🔗';
            sidebar.appendChild(indicator);
        }
        
        // Set initial collapsed state
        sidebar.classList.add('collapsed');
        sidebar.classList.remove('expanded');
        
        // Mouse enter - expand
        sidebar.addEventListener('mouseenter', function() {
            sidebar.classList.remove('collapsed');
            sidebar.classList.add('expanded');
            if (mainContainer) {
                mainContainer.classList.add('main-content-expanded');
            }
        });
        
        // Mouse leave - collapse
        sidebar.addEventListener('mouseleave', function() {
            sidebar.classList.remove('expanded');
            sidebar.classList.add('collapsed');
            if (mainContainer) {
                mainContainer.classList.remove('main-content-expanded');
            }
        });
        
        console.log('Auto-collapsing sidebar initialized successfully!');
    }
    
    // Initialize when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initAutoCollapsingSidebar);
    } else {
        initAutoCollapsingSidebar();
    }
    
    // Also initialize after a delay to handle Streamlit's dynamic loading
    setTimeout(initAutoCollapsingSidebar, 1000);
    setTimeout(initAutoCollapsingSidebar, 2000);
    </script>
    """, unsafe_allow_html=True)
