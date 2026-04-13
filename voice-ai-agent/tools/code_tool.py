"""
Code generation and saving tool using Ollama local LLM.
"""
from config import get_ollama_client
from tools.file_tool import create_file, get_output_dir
from utils.logger import log_info, log_error


class CodeGenerator:
    """Generate and save code using Ollama local LLM."""
    
    def __init__(self, model_name: str = None):
        """
        Initialize code generator.
        
        Args:
            model_name: Ollama model name (auto-detected if None)
        """
        self.model_name = model_name
        self.client = get_ollama_client()
        log_info(f"CodeGenerator initialized with Ollama")
    
    def generate_and_save_code(self, prompt: str, filename: str) -> str:
        """
        Generate code using OpenAI and save to file.
        
        Args:
            prompt: Code generation prompt
            filename: Output filename
        
        Returns:
            Preview of generated code
        
        Raises:
            ValueError: If generation or saving fails
        """
        try:
            # Generate code
            code = self._generate_code(prompt)
            
            # Save to file
            result_msg = create_file(filename, code)
            
            # Return preview
            preview = code[:500] + "..." if len(code) > 500 else code
            log_info(f"Code saved to {filename}")
            
            return f"{result_msg}\n\n--- Code Preview ---\n{preview}"
        except Exception as e:
            log_error(f"Code generation failed: {e}")
            raise ValueError(f"Code generation failed: {e}")
    
    def _generate_code(self, prompt: str) -> str:
        """
        Call OpenAI to generate code.
        
        Args:
            prompt: Code prompt
        
        Returns:
            Generated code
        """
        full_prompt = f"""You are a helpful code generator. Generate clean, well-commented code based on this request:

{prompt}

IMPORTANT: Return ONLY the code, no explanations or markdown formatting."""
        
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
                    {"role": "system", "content": "You are an expert code generator. Generate clean, professional code."},
                    {"role": "user", "content": full_prompt}
                ],
                temperature=0.7,
                max_tokens=2000
            )
            code = response.choices[0].message.content
            
            # Remove markdown code blocks if present
            if code.startswith("```"):
                code = code.split("```", 2)[1]
                if code.startswith(("python", "py", "java", "javascript", "js", "cpp", "c++", "csharp", "css", "html", "sql")):
                    code = code.split("\n", 1)[1]
            if code.endswith("```"):
                code = code.rsplit("```", 1)[0]
            
            return code.strip()
        except Exception as e:
            raise ValueError(f"LM Studio API call failed: {e}")

