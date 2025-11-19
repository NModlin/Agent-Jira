# Quick Reference Guide

Essential commands and information for the AI-Powered Jira Dashboard.

## 🚀 Quick Start

### With Ollama (Recommended - Free & Local)

```bash
# 1. Install Ollama
# Download from https://ollama.com

# 2. Run Ollama setup script
./start-with-ollama.sh  # Unix/Mac
start-with-ollama.bat   # Windows

# 3. Configure environment files
# Edit jira-tool-server/.env
# Edit agent-server/.env (LangSmith key only)

# 4. Start servers (3 separate terminals)
# Terminal 1:
cd jira-tool-server && source venv/bin/activate && python app.py

# Terminal 2:
cd agent-server && source venv/bin/activate && python app.py

# Terminal 3:
cd frontend && npm run dev

# 4. Open browser
# http://localhost:3000
```

## 📡 Server Ports

| Service | Port | URL |
|---------|------|-----|
| Frontend | 3000 | http://localhost:3000 |
| Agent Server | 5002 | http://localhost:5002 |
| Jira Tool Server | 5001 | http://localhost:5001 |
| Ollama | 11434 | http://localhost:11434 |

## 🔑 Required API Keys

### For Ollama (Recommended)
| Service | Where to Get | Environment Variable |
|---------|--------------|---------------------|
| Jira API Token | https://id.atlassian.com/manage-profile/security/api-tokens | `JIRA_API_TOKEN` |
| LangSmith API Key | https://smith.langchain.com → Settings → API Keys | `LANGCHAIN_API_KEY` |

### For Other LLM Providers
| Service | Where to Get | Environment Variable |
|---------|--------------|---------------------|
| Groq API Key | https://console.groq.com/keys | `GROQ_API_KEY` |
| Together AI Key | https://api.together.xyz/settings/api-keys | `TOGETHER_API_KEY` |
| Gemini API Key | https://makersuite.google.com/app/apikey | `GOOGLE_API_KEY` |

## 🧪 Testing Commands

### Ollama Commands
```bash
# Check if Ollama is running
curl http://localhost:11434

# List installed models
ollama list

# Download Llama 3.1
ollama pull llama3.1

# Test Ollama with LangChain
cd agent-server
source venv/bin/activate
python test_ollama.py

# Run a model interactively
ollama run llama3.1
```

### Health Checks
```bash
# Jira Tool Server
curl http://localhost:5001/health

# Agent Server
curl http://localhost:5002/health

# Ollama
curl http://localhost:11434
```

### Test Jira Tool Server
```bash
# Get bugs summary
curl -X POST http://localhost:5001/api/jira/get_bugs_summary

# Get tasks for user
curl -X POST http://localhost:5001/api/jira/get_tasks_for_user \
  -H "Content-Type: application/json" \
  -d '{"username": "Alice Smith"}'

# Get overall progress
curl -X POST http://localhost:5001/api/jira/get_overall_progress
```

### Test Agent Server
```bash
# Simple query
curl -X POST http://localhost:5002/api/agent/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "How many bugs do we have?"}'

# User-specific query
curl -X POST http://localhost:5002/api/agent/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "What is Alice Smith working on?"}'

# Progress query
curl -X POST http://localhost:5002/api/agent/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "Show me our team progress"}'
```

## 📝 Common Tasks

### Update Jira Project Key
```bash
# Edit jira-tool-server/jira_client.py
# Find and replace: YOUR_PROJECT → YOURKEY
```

### Restart Servers
```bash
# Stop with Ctrl+C in each terminal, then:

# Jira Tool Server
cd jira-tool-server
source venv/bin/activate
python app.py

# Agent Server
cd agent-server
source venv/bin/activate
python app.py

# Frontend
cd frontend
npm run dev
```

### View Logs
```bash
# Logs are in the terminal where each server is running
# For more detailed logs, set in .env:
FLASK_DEBUG=True
```

### Run Evaluations
```bash
cd agent-server
source venv/bin/activate
python evaluate.py
```

