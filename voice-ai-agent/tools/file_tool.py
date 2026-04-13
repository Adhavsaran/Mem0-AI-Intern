"""
File creation tool - safely create files in output directory.
"""
import os
from pathlib import Path
from utils.logger import log_info, log_error


OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "output")


def ensure_output_dir():
    """Ensure output directory exists."""
    os.makedirs(OUTPUT_DIR, exist_ok=True)


def sanitize_filename(filename: str) -> str:
    """
    Sanitize filename to prevent path traversal attacks.
    
    Args:
        filename: Raw filename
    
    Returns:
        Safe filename
    """
    # Remove path separators and suspicious characters
    filename = os.path.basename(filename)
    filename = filename.replace("..", "").replace("/", "").replace("\\", "")
    
    if not filename:
        filename = "output.txt"
    
    return filename


def create_file(filename: str, content: str = "") -> str:
    """
    Create a file in the output directory.
    
    Args:
        filename: Name of file to create
        content: File content (optional)
    
    Returns:
        Success message with file path
    
    Raises:
        ValueError: If creation fails
    """
    ensure_output_dir()
    
    # Sanitize filename
    safe_name = sanitize_filename(filename)
    file_path = os.path.join(OUTPUT_DIR, safe_name)
    
    try:
        # Write file
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        
        log_info(f"File created: {file_path}")
        return f"✓ File created successfully: {safe_name}"
    except Exception as e:
        log_error(f"Failed to create file: {e}")
        raise ValueError(f"Failed to create file: {e}")


def get_output_dir() -> str:
    """Get the output directory path."""
    ensure_output_dir()
    return OUTPUT_DIR
