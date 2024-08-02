import streamlit as st
from config import save_config

def render(config):
    st.title("⚙️ Settings")

    # List of available models
    available_models = [
        "deepseek-coder-v2",
        "llama3.1",
        "gemma2",
        "llava",
        "llama3",
        "gemma:2b",
        "phi3",
        "nomic-embed-text",
        "qwen2",
        "codeqwen:7b",
        "all-minilm",
        "mxbai-embed-large",
        "llama3-chatqa",
        "mistral"
    ]

    # Model selection
    selected_model = st.selectbox(
        "Select AI Model",
        options=available_models,
        index=available_models.index(config.get('model', 'deepseek-coder-v2'))
    )

    if st.button("Save Settings"):
        config['model'] = selected_model
        save_config(config)
        st.success("Settings saved successfully!")

    st.write("Current Settings:")
    st.json(config)
