# Voice-Controlled AI Agent (LM Studio Edition)

A local AI agent that converts speech to text using **Whisper (HuggingFace)** and understands intent using **LM Studio**.

## Architecture

```
Audio Input (Microphone/Upload)
        ↓
Whisper STT (HuggingFace) → Transcription
        ↓
Intent Classifier (LM Studio) → Intent Detection
        ↓
Tool Router → Write Code | Create File | Summarize | Chat
        ↓
Output Display
```

## Features

- 🎙️ **Local Speech Recognition**: Whisper model from HuggingFace (runs offline)
- 🧠 **Local Intent Understanding**: LM Studio for LLM inference (100% local)
- 🛠️ **Multi-Tool Support**: Code generation, file creation, text summarization, chat
- 🎨 **Web UI**: Built with Gradio for easy interaction
- 📁 **Safe File Handling**: All files saved to `/output` directory only

## Prerequisites

### 1. Download & Install LM Studio
- **Download**: https://lmstudio.ai
- **System Requirements**: 8GB+ RAM (16GB recommended), GPU optional
- **Setup**:
  1. Open LM Studio
  2. Search and download a model (e.g., `Mistral`, `Llama 2`, `Neural Chat`)
  3. Drag model to chat window or click "Load"
  4. Open Settings → Developer → Start Local Server
  5. Confirm server running on `http://localhost:1234/v1`

### 2. Install Python Dependencies

```bash
pip install -r requirements.txt
```

**Verify Installation**:
```bash
python setup_check.py
```

## Usage

### 1. Start LM Studio Local Server
- Open LM Studio
- Load a model
- Enable local server (Settings → Developer)
- Server binds to: `http://localhost:1234/v1`

### 2. Run the Agent

```bash
python app/main.py
```

**Expected Output**:
```
============================================================
🎤 Voice-Controlled AI Agent
   STT: Whisper (HuggingFace)
   LLM: LM Studio (Local)
============================================================

📋 Running pre-flight checks...
✓ LM Studio connected
✓ Gradio installed
✓ Transformers installed
✓ PyTorch installed
✓ Soundfile installed
✓ OpenAI library installed

✅ All checks passed!

🚀 Launching Gradio UI...
📍 Open browser to: http://127.0.0.1:7860
```

### 3. Open Web Interface
- Open browser: **http://127.0.0.1:7860**
- Interact via audio or text input

## Example Commands

### Audio Input
- Record: "Create a Python file with a fibonacci function"
- Record: "Summarize machine learning concepts"
- Record: "Write a REST API in Flask"

### Text Input
- "Generate a Python script for web scraping"
- "What is the capital of France?"
- "Create a file called utils.py with utility functions"

## Configuration

### LM Studio Endpoint (Optional)
Set custom LM Studio endpoint:

```bash
# Windows PowerShell
$env:LM_STUDIO_BASE_URL = "http://localhost:8080/v1"

# Mac/Linux
export LM_STUDIO_BASE_URL="http://localhost:8080/v1"
```

### Supported Models in LM Studio
- **Best for Speed**: Mistral 7B, Neural Chat 7B
- **Best for Quality**: Llama 2 70B, Mixtral 8x7B
- **Balanced**: Mistral 7B Instruct, Neural Chat 7B

## Project Structure

```
voice-ai-agent/
├── app/
│   ├── main.py           # Entry point
│   ├── ui.py             # Gradio interface
│   └── __init__.py
├── core/
│   ├── stt.py            # Whisper STT
│   ├── intent.py         # Intent classification (LM Studio)
│   ├── orchestrator.py    # Pipeline orchestration
│   └── __init__.py
├── tools/
│   ├── code_tool.py       # Code generation
│   ├── file_tool.py       # File creation
│   ├── summary_tool.py     # Text summarization
│   ├── chat_tool.py        # General chat
│   └── __init__.py
├── utils/
│   ├── logger.py          # Logging
│   ├── parser.py          # JSON parsing
│   └── __init__.py
├── output/                 # Generated files (safe sandbox)
├── config.py              # LM Studio configuration
├── requirements.txt       # Python dependencies
├── README.md              # This file
└── setup_check.py         # Verification script
```

## Troubleshooting

### Error: "LM Studio is not running!"
- Ensure LM Studio is open
- Ensure a model is loaded
- Verify local server enabled (Settings → Developer)
- Confirm endpoint: http://localhost:1234/v1

### Error: "No models available in LM Studio"
- Load a model in LM Studio first
- Restart the agent

### Slow Response Times
- LM Studio performance depends on model size and GPU
- Ensure sufficient RAM (16GB+ recommended)
- GPU acceleration in LM Studio improves speed significantly

### Audio Input Not Working
- Grant microphone permissions
- Check browser console for audio errors
- Try uploading WAV/MP3 file instead

### Import Errors
Run setup check:
```bash
python setup_check.py
```

Install missing packages:
```bash
pip install -r requirements.txt
```

## Safety Notes

- ✅ All generated files saved to `/output` folder only
- ✅ LM Studio runs fully local (no data sent to cloud)
- ✅ Whisper STT runs offline
- ✅ Complete privacy - your data never leaves your machine

## License

This project is provided as-is for educational purposes.

## Differences from OpenAI Edition

| Feature | This Version | OpenAI Version |
|---------|-------------|----------------|
| **LLM** | LM Studio (Local) | OpenAI API (Cloud) |
| **Cost** | Free (local) | Per-request charges |
| **Speed** | Depends on model | Usually faster |
| **Privacy** | Full (local only) | Data sent to OpenAI |
| **Internet** | Optional | Required |
| **Models** | Any HF/GGUF model | OpenAI only |
| **Setup** | LM Studio required | API key required |

## Next Steps

1. Download LM Studio: https://lmstudio.ai
2. Load a model in LM Studio
3. Start local server
4. Run: `python app/main.py`
5. Open: http://127.0.0.1:7860

Enjoy your local AI agent! 🚀
