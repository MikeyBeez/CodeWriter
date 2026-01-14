import streamlit as st
import json
from pathlib import Path
from utils import ollama_api

class ProjectPlanner:
    def __init__(self, project_path: Path):
        self.project_path = project_path
        self.plan_file = self.project_path / "project_plan.json"
        self.plan = self.load_plan()

    def load_plan(self):
        if self.plan_file.exists():
            with open(self.plan_file, 'r') as f:
                return json.load(f)
        return {"title": "", "steps": [], "notes": ""}

    def save_plan(self):
        with open(self.plan_file, 'w') as f:
            json.dump(self.plan, f, indent=2)

    def add_step(self, step):
        self.plan["steps"].append(step)
        self.save_plan()

    def update_step(self, index, step):
        self.plan["steps"][index] = step
        self.save_plan()

    def delete_step(self, index):
        del self.plan["steps"][index]
        self.save_plan()

    def update_notes(self, notes):
        self.plan["notes"] = notes
        self.save_plan()

    def generate_plan(self, project_description):
        prompt = f"""
        Given the following project description, create a detailed project plan for a Python project. 
        Format the plan as a JSON object with the following structure:
        {{
            "title": "Project Title",
            "steps": [
                {{
                    "id": 1,
                    "title": "Step Title",
                    "description": "Detailed step description",
                    "completed": false,
                    "substeps": [
                        {{
                            "id": 1.1,
                            "title": "Substep Title",
                            "description": "Detailed substep description",
                            "completed": false
                        }}
                    ]
                }}
            ],
            "notes": "Any overall project notes or considerations"
        }}

        Project Description:
        {project_description}

        Ensure that the plan includes all major phases of software development, including planning, design, implementation, testing, and deployment. Be specific about tasks related to the project description.

        Return only the JSON object, with no additional explanation.
        """
        
        response = ollama_api.generate(prompt)
        try:
            generated_plan = json.loads(response)
            self.plan = generated_plan
            self.save_plan()
            return True
        except json.JSONDecodeError:
            return False

def render_step_form(step=None, index=None):
    with st.form(f"step_form_{index if index is not None else 'new'}"):
        step_title = st.text_input("Step Title", value=step["title"] if step else "")
        step_description = st.text_area("Step Description", value=step["description"] if step else "")
        step_completed = st.checkbox("Completed", value=step.get("completed", False) if step else False)
        
        if st.form_submit_button("Save Step"):
            return {
                "id": step["id"] if step else (index + 1 if index is not None else 1),
                "title": step_title,
                "description": step_description,
                "completed": step_completed,
                "substeps": step.get("substeps", []) if step else []
            }
    return None

def render_planner(planner: ProjectPlanner):
    st.subheader("Project Plan")
    st.write(f"Project Title: {planner.plan['title']}")

    st.subheader("Project Steps")
    for i, step in enumerate(planner.plan["steps"]):
        with st.expander(f"Step {step['id']}: {step['title']}"):
            updated_step = render_step_form(step, i)
            if updated_step:
                planner.update_step(i, updated_step)
            if st.button(f"Delete Step {step['id']}"):
                planner.delete_step(i)
                st.experimental_rerun()

            # Render substeps
            for j, substep in enumerate(step.get("substeps", [])):
                with st.expander(f"Substep {substep['id']}: {substep['title']}"):
                    st.write(substep["description"])
                    substep_completed = st.checkbox(f"Completed", value=substep.get("completed", False), key=f"substep_{step['id']}_{substep['id']}")
                    if substep_completed != substep.get("completed", False):
                        substep["completed"] = substep_completed
                        planner.update_step(i, step)

    st.subheader("Add New Step")
    new_step = render_step_form()
    if new_step:
        planner.add_step(new_step)
        st.experimental_rerun()

    st.subheader("Project Notes")
    notes = st.text_area("Notes", value=planner.plan["notes"])
    if notes != planner.plan["notes"]:
        planner.update_notes(notes)

    st.subheader("Generate Plan from Description")
    project_description = st.text_area("Enter Project Description")
    if st.button("Generate Plan"):
        if planner.generate_plan(project_description):
            st.success("Plan generated and saved!")
            st.experimental_rerun()
        else:
            st.error("Failed to generate plan. Please try again.")
