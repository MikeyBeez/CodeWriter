# Code Writer

Code Writer is an AI-assisted project initialization and management tool that uses Ollama to generate project plans and code snippets. It provides a user-friendly interface for creating, managing, and developing software projects with the help of AI models.

## Features

- Project creation and management
- AI-powered project plan generation
- Customizable AI model selection
- Project details management
- Streamlit-based user interface

## Prerequisites

- Python 3.7+
- Ollama installed and running on your machine
- Required Python packages (see `requirements.txt`)

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/code-writer.git
   cd code-writer
   ```

2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

3. Ensure Ollama is installed and running on your machine. Visit [Ollama's website](https://ollama.ai/) for installation instructions.

## Usage

1. Start the application:
   ```
   streamlit run app.py
   ```

2. Open your web browser and navigate to the URL provided by Streamlit (usually `http://localhost:8501`).

3. Use the sidebar to create a new project or select an existing one.

4. Navigate through the different pages:
   - Home: Overview of the application
   - Project Prompt: Generate AI-powered project plans
   - Project Details: Manage project-specific information
   - Settings: Configure the AI model and other settings

## Project Structure

```
code-writer/
├── app.py
├── config.py
├── components/
│   └── sidebar.py
├── pages/
│   ├── home.py
│   ├── project_prompt.py
│   ├── project_details.py
│   └── settings.py
├── utils/
│   └── setup_wizard.py
└── README.md
```

## Customization

You can customize the AI model used for generating project plans by selecting a different model in the Settings page. The application currently defaults to the `deepseek-coder-v2` model.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [Streamlit](https://streamlit.io/) for the web application framework
- [Ollama](https://ollama.ai/) for the AI model integration
