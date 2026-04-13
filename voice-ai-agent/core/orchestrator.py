"""
Orchestrator - main pipeline controller that connects all components.
"""
# Defer heavy imports - these will be imported when models are actually used
from tools.file_tool import create_file
from tools.code_tool import CodeGenerator
from tools.summary_tool import TextSummarizer
from tools.chat_tool import ChatBot
from utils.logger import log_info, log_error


class VoiceAIOrchestrator:
    """Main pipeline connecting STT → Intent → Tools → Output."""
    
    def __init__(self):
        """Initialize orchestrator (models load on first use for faster startup)."""
        log_info("Initializing Voice AI Orchestrator...")
        
        # Lazy load models - they'll be created on first use
        self.stt = None
        self.intent_classifier = None
        self.code_generator = None
        self.summarizer = None
        self.chatbot = None
        
        log_info("Orchestrator initialized (models will load on first use)")
    
    def _ensure_models_loaded(self):
        """Lazily load heavy models on first use."""
        if self.stt is None:
            log_info("⏳ Loading Speech-to-Text model on first use...")
            from core.stt import SpeechToText
            self.stt = SpeechToText()
        if self.intent_classifier is None:
            log_info("⏳ Loading Intent Classifier on first use...")
            from core.intent import IntentClassifier
            self.intent_classifier = IntentClassifier()
        if self.code_generator is None:
            self.code_generator = CodeGenerator()
        if self.summarizer is None:
            self.summarizer = TextSummarizer()
        if self.chatbot is None:
            self.chatbot = ChatBot()
    
    def process_audio(self, audio_path: str) -> dict:
        """
        Main processing pipeline: Audio → STT → Intent → Tool → Output.
        
        Args:
            audio_path: Path to audio file
        
        Returns:
            Dict with transcription, intent, and result
        """
        try:
            # Ensure models are loaded
            self._ensure_models_loaded()
            
            # Step 1: Transcribe audio
            log_info("Step 1: Transcribing audio...")
            transcription = self.stt.transcribe(audio_path)
            
            # Step 2: Classify intent
            log_info("Step 2: Classifying intent...")
            intent_data = self.intent_classifier.classify(transcription)
            intent = intent_data.get("intent", "chat")
            
            # Step 3: Execute appropriate tool
            log_info(f"Step 3: Executing {intent} tool...")
            result = self._execute_tool(intent, transcription, intent_data)
            
            # Step 4: Return results
            return {
                "success": True,
                "transcription": transcription,
                "intent": intent,
                "action_result": result
            }
        
        except Exception as e:
            log_error(f"Pipeline error: {e}")
            return {
                "success": False,
                "transcription": "Error: Could not transcribe audio",
                "intent": "error",
                "action_result": f"Error: {e}"
            }
    
    def process_text(self, text: str) -> dict:
        """
        Process text input directly (without STT).
        
        Args:
            text: User input text
        
        Returns:
            Dict with intent and result
        """
        try:
            # Ensure models are loaded
            self._ensure_models_loaded()
            
            # Skip STT, go straight to intent classification
            log_info("Processing text input...")
            intent_data = self.intent_classifier.classify(text)
            intent = intent_data.get("intent", "chat")
            
            # Execute tool
            result = self._execute_tool(intent, text, intent_data)
            
            return {
                "success": True,
                "transcription": text,
                "intent": intent,
                "action_result": result
            }
        
        except Exception as e:
            log_error(f"Pipeline error: {e}")
            return {
                "success": False,
                "transcription": text,
                "intent": "error",
                "action_result": f"Error: {e}"
            }
    
    def _execute_tool(self, intent: str, text: str, intent_data: dict) -> str:
        """
        Execute the appropriate tool based on intent.
        
        Args:
            intent: Detected intent
            text: Original text/transcription
            intent_data: Intent metadata
        
        Returns:
            Tool result
        """
        try:
            if intent == "create_file":
                filename = intent_data.get("filename", "output.txt")
                if not filename:
                    filename = "output.txt"
                result = create_file(filename)
                return result
            
            elif intent == "write_code":
                filename = intent_data.get("filename", "generated_code.py")
                if not filename:
                    filename = "generated_code.py"
                result = self.code_generator.generate_and_save_code(text, filename)
                return result
            
            elif intent == "summarize":
                result = self.summarizer.summarize(text)
                return f"📝 Summary:\n{result}"
            
            else:  # chat or unknown
                result = self.chatbot.chat(text)
                return f"💬 Response:\n{result}"
        
        except Exception as e:
            log_error(f"Tool execution failed: {e}")
            return f"❌ Tool execution failed: {e}"
