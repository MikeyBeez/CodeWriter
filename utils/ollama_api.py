import requests
import streamlit as st
import time

OLLAMA_API_URL = "http://localhost:11434/api/generate"

def generate(prompt, model, max_retries=3):
    for attempt in range(max_retries):
        try:
            data = {
                "model": model,
                "prompt": prompt,
                "stream": False
            }
            response = requests.post(OLLAMA_API_URL, json=data, timeout=300)  # 5-minute timeout
            response.raise_for_status()  # Raises an HTTPError for bad responses
            return response.json()['response']
        except requests.exceptions.RequestException as e:
            st.error(f"Ollama API Error (Attempt {attempt + 1}/{max_retries}): {str(e)}")
            if attempt < max_retries - 1:
                st.warning(f"Retrying in 5 seconds...")
                time.sleep(5)
            else:
                st.error("Failed to generate response after multiple attempts.")
                st.info("Troubleshooting steps:")
                st.info("1. Ensure Ollama is running on your machine.")
                st.info(f"2. Check if the model '{model}' is properly installed.")
                st.info("3. Try restarting the Ollama service.")
                st.info("4. Check Ollama logs for more detailed error information.")
    return None
