import streamlit as st
from pathlib import Path
import importlib
from config import load_config, save_config
from components.sidebar import render_sidebar
from utils.setup_wizard import show_setup_wizard

# Set page config for consistent styling
st.set_page_config(
    page_title="Code Writer",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Load configuration
config = load_config()

# Show setup wizard if not configured
if not config.get('is_configured', False):
    config = show_setup_wizard()
    save_config(config)  # Save config after setup wizard

# Sidebar
render_sidebar(config)

# Main content area
if 'page' not in st.session_state:
    st.session_state.page = 'Home'

# Dynamically import and render the selected page
try:
    # Convert page name to lowercase and replace spaces with underscores
    page_module_name = st.session_state.page.lower().replace(' ', '_')
    page_module = importlib.import_module(f"pages.{page_module_name}")
    page_module.render(config)
except ImportError as e:
    st.error(f"Page {st.session_state.page} not found. Error: {str(e)}")
    st.write("Available pages:")
    for name in ["home", "project_prompt", "project_files", "project_details", "settings"]:
        st.write(f"- {name}")

# Display configuration for debugging
st.sidebar.write("Current Configuration:")
st.sidebar.json(config)

# Display current project and working directory for debugging
if 'current_project' in st.session_state:
    st.sidebar.write(f"Current Project: {st.session_state.current_project}")
    if 'current_project_path' in st.session_state:
        st.sidebar.write(f"Project Path: {st.session_state.current_project_path}")
