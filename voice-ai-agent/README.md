# 🎤 Voice-Controlled AI Agent

A powerful AI agent that accepts voice commands and executes various tasks through an intuitive web interface. Build with Python, Gradio, Whisper, and OpenAI API.

## ✨ Features

- **🎙️ Voice Input**: Speak commands via microphone or upload audio files
- **📝 Text Input**: Type commands as an alternative
- **🔊 Speech-to-Text**: Convert audio to text using OpenAI's Whisper model
- **🧠 Intent Understanding**: Classify user intent using OpenAI's GPT models
- **⚙️ Multi-Tool Support**: Code generation, file creation, text summarization, and chat via OpenAI
- **🎨 Clean UI**: Beautiful Gradio interface with real-time results
- **⚡ Cloud-Powered**: Uses OpenAI API for professional-grade responses

## 🏗️ Architecture

```
┌─────────────┐
│  Audio/Text │
└──────┬──────┘
       │
       ▼
┌─────────────────────────────┐
│  Speech-to-Text (Whisper)   │  ← Converts audio → text
└──────┬──────────────────────┘
       │
       ▼
┌─────────────────────────────┐
│ Intent Classification (LLM) │  ← Classifies: code/file/summarize/chat
└──────┬──────────────────────┘
       │
       ▼
┌─────────────────────────────┐
│   Tool Router & Executor    │  ← Routes to appropriate tool
└──────┬──────────────────────┘
       │
       ▼
   ┌───┴─────────────────────────────┐
   │                                 │
   ▼                                 ▼
┌──────────────────┐     ┌──────────────────────┐
│ Code Generator   │     │ File Creator / Chat  │
│ Summarizer       │     │ (via Ollama)         │
└────────┬─────────┘     └────────┬─────────────┘
         │                        │
         └────────────┬───────────┘
                      ▼
              ┌─────────────────────┐
              │  Output Display UI  │
              └─────────────────────┘
```

## 🚀 Quick Start

### Prerequisites

