# Getting Started Guide

Welcome! This guide will help you get the AI-Powered Jira Dashboard up and running in about 15 minutes.

## Prerequisites Checklist

Before you begin, make sure you have:

- [ ] Python 3.9 or higher installed
- [ ] Node.js 18 or higher installed
- [ ] A Jira account with admin access
- [ ] Access to create API tokens in Jira
- [ ] A Google account (for Gemini API)
- [ ] A LangSmith account (free tier is fine)

## Step-by-Step Setup

### Step 1: Get Your API Keys (5 minutes)

#### 1.1 Jira API Token

1. Go to https://id.atlassian.com/manage-profile/security/api-tokens
2. Click **"Create API token"**
3. Give it a name (e.g., "Jira Dashboard")
4. Click **"Create"**
5. **Copy the token** (you won't see it again!)
6. Save it somewhere safe

#### 1.2 Google Gemini API Key

1. Go to https://makersuite.google.com/app/apikey
2. Click **"Create API key"**
3. Select a Google Cloud project (or create a new one)
4. **Copy the API key**
5. Save it somewhere safe

#### 1.3 LangSmith API Key

1. Go to https://smith.langchain.com
2. Sign up for a free account
3. Create a new project:
   - Click **"New Project"**
   - Name it **"Jira-Cheer-Dashboard"**
   - Click **"Create"**
4. Go to **Settings** → **API Keys**
5. Click **"Create API Key"**
6. Give it a name (e.g., "Jira Dashboard Agent")
7. **Copy the API key**
8. Save it somewhere safe

### Step 2: Clone and Setup (3 minutes)

```bash
# Clone the repository
git clone <your-repo-url>
cd AgentJira

# Run the setup script
./setup.sh  # On Mac/Linux
setup.bat   # On Windows

# This will:
# - Create virtual environments
# - Install Python dependencies
# - Install Node.js dependencies
# - Create .env files from templates
```

### Step 3: Configure Environment Variables (3 minutes)

#### 3.1 Configure Jira Tool Server

```bash
# Open the file
cd jira-tool-server
nano .env  # or use your favorite editor

# Fill in these values:
JIRA_URL=https://your-domain.atlassian.net
JIRA_EMAIL=your-email@example.com
JIRA_API_TOKEN=your-jira-api-token-from-step-1.1

# Save and close
```

#### 3.2 Configure Agent Server

```bash
# Open the file
cd ../agent-server
nano .env  # or use your favorite editor

# Fill in these values:
LANGCHAIN_API_KEY=your-langsmith-key-from-step-1.3
GOOGLE_API_KEY=your-gemini-key-from-step-1.2

# Save and close
```

### Step 4: Update Jira Project Key (1 minute)

```bash
# Open the Jira client file
cd ../jira-tool-server
nano jira_client.py  # or use your favorite editor

# Find all instances of 'YOUR_PROJECT' and replace with your actual Jira project key
# For example, if your project key is 'TEAM', replace:
# 'project = YOUR_PROJECT' → 'project = TEAM'

# There are 3 places to update (in get_bugs_summary, get_tasks_for_user, get_overall_progress)

# Save and close
```

### Step 5: Start the Servers (2 minutes)

You'll need **three separate terminal windows**.

#### Terminal 1: Jira Tool Server

```bash
cd jira-tool-server

# Activate virtual environment
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate.bat  # Windows

# Start server
python app.py

# You should see:
# * Running on http://0.0.0.0:5001
```

#### Terminal 2: Agent Server

```bash
cd agent-server

# Activate virtual environment
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate.bat  # Windows

# Start server
python app.py

# You should see:
# * Running on http://0.0.0.0:5002
```

#### Terminal 3: Frontend

```bash
cd frontend

# Start dev server
npm run dev

# You should see:
# Local: http://localhost:3000
```

### Step 6: Test It Out! (1 minute)

1. Open your browser to **http://localhost:3000**
2. You should see the Jira Cheer Dashboard
3. Try one of the suggested queries:
   - "How many bugs do we have?"
   - "Show me our team progress"
4. The AI should respond with real data from your Jira!

### Step 7: Verify LangSmith Tracing (1 minute)

1. Go to https://smith.langchain.com
2. Select your project ("Jira-Cheer-Dashboard")
3. Click on **"Traces"**
4. You should see a trace for the query you just sent!
5. Click on it to see the full execution flow

## 🎉 Success!

If you made it here, congratulations! Your AI-Powered Jira Dashboard is now running.

## What's Next?

### Customize for Your Team

1. **Update team member names** in `agent-server/agent.py`:
   ```python
   Team members you might be asked about:
   - Your Team Member 1
   - Your Team Member 2
   - etc.
   ```

2. **Add more JQL queries** in `jira-tool-server/jira_client.py`

3. **Customize the UI** in `frontend/src/components/JiraDashboard.jsx`

### Learn More

- **[TESTING_GUIDE.md](TESTING_GUIDE.md)**: Learn how to test and improve your agent
- **[LANGSMITH_SETUP.md](LANGSMITH_SETUP.md)**: Deep dive into LangSmith features
- **[QUICK_REFERENCE.md](QUICK_REFERENCE.md)**: Common commands and tasks

### Phase 4: Testing & Refinement

Now that everything is running, you can start Phase 4:

1. **Test with various queries**
   - Try different ways of asking the same question
   - Test edge cases (users with no tasks, etc.)

2. **Review traces in LangSmith**
   - See what the agent is doing
   - Identify any issues

3. **Refine the agent**
   - Improve prompts
   - Add better tool descriptions
   - Create test datasets

4. **Iterate and improve**
   - Use LangSmith to track improvements
   - Build evaluation datasets
   - Run automated tests

## Troubleshooting

### "Server won't start"
- Check that the port isn't already in use
- Verify all environment variables are set
- See [TROUBLESHOOTING.md](TROUBLESHOOTING.md)

### "No data from Jira"
- Verify your Jira credentials are correct
- Check that you updated the project key
- Test the Jira API directly: `curl http://localhost:5001/health`

### "No traces in LangSmith"
- Verify `LANGCHAIN_TRACING_V2=true` in `agent-server/.env`
- Check that your LangSmith API key is correct
- Restart the agent server

### "Agent gives wrong answers"
- This is normal at first!
- Review traces in LangSmith to see what's happening
- Follow the [TESTING_GUIDE.md](TESTING_GUIDE.md) to improve it

## Getting Help

If you're stuck:

1. Check [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
2. Review the logs in each terminal
3. Check LangSmith traces for errors
4. Verify all environment variables are set correctly

## Quick Commands Reference

```bash
# Health checks
curl http://localhost:5001/health  # Jira Tool Server
curl http://localhost:5002/health  # Agent Server

# Test a query
curl -X POST http://localhost:5002/api/agent/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "How many bugs do we have?"}'

# Stop servers
# Press Ctrl+C in each terminal
```

## Architecture Reminder

```
Frontend (3000) → Agent Server (5002) → Jira Tool Server (5001) → Jira API
                       ↓
                  LangSmith (tracing)
```

---

**Ready to dive deeper?** Check out [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) for the full project overview!

