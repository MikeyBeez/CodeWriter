import streamlit as st
from pathlib import Path

def render(config):
    st.title("🏠 Welcome to Code Writer")
    st.write(f"👋 Hello, {config.get('username', 'User')}!")
    
    st.write("Code Writer is an AI-assisted project initialization and management tool.")
    
    st.subheader("🚀 Quick Start")
    st.write("1. Use the sidebar to create or select a project")
    st.write("2. Navigate to 'Project Prompt' to describe your project and generate a plan")
    st.write("3. Generate code based on the project plan")
    st.write("4. View and edit your project files in the 'Project Files' section")
    
    st.subheader("📊 Project Statistics")
    if 'code_directory' in config:
        code_dir = config['code_directory']
        try:
            projects = [d for d in Path(code_dir).iterdir() if d.is_dir()]
            st.write(f"Total Projects: {len(projects)}")
        except FileNotFoundError:
            st.error(f"The configured code directory does not exist: {code_dir}")
        except PermissionError:
            st.error(f"Permission denied when trying to access the code directory: {code_dir}")
        
        if 'current_project' in st.session_state:
            st.write(f"Current Project: {st.session_state.current_project}")
    else:
        st.write("Please set up your code directory in the Settings.")

    st.subheader("🛠️ Need Help?")
    st.write("Check out the different sections in the sidebar navigation to get started with your project!")
