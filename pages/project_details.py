import streamlit as st
from pathlib import Path
import json

def load_project_details(project_path):
    details_file = project_path / "project_details.json"
    if details_file.exists():
        with open(details_file, "r") as f:
            return json.load(f)
    return {
        "name": "",
        "description": "",
        "version": "0.1.0",
        "author": "",
        "dependencies": []
    }

def save_project_details(project_path, details):
    details_file = project_path / "project_details.json"
    with open(details_file, "w") as f:
        json.dump(details, f, indent=2)

def render(config):
    st.title("Project Details")

    if 'current_project' not in st.session_state or 'current_project_path' not in st.session_state:
        st.error("Please select a project from the sidebar first.")
        return

    project_path = st.session_state.current_project_path
    details = load_project_details(project_path)

    details['name'] = st.text_input("Project Name", value=details['name'])
    details['description'] = st.text_area("Project Description", value=details['description'])
    details['version'] = st.text_input("Version", value=details['version'])
    details['author'] = st.text_input("Author", value=details['author'])

    st.subheader("Dependencies")
    for i, dep in enumerate(details['dependencies']):
        col1, col2 = st.columns([3, 1])
        details['dependencies'][i] = col1.text_input(f"Dependency {i+1}", value=dep)
        if col2.button("Remove", key=f"remove_{i}"):
            details['dependencies'].pop(i)
            st.experimental_rerun()

    if st.button("Add Dependency"):
        details['dependencies'].append("")
        st.experimental_rerun()

    if st.button("Save Project Details"):
        save_project_details(project_path, details)
        st.success("Project details saved successfully!")

    st.write(f"Project Path: {project_path}")
    st.json(details)  # Display current details for debugging
