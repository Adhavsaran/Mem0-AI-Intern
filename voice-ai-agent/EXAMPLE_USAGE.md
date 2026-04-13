# Voice AI Agent - Example Usage Guide

This document shows practical examples of using the Voice AI Agent for various tasks.

## 🎯 Scenario 1: Code Generation via Voice

### User Says (Voice Input):
*"Create a Python file with a function that reverses a string"*

### System Processing:

```
1. Audio → Transcription: "Create a Python file with a function that reverses a string"
2. STT → Intent Classification → Detected Intent: "write_code"
3. Extract metadata: 
   - filename: "reverse_string.py" (inferred from context)
   - language: "python"
4. Execute: CodeGenerator.generate_and_save_code()
5. Ollama generates code and saves to: output/reverse_string.py
6. UI displays generated code preview
```

### What Gets Returned to UI:
```
Transcription: "Create a Python file with a function that reverses a string"
Detected Intent: write_code
Action Result: 
✓ File created successfully: reverse_string.py

--- Code Preview ---
def reverse_string(s: str) -> str:
    """Reverse a string.
    
    Args:
        s: Input string
    
    Returns:
        Reversed string
    """
    return s[::-1]

# Test the function
if __name__ == "__main__":
    test_str = "Hello, World!"
    print(f"Original: {test_str}")
    print(f"Reversed: {reverse_string(test_str)}")
```

---

## 📝 Scenario 2: File Creation via Text

### User Types (Text Input):
"Create a new file called notes.md for my project todo list"

### System Processing:

```
1. Text input (no STT needed)
2. Text → Intent Classification → Detected Intent: "create_file"
3. Extract metadata:
   - filename: "notes.md"
4. Execute: create_file("notes.md", content="")
5. File created at: output/notes.md
```

### Result:
```
Transcription: Create a new file called notes.md for my project todo list
Detected Intent: create_file
Action Result:
✓ File created successfully: notes.md
```

---

## 📄 Scenario 3: Text Summarization

### User Says (Voice Input):
*"Summarize: Machine learning is a branch of artificial intelligence..."*

### System Processing:

```
1. Audio → Transcription: "Summarize: Machine learning is..."
2. Intent Classification → Detected Intent: "summarize"
3. Extract the text to summarize from transcription
4. Execute: TextSummarizer.summarize(text)
5. Ollama generates concise 2-3 sentence summary
```

### Result:
```
Transcription: Summarize: Machine learning is a branch of artificial intelligence...
Detected Intent: summarize
Action Result:
📝 Summary:
Machine learning is an AI field that enables systems to learn and improve from 
experience without explicit programming. It uses data and algorithms to build 
statistical models that improve performance on specific tasks.
```

---

## 💬 Scenario 4: General Chat

### User Says (Voice Input):
*"What is the difference between supervised and unsupervised learning?"*

### System Processing:

```
1. Audio → Transcription: "What is the difference between..."
2. Intent Classification → No match with specific intents → "chat"
3. Execute: ChatBot.chat(text)
4. Ollama generates conversational response
```

### Result:
```
Transcription: What is the difference between supervised and unsupervised learning?
Detected Intent: chat
Action Result:
💬 Response:
Supervised learning uses labeled data with input-output pairs to train models,
where the algorithm learns the mapping between inputs and expected outputs.
Unsupervised learning works with unlabeled data, discovering hidden patterns
or structures without predefined output labels. Common applications include
clustering and dimensionality reduction.
```

---

## 🔧 Programmatic Usage Examples

### Using the Orchestrator Directly

```python
from core.orchestrator import VoiceAIOrchestrator

# Initialize
orchestrator = VoiceAIOrchestrator()

# Process audio file
result = orchestrator.process_audio("path/to/audio.wav")
print(result)
# Output:
# {
#     "success": True,
#     "transcription": "Create a Python file...",
#     "intent": "write_code",
#     "action_result": "✓ File created successfully: generated_code.py"
# }

# Process text directly
result = orchestrator.process_text("Create a Python hello world file")
print(result["action_result"])
```

### Using Individual Components

