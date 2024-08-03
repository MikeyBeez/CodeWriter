import streamlit as st
from pathlib import Path
import json
from utils import ollama_api

def save_plan_to_file(plan, project_path):
    plan_file = project_path / "project_plan.json"
    with open(plan_file, "w") as f:
        json.dump(plan, f, indent=2)

def load_plan_from_file(project_path):
    plan_file = project_path / "project_plan.json"
    if plan_file.exists():
        with open(plan_file, "r") as f:
            return json.load(f)
    return None

def generate_structured_plan(project_details, model):
    prompt = f"""
    Create a structured project plan for a {project_details['type']} with the following specifications:
    
    Project Description: {project_details['description']}
    Target Audience: {project_details['audience']}
    Main Features: {project_details['features']}
    User Interface: {project_details['ui']}
    Data Storage: {project_details['storage']}
    External APIs/Services: {project_details['apis']}
    Performance Requirements: {project_details['performance']}
    Scalability Importance: {project_details['scalability']}
    Additional Requirements: {project_details['additional']}

    Please provide a plan with the following structure:
    1. Project Title
    2. 5-7 main steps, each with:
       - Step title
       - Step description
       - 2-4 substeps for each step, each with:
         * Substep title
         * Substep description

    Format the output as a JSON object matching this structure:
    {
        "title": "Project Title",
        "steps": [
            {
                "id": 1,
                "title": "Step 1 Title",
                "description": "Step 1 Description",
                "substeps": [
                    {
                        "id": 1.1,
                        "title": "Substep 1.1 Title",
                        "description": "Substep 1.1 Description"
                    },
                    ...
                ]
            },
            ...
        ]
    }
    """
    response = ollama_api.generate(prompt, model)
    try:
        plan = json.loads(response)
        # Add completed, context, and code fields
        for step in plan['steps']:
            step['completed'] = False
            for substep in step['substeps']:
                substep['completed'] = False
                substep['context'] = ""
                substep['code'] = ""
        return plan
    except json.JSONDecodeError:
        st.error("Failed to parse the generated plan. Please try again.")
        return None

def execute_step(step, substep, context, model):
    prompt = f"""
    Execute the following step in a software development project:

    Step: {step['title']}
    Substep: {substep['title']}
    Description: {substep['description']}
    Additional Context: {context}

    Please provide the code necessary to implement this substep. 
    If the substep doesn't require code, provide a detailed explanation of the actions to be taken.
    """
    return ollama_api.generate(prompt, model)

def render(config):
    st.title("Project Prompt and Step-by-Step Execution")

    if 'current_project' not in st.session_state or 'current_project_path' not in st.session_state:
        st.error("Please select a project from the sidebar first.")
        return

    project_path = Path(st.session_state.current_project_path)
    st.write(f"Current Project: {st.session_state.current_project}")
    st.write(f"Project Path: {project_path}")
    st.write(f"Using AI Model: {config.get('model', 'deepseek-coder-v2')}")

    plan = load_plan_from_file(project_path)

    if plan is None:
        if 'project_details' not in st.session_state:
            st.session_state.project_details = {
                'type': '', 'description': '', 'audience': '', 'features': '',
                'ui': '', 'storage': '', 'apis': '', 'performance': '',
                'scalability': '', 'additional': ''
            }

        st.subheader("Project Specification Questions")
        
        st.session_state.project_details['type'] = st.text_input("Project Type", st.session_state.project_details['type'])
        st.session_state.project_details['description'] = st.text_area("Project Description", st.session_state.project_details['description'])
        st.session_state.project_details['audience'] = st.text_input("Target Audience", st.session_state.project_details['audience'])
        st.session_state.project_details['features'] = st.text_area("Main Features", st.session_state.project_details['features'])
        st.session_state.project_details['ui'] = st.selectbox("User Interface", ["", "Command Line", "GUI", "Web-based", "Mobile App", "Other"])
        st.session_state.project_details['storage'] = st.selectbox("Data Storage", ["", "No", "Local File", "Database", "Cloud Storage"])
        st.session_state.project_details['apis'] = st.text_input("External APIs", st.session_state.project_details['apis'])
        st.session_state.project_details['performance'] = st.text_area("Performance Requirements", st.session_state.project_details['performance'])
        st.session_state.project_details['scalability'] = st.selectbox("Scalability Importance", ["", "Not important", "Somewhat important", "Very important", "Critical"])
        st.session_state.project_details['additional'] = st.text_area("Additional Requirements", st.session_state.project_details['additional'])

        if st.button("Generate Project Plan"):
            with st.spinner("Generating project plan..."):
                plan = generate_structured_plan(st.session_state.project_details, config.get('model', 'deepseek-coder-v2'))
                if plan:
                    save_plan_to_file(plan, project_path)
                    st.success("Project plan generated and saved successfully!")
                    st.experimental_rerun()
    else:
        st.subheader(plan['title'])
        for step in plan['steps']:
            st.write(f"Step {step['id']}: {step['title']} ({'Completed' if step['completed'] else 'In Progress'})")
            for substep in step['substeps']:
                col1, col2, col3 = st.columns([3, 1, 1])
                with col1:
                    st.write(f"  {substep['id']}: {substep['title']} ({'Completed' if substep['completed'] else 'Pending'})")
                with col2:
                    if not substep['completed']:
                        if st.button(f"Do Step {substep['id']}"):
                            context = st.text_area(f"Additional context for step {substep['id']}:", key=f"context_{substep['id']}")
                            with st.spinner(f"Executing step {substep['id']}..."):
                                result = execute_step(step, substep, context, config.get('model', 'deepseek-coder-v2'))
                                substep['code'] = result
                                substep['context'] = context
                                substep['completed'] = True
                                save_plan_to_file(plan, project_path)
                                st.success(f"Step {substep['id']} completed!")
                                st.experimental_rerun()
                with col3:
                    if substep['completed']:
                        if st.button(f"View Result {substep['id']}"):
                            st.code(substep['code'])
                            st.write("Context:", substep['context'])

        if all(step['completed'] for step in plan['steps']):
            st.success("All steps completed! Project is ready for review.")

    if st.button("View Project Files"):
        st.session_state.page = "project_files"
        st.experimental_rerun()
