import streamlit as st

def render(config):
    st.title("🏠 Welcome to Code Writer")
    st.write(f"👋 Hello, {config.get('username', 'User')}!")
    st.write(f"📂 Your code directory is set to: {config.get('code_directory', 'Not set')}")
    
    st.subheader("🚀 Quick Start")
    st.write("1. Use the sidebar to create or select a project")
    st.write("2. Navigate to different sections using the sidebar")
    st.write("3. Generate code, edit your project plan, and more!")
    
    st.subheader("📊 Project Statistics")
    # Add project statistics here (e.g., number of projects, files, etc.)
