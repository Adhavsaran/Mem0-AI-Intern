"""
Text summarization tool using LM Studio local LLM.
"""
from config import get_lm_studio_client
from utils.logger import log_info, log_error


class TextSummarizer:
    """Summarize text using LM Studio local LLM."""
    
    def __init__(self, model_name: str = None):
        """
        Initialize summarizer.
        
        Args:
            model_name: LM Studio model name (auto-detected if None)
        """
        self.model_name = model_name
        self.client = get_lm_studio_client()
        log_info(f"TextSummarizer initialized with LM Studio")
    
    def summarize(self, text: str) -> str:
        """
        Summarize text.
        
        Args:
            text: Text to summarize
        
        Returns:
            Summary
        """
        if not text.strip():
            return "No text to summarize."
        
        try:
            log_info("Generating summary...")
            summary = self._call_openai(text)
            log_info("Summary generated")
            return summary
        except Exception as e:
            log_error(f"Summarization failed: {e}")
            return f"Error: Failed to summarize text - {e}"
    
    def _call_openai(self, text: str) -> str:
        """
        Call LM Studio to summarize.
        
        Args:
            text: Text to summarize
        
        Returns:
            Summary
        """
        prompt = f"""Please provide a concise summary of the following text in 2-3 sentences:

{text}

Summary:"""
        
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
                    {"role": "system", "content": "You are a helpful summarizer. Provide concise, clear summaries."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.5,
                max_tokens=200
            )
            return response.choices[0].message.content
        except Exception as e:
            raise ValueError(f"LM Studio API call failed: {e}")

