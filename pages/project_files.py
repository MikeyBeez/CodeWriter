import streamlit as st
from pathlib import Path

def render(config):
    st.title("Project Files")

    if 'current_project' not in st.session_state or 'current_project_path' not in st.session_state:
        st.error("Please select a project from the sidebar first.")
        return

    project_path = Path(st.session_state.current_project_path)
    st.write(f"Current Project: {st.session_state.current_project}")
    st.write(f"Project Path: {project_path}")

    # Get all files in the project directory
    files = list(project_path.rglob("*"))
    files = [f for f in files if f.is_file()]

    # Create a selectbox to choose a file
    selected_file = st.selectbox("Select a file to view/edit:", [f.relative_to(project_path) for f in files])

    if selected_file:
        file_path = project_path / selected_file
        with open(file_path, "r") as f:
            content = f.read()

        # Display file content in a text area
        new_content = st.text_area(f"Editing: {selected_file}", value=content, height=400)

        # Save changes if the content has been modified
        if st.button("Save Changes") and new_content != content:
            with open(file_path, "w") as f:
                f.write(new_content)
            st.success(f"Changes saved to {selected_file}")

    # Option to create a new file
    new_file_name = st.text_input("Create a new file (enter file name):")
    if st.button("Create File") and new_file_name:
        new_file_path = project_path / new_file_name
        if not new_file_path.exists():
            with open(new_file_path, "w") as f:
                f.write("")
            st.success(f"Created new file: {new_file_name}")
            st.experimental_rerun()
        else:
            st.error(f"File {new_file_name} already exists.")
