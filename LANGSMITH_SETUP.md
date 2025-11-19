# LangSmith Setup Guide

This guide walks you through setting up LangSmith for tracing, testing, and monitoring your Jira AI agent.

## What is LangSmith?

LangSmith is LangChain's platform for:
- **Tracing**: See every step of your agent's reasoning
- **Testing**: Create test cases and evaluate performance
- **Monitoring**: Track agent behavior in production
- **Debugging**: Identify and fix issues quickly

## Step 1: Create a LangSmith Account

1. Go to https://smith.langchain.com
2. Sign up for a free account
3. Verify your email

## Step 2: Create a Project

1. Click "New Project" in the LangSmith dashboard
2. Name it "Jira-Cheer-Dashboard" (or your preferred name)
3. Click "Create"

## Step 3: Generate API Key

1. Click on your profile icon (top right)
2. Go to "Settings" → "API Keys"
3. Click "Create API Key"
4. Give it a name (e.g., "Jira Dashboard Agent")
5. Copy the API key (you won't see it again!)

## Step 4: Configure Agent Server

1. Open `agent-server/.env`
2. Add your LangSmith credentials:

```bash
LANGCHAIN_TRACING_V2=true
LANGCHAIN_ENDPOINT=https://api.smith.langchain.com
LANGCHAIN_API_KEY=your-api-key-here
LANGCHAIN_PROJECT=Jira-Cheer-Dashboard
```

## Step 5: Test the Integration

1. Start the Agent Server:
```bash
cd agent-server
python app.py
```

2. Send a test query:
```bash
curl -X POST http://localhost:5002/api/agent/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "How many bugs do we have?"}'
```

3. Go to LangSmith dashboard
4. You should see a new trace appear!

## Understanding Traces

Each trace shows:

### 1. Input
- The user's query
- The system prompt
- The conversation history

### 2. LLM Calls
- Which model was called (Gemini)
- The prompt sent to the model
- The model's response
- Token usage and latency

### 3. Tool Calls
- Which tool the agent decided to use
- The arguments passed to the tool
- The data returned from the tool

### 4. Output
- The final response sent to the user

## Creating Test Cases

### From a Trace

1. Find a trace in LangSmith
2. Click "Add to Dataset"
3. Create a new dataset or add to existing
4. The query and expected output are saved

### Manually

1. Go to "Datasets" in LangSmith
2. Click "New Dataset"
3. Name it (e.g., "Jira Queries")
4. Add examples:
   - Input: "How many bugs do we have?"
   - Expected output: Should mention total bug count
   - Tags: bug-summary, basic-query

## Running Evaluations

### 1. Create an Evaluation

```python
from langsmith import Client
from langsmith.evaluation import evaluate

client = Client()

# Define your evaluation function
def correctness_evaluator(run, example):
    # Check if the response contains expected information
    response = run.outputs["response"]
    
    # Example: Check if bug count is mentioned
    if "bug" in example.inputs["query"].lower():
        return {"score": 1 if "bug" in response.lower() else 0}
    
    return {"score": 1}

# Run evaluation
results = evaluate(
    lambda inputs: agent_app.invoke({"messages": [HumanMessage(content=inputs["query"])]}),
    data="Jira Queries",  # Your dataset name
    evaluators=[correctness_evaluator],
    experiment_prefix="jira-agent-v1"
)
```

### 2. View Results

1. Go to "Datasets" → Your dataset
2. Click on the experiment
3. See scores for each example
4. Identify failing cases

## Refining the Agent

### Common Issues and Fixes

#### Issue: Agent uses wrong username format

**Trace shows**: Tool called with `username: "Alice"` instead of `"Alice Smith"`

**Fix**: Update system prompt in `agent.py`:
```python
SYSTEM_PROMPT = """...
IMPORTANT: When using get_tasks_for_user, you MUST use the user's full name 
(e.g., 'Alice Smith', 'Charlie Lee'). Never use just first names.
..."""
```

#### Issue: Agent doesn't call the right tool

**Trace shows**: Agent called `get_overall_progress` when asked about a specific user

**Fix**: Improve tool descriptions in `tools.py`:
```python
@tool
def get_tasks_for_user(username: str) -> dict:
    """
    Get tasks for a SPECIFIC team member by name.
    
    Use this when the user asks about:
    - A specific person's workload
    - What someone is working on
    - How many tasks/bugs a person has
    
    Do NOT use this for team-wide queries.
    """
```

#### Issue: Agent provides incomplete information

**Trace shows**: Tool returned data but agent didn't summarize it well

**Fix**: Add examples to system prompt:
```python
SYSTEM_PROMPT = """...
Example interactions:
User: "How many bugs does Alice Smith have?"
You: Call get_tasks_for_user("Alice Smith"), then respond:
"Alice Smith currently has 2 open bugs: BUG-123 (Login issue) and BUG-456 (UI glitch)."
..."""
```

## Best Practices

### 1. Tag Your Traces
Add metadata to traces for easier filtering:
```python
from langsmith import traceable

@traceable(tags=["production", "bug-query"])
def handle_query(query):
    return agent_app.invoke({"messages": [HumanMessage(content=query)]})
```

### 2. Create Diverse Test Cases
Include:
- Simple queries ("How many bugs?")
- Complex queries ("Show me Alice's critical bugs from last week")
- Edge cases ("What is Bob working on?" when Bob has no tasks)
- Ambiguous queries ("How are we doing?")

### 3. Monitor Production
- Set up alerts for high error rates
- Track average response time
- Monitor token usage

### 4. Iterate Regularly
1. Review traces weekly
2. Add failing cases to test dataset
3. Refine prompts and tools
4. Re-run evaluations
5. Deploy improvements

## Advanced Features

### Custom Evaluators

Create evaluators for specific criteria:

```python
def has_bug_count(run, example):
    """Check if response includes a specific bug count."""
    response = run.outputs["response"]
    import re
    has_number = bool(re.search(r'\d+', response))
    return {"score": 1 if has_number else 0, "key": "has_count"}

def is_polite(run, example):
    """Check if response is polite and helpful."""
    response = run.outputs["response"].lower()
    polite_words = ["please", "thank", "help", "happy to"]
    score = any(word in response for word in polite_words)
    return {"score": 1 if score else 0, "key": "politeness"}
```

### A/B Testing

Compare different prompts or models:

```python
# Test two different system prompts
results_v1 = evaluate(agent_v1, data="Jira Queries", experiment_prefix="v1-formal")
results_v2 = evaluate(agent_v2, data="Jira Queries", experiment_prefix="v2-casual")

# Compare in LangSmith UI
```

## Troubleshooting

### Traces not appearing
- Check `LANGCHAIN_TRACING_V2=true` in `.env`
- Verify `LANGCHAIN_API_KEY` is correct
- Ensure agent server restarted after changing `.env`

### Slow traces
- Check Jira Tool Server response time
- Consider caching frequently requested data
- Optimize JQL queries

### High costs
- Monitor token usage in LangSmith
- Use shorter system prompts
- Consider using a smaller model for simple queries

## Resources

- [LangSmith Documentation](https://docs.smith.langchain.com)
- [LangChain Documentation](https://python.langchain.com)
- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)

