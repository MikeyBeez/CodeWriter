import streamlit as st
from pathlib import Path
import importlib
import time
import os
from config import load_config, save_config
from components.sidebar import render_sidebar
from utils.setup_wizard import show_setup_wizard

def save_all_state():
    # Save any necessary state here
    save_config(config)
    # Add any other state saving operations

def goodbye_screen():
    st.empty()  # Clear the screen
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.title("Goodbye!")
        st.write("Thank you for using Code Writer. Have a great day!")
        st.write("Exiting in 3 seconds...")
        time.sleep(3)

# Set page config for consistent styling
st.set_page_config(
    page_title="Code Writer",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for text wrapping
st.markdown("""
<style>
.stText, .stMarkdown {
    text-align: justify;
    word-wrap: break-word;
}
.wrapped-text {
    white-space: normal !important;
    overflow-wrap: break-word !important;
    word-wrap: break-word !important;
}
</style>
""", unsafe_allow_html=True)

# Load configuration
config = load_config()

# Show setup wizard if not configured
if not config.get('is_configured', False):
    config = show_setup_wizard()
    save_config(config)  # Save config after setup wizard

# Initialize session state for last project and exit flag
if 'last_project' not in st.session_state:
    st.session_state.last_project = config.get('last_project', '')
if 'exit_program' not in st.session_state:
    st.session_state.exit_program = False

# Check if we should exit the program
if st.session_state.exit_program:
    goodbye_screen()
    os._exit(0)  # Force exit the program

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
    for name in ["home", "project_prompt", "project_execution", "view_step", "project_files", "settings"]:
        st.write(f"- {name}")

# Save last project to config
if 'current_project' in st.session_state and st.session_state.current_project != config.get('last_project', ''):
    config['last_project'] = st.session_state.current_project
    save_config(config)

# Quit button
#if st.sidebar.button("Quit Program"):
#    save_all_state()
 #   st.session_state.exit_program = True
  #  st.experimental_rerun()

# Display configuration for debugging
st.sidebar.write("Current Configuration:")
st.sidebar.json(config)

# Display current project and working directory for debugging
if 'current_project' in st.session_state:
    st.sidebar.write(f"Current Project: {st.session_state.current_project}")
    if 'current_project_path' in st.session_state:
        st.sidebar.write(f"Project Path: {st.session_state.current_project_path}")
