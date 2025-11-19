# Troubleshooting Guide

Common issues and solutions for the AI-Powered Jira Dashboard.

## Table of Contents
- [Setup Issues](#setup-issues)
- [Jira Tool Server Issues](#jira-tool-server-issues)
- [Agent Server Issues](#agent-server-issues)
- [Frontend Issues](#frontend-issues)
- [LangSmith Issues](#langsmith-issues)
- [Performance Issues](#performance-issues)

## Setup Issues

### Python virtual environment not activating

**Windows:**
```bash
# If you get execution policy error
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Then activate
cd jira-tool-server
venv\Scripts\activate.bat
```

**Mac/Linux:**
```bash
cd jira-tool-server
source venv/bin/activate
```

### Dependencies installation fails

**Issue:** `pip install` fails with permission errors

**Solution:**
```bash
# Use --user flag
pip install --user -r requirements.txt

# Or upgrade pip first
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### Node modules installation fails

**Issue:** `npm install` fails

**Solution:**
```bash
# Clear npm cache
npm cache clean --force

# Delete node_modules and package-lock.json
rm -rf node_modules package-lock.json

# Reinstall
npm install
```

## Jira Tool Server Issues

### "Missing required environment variables"

**Issue:** Server won't start, complains about missing env vars

**Solution:**
1. Make sure `.env` file exists in `jira-tool-server/`
2. Copy from example: `cp .env.example .env`
3. Fill in all required values:
   - `JIRA_URL`
   - `JIRA_EMAIL`
   - `JIRA_API_TOKEN`

### "Authentication failed" or 401 errors

**Issue:** Can't connect to Jira

**Solution:**
1. Verify your Jira API token is correct
2. Generate a new token at https://id.atlassian.com/manage-profile/security/api-tokens
3. Make sure `JIRA_EMAIL` matches the account that created the token
4. Check `JIRA_URL` format: `https://your-domain.atlassian.net` (no trailing slash)

### "JQL query failed" or no results

**Issue:** Queries return empty results or errors

**Solution:**
1. Open `jira-tool-server/jira_client.py`
2. Replace `YOUR_PROJECT` with your actual Jira project key
3. Test JQL in Jira web interface first:
   - Go to Jira → Filters → Advanced search
   - Try: `project = YOURKEY AND type = Bug AND status != Done`
4. Adjust JQL queries to match your Jira setup

### Port 5001 already in use

**Issue:** `Address already in use`

**Solution:**
```bash
# Find process using port 5001
# Windows:
netstat -ano | findstr :5001
taskkill /PID <PID> /F

# Mac/Linux:
lsof -ti:5001 | xargs kill -9

# Or change port in .env
FLASK_PORT=5003
```

## Agent Server Issues

### "Missing required environment variables"

**Issue:** Agent server won't start

**Solution:**
1. Create `.env` in `agent-server/`: `cp .env.example .env`
2. Add required keys:
   - `LANGCHAIN_API_KEY` (from LangSmith)
   - `GOOGLE_API_KEY` (from Google AI Studio)

### "Failed to import langchain" or module errors

**Issue:** Import errors when starting server

**Solution:**
```bash
# Make sure virtual environment is activated
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate.bat  # Windows

# Reinstall dependencies
pip install -r requirements.txt

# If still failing, try specific versions
pip install langchain==0.1.0 langchain-google-genai==0.0.5
```

### "Connection refused" to Jira Tool Server

**Issue:** Agent can't reach Jira Tool Server

**Solution:**
1. Make sure Jira Tool Server is running (port 5001)
2. Check `JIRA_TOOL_SERVER_URL` in `agent-server/.env`
3. Test manually:
   ```bash
   curl http://localhost:5001/health
   ```

### "Gemini API error" or quota exceeded

**Issue:** Gemini API calls failing

**Solution:**
1. Verify API key is correct
2. Check quota at https://makersuite.google.com
3. Try a different model in `agent.py`:
   ```python
   llm = ChatGoogleGenerativeAI(
       model="gemini-1.5-flash",  # Cheaper, faster
       google_api_key=Config.GOOGLE_API_KEY
   )
   ```

### Agent gives wrong answers

**Issue:** Agent calls wrong tools or provides incorrect information

**Solution:**
1. Check traces in LangSmith
2. Review system prompt in `agent.py`
3. Improve tool descriptions in `tools.py`
4. See [TESTING_GUIDE.md](TESTING_GUIDE.md) for debugging steps

## Frontend Issues

### "Failed to fetch" errors

**Issue:** Frontend can't reach Agent Server

**Solution:**
1. Make sure Agent Server is running (port 5002)
2. Check proxy config in `vite.config.js`
3. Test API directly:
   ```bash
   curl -X POST http://localhost:5002/api/agent/chat \
     -H "Content-Type: application/json" \
     -d '{"query": "test"}'
   ```
4. Check browser console for CORS errors

### Blank screen or white page

**Issue:** Frontend loads but shows nothing

**Solution:**
1. Check browser console for errors (F12)
2. Verify all files are in place:
   ```
   frontend/
   ├── src/
   │   ├── components/
   │   │   ├── JiraDashboard.jsx
   │   │   └── JiraDashboard.css
   │   ├── App.jsx
   │   ├── main.jsx
   │   └── index.css
   └── index.html
   ```
3. Clear browser cache
4. Restart dev server: `npm run dev`

### Styles not loading

**Issue:** UI looks broken or unstyled

**Solution:**
1. Check that CSS files are imported:
   - `JiraDashboard.css` in `JiraDashboard.jsx`
   - `index.css` in `main.jsx`
2. Clear browser cache
3. Check browser console for 404 errors

### "Cannot find module" errors

**Issue:** Import errors in browser console

**Solution:**
```bash
# Reinstall dependencies
rm -rf node_modules package-lock.json
npm install

# Make sure all imports use correct paths
# Check for typos in import statements
```

## LangSmith Issues

### No traces appearing

**Issue:** Queries work but no traces in LangSmith

**Solution:**
1. Check environment variables in `agent-server/.env`:
   ```
   LANGCHAIN_TRACING_V2=true
   LANGCHAIN_API_KEY=your-key-here
   ```
2. Restart agent server after changing `.env`
3. Verify API key at https://smith.langchain.com → Settings → API Keys
4. Check agent server logs for LangSmith errors

### "Invalid API key" errors

**Issue:** LangSmith authentication fails

**Solution:**
1. Generate new API key at https://smith.langchain.com
2. Update `LANGCHAIN_API_KEY` in `.env`
3. Make sure no extra spaces or quotes in `.env` file

### Can't create dataset

**Issue:** Dataset creation fails in LangSmith

**Solution:**
1. Make sure you have a project created
2. Check project name matches `LANGCHAIN_PROJECT` in `.env`
3. Try creating dataset through UI first
4. Verify you have permissions (if using team account)

## Performance Issues

### Slow responses

**Issue:** Agent takes too long to respond

**Solution:**
1. Check Jira Tool Server response time:
   ```bash
   time curl -X POST http://localhost:5001/api/jira/get_bugs_summary
   ```
2. Optimize JQL queries in `jira_client.py`:
   - Add `maxResults` limit
   - Use more specific filters
   - Index frequently queried fields in Jira
3. Consider caching:
   ```python
   from functools import lru_cache
   
   @lru_cache(maxsize=100)
   def get_bugs_summary_cached():
       return get_bugs_summary()
   ```

### High token usage / costs

**Issue:** LangSmith shows high token counts

**Solution:**
1. Shorten system prompt in `agent.py`
2. Use a smaller model:
   ```python
   model="gemini-1.5-flash"  # Instead of gemini-1.5-pro
   ```
3. Reduce conversation history
4. Cache common queries

### Memory issues

**Issue:** Server crashes or runs out of memory

**Solution:**
1. Limit `maxResults` in JQL queries
2. Don't store full conversation history
3. Restart servers periodically
4. Use pagination for large result sets

## Getting Help

If you're still stuck:

1. **Check logs:**
   - Jira Tool Server: Terminal output
   - Agent Server: Terminal output
   - Frontend: Browser console (F12)

2. **Enable debug mode:**
   ```bash
   # In .env files
   FLASK_DEBUG=True
   ```

3. **Test components individually:**
   ```bash
   # Test Jira Tool Server
   curl http://localhost:5001/health
   
   # Test Agent Server
   curl http://localhost:5002/health
   
   # Test frontend
   curl http://localhost:3000
   ```

4. **Review documentation:**
   - [README.md](README.md) - Main setup
   - [LANGSMITH_SETUP.md](LANGSMITH_SETUP.md) - LangSmith config
   - [TESTING_GUIDE.md](TESTING_GUIDE.md) - Testing and debugging

5. **Check LangSmith traces:**
   - Often the best way to debug agent issues
   - Shows exactly what the agent is doing

6. **Common fixes:**
   - Restart all servers
   - Clear caches
   - Reinstall dependencies
   - Check environment variables
   - Verify API keys

