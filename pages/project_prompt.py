import streamlit as st
import requests
import json

OLLAMA_API_URL = "http://localhost:11434/api/generate"

def generate_response(prompt, model):
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
    st.write(f"Using AI Model: {config.get('model', 'deepseek-coder-v2')}")

    # Initialize session state for questions
    if 'questions_completed' not in st.session_state:
        st.session_state.questions_completed = False

    if not st.session_state.questions_completed:
        st.subheader("Project Specification Questions")
        
        project_type = st.text_input("What type of project do you want to create? (e.g., game, web application, mobile app, data analysis tool, etc.)")
        
        project_description = st.text_area("Provide a brief description of your project and its main purpose.")
        
        target_audience = st.text_input("Who is the target audience for this project?")
        
        main_features = st.text_area("What are the main features or functionalities you want to include? (List them separated by commas)")
        
        user_interface = st.selectbox("What type of user interface does your project require?", 
                                      ["Command Line", "Graphical User Interface (GUI)", "Web-based", "Mobile App", "Other"])
        if user_interface == "Other":
            user_interface = st.text_input("Please specify the user interface type:")
        
        data_storage = st.selectbox("Will your project require data storage?", 
                                    ["No", "Yes - Local File Storage", "Yes - Database", "Yes - Cloud Storage", "Not sure"])
        
        external_apis = st.text_input("Are there any external APIs or services your project needs to integrate with? If yes, please list them.")
        
        performance_requirements = st.text_area("Are there any specific performance requirements or constraints for your project?")
        
        scalability = st.selectbox("How important is scalability for your project?", 
                                   ["Not important", "Somewhat important", "Very important", "Critical"])
        
        additional_requirements = st.text_area("Any additional requirements, constraints, or specifications?")

        if st.button("Generate Project Plan"):
            if project_type and project_description:
                st.session_state.questions_completed = True
                st.session_state.project_prompt = f"""
                Create a detailed project plan for a {project_type} with the following specifications:
                
                Project Description: {project_description}
                Target Audience: {target_audience}
                Main Features: {main_features}
                User Interface: {user_interface}
                Data Storage: {data_storage}
                External APIs/Services: {external_apis}
                Performance Requirements: {performance_requirements}
                Scalability Importance: {scalability}
                Additional Requirements: {additional_requirements}

                Please provide:
                1. A comprehensive project overview
                2. A detailed list of features and functionalities
                3. A suggested technology stack and architecture
                4. A proposed file/folder structure for the project
                5. A development roadmap with milestones and estimated timelines
                6. Potential challenges, considerations, and mitigation strategies
                7. Testing and quality assurance recommendations
                8. Deployment and maintenance considerations
                """
                st.experimental_rerun()
            else:
                st.warning("Please provide at least the project type and description before generating the plan.")
    else:
        st.subheader("Generated Project Plan")
        
        if st.button("Regenerate Project Plan"):
            st.session_state.questions_completed = False
            st.experimental_rerun()
        
        prompt = st.session_state.project_prompt
        
        with st.spinner("Generating project plan..."):
            response = generate_response(prompt, config.get('model', 'deepseek-coder-v2'))
            st.write(response)

            # Save the generated plan
            plan_file = st.session_state.current_project_path / "project_plan.md"
            with open(plan_file, "w") as f:
                f.write(response)
            st.success(f"Project plan saved to {plan_file}")

    st.divider()
    
    st.subheader("Existing Project Plan")
    plan_file = st.session_state.current_project_path / "project_plan.md"
    if plan_file.exists():
        with open(plan_file, "r") as f:
            existing_plan = f.read()
        st.text_area("Existing Plan", value=existing_plan, height=300, disabled=True)
    else:
        st.info("No existing project plan found.")
