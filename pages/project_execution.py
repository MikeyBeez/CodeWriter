import streamlit as st
from pathlib import Path
import json

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

def render(config):
    st.title("Project Execution")

    if 'current_project' not in st.session_state or 'current_project_path' not in st.session_state:
        st.error("Please select a project from the sidebar first.")
        return

    project_path = Path(st.session_state.current_project_path)
    st.write(f"Current Project: {st.session_state.current_project}")
    st.write(f"Project Path: {project_path}")
    st.write(f"Using AI Model: {config.get('model', 'deepseek-coder-v2')}")

    plan = load_plan_from_file(project_path)

    if plan is None:
        st.error("No project plan found. Please generate a plan first.")
        return

    st.subheader(plan['title'])
    for step in plan['steps']:
        st.write(f"Step {step['id']}: {step['title']} ({'Completed' if step['completed'] else 'In Progress'})")
        for substep in step['substeps']:
            col1, col2, col3 = st.columns([3, 1, 1])
            with col1:
                st.write(f"  {substep['id']}: {substep['title']} ({'Completed' if substep['completed'] else 'Pending'})")
            with col2:
                if st.button(f"View/Execute {substep['id']}"):
                    st.session_state.current_step = step['id']
                    st.session_state.current_substep = substep['id']
                    st.session_state.page = "View Step"
                    st.experimental_rerun()
            with col3:
                if not substep['completed']:
                    if st.button(f"Skip {substep['id']}"):
                        substep['completed'] = True
                        substep['skipped'] = True
                        save_plan_to_file(plan, project_path)
                        st.info(f"Step {substep['id']} skipped.")
                        st.experimental_rerun()

    if all(step['completed'] for step in plan['steps']):
        st.success("All steps completed! Project is ready for review.")

    if st.button("Back to Project Prompt"):
        st.session_state.page = "Project Prompt"
        st.experimental_rerun()

    if st.button("View Project Files"):
        st.session_state.page = "Project Files"
        st.experimental_rerun()
