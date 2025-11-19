# Ollama Setup Guide

This guide will help you set up Ollama to run Llama models locally for your Jira AI Dashboard.

## Why Ollama?

✅ **Free** - No API costs  
✅ **Private** - Data stays on your machine  
✅ **Fast** - No network latency  
✅ **Offline** - Works without internet  
✅ **Easy** - Simple installation and usage  

## Step 1: Install Ollama

### Windows

1. Download Ollama from https://ollama.com/download/windows
2. Run the installer
3. Ollama will start automatically

### Mac

```bash
# Download and install
curl -fsSL https://ollama.com/install.sh | sh

# Or use Homebrew
brew install ollama
```

### Linux

```bash
curl -fsSL https://ollama.com/install.sh | sh
```

## Step 2: Start Ollama

Ollama should start automatically after installation. If not:

```bash
# Start Ollama service
ollama serve
```

You should see:
```
Ollama is running on http://localhost:11434
```

## Step 3: Download a Llama Model

Choose a model based on your hardware:

### Recommended Models

**For 8GB+ RAM:**
```bash
ollama pull llama3.1
```
This downloads Llama 3.1 8B (4.7GB) - Good balance of speed and quality

**For 16GB+ RAM:**
```bash
ollama pull llama3.1:70b
```
This downloads Llama 3.1 70B (40GB) - Better quality, slower

**For 32GB+ RAM:**
```bash
ollama pull llama3.1:405b
```
This downloads Llama 3.1 405B (231GB) - Best quality, requires powerful hardware

**Lightweight option (4GB+ RAM):**
```bash
ollama pull llama3.2
```
This downloads Llama 3.2 3B (2GB) - Faster, less capable

### Verify Installation

```bash
# List installed models
ollama list

# Test the model
ollama run llama3.1
>>> Hello! How are you?
```

Type `/bye` to exit the test.

## Step 4: Configure Agent Server

1. **Update your `.env` file:**

```bash
cd agent-server
nano .env  # or use your favorite editor
```

2. **Set these values:**

```bash
# LLM Provider
LLM_PROVIDER=ollama

# Ollama Configuration
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.1
```

3. **Save and close**

## Step 5: Install Dependencies

```bash
cd agent-server

# Activate virtual environment
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate.bat  # Windows

# Install/update dependencies
pip install -r requirements.txt
```

## Step 6: Test It!

1. **Start Ollama** (if not already running):
```bash
ollama serve
```

2. **Start the Agent Server**:
```bash
cd agent-server
source venv/bin/activate
python app.py
```

3. **Test with curl**:
```bash
curl -X POST http://localhost:5002/api/agent/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "Hello, are you working?"}'
```

You should get a response from your local Llama model!

## Model Comparison

| Model | Size | RAM Needed | Speed | Quality | Best For |
|-------|------|------------|-------|---------|----------|
| llama3.2 | 2GB | 4GB+ | ⚡⚡⚡ | ⭐⭐ | Testing, low-end hardware |
| llama3.1 | 4.7GB | 8GB+ | ⚡⚡ | ⭐⭐⭐ | **Recommended** - Good balance |
| llama3.1:70b | 40GB | 16GB+ | ⚡ | ⭐⭐⭐⭐ | High quality responses |
| llama3.1:405b | 231GB | 32GB+ | 🐌 | ⭐⭐⭐⭐⭐ | Best quality, powerful hardware |

## Troubleshooting

### "Connection refused" error

**Problem:** Agent can't connect to Ollama

**Solution:**
```bash
# Check if Ollama is running
curl http://localhost:11434

# If not, start it
ollama serve
```

### "Model not found" error

**Problem:** Model not downloaded

**Solution:**
```bash
# Download the model
ollama pull llama3.1

# Verify it's installed
ollama list
```

### Slow responses

**Problem:** Model is too large for your hardware

**Solution:**
```bash
# Use a smaller model
ollama pull llama3.2

# Update .env
OLLAMA_MODEL=llama3.2
```

### Out of memory errors

**Problem:** Not enough RAM

**Solution:**
1. Close other applications
2. Use a smaller model (llama3.2)
3. Or use a cloud provider (Groq, Together AI)

## Advanced Configuration

### Change Model Temperature

Edit `agent-server/agent.py`:

```python
elif provider == 'ollama':
    from langchain_community.chat_models import ChatOllama
    return ChatOllama(
        base_url=Config.OLLAMA_BASE_URL,
        model=Config.OLLAMA_MODEL,
        temperature=0.3  # Lower = more focused, Higher = more creative
    )
```

### Use GPU Acceleration

Ollama automatically uses GPU if available. To verify:

```bash
# Check GPU usage while running
nvidia-smi  # For NVIDIA GPUs
```

### Run Ollama on a Different Port

```bash
# Set environment variable
export OLLAMA_HOST=0.0.0.0:11435

# Start Ollama
ollama serve

# Update .env
OLLAMA_BASE_URL=http://localhost:11435
```

## Switching Between Models

You can easily switch models without reinstalling:

```bash
# Download multiple models
ollama pull llama3.1
ollama pull llama3.2
ollama pull codellama

# Switch in .env
OLLAMA_MODEL=llama3.1  # or llama3.2, or codellama
```

## Comparing with Cloud Providers

| Feature | Ollama | Groq | Together AI | Gemini |
|---------|--------|------|-------------|--------|
| Cost | Free | Free tier | Paid | Free tier |
| Privacy | ✅ Local | ❌ Cloud | ❌ Cloud | ❌ Cloud |
| Speed | Depends on hardware | ⚡⚡⚡ Very fast | ⚡⚡ Fast | ⚡⚡ Fast |
| Setup | Medium | Easy | Easy | Easy |
| Offline | ✅ Yes | ❌ No | ❌ No | ❌ No |

## Next Steps

1. ✅ Ollama installed and running
2. ✅ Model downloaded
3. ✅ Agent configured
4. ✅ Test successful

Now you can:
- Start all three servers (Jira Tool Server, Agent Server, Frontend)
- Open http://localhost:3000
- Chat with your local Llama model!

## Resources

- **Ollama Website**: https://ollama.com
- **Model Library**: https://ollama.com/library
- **Ollama GitHub**: https://github.com/ollama/ollama
- **LangChain Ollama Docs**: https://python.langchain.com/docs/integrations/chat/ollama

---

**Need help?** See [TROUBLESHOOTING.md](TROUBLESHOOTING.md) or [QUICK_REFERENCE.md](QUICK_REFERENCE.md)

