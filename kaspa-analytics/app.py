import streamlit as st
import sys
import os

# Debug the import path
current_dir = os.path.dirname(__file__)
components_path = os.path.join(current_dir, 'components')

st.write(f"Current directory: {current_dir}")
st.write(f"Components path: {components_path}")
st.write(f"Components path exists: {os.path.exists(components_path)}")

# Add the components directory to the path
sys.path.append(components_path)

st.write(f"Python path: {sys.path}")

# Try to import
try:
    import shared_components
    st.success("✅ shared_components imported successfully")
    
    # Check what functions are available
    functions = [func for func in dir(shared_components) if not func.startswith('_')]
    st.write(f"Available functions: {functions}")
    
    # Test specific function
    if hasattr(shared_components, 'render_hover_tabs_sidebar'):
        st.success("✅ render_hover_tabs_sidebar function found")
        
        # Try to use it
        try:
            selected = shared_components.render_hover_tabs_sidebar()
            st.write(f"Function returned: {selected}")
        except Exception as e:
            st.error(f"Error calling function: {e}")
    else:
        st.error("❌ render_hover_tabs_sidebar function NOT found")
        
except Exception as e:
    st.error(f"❌ Error importing shared_components: {e}")

# Also test the hover tabs package
try:
    from st_on_hover_tabs import on_hover_tabs
    st.success("✅ st_on_hover_tabs imported successfully")
except Exception as e:
    st.error(f"❌ st_on_hover_tabs import failed: {e}")
    st.info("Make sure 'streamlit-on-Hover-tabs==0.0.2' is in your requirements.txt")
