import streamlit as st
from components.shared_components import (
    render_page_config,
    render_custom_css,
    render_professional_header,
    render_page_header
)

# MUST be first Streamlit command
render_page_config(page_title="Header Test")

# Apply custom CSS
render_custom_css()

# Render professional header
render_professional_header(
    current_page="Analytics",
    user_name=None,  # Try changing to "John Doe" to test user menu
    show_auth=True
)

# Render page header
render_page_header(
    title="Header Test Page",
    subtitle="Testing the professional header component",
    show_breadcrumb=True,
    breadcrumb_items=["Home", "Test", "Header Test"]
)

# Test content
st.write("# Header Test")
st.write("If you can see this content and the header above, it's working!")

# Test some metrics
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Test Metric 1", "123.45", "2.3%")

with col2:
    st.metric("Test Metric 2", "67.89", "-1.2%")

with col3:
    st.metric("Test Metric 3", "98.76", "0.5%")

st.write("---")
st.write("**Instructions:**")
st.write("1. Check if the header appears at the top")
st.write("2. Check if the header has the KaspaMetrics logo")
st.write("3. Check if navigation buttons are visible")
st.write("4. Check if Login/Get Started buttons appear")
st.write("5. Try scrolling - header should stay fixed at top")
