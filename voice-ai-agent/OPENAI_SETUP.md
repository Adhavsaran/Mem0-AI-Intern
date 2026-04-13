# OpenAI Setup Guide

## Converting from Ollama to OpenAI

This Voice AI Agent has been updated to use **OpenAI API** instead of local Ollama models. This means:

✅ **Advantages**:
- Better quality responses (GPT-3.5 Turbo or GPT-4)
- No need to install Ollama or manage local models
- Better code generation and intent classification
- Faster responses (no model loading time)

💰 **Costs**:
- OpenAI API usage is paid (cheap, but not free)
- Typical costs: $0.001 per 1000 tokens for GPT-3.5 Turbo

---

## Step 1: Get Your OpenAI API Key

1. Go to https://platform.openai.com/api-keys
2. Sign in with your OpenAI account (or create one)
3. Click "Create new secret key"
4. Copy your API key (keep it secret!)

---

## Step 2: Set the Environment Variable

### Option A: Set Temporarily (Windows PowerShell)
```powershell
$env:OPENAI_API_KEY = "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"
python app/main.py
```

### Option B: Set Temporarily (Windows Command Prompt)
```cmd
set OPENAI_API_KEY=your_api_key_here
python app/main.py
```

### Option C: Set Permanently (Windows)
1. Press `Win + X` → System
2. Click "Advanced system settings"
3. Click "Environment Variables"
4. Click "New" under User variables
5. **Variable name**: `OPENAI_API_KEY`
6. **Variable value**: Your API key
7. Click OK, then restart terminal

### Option D: Use .env File
1. Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```
2. Edit `.env` and add your API key:
   ```
   OPENAI_API_KEY=sk-...your_key...
   ```
3. The app will automatically load it (python-dotenv installed)

### Option E: Set (Mac/Linux)
```bash
export OPENAI_API_KEY="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"
python app/main.py
```

Or add to `~/.bash_profile` or `~/.zshrc`:
```bash
export OPENAI_API_KEY="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"
```

---

## Step 3: Verify Setup

Run the setup check:
```bash
python setup_check.py
```

You should see:
```
✓ PASS: OpenAI API configured
✓ PASS: All checks passed
```

---

## Step 4: Launch the App

```bash
python app/main.py
```

Open your browser to: http://127.0.0.1:7860

---

## Configuration Options

### Change the Model

Edit `core/intent.py`, `tools/code_tool.py`, etc.:

```python
# Use GPT-4 for better quality (more expensive)
classifier = IntentClassifier(model_name="gpt-4")

# Use GPT-3.5 Turbo for cheaper costs (recommended)
classifier = IntentClassifier(model_name="gpt-3.5-turbo")
```

Available models:
- `gpt-3.5-turbo` - Fast, cheap, good quality (recommended)
- `gpt-4` - Best quality, more expensive, slower
- `gpt-4-turbo-preview` - Good balance of speed and quality

---

## Monitoring Costs

Track your OpenAI usage and costs:
1. Go to https://platform.openai.com/account/billing/overview
2. View usage details
3. Set budget limits to avoid surprises

### Rough Pricing
- **GPT-3.5 Turbo**: $0.0015 per 1K input tokens, $0.002 per 1K output tokens
- **GPT-4**: $0.03 per 1K input tokens, $0.06 per 1K output tokens

For typical voice commands (100-200 tokens), expect:
- GPT-3.5: $0.0003 - $0.0005 per request
- GPT-4: $0.003 - $0.006 per request

---

## Troubleshooting

### "OPENAI_API_KEY not set"
```bash
# Check if variable is set
echo %OPENAI_API_KEY%  # Windows
echo $OPENAI_API_KEY   # Mac/Linux

# If empty, follow steps above to set it
```

### "Invalid API key"
- Make sure you copied the entire key
- Check for extra spaces
- Verify the key is active at https://platform.openai.com/api-keys

### "Rate limit exceeded"
- You're making too many requests
- Wait a few seconds before making new requests
- Consider using a cheaper model

### "Quota exceeded"
- You've used your monthly quota
- Check billing at https://platform.openai.com/account/billing/overview
- Add billing method or increase budget

---

## Reverting to Ollama (Optional)

If you want to go back to local Ollama:

1. Checkout the previous version:
   ```bash
   git log --oneline
   git checkout <commit_hash>  # Before OpenAI changes
   ```

2. Or manually revert files using git

---

## Support

- **OpenAI Docs**: https://platform.openai.com/docs/api-reference
- **API Status**: https://status.openai.com
- **Pricing Calculator**: https://openai.com/pricing/

---

**You're all set! Enjoy your voice-controlled AI agent powered by OpenAI.** 🚀
