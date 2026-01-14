import streamlit as st
from pathlib import Path

def render_sidebar(config):
    st.sidebar.title("🚀 Code Writer")

    if 'code_directory' in config:
        code_dir = Path(config['code_directory'])
        projects = [d.name for d in code_dir.iterdir() if d.is_dir()]
        
        # Select the last project if it exists
        default_index = projects.index(st.session_state.last_project) if st.session_state.last_project in projects else 0
        
        selected_project = st.sidebar.selectbox("Select Project", [""] + projects, index=default_index)
        
        if selected_project:
            st.session_state.current_project = selected_project
            project_path = code_dir / selected_project
            st.session_state.current_project_path = project_path
            st.sidebar.success(f"Selected project: {selected_project}")
        
        new_project = st.sidebar.text_input("Create New Project (Press Enter to create)")
        if new_project:
            new_project_path = code_dir / new_project
            if not new_project_path.exists():
                new_project_path.mkdir(parents=True)
                st.session_state.current_project = new_project
                st.session_state.current_project_path = new_project_path
                st.sidebar.success(f"Created project: {new_project}")
                st.experimental_rerun()
            else:
                st.sidebar.error(f"Project {new_project} already exists.")

    # Navigation
    st.sidebar.subheader("🧭 Navigation")
    pages = ["Home", "Project Prompt", "Project Execution", "Project Files", "Settings"]
    for page in pages:
        if st.sidebar.button(page, key=page):
            st.session_state.page = page

    # Quit button
    if st.sidebar.button("Quit Program"):
        st.session_state.exit_program = True
        st.experimental_rerun()

    # Display current project for debugging
    if 'current_project' in st.session_state:
        st.sidebar.write(f"Current Project: {st.session_state.current_project}")
        st.sidebar.write(f"Project Path: {st.session_state.current_project_path}")

    # Display configuration for debugging
    st.sidebar.write("Current Configuration:")
    st.sidebar.json(config)
