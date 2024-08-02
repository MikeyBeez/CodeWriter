import streamlit as st
import requests
import json

OLLAMA_API_URL = "http://localhost:11434/api/generate"

def generate_response(prompt, model="deepseek-coder-v2"):
    data = {
        "model": model,
        "prompt": prompt,
        "stream": False
    }
    response = requests.post(OLLAMA_API_URL, json=data)
    if response.status_code == 200:
        return response.json()['response']
    else:
        return f"Error: {response.status_code} - {response.text}"

def render(config):
    st.title("Project Prompt")

    if 'current_project' not in st.session_state or 'current_project_path' not in st.session_state:
        st.error("Please select a project from the sidebar first.")
        return

    st.write(f"Current Project: {st.session_state.current_project}")
    st.write(f"Project Path: {st.session_state.current_project_path}")

    prompt = st.text_area("Enter your project prompt", height=150,
                          help="Describe the project you want to create. Be as specific as possible.")
    
    if st.button("Generate Project Plan"):
        if prompt:
            with st.spinner("Generating project plan..."):
                response = generate_response(prompt)
                st.subheader("Generated Project Plan")
                st.write(response)

                # Save the generated plan
                plan_file = st.session_state.current_project_path / "project_plan.md"
                with open(plan_file, "w") as f:
                    f.write(response)
                st.success(f"Project plan saved to {plan_file}")
        else:
            st.warning("Please enter a prompt before generating a project plan.")

    st.divider()
    
    st.subheader("Existing Project Plan")
    plan_file = st.session_state.current_project_path / "project_plan.md"
    if plan_file.exists():
        with open(plan_file, "r") as f:
            existing_plan = f.read()
        st.text_area("Existing Plan", value=existing_plan, height=300, disabled=True)
    else:
        st.info("No existing project plan found.")
