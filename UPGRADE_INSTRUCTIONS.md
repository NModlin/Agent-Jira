# MCP Server Upgrade Instructions

## Problem Identified

The current MCP Atlassian server is using the **deprecated Jira API v2** which has been removed by Atlassian. This causes a 500 Internal Server Error when trying to query Jira issues.

**Error message:**
```
The requested API has been removed. Please migrate to the /rest/api/3/search/jql API.
```

## Solution

Upgrade to the **phuc-nt/mcp-atlassian-server** which uses **Jira API v3** and **Confluence API v2**.

## Upgrade Steps

### Option 1: Automated Setup (Recommended)

Run the PowerShell setup script:

```powershell
.\setup-mcp-server.ps1
```

This script will:
1. Prompt you for Jira credentials (if .env doesn't exist)
2. Build the new Docker image
3. Stop and remove the old container
4. Start the new container with the same name (`friendly_goldberg`)

### Option 2: Manual Setup

1. **Create the .env file:**

```bash
cd mcp-atlassian-updated
```

Create a `.env` file with your Jira credentials:

```env
# Atlassian Configuration
ATLASSIAN_SITE_NAME=rehrig.atlassian.net
ATLASSIAN_USER_EMAIL=nmodlin@rehrig.com
ATLASSIAN_API_TOKEN=your-api-token-here

# MCP Configuration
MCP_SERVER_NAME=mcp-atlassian-integration
MCP_SERVER_VERSION=2.1.1

# Logging Configuration
LOG_LEVEL=info
```

2. **Build the Docker image:**

```bash
docker build -t mcp-atlassian-server:latest .
```

3. **Stop and remove the old container:**

```bash
docker stop friendly_goldberg
docker rm friendly_goldberg
```

4. **Run the new container:**

```bash
docker run -d \
    --name friendly_goldberg \
    --env-file .env \
    -i \
    mcp-atlassian-server:latest
```

## Verify the Fix

After upgrading, test the agent:

```bash
cd agent-server
python debug_agent.py
```

You should see the agent successfully query Jira without the API v2 deprecation error.

## What Changed

- **Old MCP Server:** `ghcr.io/sooperset/mcp-atlassian` (uses Jira API v2 - deprecated)
- **New MCP Server:** `phuc-nt/mcp-atlassian-server` (uses Jira API v3 - current)

The new server includes:
- ✅ Jira API v3 support
- ✅ Confluence API v2 support
- ✅ 48 features (expanded from 21)
- ✅ Enhanced board & sprint management
- ✅ Advanced Confluence features

## Notes

- The container name remains `friendly_goldberg` for compatibility with existing code
- The command to execute inside the container is still `mcp-atlassian`
- No changes needed to `agent-server/mcp_client.py`
- The agent server will automatically connect to the new container

## Troubleshooting

If you encounter issues:

1. **Check container is running:**
   ```bash
   docker ps | findstr friendly_goldberg
   ```

2. **Check container logs:**
   ```bash
   docker logs friendly_goldberg
   ```

3. **Verify environment variables:**
   ```bash
   docker exec friendly_goldberg env | findstr ATLASSIAN
   ```

4. **Test MCP server directly:**
   ```bash
   docker exec -i friendly_goldberg mcp-atlassian
   ```

