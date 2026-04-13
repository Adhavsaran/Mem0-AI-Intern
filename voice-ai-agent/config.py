"""
Configuration for Ollama local LLM connection.
Ollama provides OpenAI-compatible API on localhost:11434
"""
import os
from utils.logger import log_info, log_error

# Ollama Configuration
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434/v1")
OLLAMA_API_KEY = os.getenv("OLLAMA_API_KEY", "not-needed")  # Dummy key for local Ollama

def get_ollama_client():
    """
    Create and return Ollama client (OpenAI-compatible).
    
    Returns:
        OpenAI client configured for Ollama
    """
    from openai import OpenAI
    
    client = OpenAI(
        base_url=OLLAMA_BASE_URL,
        api_key=OLLAMA_API_KEY
    )
    return client


def check_ollama():
    """
    Check if Ollama is running and accessible.
    
    Returns:
        True if Ollama is accessible, False otherwise
    """
    try:
        import requests
        response = requests.get(f"{OLLAMA_BASE_URL}/models", timeout=5)
        if response.status_code == 200:
            log_info("✓ Ollama is running and accessible")
            return True
    except Exception as e:
        log_error(f"Cannot connect to Ollama at {OLLAMA_BASE_URL}: {e}")
        return False


def get_ollama_models():
    """
    Get list of available models from Ollama.
    
    Returns:
        List of model names or empty list if error
    """
    try:
        client = get_ollama_client()
        models = client.models.list()
        model_list = [model.id for model in models.data]
        log_info(f"Available Ollama models: {model_list}")
        return model_list
    except Exception as e:
        log_error(f"Failed to get models from Ollama: {e}")
        return []
