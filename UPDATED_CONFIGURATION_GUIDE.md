# Updated Configuration Guide - AgentJira

**Last Updated:** 2025-11-19

---

## Quick Start

After running `setup.bat`, you need to configure two `.env` files:

### 1. Jira Tool Server Configuration

**File:** `jira-tool-server/.env`

```ini
# Jira Configuration
JIRA_URL=https://your-domain.atlassian.net
JIRA_EMAIL=your-email@example.com
JIRA_API_TOKEN=your-jira-api-token
JIRA_PROJECT=YOUR_PROJECT_KEY

# Optional: Custom field ID for story points (default: customfield_10016)
# Find your field ID: Jira Settings > Issues > Custom Fields > Story Points > View
# JIRA_STORY_POINTS_FIELD=customfield_10016

# Server Configuration
FLASK_PORT=5001
FLASK_DEBUG=False
```

**How to get your Jira credentials:**

1. **JIRA_URL:** Your Jira instance URL (e.g., `https://mycompany.atlassian.net`)
2. **JIRA_EMAIL:** Your Jira account email
3. **JIRA_API_TOKEN:** 
   - Go to https://id.atlassian.com/manage-profile/security/api-tokens
   - Click "Create API token"
   - Copy the token
4. **JIRA_PROJECT:** Your project key (e.g., `PROJ`, `DEV`, `TEAM`)
   - Find it in Jira: Project Settings > Details > Key

**How to find your Story Points custom field ID:**

1. Go to Jira Settings (⚙️) > Issues > Custom Fields
2. Find "Story Points" field
3. Click "..." > View
4. Look at the URL: `customfield_XXXXX` is your field ID
5. Add to .env: `JIRA_STORY_POINTS_FIELD=customfield_XXXXX`

---

### 2. Agent Server Configuration

**File:** `agent-server/.env`

```ini
# LangSmith Configuration
LANGCHAIN_TRACING_V2=true
LANGCHAIN_ENDPOINT=https://api.smith.langchain.com
LANGCHAIN_API_KEY=your-langsmith-api-key
LANGCHAIN_PROJECT=Jira-Cheer-Dashboard

# LLM Provider Configuration
# Options: ollama, groq, together, gemini, replicate
LLM_PROVIDER=ollama

# Ollama Configuration (default - runs locally)
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.1

# Groq Configuration (uncomment if using Groq)
# GROQ_API_KEY=your-groq-api-key-here
# GROQ_MODEL=llama-3.1-70b-versatile

# Together AI Configuration (uncomment if using Together)
# TOGETHER_API_KEY=your-together-api-key-here
# TOGETHER_MODEL=meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo

# Gemini Configuration (uncomment if using Gemini)
# GOOGLE_API_KEY=your-gemini-api-key
# GEMINI_MODEL=gemini-1.5-pro

# Replicate Configuration (uncomment if using Replicate)
# REPLICATE_API_TOKEN=your-replicate-token-here
# REPLICATE_MODEL=meta/meta-llama-3.1-405b-instruct

# Jira Tool Server Configuration
JIRA_TOOL_SERVER_URL=http://localhost:5001

# Server Configuration
FLASK_PORT=5002
# WARNING: Set to False in production to avoid exposing sensitive information
FLASK_DEBUG=False
```

**LLM Provider Options:**

1. **Ollama (Default - Free, Local)**
   - Install Ollama: https://ollama.ai
   - Run: `ollama pull llama3.1`
   - No API key needed!

2. **Groq (Fast, Cloud)**
   - Get API key: https://console.groq.com
   - Set `LLM_PROVIDER=groq`
   - Add `GROQ_API_KEY`

3. **Together AI (Cloud)**
   - Get API key: https://api.together.xyz
   - Set `LLM_PROVIDER=together`
   - Add `TOGETHER_API_KEY`

4. **Google Gemini (Cloud)**
   - Get API key: https://makersuite.google.com/app/apikey
   - Set `LLM_PROVIDER=gemini`
   - Add `GOOGLE_API_KEY`

**LangSmith Setup:**

