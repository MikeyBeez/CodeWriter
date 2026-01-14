import streamlit as st
from pathlib import Path
import json
from utils import ollama_api
from utils.project_planner import ProjectPlanner, render_planner

def save_project_details(details, project_path):
    details_file = project_path / "project_details.json"
    with open(details_file, "w") as f:
        json.dump(details, f, indent=2)

def load_project_details(project_path):
    details_file = project_path / "project_details.json"
    if details_file.exists():
        with open(details_file, "r") as f:
            return json.load(f)
    return {
        'type': '', 'description': '', 'audience': '', 'features': '',
        'ui': '', 'storage': '', 'apis': '', 'performance': '',
        'scalability': '', 'additional': ''
    }

def render(config):
    st.title("Project Prompt and Planning")

    if 'current_project' not in st.session_state or 'current_project_path' not in st.session_state:
        st.error("Please select a project from the sidebar first.")
        return

    project_path = Path(st.session_state.current_project_path)
    st.write(f"Current Project: {st.session_state.current_project}")
    st.write(f"Project Path: {project_path}")
    st.write(f"Using AI Model: {config.get('model', 'deepseek-coder-v2')}")

    # Project Planner
    planner = ProjectPlanner(project_path)
    render_planner(planner)

    # Load or initialize project details
    project_details = load_project_details(project_path)

    # Project Details Form
    st.subheader("Project Specification")
    with st.form("project_details_form"):
        project_details['type'] = st.text_input("Project Type", project_details['type'])
        project_details['description'] = st.text_area("Project Description", project_details['description'])
        project_details['audience'] = st.text_input("Target Audience", project_details['audience'])
        project_details['features'] = st.text_area("Main Features", project_details['features'])
        project_details['ui'] = st.selectbox("User Interface", ["", "Command Line", "GUI", "Web-based", "Mobile App", "Other"], index=["", "Command Line", "GUI", "Web-based", "Mobile App", "Other"].index(project_details['ui']))
        project_details['storage'] = st.selectbox("Data Storage", ["", "No", "Local File", "Database", "Cloud Storage"], index=["", "No", "Local File", "Database", "Cloud Storage"].index(project_details['storage']))
        project_details['apis'] = st.text_input("External APIs", project_details['apis'])
        project_details['performance'] = st.text_area("Performance Requirements", project_details['performance'])
        project_details['scalability'] = st.selectbox("Scalability Importance", ["", "Not important", "Somewhat important", "Very important", "Critical"], index=["", "Not important", "Somewhat important", "Very important", "Critical"].index(project_details['scalability']))
        project_details['additional'] = st.text_area("Additional Requirements", project_details['additional'])

        if st.form_submit_button("Save Project Details"):
            save_project_details(project_details, project_path)
            st.success("Project details saved successfully!")

    if st.button("View Project Files"):
        st.session_state.page = "Project Files"
        st.experimental_rerun()
