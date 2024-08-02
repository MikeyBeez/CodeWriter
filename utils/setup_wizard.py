import streamlit as st
from pathlib import Path
from config import save_config, load_config
import os

def get_directory_contents(path):
    contents = [('..', path.parent)] if path != path.root else []
    contents.extend((item.name, item) for item in path.iterdir() if item.is_dir())
    return contents

def show_setup_wizard():
    st.title("🧙‍♂️ Setup Wizard")
    
    # Load existing config
    config = load_config()
    
    config['username'] = st.text_input("👤 Your Name", value=config.get('username', ''))
    
    st.write("📂 Code Directory")
    
    # Initialize session state for current directory
    if 'current_dir' not in st.session_state:
        st.session_state.current_dir = Path(config.get('code_directory', Path.home()))
    
    # Manual path entry
    manual_path = st.text_input("Enter path manually", str(st.session_state.current_dir))
    if Path(manual_path).is_dir():
        st.session_state.current_dir = Path(manual_path)
    
    # Directory browser
    st.write("Or use the directory browser:")
    contents = get_directory_contents(st.session_state.current_dir)
    selected = st.selectbox("Select directory", options=[name for name, _ in contents], format_func=lambda x: f"📁 {x}")
    selected_path = dict(contents)[selected]
    
    if st.button("Open"):
        if selected_path.is_dir():
            st.session_state.current_dir = selected_path
            st.experimental_rerun()
    
    # Set as code directory button
    if st.button("Set as Code Directory"):
        config['code_directory'] = str(st.session_state.current_dir)
        st.success(f"Code directory set to: {st.session_state.current_dir}")
    
    # Display current path
    st.write(f"Current path: {st.session_state.current_dir}")
    
    # Save configuration
    if st.button("Save Configuration"):
        if 'code_directory' in config:
            config['is_configured'] = True
            save_config(config)
            st.success("Configuration saved successfully!")
            st.experimental_rerun()
        else:
            st.error("Please set a valid code directory before saving.")

    # Display current working directory for reference
    st.write(f"Current working directory: {os.getcwd()}")

    # Debug information
    st.write("Debug Info:")
    st.json(config)

    return config
