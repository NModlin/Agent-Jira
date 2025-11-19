# Testing Guide - Phase 4: Agentic Studio Loop

This guide helps you test, trace, and refine your Jira AI agent using LangSmith.

## Overview

Phase 4 is about continuous improvement through:
1. Testing the agent with real queries
2. Reviewing traces in LangSmith
3. Identifying and fixing failures
4. Building evaluation datasets

## Step 1: Test with Sample Queries

### Basic Queries

Start with simple queries to verify basic functionality:

```bash
# Test bug summary
curl -X POST http://localhost:5002/api/agent/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "How many bugs do we have?"}'

# Test user-specific query
curl -X POST http://localhost:5002/api/agent/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "What is Alice Smith working on?"}'

# Test progress query
curl -X POST http://localhost:5002/api/agent/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "Show me our team progress this week"}'
```

### Complex Queries

Test more challenging scenarios:

```bash
# Ambiguous user reference
curl -X POST http://localhost:5002/api/agent/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "How is Alice doing?"}'

# Multiple questions
curl -X POST http://localhost:5002/api/agent/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "How many bugs do we have and who has the most?"}'

# Edge case - user with no tasks
curl -X POST http://localhost:5002/api/agent/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "What is Bob Johnson working on?"}'
```

### Using the Frontend

1. Open http://localhost:3000
2. Try the suggested queries
3. Ask follow-up questions
4. Test edge cases

## Step 2: Review Traces in LangSmith

### Accessing Traces

1. Go to https://smith.langchain.com
2. Select your project ("Jira-Cheer-Dashboard")
3. Click on "Traces"
4. You'll see a list of all agent runs

### Understanding a Trace

Click on any trace to see:

#### Input Section
- User's query
- System prompt
- Conversation history

#### Chain Steps
1. **Agent Node**: Shows the LLM call
   - Prompt sent to Gemini
   - Model's response
   - Tool calls requested

2. **Tools Node**: Shows tool execution
   - Which tool was called
   - Arguments passed
   - Data returned

3. **Agent Node (again)**: Final synthesis
   - How the agent summarized the tool results
   - Final response

#### Metadata
- Total duration
- Token usage
- Cost estimate
- Timestamps

### What to Look For

✅ **Good Traces**
- Agent calls the correct tool
- Uses proper arguments (e.g., full names)
- Provides helpful, accurate summaries
- Completes in reasonable time

❌ **Problem Traces**
- Wrong tool called
- Incorrect arguments (e.g., "Alice" instead of "Alice Smith")
- Incomplete or confusing responses
- Errors or timeouts

## Step 3: Identify and Fix Failures

### Common Issues

#### Issue 1: Wrong Username Format

**Symptom**: Agent calls `get_tasks_for_user` with "Alice" instead of "Alice Smith"

**How to identify**:
1. Find the trace in LangSmith
2. Look at the "Tools" node
3. Check the arguments: `{"username": "Alice"}`

**Fix**:
1. Open `agent-server/agent.py`
2. Update the system prompt:

```python
SYSTEM_PROMPT = """...
CRITICAL: When using get_tasks_for_user, you MUST use the user's full name.

Examples:
- ✅ "Alice Smith"
- ✅ "Bob Johnson"
- ❌ "Alice"
- ❌ "Bob"

Team members:
- Alice Smith
- Bob Johnson
- Charlie Lee
- Diana Martinez
- Eve Chen
..."""
```

3. Restart the agent server
4. Re-test the query

**Verify**:
1. Send the same query again
2. Check the new trace
3. Verify the tool is called with "Alice Smith"

#### Issue 2: Wrong Tool Selected

**Symptom**: User asks about a specific person, but agent calls `get_overall_progress`

**How to identify**:
1. Find the trace
2. Look at which tool was called
3. Compare to what should have been called

**Fix**:
1. Open `agent-server/tools.py`
2. Improve tool descriptions:

```python
@tool
def get_tasks_for_user(username: str) -> dict:
    """
    Get tasks for a SPECIFIC team member.
    
    Use this ONLY when the user asks about a specific person by name.
    Examples: "What is Alice working on?", "How many bugs does Bob have?"
    
    Do NOT use for team-wide queries.
    """

@tool
def get_overall_progress() -> dict:
    """
    Get TEAM-WIDE progress metrics.
    
    Use this when the user asks about the team as a whole.
    Examples: "How is the team doing?", "What's our progress?"
    
    Do NOT use for individual person queries.
    """
```

#### Issue 3: Incomplete Response

**Symptom**: Agent gets data but doesn't summarize it well

