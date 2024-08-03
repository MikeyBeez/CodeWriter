# CodeWriter Architectural Guide

## 1. Overview

CodeWriter is an AI-assisted project initialization and management tool that uses Ollama to generate project plans and code snippets. This document outlines the architectural design of the CodeWriter application, focusing on its project structure, data flow, and key components.

## 2. Project Structure

```
codewriter/
├── app.py
├── config.py
├── components/
│   └── sidebar.py
├── pages/
│   ├── home.py
│   ├── project_prompt.py
│   ├── project_files.py
│   └── settings.py
├── utils/
│   └── ollama_api.py
├── documents/
│   └── architectural_guide.md
└── README.md
```

## 3. Key Components

### 3.1 app.py
The main entry point of the application. It sets up the Streamlit configuration, loads the global configuration, and manages the navigation between different pages.

### 3.2 config.py
Handles loading and saving of the application configuration, including the code directory and AI model settings.

### 3.3 components/sidebar.py
Renders the sidebar component, which includes project selection, creation, and navigation controls.

### 3.4 pages/
Contains individual Streamlit pages for different functionalities:
- `home.py`: The landing page of the application.
- `project_prompt.py`: Handles project plan generation and step-by-step execution.
- `project_files.py`: Manages viewing and editing of project files.
- `settings.py`: Allows users to configure application settings.

### 3.5 utils/ollama_api.py
Provides a wrapper for interacting with the Ollama API, handling requests and error management.

## 4. Data Flow

1. User inputs project details in `project_prompt.py`.
2. `project_prompt.py` uses `ollama_api.py` to generate a structured project plan.
3. The plan is saved as a JSON file in the project directory.
4. Users can execute each step of the plan, with results saved back to the JSON file.
5. Generated code is saved into appropriate files in the project directory.

## 5. Project Plan Structure

The project plan is stored as a JSON file with the following structure:

```json
{
    "title": "Project Title",
    "steps": [
        {
            "id": 1,
            "title": "Step 1 Title",
            "description": "Step 1 Description",
            "completed": false,
            "substeps": [
                {
                    "id": 1.1,
                    "title": "Substep 1.1 Title",
                    "description": "Substep 1.1 Description",
                    "completed": false,
                    "context": "",
                    "code": ""
                },
                // More substeps...
            ]
        },
        // More steps...
    ]
}
```

## 6. State Management

- Application state is managed using Streamlit's `st.session_state`.
- Project-specific state (plan, completion status) is stored in the JSON file within each project directory.
- Configuration state is managed by `config.py` and stored in a JSON file in the user's home directory.

## 7. AI Integration

- The application uses Ollama for AI-powered code and plan generation.
- Interactions with Ollama are abstracted through the `ollama_api.py` module.
- The AI model can be configured in the settings page.

## 8. User Interface

- The UI is built using Streamlit, providing a web-based interface.
- The sidebar (from `sidebar.py`) is consistent across all pages for navigation.
- Each page (`home.py`, `project_prompt.py`, etc.) renders its specific content in the main area.

## 9. File Management

- Project files are managed within subdirectories of the configured code directory.
- Each project has its own directory containing:
  - `project_plan.json`: The structured project plan
  - Generated code files
  - Any additional project-specific files

## 10. Error Handling

- API errors are handled in the `ollama_api.py` module.
- UI-level error messages are displayed using Streamlit's `st.error()` function.
- File I/O errors are caught and reported in the respective functions.

## 11. Extensibility

- New pages can be added to the `pages/` directory and integrated into the navigation.
- Additional AI capabilities can be implemented by extending the `ollama_api.py` module or creating new API modules.

## 12. Security Considerations

- User inputs should be sanitized to prevent injection attacks.
- File paths should be validated to prevent unauthorized access outside the project directory.
- API keys and sensitive configuration should be stored securely and not exposed in the UI.

This architectural guide provides an overview of the CodeWriter application's structure and key components. It serves as a reference for understanding the application's design and can be used to onboard new developers or plan future enhancements.
