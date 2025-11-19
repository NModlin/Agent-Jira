# Agent Server

LangChain/LangGraph agent server with LangSmith integration for the AI-Powered Jira Dashboard.

## Features

- **LangGraph Agent**: Stateful agent that reasons about user queries
- **LangSmith Tracing**: Full observability and debugging of agent runs
- **Gemini Integration**: Uses Google's Gemini model for natural language understanding
- **Tool Calling**: Automatically calls Jira Tool Server endpoints based on user intent

## Setup

### 1. Install Dependencies

```bash
cd agent-server
pip install -r requirements.txt
```

### 2. Configure Environment Variables

Copy the example environment file and fill in your credentials:

```bash
cp .env.example .env
```

Edit `.env` with your details:
- `LANGCHAIN_API_KEY`: Your LangSmith API key (get from https://smith.langchain.com)
- `GOOGLE_API_KEY`: Your Google Gemini API key (get from https://makersuite.google.com/app/apikey)
- `JIRA_TOOL_SERVER_URL`: URL of your Jira Tool Server (default: http://localhost:5001)

### 3. Start the Jira Tool Server

Make sure the Jira Tool Server is running first:

```bash
cd ../jira-tool-server
python app.py
```

### 4. Run the Agent Server

```bash
python app.py
```

The server will start on `http://localhost:5002`

## API Endpoints

### Health Check
```
GET /health
```

### Chat with Agent
```
POST /api/agent/chat
Content-Type: application/json

{
  "query": "How many bugs does Alice Smith have?"
}
```

Response:
```json
{
  "response": "Alice Smith has 5 open tasks and 2 open bugs...",
  "query": "How many bugs does Alice Smith have?"
}
```

## LangSmith Integration

All agent runs are automatically traced in LangSmith. To view traces:

1. Go to https://smith.langchain.com
2. Select your project (default: "Jira-Cheer-Dashboard")
3. View traces for each query

Each trace shows:
- The full conversation history
- Which tools were called
- The arguments passed to each tool
- The data returned from tools
- The final response generated

## Testing

Test the agent using curl:

```bash
# Health check
curl http://localhost:5002/health

# Ask about bugs
curl -X POST http://localhost:5002/api/agent/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "How many bugs do we have?"}'

# Ask about a specific user
curl -X POST http://localhost:5002/api/agent/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "What is Alice Smith working on?"}'

# Ask about team progress
curl -X POST http://localhost:5002/api/agent/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "What is our team progress this week?"}'
```

## Architecture

The agent uses LangGraph to create a stateful conversation flow:

1. **User Query** → Agent receives the query
2. **Reasoning** → Gemini model decides which tool(s) to call
3. **Tool Execution** → Calls Jira Tool Server endpoints
4. **Synthesis** → Gemini summarizes the results
5. **Response** → Returns natural language answer to user

## Customization

### Adding New Tools

1. Add a new endpoint to the Jira Tool Server
2. Create a new `@tool` function in `tools.py`
3. Add the tool to the `ALL_TOOLS` list
4. The agent will automatically have access to it

### Modifying the System Prompt

Edit the `SYSTEM_PROMPT` in `agent.py` to change the agent's behavior, personality, or instructions.

## Troubleshooting

- **No traces in LangSmith**: Check that `LANGCHAIN_TRACING_V2=true` and `LANGCHAIN_API_KEY` is set correctly
- **Tool errors**: Ensure the Jira Tool Server is running and accessible
- **Gemini errors**: Verify your `GOOGLE_API_KEY` is valid and has quota