**How to identify**:
1. Find the trace
2. Look at the tool's return value (has good data)
3. Look at the final response (missing key information)

**Fix**:
1. Open `agent-server/agent.py`
2. Add examples to the system prompt:

```python
SYSTEM_PROMPT = """...
Example interactions:

User: "How many bugs does Alice Smith have?"
Assistant: 
1. Call get_tasks_for_user("Alice Smith")
2. Respond: "Alice Smith currently has 2 open bugs:
   - BUG-123: Login issue
   - BUG-456: UI glitch
   She also has 5 open tasks."

User: "Show me our team progress"
Assistant:
1. Call get_overall_progress()
2. Respond: "This week, the team completed 12 tasks (15 story points).
   Currently, there are 8 tasks in progress and 20 in the backlog."
..."""
```

### Creating Test Cases from Failures

1. In LangSmith, find a failing trace
2. Click "Add to Dataset"
3. Select or create a dataset (e.g., "Jira Agent Tests")
4. Add expected output
5. Save

Now you can re-run this test case after making fixes!

## Step 4: Build Evaluation Datasets

### Creating a Dataset

1. Go to LangSmith → Datasets
2. Click "New Dataset"
3. Name it "Jira Agent Tests"
4. Add examples manually or from traces

### Example Dataset

| Input | Expected Output | Tags |
|-------|----------------|------|
| "How many bugs do we have?" | Should mention total bug count and breakdown by priority | bug-query, basic |
| "What is Alice Smith working on?" | Should list Alice's tasks and bugs with issue keys | user-query, basic |
| "Show me our team progress" | Should mention completed tasks, in-progress, and backlog | progress-query, basic |
| "How is Alice doing?" | Should use full name "Alice Smith" and provide her workload | user-query, ambiguous |
| "Who has the most bugs?" | Should call get_tasks_for_user for each team member | complex, multi-tool |

### Running Evaluations

Create `agent-server/evaluate.py`:

```python
from langsmith import Client
from langsmith.evaluation import evaluate
from langchain_core.messages import HumanMessage
from agent import agent_app

client = Client()

def correctness_evaluator(run, example):
    """Check if the response is correct."""
    response = run.outputs["messages"][-1].content.lower()
    query = example.inputs["messages"][0].content.lower()
    
    # Check for bug queries
    if "bug" in query:
        score = 1 if "bug" in response else 0
        return {"score": score, "key": "mentions_bugs"}
    
    # Check for user queries
    if any(name in query for name in ["alice", "bob", "charlie"]):
        # Should mention tasks or bugs
        score = 1 if ("task" in response or "bug" in response) else 0
        return {"score": score, "key": "mentions_workload"}
    
    return {"score": 1}

# Run evaluation
results = evaluate(
    lambda inputs: agent_app.invoke(inputs),
    data="Jira Agent Tests",
    evaluators=[correctness_evaluator],
    experiment_prefix="jira-agent-v1"
)

print(results)
```

Run it:
```bash
cd agent-server
source venv/bin/activate
python evaluate.py
```

### Viewing Results

1. Go to LangSmith → Datasets → "Jira Agent Tests"
2. Click on the experiment
3. See scores for each test case
4. Click on failing cases to see traces
5. Identify patterns in failures

## Continuous Improvement Cycle

```
1. Deploy changes
   ↓
2. Monitor traces
   ↓
3. Identify issues
   ↓
4. Add to test dataset
   ↓
5. Fix the issue
   ↓
6. Run evaluations
   ↓
7. Verify improvement
   ↓
(repeat)
```

## Best Practices

### 1. Test Regularly
- Run manual tests after each change
- Run automated evaluations before deploying

### 2. Diverse Test Cases
- Simple queries
- Complex queries
- Edge cases
- Ambiguous queries
- Error scenarios

### 3. Monitor Production
- Review traces daily
- Set up alerts for errors
- Track response times

### 4. Version Your Prompts
- Use git to track prompt changes
- Tag experiments in LangSmith
- Compare versions with A/B tests

### 5. Document Learnings
- Keep notes on what works
- Document common failure patterns
- Share insights with the team

## Troubleshooting

### No traces appearing
- Check `LANGCHAIN_TRACING_V2=true`
- Verify API key is correct
- Restart agent server

### Evaluations failing
- Check dataset format
- Verify evaluator function
- Test with a single example first

### Slow performance
- Check Jira Tool Server response time
- Optimize JQL queries
- Consider caching

## Next Steps

After Phase 4, consider:
- Adding more tools (create issues, update status)
- Implementing streaming responses
- Adding authentication
- Deploying to production
- Setting up monitoring and alerts

