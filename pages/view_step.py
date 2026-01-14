import streamlit as st
from pathlib import Path
import json
from utils import ollama_api

def load_plan_from_file(project_path):
    plan_file = project_path / "project_plan.json"
    if plan_file.exists():
        with open(plan_file, "r") as f:
            return json.load(f)
    return None

def save_plan_to_file(plan, project_path):
    plan_file = project_path / "project_plan.json"
    with open(plan_file, "w") as f:
        json.dump(plan, f, indent=2)

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
    st.title("View and Execute Step")

    if 'current_project' not in st.session_state or 'current_project_path' not in st.session_state:
        st.error("Please select a project from the sidebar first.")
        return

    project_path = Path(st.session_state.current_project_path)
    plan = load_plan_from_file(project_path)

    if plan is None:
        st.error("No project plan found. Please generate a plan first.")
        return

    st.write(f"Project: {plan['title']}")

    # Step selection
    step_options = [f"Step {step['id']}: {step['title']}" for step in plan['steps']]
    selected_step_index = st.selectbox("Select Step", range(len(step_options)), format_func=lambda x: step_options[x])
    selected_step = plan['steps'][selected_step_index]

    st.header(f"Step {selected_step['id']}: {selected_step['title']}")
    st.text_area("Step Description", value=selected_step['description'], height=100, disabled=True)

    # Substep selection
    substep_options = [f"Substep {substep['id']}: {substep['title']}" for substep in selected_step['substeps']]
    selected_substep_index = st.selectbox("Select Substep", range(len(substep_options)), format_func=lambda x: substep_options[x])
    selected_substep = selected_step['substeps'][selected_substep_index]

    st.subheader(f"Substep {selected_substep['id']}: {selected_substep['title']}")
    st.text_area("Substep Description", value=selected_substep['description'], height=100, disabled=True)

    # Display existing context and code
    if selected_substep.get('context'):
        st.subheader("Existing Context:")
        st.text_area("Context", value=selected_substep['context'], height=150, disabled=True)
    
    if selected_substep.get('code'):
        st.subheader("Existing Code:")
        st.code(selected_substep['code'])

    # Execute or update step
    context = st.text_area("Additional Context", value=selected_substep.get('context', ''), height=150)
    if st.button("Execute Step"):
        with st.spinner(f"Executing step {selected_substep['id']}..."):
            result = execute_step(selected_step, selected_substep, context, config.get('model', 'deepseek-coder-v2'))
            selected_substep['code'] = result
            selected_substep['context'] = context
            selected_substep['completed'] = True
            save_plan_to_file(plan, project_path)
            st.success(f"Step {selected_substep['id']} completed!")
            st.subheader("Generated Code:")
            st.code(result)

    if st.button("Back to Project Execution"):
        st.session_state.page = "Project Execution"
        st.experimental_rerun()
