"""
Intent classification module using Ollama local LLM.
"""
from config import get_ollama_client, OLLAMA_BASE_URL
from utils.parser import safe_parse_json, sanitize_intent
from utils.logger import log_info, log_error


class IntentClassifier:
    """Classify user intent using Ollama local LLM."""
    
    def __init__(self, model_name: str = None):
        """
        Initialize the intent classifier.
        
        Args:
            model_name: Ollama model name (auto-detected if None)
        """
        self.model_name = model_name
        self.client = get_ollama_client()
        log_info(f"Ollama client initialized at: {OLLAMA_BASE_URL}")
    
    def check_ollama(self):
        """Check if Ollama is accessible."""
        try:
            self.client.models.list()
            log_info("Ollama is accessible")
            return True
        except Exception as e:
            log_error(f"Ollama check failed: {e}")
            return False
    
    def classify(self, text: str) -> dict:
        """
        Classify user intent from text.
        
        Args:
            text: User input text
        
        Returns:
            Dict with 'intent' and metadata (filename, language)
        """
        if not text.strip():
            return {"intent": "chat"}
        
        prompt = self._build_prompt(text)
        
        try:
            log_info(f"Classifying intent for: {text[:80]}...")
            response = self._call_ollama(prompt)
            intent_data = safe_parse_json(response)
            sanitized = sanitize_intent(intent_data)
            log_info(f"Intent classified as: {sanitized['intent']}")
            return sanitized
        except Exception as e:
            log_error(f"Intent classification failed: {e}")
            return {"intent": "chat"}
    
    def _build_prompt(self, text: str) -> str:
        """Build classification prompt."""
        return f"""You are an intent classifier. Analyze the user's request and classify it into one of these intents:
- create_file: User wants to create a file
- write_code: User wants to generate code
- summarize: User wants to summarize text
- chat: General conversation

User request: "{text}"

Extract if mentioned:
- filename (if creating/writing file)
- programming language (if writing code)

Respond with ONLY valid JSON, no other text:
{{
  "intent": "one of the four intents",
  "filename": "filename if mentioned or empty string",
  "language": "programming language if mentioned or empty string"
}}"""
    
    def _call_ollama(self, prompt: str) -> str:
        """
        Call Ollama local LLM with prompt.
        
        Args:
            prompt: Prompt text
        
        Returns:
            LLM response
        """
        try:
            # Get available models if not already set
            if not self.model_name:
                models = self.client.models.list()
                if models.data:
                    self.model_name = models.data[0].id
                else:
                    raise ValueError("No models available in Ollama")
            
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": "You are a JSON classifier. Always respond with valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=200
            )
            return response.choices[0].message.content
        except Exception as e:
            raise ValueError(f"Ollama API call failed: {e}")

