"""
Speech-to-Text module using HuggingFace Whisper.
"""
from transformers import WhisperProcessor, WhisperForConditionalGeneration
import librosa
import torch
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
        self.processor = None
        self.model = None
        self.device = "cpu"  # Use CPU for stability
        
        try:
            log_info(f"Loading {model_name} model...")
            log_info("⏳ Downloading processor (this may take a minute on first run)...")
            self.processor = WhisperProcessor.from_pretrained(model_name)
            log_info("✓ Processor downloaded. Now downloading model (500MB+)...")
            self.model = WhisperForConditionalGeneration.from_pretrained(model_name)
            log_info("✓ Model downloaded. Converting to device...")
            self.model = self.model.to(self.device)
            self.model.eval()
            log_info(f"✓ Model {model_name} loaded successfully on {self.device}!")
        except Exception as e:
            log_error(f"Failed to load model {model_name}: {e}")
            self.processor = None
            self.model = None
    
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
        if not self.processor or not self.model:
            raise ValueError("STT pipeline not initialized. Model loading failed.")
        
        try:
            import os
            
            # Verify file exists
            if not os.path.exists(audio_path):
                raise FileNotFoundError(f"Audio file not found: {audio_path}")
            
            # Check file size
            file_size = os.path.getsize(audio_path)
            if file_size == 0:
                raise ValueError("Audio file is empty (0 bytes)")
            
            log_info(f"Transcribing audio: {audio_path} ({file_size} bytes)")
            
            # Load and preprocess audio with librosa
            log_info("Loading audio with librosa...")
            audio, sr = librosa.load(audio_path, sr=16000, mono=True)
            
            # Check audio duration
            duration = len(audio) / sr
            if duration < 0.5:
                log_info(f"Warning: Audio too short ({duration:.2f}s). May have poor transcription.")
            
            log_info(f"Audio loaded: {duration:.2f}s at 16kHz, mono")
            
            # Prepare audio for model
            log_info("Processing audio for model...")
            inputs = self.processor(audio, sampling_rate=16000, return_tensors="pt")
            
            # Move to device
            input_features = inputs.input_features.to(self.device)
            
            # Transcribe
            log_info("Running transcription...")
            with torch.no_grad():
                predicted_ids = self.model.generate(input_features)
            
            # Decode
            text = self.processor.batch_decode(predicted_ids, skip_special_tokens=True)[0]
            text = text.strip()
            
            if not text:
                log_info("Warning: Transcription returned empty result. Audio may be silent or unclear.")
            else:
                log_info(f"Transcription complete: {text[:100]}...")
            
            return text
            
        except FileNotFoundError as e:
            log_error(f"Audio file error: {e}")
            raise ValueError(f"Audio file error: {e}")
        except Exception as e:
            log_error(f"Transcription failed: {e}")
            raise ValueError(f"Transcription failed: {e}")
