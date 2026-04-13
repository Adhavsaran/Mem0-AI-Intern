"""
Configuration for LM Studio local LLM connection.
LM Studio provides OpenAI-compatible API on localhost:1234
"""
import os
from utils.logger import log_info, log_error

# LM Studio Configuration
LM_STUDIO_BASE_URL = os.getenv("LM_STUDIO_BASE_URL", "http://localhost:1234/v1")
LM_STUDIO_API_KEY = os.getenv("LM_STUDIO_API_KEY", "not-needed")  # Dummy key for local LM Studio

def get_lm_studio_client():
    """
    Create and return LM Studio client (OpenAI-compatible).
    
    Returns:
        OpenAI client configured for LM Studio
    """
    from openai import OpenAI
    
    client = OpenAI(
        base_url=LM_STUDIO_BASE_URL,
        api_key=LM_STUDIO_API_KEY
    )
    return client


def check_lm_studio():
    """
    Check if LM Studio is running and accessible.
    
    Returns:
        True if LM Studio is accessible, False otherwise
    """
    try:
        import requests
        response = requests.get(f"{LM_STUDIO_BASE_URL}/models", timeout=5)
        if response.status_code == 200:
            log_info("✓ LM Studio is running and accessible")
            return True
    except Exception as e:
        log_error(f"Cannot connect to LM Studio at {LM_STUDIO_BASE_URL}: {e}")
        return False


def get_lm_studio_models():
    """
    Get list of available models from LM Studio.
    
    Returns:
        List of model names or empty list if error
    """
    try:
        client = get_lm_studio_client()
        models = client.models.list()
        model_list = [model.id for model in models.data]
        log_info(f"Available LM Studio models: {model_list}")
        return model_list
    except Exception as e:
        log_error(f"Failed to get models from LM Studio: {e}")
        return []
