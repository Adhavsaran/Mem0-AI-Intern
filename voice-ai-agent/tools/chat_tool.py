"""
General chat tool using LM Studio local LLM.
"""
from config import get_lm_studio_client
from utils.logger import log_info, log_error


class ChatBot:
    """General chat interface using LM Studio local LLM."""
    
    def __init__(self, model_name: str = None):
        """
        Initialize chatbot.
        
        Args:
            model_name: LM Studio model name (auto-detected if None)
        """
        self.model_name = model_name
        self.client = get_lm_studio_client()
        log_info(f"ChatBot initialized with LM Studio")
    
    def chat(self, text: str) -> str:
        """
        Chat with the user.
        
        Args:
            text: User message
        
        Returns:
            Chat response
        """
        if not text.strip():
            return "I didn't catch that. Please say something."
        
        try:
            log_info("Processing chat message...")
            response = self._call_openai(text)
            log_info("Chat response generated")
            return response
        except Exception as e:
            log_error(f"Chat failed: {e}")
            return f"I'm having trouble responding right now. Error: {e}"
    
    def _call_openai(self, text: str) -> str:
        """
        Call LM Studio for chat.
        
        Args:
            text: User message
        
        Returns:
            Chat response
        """
        try:
            # Auto-detect model if not set
            if not self.model_name:
                models = self.client.models.list()
                if models.data:
                    self.model_name = models.data[0].id
                else:
                    raise ValueError("No models available in LM Studio")
            
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": "You are a helpful, friendly AI assistant."},
                    {"role": "user", "content": text}
                ],
                temperature=0.7,
                max_tokens=500
            )
            return response.choices[0].message.content
        except Exception as e:
            raise ValueError(f"LM Studio API call failed: {e}")

