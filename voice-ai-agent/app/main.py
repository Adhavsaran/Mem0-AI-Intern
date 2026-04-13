"""
Main entry point for Voice AI Agent application.
Uses: Whisper (HuggingFace) for STT + LM Studio for Intent Classification
"""
import sys
import os

# Add parent directory to path to allow imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.ui import create_ui
from utils.logger import log_info, log_error
from config import check_lm_studio, LM_STUDIO_BASE_URL


def main():
    """Main application entry point."""
    log_info("=" * 60)
    log_info("🎤 Voice-Controlled AI Agent")
    log_info("   STT: Whisper (HuggingFace)")
    log_info("   LLM: LM Studio (Local)")
    log_info("=" * 60)
    
    try:
        # Pre-flight checks
        log_info("\n📋 Running pre-flight checks...")
        
        # Check LM Studio
        if not check_lm_studio():
            log_error("✗ LM Studio is not running!")
            log_info("\n⚠️  To use this agent, start LM Studio:")
            log_info(f"   1. Download LM Studio from: https://lmstudio.ai")
            log_info(f"   2. Open an LLM model in LM Studio")
            log_info(f"   3. Start the local server (default: {LM_STUDIO_BASE_URL})")
            log_info(f"\n   Troubleshooting:")
            log_info(f"   - Ensure LM Studio is listening on {LM_STUDIO_BASE_URL}")
            log_info(f"   - Set LM_STUDIO_BASE_URL environment variable if using different port")
            return
        log_info("✓ LM Studio connected")
        
        # Check for required tools
        try:
            import gradio
            log_info("✓ Gradio installed")
        except ImportError:
            log_error("✗ Gradio not found. Install with: pip install gradio")
            return
        
        try:
            import transformers
            log_info("✓ Transformers installed")
        except ImportError:
            log_error("✗ Transformers not found. Install with: pip install transformers")
            return
        
        try:
            import torch
            log_info("✓ PyTorch installed")
        except ImportError:
            log_error("✗ PyTorch not found. Install with: pip install torch")
            return
        
        try:
            import soundfile
            log_info("✓ Soundfile installed")
        except ImportError:
            log_error("✗ Soundfile not found. Install with: pip install soundfile")
            return
        
        try:
            import openai
            log_info("✓ OpenAI library installed")
        except ImportError:
            log_error("✗ OpenAI library not found. Install with: pip install openai")
            return
        
        log_info("\n✅ All checks passed!\n")
        
        # Launch UI
        log_info("🚀 Launching Gradio UI...")
        log_info("📍 Open browser to: http://127.0.0.1:7860")
        log_info("   Press Ctrl+C to stop\n")
        
        ui = create_ui()
        ui.launch(
            share=False,
            server_name="127.0.0.1",
            server_port=7860
        )
    
    except KeyboardInterrupt:
        log_info("\n\n👋 Shutting down...")
    except Exception as e:
        log_error(f"Fatal error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