```python
# Speech-to-Text
from core.stt import SpeechToText

stt = SpeechToText()
text = stt.transcribe("audio.wav")
print(f"Transcribed: {text}")

# Intent Classification
from core.intent import IntentClassifier

classifier = IntentClassifier()
intent = classifier.classify("Create a Python file")
print(f"Intent: {intent}")
# Output: {'intent': 'write_code', 'filename': '', 'language': 'python'}

# Code Generation
from tools.code_tool import CodeGenerator

gen = CodeGenerator()
result = gen.generate_and_save_code("Write a function to calculate factorial", "factorial.py")
print(result)

# Text Summarization
from tools.summary_tool import TextSummarizer

summarizer = TextSummarizer()
summary = summarizer.summarize("Long text to summarize...")
print(f"Summary: {summary}")

# Chat
from tools.chat_tool import ChatBot

bot = ChatBot()
response = bot.chat("What is Python?")
print(f"Response: {response}")

# File Operations
from tools.file_tool import create_file

create_file("my_notes.txt", "Important notes go here")
```

---

## 🎙️ Voice Command Examples

### Code Generation Examples
- "Create a JavaScript file with a function to validate emails"
- "Generate a Python script that reads a CSV file"
- "Write a function in Java that sorts an array using quicksort"

### File Creation Examples
- "Create a new todo list file"
- "Create a file called requirements.txt"
- "Make a new file named configuration.json"

### Summarization Examples
- "Summarize: The brain is composed of neurons..."
- "Give me a summary of this article: [paste text]"
- "Summarize the following: [long text]"

### General Chat Examples
- "What is machine learning?"
- "Explain how neural networks work"
- "How do I learn Python programming?"

---

## 🔐 Safety Guarantees in Action

### Safe File Operations

**Attempting to write outside /output:**
```python
create_file("../../../etc/passwd")
# ✓ Sanitized to: "etcpasswd" 
# ✓ Saved to: /output/etcpasswd
# ✓ No path traversal possible
```

**What gets prevented:**
```
❌ /home/user/sensitive.txt     → Blocked (outside /output)
❌ ../../../../private           → Blocked (path traversal attempt)
✅ generated_code.py            → Allowed (safe filename)
✅ my_notes.txt                  → Allowed (safe filename)
```

### Safe JSON Parsing

**Mallformed LLM response:**
```python
# LLM returns: "```json\n{"intent": "write_code"}\n```"
result = safe_parse_json(response)
# ✓ Extracted JSON from markdown code block
# ✓ Result: {"intent": "write_code"}

# LLM returns: "I think the intent is write_code right?"
result = safe_parse_json(response)
# ✓ Fallback to default: {"intent": "chat"}
```

---

## ⚡ Performance Tips

### For Faster Processing:

1. **Use smaller STT model** (faster transcription):
   ```python
   stt = SpeechToText(model_name="openai/whisper-base")
   ```

2. **Use faster LLM model** (faster intent/generation):
   ```python
   classifier = IntentClassifier(model_name="mistral")
   ```

3. **Run with GPU** (significantly faster):
   - Ensure CUDA is installed
   - PyTorch will auto-detect GPU

4. **Pre-load models** (avoid repeated initialization):
   ```python
   # Create once at startup
   orchestrator = VoiceAIOrchestrator()
   
   # Reuse for multiple requests
   result1 = orchestrator.process_text("request 1")
   result2 = orchestrator.process_text("request 2")  # Fast!
   ```

---

## 🐛 Troubleshooting Examples

### Issue: "Ollama not found"
```python
# Check installation
import subprocess
result = subprocess.run(["ollama", "--version"], capture_output=True)
# If fails: Download from https://ollama.ai
```

### Issue: Model taking too long
```python
# Check if model is loaded
orchestrator.intent_classifier._call_ollama("test")
# If timeout: Run "ollama list" to see loaded models
# Run "ollama pull llama3" to load model
```

### Issue: Audio not transcribing
```python
# Verify audio file format
import soundfile as sf
import numpy as np

# Read audio to check validity
try:
    data, sr = sf.read("audio.wav")
    print(f"Audio shape: {data.shape}, Sample rate: {sr}")
except Exception as e:
    print(f"Invalid audio: {e}")
```

---

## 📊 Output Formats

### Successful Process
```json
{
  "success": true,
  "transcription": "User's command text",
  "intent": "write_code|create_file|summarize|chat",
  "action_result": "Result from executing the tool"
}
```

### Failed Process
```json
{
  "success": false,
  "transcription": "Error message or partial transcription",
  "intent": "error",
  "action_result": "Error: [specific error message]"
}
```

---

## 🎓 Next Steps

1. **Deploy**: Run `python app/main.py` to launch the UI
2. **Extend**: Add custom tools in `tools/` folder
3. **Integrate**: Use as library in other projects
4. **Optimize**: Fine-tune models for your use case

---

**For more info, see README.md**
