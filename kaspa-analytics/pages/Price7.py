import streamlit as st
from components.shared_components import (
    render_page_config,
    render_custom_css_with_sidebar,
    render_clean_header,
    render_sidebar_navigation,
    render_simple_page_header
)

# MUST be first Streamlit command
render_page_config(page_title="Analytics - Kaspa Analytics Pro")

# Apply custom CSS with sidebar support
render_custom_css_with_sidebar()

# Render clean header (no navigation in header)
render_clean_header(
    user_name=None,  # Try "John Doe" to test user menu
    show_auth=True
)

# Render sidebar navigation
render_sidebar_navigation(current_page="Analytics")

# Render simple page header
render_simple_page_header(
    title="Price Analysis",
    subtitle="Advanced cryptocurrency market analysis and predictions"
)

# Main content
st.write("## 🚀 Header + Sidebar Working!")

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

# Test the layout with some charts
st.write("### Sample Chart Area")

# Create a simple chart
import plotly.graph_objects as go
import numpy as np

# Sample data
x = np.linspace(0, 10, 100)
y = np.sin(x) + np.random.normal(0, 0.1, 100)

fig = go.Figure(data=go.Scatter(x=x, y=y, mode='lines', name='Sample Data'))
fig.update_layout(
    title="Sample Price Chart",
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    font=dict(color='#e2e8f0'),
    height=400
)

st.plotly_chart(fig, use_container_width=True)

st.write("---")

st.write("### Layout Test Results:")
st.success("✅ Clean header with branding and auth")
st.success("✅ Sidebar navigation with icons") 
st.success("✅ Proper content spacing")
st.success("✅ Responsive design")

# Instructions
with st.expander("🔧 Customization Instructions"):
    st.write("""
    **To use this layout in your pages:**
    
    1. **Copy the functions** from the improved shared_components.py
    2. **Replace your page header calls** with:
    ```python
    render_page_config()
    render_custom_css_with_sidebar()
    render_clean_header()
    render_sidebar_navigation(current_page="YourPage")
    render_simple_page_header("Your Title", "Your subtitle")
    ```
    
    3. **Customize navigation** by editing the nav_items in render_sidebar_navigation()
    4. **Add user authentication** by passing user_name to render_clean_header()
    
    **Benefits:**
    - Clean, professional header
    - Left sidebar navigation 
    - Better use of screen space
    - Mobile responsive
    - Easy to maintain
    """)

st.write("### Next Steps:")
st.info("""
1. 🎯 **Update your existing pages** to use this new layout
2. 🔗 **Add page routing** to make navigation functional  
3. 👤 **Implement user authentication** system
4. 📱 **Test on mobile devices**
5. 🎨 **Customize colors and branding** as needed
""")
