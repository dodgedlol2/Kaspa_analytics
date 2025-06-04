import streamlit as st
import sys
import os

# Add the components directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'components'))

from shared_components import render_hover_tabs_sidebar

st.set_page_config(
    page_title="Kaspa Network Analytics",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Simple test
st.title("🔍 Kaspa Network Analytics")
st.write("Testing the hover tabs navigation...")

# Use the hover tabs sidebar
selected_page = render_hover_tabs_sidebar()

# Show what was selected
st.write(f"**Selected page:** {selected_page}")

# Simple routing
if selected_page and selected_page != "Home":
    st.info(f"You selected: {selected_page}")
    st.write("Navigation is working! ✅")
else:
    st.write("Welcome to the home page!")
    st.write("Try clicking on different tabs in the sidebar.")
