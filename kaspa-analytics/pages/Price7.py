import streamlit as st
from components.shared_components import (
    render_page_config,
    render_custom_css_with_sidebar,
    render_clean_header,
    render_beautiful_sidebar,  # Updated function name
    render_simple_page_header
)

# MUST be first Streamlit command
render_page_config(page_title="Analytics - Kaspa Analytics Pro")

# Apply custom CSS with beautiful sidebar support
render_custom_css_with_sidebar()

# Render clean header
render_clean_header(
    user_name=None,  # Try "John Doe" to test user menu
    show_auth=True
)

# Render beautiful dropdown sidebar (this replaces the old navigation)
render_beautiful_sidebar(current_page="Price")  # Change this to test different active states

# Render simple page header
render_simple_page_header(
    title="Price Analysis",
    subtitle="Advanced cryptocurrency market analysis and predictions"
)

# Main content
st.write("## 🚀 Beautiful Dropdown Sidebar!")

# Create some content to test the layout
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        label="Current Price",
        value="$0.08734",
        delta="2.4%",
        delta_color="normal"
    )

with col2:
    st.metric(
        label="24h Volume", 
        value="$45.2M",
        delta="-5.1%",
        delta_color="inverse"
    )

with col3:
    st.metric(
        label="Market Cap",
        value="$2.1B",
        delta="1.8%",
        delta_color="normal"
    )

st.write("---")

# Test different sidebar states
st.write("### 🎯 Sidebar Features:")
st.success("✅ **Dropdown Navigation** - Click 'Market Metrics' to expand")
st.success("✅ **Glow Effects** - Hover over navigation items")
st.success("✅ **Live Stats** - Real-time data with pulsing indicator")
st.success("✅ **Smooth Animations** - Beautiful transitions")
st.success("✅ **Active States** - Current page highlighting")

# Test the layout with some charts
st.write("### Sample Chart Area")

import plotly.graph_objects as go
import numpy as np

# Sample data
x = np.linspace(0, 10, 100)
y = np.sin(x) + np.random.normal(0, 0.1, 100)

fig = go.Figure(data=go.Scatter(x=x, y=y, mode='lines', name='Sample Data', line=dict(color='#00d4ff', width=3)))
fig.update_layout(
    title="Sample Price Chart",
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    font=dict(color='#e2e8f0'),
    height=400
)

st.plotly_chart(fig, use_container_width=True)

st.write("---")

# Instructions for testing different pages
st.write("### 🔧 Testing Different Active States:")

test_pages = ["Price", "MarketCap", "Volume", "Hashrate", "Difficulty", "Transactions"]

st.write("**Change the `current_page` parameter to test different active states:**")

for page in test_pages:
    st.code(f'render_beautiful_sidebar(current_page="{page}")')

with st.expander("📋 Navigation Structure"):
    st.write("""
    **Market Metrics:**
    - Price Analysis (current)
    - Market Cap
    - Trading Volume  
    - Supply Metrics
    
    **Mining:**
    - Hashrate
    - Difficulty
    - Mining Revenue
    
    **Network:**
    - Transactions
    - Addresses
    - Blocks
    
    **Features:**
    - ✨ Smooth dropdown animations
    - 🎯 Hover glow effects
    - 📊 Live stats with pulsing indicator
    - 🎨 Beautiful glassmorphism design
    - 📱 Mobile responsive
    """)

st.write("### Next Steps:")
st.info("""
1. 🎯 **Test the dropdowns** - Click on 'Market Metrics' and 'Mining' 
2. 🖱️ **Hover effects** - Move mouse over navigation items
3. 📊 **Live stats** - Check the pulsing indicator
4. 🔄 **Change active page** - Modify `current_page` parameter
5. 🎨 **Customize** - Add more sections or modify styling
""")
