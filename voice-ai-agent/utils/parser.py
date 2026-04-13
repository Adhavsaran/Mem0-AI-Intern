"""
Safe JSON parsing utilities for handling LLM outputs.
"""
import json
import re
from typing import Dict, Any


def safe_parse_json(response: str, default: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    Safely parse JSON from LLM output.
    
    Args:
        response: Raw response from LLM
        default: Default dict to return if parsing fails
    
    Returns:
        Parsed JSON dict or default
    """
    if default is None:
        default = {"intent": "chat"}
    
    # Try direct JSON parsing first
    try:
        return json.loads(response)
    except json.JSONDecodeError:
        pass
    
    # Try to extract JSON from markdown code blocks
    try:
        match = re.search(r'```(?:json)?\s*({.*?})\s*```', response, re.DOTALL)
        if match:
            return json.loads(match.group(1))
    except (json.JSONDecodeError, AttributeError):
        pass
    
    # Try to extract JSON object from response
    try:
        # Find first { and last }
        start = response.find('{')
        end = response.rfind('}')
        if start != -1 and end != -1 and start < end:
            json_str = response[start:end+1]
            return json.loads(json_str)
    except json.JSONDecodeError:
        pass
    
    # Return default
    return default


def sanitize_intent(intent_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validate and sanitize intent data.
    
    Args:
        intent_data: Raw intent data
    
    Returns:
        Sanitized intent data
    """
    valid_intents = ["create_file", "write_code", "summarize", "chat"]
    
    intent = intent_data.get("intent", "chat")
    if intent not in valid_intents:
        intent = "chat"
    
    return {
        "intent": intent,
        "filename": intent_data.get("filename", ""),
        "language": intent_data.get("language", ""),
    }
