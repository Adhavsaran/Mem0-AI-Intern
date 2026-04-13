# Quick Start Guide - Voice AI Agent with LM Studio

Get your voice-controlled AI agent running in 5 minutes!

## Prerequisites
- Python 3.8+ installed
- 8GB+ RAM (16GB recommended)

## Step 1: Download & Install LM Studio (2 minutes)

1. **Download**: https://lmstudio.ai
2. **Install** and open LM Studio
3. **Search** for a model (e.g., "Mistral", "Llama 2", "Neural Chat")
4. **Download** the model
5. **Load** the model (drag to chat or click Load button)
6. **Enable Server**: Settings → Developer → ✓ Start Local Server

**Verify**: You should see "Server is listening on http://localhost:1234"

## Step 2: Install Python Dependencies (1 minute)

```bash
cd "c:\Users\ADHAVSARAN\OneDrive\Desktop\Mem0 AI Intern\voice-ai-agent"
pip install -r requirements.txt
```

## Step 3: Verify Setup (1 minute)

```bash
python setup_check.py
```

**Expected Output:**
```
✅ PASS: Python Version
✅ PASS: LM Studio Connection
✅ PASS: Python Packages
✅ PASS: Project Structure

Result: 4/4 checks passed
```

If any checks fail, fix them before proceeding.

## Step 4: Launch the Agent (1 minute)

```bash
python app/main.py
```

**You should see:**
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

## Step 5: Open Web Interface (instant)

**Open your browser to:** http://127.0.0.1:7860

## Try It Out

### Via Audio
1. Click "Microphone Input"
2. Speak: "Create a Python file with a hello world function"
3. Click "🚀 Process"
4. View results!

### Via Text
1. Type in "Or Type Your Request" box
2. Example: "Write a Python script to count words in a file"
3. Click "🚀 Process"
4. View results!

## Example Commands

- "Create a Python file with a fibonacci function"
- "Write a REST API using Flask"
- "Summarize machine learning concepts"
- "What is the capital of France?"
- "Generate a function to merge two sorted lists"

## Troubleshooting

### "LM Studio is not running!"
- Open LM Studio
- Load a model
- Go to Settings → Developer
- Click "Start Local Server"
- Restart the agent

### "No models available in LM Studio"
- Load at least one model in LM Studio first
- Restart the agent

### "Slow responses"
- LM Studio performance depends on model size and GPU
- Try smaller models: Mistral 7B, Neural Chat 7B
- Enable GPU acceleration in LM Studio settings

### Audio input not working
- Grant microphone permissions
- Try uploading a WAV/MP3 file instead
- Check browser console for errors (F12)

### Python packages missing
Run: `pip install -r requirements.txt`

## Architecture

```
Your Voice/Text
    ↓
Gradio Interface (Web UI)
    ↓
┌─────────────────────────┐
│ STT: Whisper (Local)    │ ← Converts speech to text
│ Runs offline            │
└─────────────────────────┘
    ↓
Transcription
    ↓
┌─────────────────────────┐
│ LM Studio (Local)       │ ← Understands intent
│ Intent Classification   │
└─────────────────────────┘
    ↓
Intent Detected
    ↓
Tool Router
    ├─ Write Code
    ├─ Create File
    ├─ Summarize Text
    └─ Chat
    ↓
Results
    ↓
Display to User
```

## Privacy & Performance

✅ **100% Local**: All data stays on your machine
✅ **No Internet Required**: Works completely offline
✅ **Free**: No API charges or subscriptions
✅ **Fast**: Runs on CPU (faster with GPU)

## Next Steps

- 📖 Read [LM_STUDIO_SETUP.md](LM_STUDIO_SETUP.md) for detailed configuration
- 🔧 Explore [README.md](README.md) for full documentation
- 🛠️ Check [PROJECT_COMPLETION.md](PROJECT_COMPLETION.md) for architecture details

## Support

Check the project files:
- [LM_STUDIO_SETUP.md](LM_STUDIO_SETUP.md) - Detailed LM Studio configuration
- [README.md](README.md) - Complete documentation
- [CONVERSION_COMPLETE.md](CONVERSION_COMPLETE.md) - Architecture overview

---

**You're all set! Enjoy your local AI agent! 🚀**
