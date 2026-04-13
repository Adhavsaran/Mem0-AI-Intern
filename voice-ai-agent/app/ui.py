"""
Gradio UI for Voice AI Agent.
Provides a clean interface for audio input, processing, and result display.
"""
import gradio as gr
import os
from core.orchestrator import VoiceAIOrchestrator
from utils.logger import log_info


class VoiceAIUI:
    """Gradio interface for Voice AI Agent."""
    
    def __init__(self):
        """Initialize UI and orchestrator."""
        self.orchestrator = VoiceAIOrchestrator()
        log_info("UI initialized")
    
    def process_audio_input(self, audio, text_input):
        """
        Process audio or text input.
        
        Args:
            audio: Tuple of (sample_rate, audio_data) from Gradio
            text_input: Text input from user
        
        Returns:
            Tuple of (transcription, intent, result)
        """
        try:
            # Handle audio input
            if audio is not None:
                log_info("Audio input received")
                import numpy as np
                import soundfile as sf
                
                sample_rate, audio_data = audio
                log_info(f"Audio format: sample_rate={sample_rate}, shape={audio_data.shape}, dtype={audio_data.dtype}")
                
                # Convert to numpy float32
                audio_data = np.array(audio_data, dtype=np.float32)
                
                # Handle stereo -> mono conversion at normalization
                if audio_data.ndim > 1:
                    # If stereo, take average of channels
                    audio_data = np.mean(audio_data, axis=1)
                    log_info(f"Converted stereo to mono: {audio_data.shape}")
                
                # Normalize to [-1, 1]
                max_val = np.max(np.abs(audio_data))
                if max_val > 0:
                    audio_data = audio_data / max_val
                
                # Save as WAV file (librosa in STT will handle resampling)
                temp_path = "temp_audio.wav"
                sf.write(temp_path, audio_data, sample_rate)
                log_info(f"Audio saved to {temp_path}")
                
                # Process audio
                result = self.orchestrator.process_audio(temp_path)
                
                # Clean up
                if os.path.exists(temp_path):
                    os.remove(temp_path)
                
                transcription = result.get("transcription", "")
                intent = result.get("intent", "")
                action_result = result.get("action_result", "")
                
                return transcription, intent, action_result
            
            # Handle text input
            elif text_input.strip():
                log_info("Text input received")
                result = self.orchestrator.process_text(text_input)
                
                transcription = result.get("transcription", "")
                intent = result.get("intent", "")
                action_result = result.get("action_result", "")
                
                return transcription, intent, action_result
            
            else:
                return "", "Error", "Please provide audio or text input"
        
        except Exception as e:
            log_info(f"Error processing input: {e}")
            return "", "Error", f"Error: {e}"
    
    def launch(self, share=False, server_name="127.0.0.1", server_port=7860):
        """
        Launch Gradio interface.
        
        Args:
            share: Whether to share the interface
            server_name: Server hostname
            server_port: Server port
        """
        with gr.Blocks(
            title="Voice AI Agent",
            theme=gr.themes.Soft()
        ) as demo:
            gr.Markdown(
                """
                # 🎤 Voice-Controlled AI Agent
                
                **Process audio or text input through a local AI pipeline:**
                - 🎙️ Speech-to-Text (via Whisper)
                - 🧠 Intent Classification (via OpenAi API)
                - ⚙️ Tool Execution (code generation, file creation, etc.)
                
                ---
                """
            )
            
            with gr.Row():
                with gr.Column(scale=1):
                    gr.Markdown("### Input")
                    
                    # Audio input
                    audio_input = gr.Audio(
                        label="🎙️ Microphone Input",
                        type="numpy",
                        sources=["microphone", "upload"]
                    )
                    
                    # Text input
                    text_input = gr.Textbox(
                        label="📝 Or Type Your Request",
                        placeholder="e.g., 'Create a Python file with a hello world function'",
                        lines=3
                    )
                    
                    # Process button
                    process_btn = gr.Button(
                        "🚀 Process",
                        variant="primary",
                        size="lg"
                    )
                
                with gr.Column(scale=1):
                    gr.Markdown("### Results")
                    
                    # Transcription output
                    transcription_output = gr.Textbox(
                        label="📄 Transcription",
                        interactive=False,
                        lines=3
                    )
                    
                    # Intent output
                    intent_output = gr.Textbox(
                        label="🧠 Detected Intent",
                        interactive=False
                    )
                    
                    # Action result output
                    result_output = gr.Textbox(
                        label="✨ Action Result",
                        interactive=False,
                        lines=5
                    )
            
            # Connect button to processing function
            process_btn.click(
                fn=self.process_audio_input,
                inputs=[audio_input, text_input],
                outputs=[transcription_output, intent_output, result_output]
            )
            
            # Example usage
            gr.Markdown(
                """
                ---
                ### Example Commands
                - "Create a Python file with a fibonacci function"
                - "Summarize machine learning concepts"
                - "Where are generated files saved?"
                
                ### ⚠️ Safety Note
                All generated files are saved to the `/output` folder only.
                """
            )
        
        demo.launch(
            share=share,
            server_name=server_name,
            server_port=server_port
        )


def create_ui() -> VoiceAIUI:
    """Factory function to create UI instance."""
    return VoiceAIUI()


if __name__ == "__main__":
    ui = create_ui()
    ui.launch()