1. Create account: https://smith.langchain.com
2. Get API key: Settings > API Keys
3. Add to .env: `LANGCHAIN_API_KEY=your-key`

---

## Configuration Changes from Previous Version

### What Changed?

1. **JIRA_PROJECT is now in .env** (was hardcoded in jira_client.py)
2. **JIRA_STORY_POINTS_FIELD is configurable** (was hardcoded)
3. **LLM_PROVIDER defaults to 'ollama'** (was 'groq')
4. **FLASK_DEBUG defaults to False** (was True)

### Migration Steps

If you have an existing installation:

```bash
# 1. Add to jira-tool-server/.env
JIRA_PROJECT=YOUR_PROJECT_KEY

# 2. (Optional) If your story points field is different
JIRA_STORY_POINTS_FIELD=customfield_XXXXX

# 3. (Recommended) Update debug setting in both .env files
FLASK_DEBUG=False
```

---

## Environment Variables Reference

### Jira Tool Server

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| JIRA_URL | ✅ Yes | - | Your Jira instance URL |
| JIRA_EMAIL | ✅ Yes | - | Your Jira account email |
| JIRA_API_TOKEN | ✅ Yes | - | Jira API token |
| JIRA_PROJECT | ✅ Yes | - | Jira project key |
| JIRA_STORY_POINTS_FIELD | ❌ No | customfield_10016 | Custom field ID for story points |
| FLASK_PORT | ❌ No | 5001 | Server port |
| FLASK_DEBUG | ❌ No | False | Debug mode (set False for production) |

### Agent Server

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| LANGCHAIN_TRACING_V2 | ❌ No | false | Enable LangSmith tracing |
| LANGCHAIN_API_KEY | ✅ Yes | - | LangSmith API key |
| LANGCHAIN_PROJECT | ❌ No | Jira-Cheer-Dashboard | LangSmith project name |
| LLM_PROVIDER | ❌ No | ollama | LLM provider (ollama/groq/together/gemini/replicate) |
| OLLAMA_BASE_URL | ❌ No | http://localhost:11434 | Ollama server URL |
| OLLAMA_MODEL | ❌ No | llama3.1 | Ollama model name |
| GROQ_API_KEY | Conditional | - | Required if LLM_PROVIDER=groq |
| TOGETHER_API_KEY | Conditional | - | Required if LLM_PROVIDER=together |
| GOOGLE_API_KEY | Conditional | - | Required if LLM_PROVIDER=gemini |
| REPLICATE_API_TOKEN | Conditional | - | Required if LLM_PROVIDER=replicate |
| JIRA_TOOL_SERVER_URL | ❌ No | http://localhost:5001 | Jira Tool Server URL |
| FLASK_PORT | ❌ No | 5002 | Server port |
| FLASK_DEBUG | ❌ No | False | Debug mode (set False for production) |

---

## Troubleshooting

### "Missing required environment variables: JIRA_PROJECT"

**Solution:** Add `JIRA_PROJECT=YOUR_KEY` to `jira-tool-server/.env`

### "Story points not showing correctly"

**Solution:** Find your custom field ID and add to .env:
```ini
JIRA_STORY_POINTS_FIELD=customfield_XXXXX
```

### "LLM provider not working"

**Solution:** Check that you've set the correct API key for your provider:
- Ollama: No API key needed, just install and run
- Groq: Set `GROQ_API_KEY`
- Together: Set `TOGETHER_API_KEY`
- Gemini: Set `GOOGLE_API_KEY`

---

## Security Best Practices

1. ✅ **Never commit .env files** - They're in .gitignore
2. ✅ **Set FLASK_DEBUG=False in production**
3. ✅ **Rotate API tokens regularly**
4. ✅ **Use environment-specific .env files**
5. ✅ **Restrict CORS in production** (requires code changes)

---

## Next Steps

After configuration:

1. Start the servers (see setup.bat output for commands)
2. Open http://localhost:3000
3. Test the dashboard
4. Check LangSmith for traces (if enabled)

For more details, see:
- `README.md` - Main documentation
- `LANGSMITH_SETUP.md` - LangSmith configuration
- `CRITICAL_FIXES_APPLIED.md` - Recent changes

