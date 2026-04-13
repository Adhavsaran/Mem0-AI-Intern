"""
Main entry point for Voice AI Agent application.
Uses: Whisper (HuggingFace) for STT + Ollama for Intent Classification
"""
import sys
import os

# Add parent directory to path to allow imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.ui import create_ui
from utils.logger import log_info, log_error
from config import check_ollama, OLLAMA_BASE_URL


def main():
    """Main application entry point."""
    import sys
    import io
    
    # Ensure output is unbuffered for real-time logging
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', line_buffering=True)
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', line_buffering=True)
    
    log_info("=" * 60)
    log_info("🎤 Voice-Controlled AI Agent")
    log_info("   STT: Whisper (HuggingFace)")
    log_info("   LLM: Ollama (Local)")
    log_info("=" * 60)
    
    try:
        # Pre-flight checks
        log_info("\n📋 Running pre-flight checks...")
        
        # Check Ollama
        if not check_ollama():
            log_error("✗ Ollama is not running!")
            log_info("\n⚠️  To use this agent, start Ollama:")
            log_info(f"   1. Download Ollama from: https://ollama.ai")
            log_info(f"   2. Install and run: ollama serve")
            log_info(f"   3. Pull a model: ollama pull mistral (or another model)")
            log_info(f"\n   Troubleshooting:")
            log_info(f"   - Ensure Ollama is listening on {OLLAMA_BASE_URL}")
            log_info(f"   - Set OLLAMA_BASE_URL environment variable if using different port")
            return
        log_info("✓ Ollama connected")
        log_info("✅ Pre-flight checks passed!\n")
        
        # Initialize UI
        log_info("Creating UI...")
        ui = create_ui()
        
        # Find available port
        import socket
        def find_available_port(start_port=7860):
            """Find an available port starting from start_port."""
            port = start_port
            for _ in range(100):  # Try up to 100 ports
                try:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    result = sock.connect_ex(('127.0.0.1', port))
                    sock.close()
                    if result != 0:  # Port is available
                        return port
                except Exception:
                    pass
                port += 1
            return start_port  # Fall back to original port
        
        port = find_available_port()
        
        # Launch UI
        log_info("🚀 Launching Gradio UI...")
        log_info(f"📍 Open browser to: http://127.0.0.1:{port}")
        log_info("   Press Ctrl+C to stop\n")
        log_info("DEBUG: About to call ui.launch()...")
        
        ui.launch(
            share=False,
            server_name="127.0.0.1",
            server_port=port
        )
        
        log_info("DEBUG: ui.launch() completed (this shouldn't print if blocking)")
    
    except KeyboardInterrupt:
        log_info("\n\n👋 Shutting down...")
    except Exception as e:
        log_error(f"Fatal error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
