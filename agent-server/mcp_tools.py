from langchain.tools import tool
from mcp_client import mcp_client
import logging
import json

logger = logging.getLogger(__name__)

# Project key for the help desk
PROJECT_KEY = "HD"

@tool
async def get_bugs_summary() -> dict:
    """
    Get a summary of all open bugs for the team.
    
    This tool returns information about:
    - Total number of open bugs
    - Breakdown by priority level
    
    Use this when the user asks about bugs, bug count, or bug status.
    
    Returns:
        dict: Summary containing totalBugs and priorityBreakdown
    """
    try:
        logger.info("Calling get_bugs_summary via MCP")
        jql = f"project = {PROJECT_KEY} AND type = Bug AND status != Done"
        
        result = await mcp_client.call_tool("jira_search", {
            "jql": jql,
            "fields": "priority",
            "limit": 100
        })
        
        # Parse MCP result
        # The result structure depends on the MCP server implementation
        # Usually result.content is a list of TextContent or ImageContent
        
        logger.info(f"MCP Result type: {type(result)}")
        logger.info(f"MCP Result content: {result.content}")

        if not result.content:
            return {"totalBugs": 0, "priorityBreakdown": {}}
            
        # Assuming the first content item contains the JSON response text
        data_text = result.content[0].text
        logger.info(f"Raw data text: {data_text}")
        data = json.loads(data_text)
        
        issues = data.get("issues", [])
        total_bugs = len(issues) # Or data.get('total') if available and accurate for pagination
        
        priority_breakdown = {}
        for issue in issues:
            priority = issue.get("fields", {}).get("priority", {}).get("name", "Unknown")
            priority_breakdown[priority] = priority_breakdown.get(priority, 0) + 1
            
        return {
            "totalBugs": total_bugs,
            "priorityBreakdown": priority_breakdown
        }
    except Exception as e:
        logger.error(f"Error in get_bugs_summary: {str(e)}")
        return {"error": str(e)}

@tool
async def get_tasks_for_user(username: str) -> dict:
    """
    Get the task and bug count for a specific team member.
    
    IMPORTANT: You MUST use the user's full name or email.
    
    This tool returns:
    - Total number of open issues
    - List of recent tasks and bugs
    
    Use this when the user asks about a specific person's workload, tasks, or bugs.
    
    Args:
        username (str): The full name or email of the team member
    
    Returns:
        dict: Summary containing username, totalIssues, and issues list
    """
    try:
        logger.info(f"Calling get_tasks_for_user via MCP for {username}")
        # Try to match assignee by name or email
        # Note: 'assignee' in JQL usually takes a username or account ID. 
        # For simplicity, we'll try to search by text if username isn't an ID.
        # But standard JQL is 'assignee = "name"'.
        
        jql = f"project = {PROJECT_KEY} AND assignee = \"{username}\" AND status != Done"
        
        result = await mcp_client.call_tool("jira_search", {
            "jql": jql,
            "fields": "summary,status,issuetype",
            "limit": 20
        })
        
        if not result.content:
            return {"totalIssues": 0, "issues": []}
            
        data_text = result.content[0].text
        data = json.loads(data_text)
        issues = data.get("issues", [])
        
        formatted_issues = []
        for issue in issues:
            formatted_issues.append({
                "key": issue.get("key"),
                "summary": issue.get("fields", {}).get("summary"),
                "status": issue.get("fields", {}).get("status", {}).get("name"),
                "type": issue.get("fields", {}).get("issuetype", {}).get("name")
            })
            
        return {
            "username": username,
            "totalIssues": len(issues),
            "issues": formatted_issues
        }
    except Exception as e:
        logger.error(f"Error in get_tasks_for_user: {str(e)}")
        return {"error": str(e)}

@tool
async def get_overall_progress() -> dict:
    """
    Get overall team progress metrics.
    
    This tool returns:
    - Number of tasks completed in the last 7 days
    
    Use this when the user asks about team progress, velocity, or overall status.
    
    Returns:
        dict: Progress metrics
    """
    try:
        logger.info("Calling get_overall_progress via MCP")
        jql = f"project = {PROJECT_KEY} AND status = Done AND updated >= -7d"
        
        result = await mcp_client.call_tool("jira_search", {
            "jql": jql,
            "limit": 50
        })
        
        if not result.content:
            return {"completedLast7Days": 0}
            
        data_text = result.content[0].text
        data = json.loads(data_text)
        issues = data.get("issues", [])
        
        return {
            "completedLast7Days": len(issues),
            "recentCompletions": [i.get("key") for i in issues[:5]]
        }
    except Exception as e:
        logger.error(f"Error in get_overall_progress: {str(e)}")
        return {"error": str(e)}

# List of all available tools
ALL_TOOLS = [get_bugs_summary, get_tasks_for_user, get_overall_progress]