- **Python 3.8+**
- **OpenAI API Key** - Get one free at [platform.openai.com](https://platform.openai.com/api-keys)
- **GPU optional** (for faster audio processing)

### 1. Get OpenAI API Key

Sign up and get your free API key from [platform.openai.com/api-keys](https://platform.openai.com/api-keys)

### 2. Set Environment Variable

**Windows (PowerShell):**
```powershell
$env:OPENAI_API_KEY = "your_api_key_here"
```

**Mac/Linux:**
```bash
export OPENAI_API_KEY="your_api_key_here"
```

Or create a `.env` file (copy from `.env.example`):
```bash
OPENAI_API_KEY=your_api_key_here
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the Application

```bash
python app/main.py
```

Open your browser to: **http://127.0.0.1:7860**

## 📚 Usage Examples

### Example 1: Generate Python Code
**Voice Input**: *"Create a Python file with a function that calculates fibonacci numbers"*

**Result**:
- Intent: `write_code`
- File created: `output/generated_code.py`
- Code preview displayed in UI

### Example 2: Create an Empty File
**Voice Input**: *"Create a new file called shopping_list.txt"*

**Result**:
- Intent: `create_file`
- File created: `output/shopping_list.txt`

### Example 3: Summarize Text
**Text Input**: *"Summarize: Machine learning is..."*

**Result**:
- Intent: `summarize`
- 2-3 sentence summary displayed

### Example 4: General Chat
**Voice Input**: *"What is artificial intelligence?"*

**Result**:
- Intent: `chat`
- AI response displayed

## 📁 Project Structure

```
voice-ai-agent/
│
├── app/
│   ├── main.py              # Entry point with pre-flight checks
│   ├── ui.py                # Gradio interface
│
├── core/
│   ├── stt.py               # Speech-to-text (Whisper)
│   ├── intent.py            # Intent classification (Ollama)
│   ├── orchestrator.py       # Pipeline controller
│
├── tools/
│   ├── file_tool.py         # File creation (with safety)
│   ├── code_tool.py         # Code generation (Ollama)
│   ├── summary_tool.py      # Text summarization (Ollama)
│   ├── chat_tool.py         # General chat (Ollama)
│
├── utils/
│   ├── parser.py            # Safe JSON parsing
│   ├── logger.py            # Logging utilities
│
├── output/                  # 🔐 SAFE directory for generated files
├── requirements.txt         # Python dependencies
├── README.md               # This file
└── .gitignore             # Git ignore rules
```

## ⚙️ Configuration

### Changing OpenAI Model

Edit `core/intent.py`, `tools/code_tool.py`, etc.:

```python
classifier = IntentClassifier(model_name="gpt-4")  # Use GPT-4 (best quality)
classifier = IntentClassifier(model_name="gpt-3.5-turbo")  # Use GPT-3.5 (cheaper)
```

Available models:
- `gpt-3.5-turbo` - Fast, affordable, good quality (recommended)
- `gpt-4` - Premium quality, slower, more expensive
- `gpt-4-turbo-preview` - Better than 3.5, cheaper than 4

### Changing STT Model

Edit `core/stt.py`:

```python
stt = SpeechToText(model_name="openai/whisper-medium")  # Use larger model (more accurate)
stt = SpeechToText(model_name="openai/whisper-base")    # Use smaller model (faster)
```

Models: `whisper-small`, `whisper-base`, `whisper-medium`, `whisper-large`

## 🔐 Safety Features

✅ **Path Traversal Prevention**: Sanitizes filenames to prevent `../` attacks

✅ **Isolated Output Directory**: All generated files restricted to `/output` folder

✅ **Safe JSON Parsing**: Handles malformed LLM responses gracefully

✅ **Error Handling**: Catches exceptions and returns user-friendly error messages

## 🛠️ Troubleshooting

### "OPENAI_API_KEY not set" Error
```bash
# Check if variable is set
echo %OPENAI_API_KEY%  # Windows
echo $OPENAI_API_KEY   # Mac/Linux

# If empty, set it:
$env:OPENAI_API_KEY = "your_key_here"  # Windows PowerShell
export OPENAI_API_KEY="your_key_here"  # Mac/Linux
```

### "Invalid API Key" Error
- Make sure you copied the entire key from https://platform.openai.com/api-keys
- Check for extra spaces
- Verify the key is active in your OpenAI account

### Audio input not working
```bash
# Install soundfile
pip install soundfile

# Check microphone permissions (macOS/Linux)
# Windows: Check audio device in Sound Settings
```

### Slow transcription/responses
- Using local Whisper model? It processes on CPU/GPU
- OpenAI API calls depend on network speed
- Try using smaller Whisper model: `whisper-base` or `whisper-small`

### Rate limit or "Quota exceeded"
- Check your usage at https://platform.openai.com/account/billing/overview
- You may have hit your usage limit
- Add a payment method or increase budget limits

## 📖 API Reference

### Orchestrator

```python
from core.orchestrator import VoiceAIOrchestrator

orchestrator = VoiceAIOrchestrator()

# Process audio file
result = orchestrator.process_audio("audio.wav")
# Returns: {
#   "success": True,
#   "transcription": "...",
#   "intent": "write_code",
#   "action_result": "..."
# }

# Process text directly
result = orchestrator.process_text("Create a Python file")
```

### Individual Tools

```python
from tools.code_tool import CodeGenerator
from tools.summary_tool import TextSummarizer
from tools.chat_tool import ChatBot

code_gen = CodeGenerator()
code_gen.generate_and_save_code("Make a hello world", "hello.py")

summarizer = TextSummarizer()
summary = summarizer.summarize("Long text...")

chatbot = ChatBot()
response = chatbot.chat("What is AI?")
```

## 🎯 Future Enhancements

- [ ] Multi-language support
- [ ] Web search capability
- [ ] Email/Slack integration
- [ ] Custom tool creation
- [ ] Voice response feedback
- [ ] Conversation history
- [ ] Advanced intent fine-tuning

## 📝 License

MIT License - Feel free to use and modify for your projects!

## 🤝 Contributing

Found a bug? Have a feature idea? Feel free to modify and improve!

## 📧 Support

For issues with:
- **OpenAI API**: Visit [platform.openai.com/docs](https://platform.openai.com/docs/api-reference)
- **OpenAI Status**: Check [status.openai.com](https://status.openai.com)
- **Whisper**: Visit [openai/whisper](https://github.com/openai/whisper)
- **Gradio**: Visit [gradio.app](https://www.gradio.app)

For setup help, see [OPENAI_SETUP.md](OPENAI_SETUP.md)

---

**Made with ❤️ for AI enthusiasts**