## 🔧 Configuration Files

### Jira Tool Server (.env)
```bash
JIRA_URL=https://your-domain.atlassian.net
JIRA_EMAIL=your-email@example.com
JIRA_API_TOKEN=your-token
FLASK_PORT=5001
FLASK_DEBUG=True
```

### Agent Server (.env)
```bash
LANGCHAIN_TRACING_V2=true
LANGCHAIN_ENDPOINT=https://api.smith.langchain.com
LANGCHAIN_API_KEY=your-langsmith-key
LANGCHAIN_PROJECT=Jira-Cheer-Dashboard
GOOGLE_API_KEY=your-gemini-key
JIRA_TOOL_SERVER_URL=http://localhost:5001
FLASK_PORT=5002
FLASK_DEBUG=True
```

## 🐛 Quick Troubleshooting

### Server won't start
```bash
# Check if port is in use
# Windows:
netstat -ano | findstr :5001

# Mac/Linux:
lsof -ti:5001

# Kill process if needed
# Windows:
taskkill /PID <PID> /F

# Mac/Linux:
kill -9 <PID>
```

### Dependencies issues
```bash
# Reinstall Python dependencies
cd jira-tool-server  # or agent-server
rm -rf venv
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Reinstall Node dependencies
cd frontend
rm -rf node_modules package-lock.json
npm install
```

### No traces in LangSmith
```bash
# Check environment variables
cd agent-server
cat .env | grep LANGCHAIN

# Should show:
# LANGCHAIN_TRACING_V2=true
# LANGCHAIN_API_KEY=your-key

# Restart agent server after changes
```

## 📚 Documentation Quick Links

- **Setup**: [README.md](README.md)
- **LangSmith**: [LANGSMITH_SETUP.md](LANGSMITH_SETUP.md)
- **Testing**: [TESTING_GUIDE.md](TESTING_GUIDE.md)
- **Issues**: [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
- **Summary**: [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)

## 💡 Example Queries

Try these in the frontend:

- "How many bugs do we have?"
- "What is Alice Smith working on?"
- "Show me our team progress"
- "How many critical bugs are there?"
- "What tasks does Bob Johnson have?"
- "How many tasks were completed this week?"

## 🎯 Key Files to Edit

### To add new Jira queries:
1. `jira-tool-server/jira_client.py` - Add method
2. `jira-tool-server/app.py` - Add endpoint
3. `agent-server/tools.py` - Add tool
4. Test and deploy

### To improve agent responses:
1. `agent-server/agent.py` - Edit `SYSTEM_PROMPT`
2. `agent-server/tools.py` - Improve tool descriptions
3. Test in LangSmith
4. Iterate

### To customize UI:
1. `frontend/src/components/JiraDashboard.jsx` - Logic
2. `frontend/src/components/JiraDashboard.css` - Styles
3. `frontend/src/index.css` - Global styles

## 🔄 Development Workflow

1. **Make changes** to code
2. **Restart** affected server
3. **Test** manually or with curl
4. **Check** LangSmith traces
5. **Iterate** based on results
6. **Document** changes

## 📊 Monitoring

### LangSmith Dashboard
- URL: https://smith.langchain.com
- View traces, create datasets, run evaluations

### Check System Health
```bash
# All services healthy?
curl http://localhost:5001/health && \
curl http://localhost:5002/health && \
curl http://localhost:3000

# If all return 200, system is healthy
```

## 🚨 Emergency Commands

### Stop all servers
```bash
# Press Ctrl+C in each terminal
# Or kill all Python/Node processes (use with caution!)
```

### Reset everything
```bash
# Delete all virtual environments and node_modules
rm -rf jira-tool-server/venv
rm -rf agent-server/venv
rm -rf frontend/node_modules

# Re-run setup
./setup.sh
```

### Clear caches
```bash
# Python cache
find . -type d -name __pycache__ -exec rm -rf {} +

# npm cache
cd frontend
npm cache clean --force
```

---

**Need more help?** See [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for detailed solutions.

