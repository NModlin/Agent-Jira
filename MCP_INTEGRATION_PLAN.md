# MCP Integration Plan for AgentJira

## Current Situation

You have an **Atlassian MCP server** running in Docker:
- Container ID: `b6d58f3d1f5d`
- Container Name: `friendly_goldberg`
- Image: `ghcr.io/sooperset/mcp-atlassian@sha256:27c8e5b890e1...`
- Version: 1.9.4
- Already configured with your Jira credentials:
  - `JIRA_URL=https://rehrig.atlassian.net/jira/servicedesk/projects/HD`
  - `JIRA_USERNAME=nmodlin@rehrig.com`
  - `JIRA_API_TOKEN=ATATT3xFfGF0...`

## Problem

The current `jira-tool-server` is trying to use the Python `jira` library directly, which:
1. Uses deprecated Jira API v2 (returns HTTP 410)
2. Duplicates credentials that are already in the MCP server
3. Doesn't leverage the MCP server you already have running

## Solution Options

### Option 1: Direct MCP Integration (Recommended)

**Replace the entire `jira-tool-server` with MCP client integration in the Agent Server.**

#### Architecture:
```
Frontend (3099)
    ↓
Agent Server (5002) with MCP Client
    ↓
Atlassian MCP Server (Docker)
    ↓
Jira API
```

#### Implementation:
1. Install MCP Python SDK in `agent-server`:
   ```bash
   pip install mcp
   ```

2. Create MCP client in `agent-server/mcp_tools.py`:
   ```python
   from mcp import ClientSession, StdioServerParameters
   from mcp.client.stdio import stdio_client
   
   # Connect to Docker MCP server
   server_params = StdioServerParameters(
       command="docker",
       args=["exec", "-i", "b6d58f3d1f5d", "mcp-atlassian"]
   )
   
   async with stdio_client(server_params) as (read, write):
       async with ClientSession(read, write) as session:
           await session.initialize()
           tools = await session.list_tools()
           # Use tools...
   ```

3. Wrap MCP tools as LangChain tools
4. Remove `jira-tool-server` entirely

**Pros:**
- Eliminates middle layer (jira-tool-server)
- Uses your existing MCP server
- Simpler architecture
- No credential duplication

**Cons:**
- Requires async/await in Agent Server
- More complex integration

---

### Option 2: MCP Proxy Server (Current Architecture)

**Keep the `jira-tool-server` but make it an MCP client proxy.**

#### Architecture:
```
Frontend (3099)
    ↓
Agent Server (5002)
    ↓
Jira Tool Server (5001) - MCP Client Proxy
    ↓
Atlassian MCP Server (Docker)
    ↓
Jira API
```

#### Implementation:
1. Update `jira-tool-server/requirements.txt`:
   ```
   Flask==3.0.0
   Flask-CORS==4.0.0
   python-dotenv==1.0.0
   mcp>=1.0.0
   ```

2. Replace `jira_client.py` with MCP client
3. Keep REST endpoints but call MCP tools internally

**Pros:**
- Maintains current architecture
- Agent Server doesn't need changes
- Easier to test incrementally

**Cons:**
- Extra layer of abstraction
- More complex than Option 1

---

### Option 3: Expose MCP Server via HTTP (Not Recommended)

**Add an HTTP wrapper around the MCP server.**

**Cons:**
- MCP is designed for stdio, not HTTP
- Adds unnecessary complexity
- Defeats the purpose of MCP

---

## Recommended Approach: Option 1

### Step-by-Step Implementation

#### 1. Test MCP Server Tools

First, let's discover what tools the MCP server provides:

```bash
# Create a persistent connection test
python test_mcp_persistent.py
```

#### 2. Update Agent Server

```bash
cd agent-server
pip install mcp
```

Create `agent-server/mcp_tools.py`:
```python
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from langchain.tools import tool
import asyncio

# MCP connection
MCP_CONTAINER = "b6d58f3d1f5d"

async def get_mcp_session():
    """Get MCP session."""
    server_params = StdioServerParameters(
        command="docker",
        args=["exec", "-i", MCP_CONTAINER, "mcp-atlassian"]
    )
    return stdio_client(server_params)

@tool
async def search_jira_issues(jql: str, max_results: int = 50):
    """Search Jira issues using JQL query."""
    async with await get_mcp_session() as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            result = await session.call_tool("jira_search_issues", {
                "jql": jql,
                "maxResults": max_results
            })
            return result
```

#### 3. Update Agent

Modify `agent-server/agent.py` to use async tools.

#### 4. Remove Jira Tool Server

Once MCP integration works, remove:
- `jira-tool-server/` directory
- References in documentation
- Port 5001 from architecture

---

## Next Steps

1. **Test MCP server tools** - Discover available tools
2. **Create MCP client** - Build persistent connection
3. **Integrate with LangChain** - Wrap as LangChain tools
4. **Test end-to-end** - Verify queries work
5. **Update documentation** - Reflect new architecture

---

## Questions to Answer

1. What tools does the Atlassian MCP server provide?
2. What are the exact parameters for each tool?
3. Does the MCP server support the queries we need (bugs, tasks, progress)?
4. Can we maintain a persistent MCP connection in Flask?

---

## Testing Plan

1. ✅ Verify MCP server is running
2. ⏳ List available MCP tools
3. ⏳ Test calling each tool
4. ⏳ Integrate with Agent Server
5. ⏳ End-to-end test with Frontend


