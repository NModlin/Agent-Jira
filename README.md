# AI-Powered Jira Dashboard with LangSmith Agent

An intelligent, agentic "Cheer Dashboard" that connects to Jira and uses LangChain/LangGraph with LangSmith for tracing, testing, and monitoring.

## 🏗️ Architecture

This project uses a decoupled three-part architecture:

```
┌─────────────────┐
│  React Frontend │ (Port 3000)
│   (Vite + React)│
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Agent Server   │ (Port 5002)
│  (LangChain +   │
│   LangGraph +   │
│   LangSmith)    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Jira Tool Server│ (Port 5001)
│  (Flask + Jira  │
│      API)       │
└────────┬────────┘
         │
         ▼
    ┌────────┐
    │  Jira  │
    └────────┘
```

### Components

1. **Frontend (React)**: Beautiful chat interface for user queries
2. **Agent Server (Python)**: LangChain/LangGraph agent with LLM (Ollama/Groq/Gemini) and LangSmith tracing
3. **Jira Tool Server (Python)**: Secure API that holds Jira credentials and executes JQL queries

## 🚀 Quick Start

### Prerequisites

- Python 3.9+
- Node.js 18+
- Jira account with API access
- **LLM Provider** (choose one):
  - **Ollama** (recommended) - Free, runs locally, private
  - Groq - Fast cloud API with free tier
  - Together AI - Cloud API
  - Google Gemini - Cloud API
- LangSmith account (free tier available)

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd AgentJira
```

### 2. Set Up Jira Tool Server

```bash
cd jira-tool-server
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your Jira credentials
# Edit jira_client.py to replace YOUR_PROJECT with your Jira project key
python app.py
```

### 3. Set Up Agent Server

```bash
cd ../agent-server
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your LangSmith and Gemini API keys
python app.py
```

### 4. Set Up Frontend

```bash
cd ../frontend
npm install
npm run dev
```

### 5. Open the Dashboard

Navigate to `http://localhost:3000` and start chatting!

## 📋 Detailed Setup Guides

- [Jira Tool Server Setup](jira-tool-server/README.md)
- [Agent Server Setup](agent-server/README.md)
- [Frontend Setup](frontend/README.md)

## 🔑 Getting API Keys

### Jira API Token

1. Go to https://id.atlassian.com/manage-profile/security/api-tokens
2. Click "Create API token"
3. Copy the token to your `jira-tool-server/.env` file

### Google Gemini API Key

1. Go to https://makersuite.google.com/app/apikey
2. Create a new API key
3. Copy the key to your `agent-server/.env` file

### LangSmith API Key

1. Go to https://smith.langchain.com
2. Create a new project (e.g., "Jira-Cheer-Dashboard")
3. Go to Settings → API Keys
4. Create a new API key
5. Copy the key to your `agent-server/.env` file

## 💬 Example Queries

Try asking the AI assistant:

- "How many bugs do we have?"
- "What is Alice Smith working on?"
- "Show me our team progress this week"
- "How many critical bugs are there?"
- "What tasks does Bob Johnson have?"

## 🧪 Testing with LangSmith

All agent interactions are automatically traced in LangSmith:

1. Go to https://smith.langchain.com
2. Select your project
3. View traces for each query
4. Inspect tool calls, arguments, and responses
5. Fork failing traces to create test cases
6. Refine prompts and re-run tests

## 📊 Project Structure

```
AgentJira/
├── jira-tool-server/      # Secure Jira API wrapper
│   ├── app.py             # Flask application
│   ├── jira_client.py     # Jira API client
│   ├── config.py          # Configuration
│   └── requirements.txt   # Python dependencies
│
├── agent-server/          # LangChain agent
│   ├── app.py             # Flask application
│   ├── agent.py           # LangGraph agent
│   ├── tools.py           # LangChain tools
│   ├── config.py          # Configuration
│   └── requirements.txt   # Python dependencies
│
└── frontend/              # React UI
    ├── src/
    │   ├── components/
    │   │   └── JiraDashboard.jsx
    │   ├── App.jsx
    │   └── main.jsx
    └── package.json
```

## 🔒 Security Notes

- Never commit `.env` files
- Keep API keys secure
- The Jira Tool Server should be behind authentication in production
- Consider rate limiting for production deployments

## 🎯 Roadmap

- [x] Phase 1: Jira Tool Server
- [x] Phase 2: LangChain Agent Server
- [x] Phase 3: React Frontend
- [ ] Phase 4: LangSmith Testing & Refinement
- [ ] Streaming responses with SSE
- [ ] Message history persistence
- [ ] Additional Jira tools (create issues, update status)
- [ ] Multi-user support with authentication

## 📝 License

MIT

## 🤝 Contributing

Contributions welcome! Please read the contributing guidelines first.

