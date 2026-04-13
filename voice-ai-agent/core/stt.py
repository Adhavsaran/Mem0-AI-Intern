"""
Speech-to-Text module using HuggingFace Whisper.
"""
from transformers import pipeline
from utils.logger import log_info, log_error


class SpeechToText:
    """Convert audio files to text using Whisper."""
    
    def __init__(self, model_name: str = "openai/whisper-small"):
        """
        Initialize the STT pipeline.
        
        Args:
            model_name: HuggingFace model identifier
        """
        self.model_name = model_name
        try:
            log_info(f"Loading {model_name} model...")
            self.pipeline = pipeline("automatic-speech-recognition", model=model_name)
            log_info(f"Model {model_name} loaded successfully!")
        except Exception as e:
            log_error(f"Failed to load model {model_name}: {e}")
            self.pipeline = None
    
    def transcribe(self, audio_path: str) -> str:
        """
        Transcribe audio file to text.
        
        Args:
            audio_path: Path to audio file (.wav, .mp3, etc.)
        
        Returns:
            Transcribed text
        
        Raises:
            ValueError: If model not loaded or transcription fails
        """
        if not self.pipeline:
            raise ValueError("STT pipeline not initialized. Model loading failed.")
        
        try:
            log_info(f"Transcribing audio: {audio_path}")
            result = self.pipeline(audio_path)
            text = result.get("text", "").strip()
            log_info(f"Transcription complete: {text[:100]}...")
            return text
        except Exception as e:
            log_error(f"Transcription failed: {e}")
            raise ValueError(f"Transcription failed: {e}")
