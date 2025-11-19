"""
LangChain tools that wrap the Jira Tool Server endpoints.
These tools are used by the agent to query Jira data.
"""
import requests
from langchain.tools import tool
from config import Config
import logging

logger = logging.getLogger(__name__)

TOOL_SERVER_URL = f"{Config.JIRA_TOOL_SERVER_URL}/api/jira"


@tool
def get_bugs_summary() -> dict:
    """
    Get a summary of all open bugs for the team.
    
    This tool returns information about:
    - Total number of open bugs
    - Number of critical/high priority bugs
    - Breakdown by priority level
    
    Use this when the user asks about bugs, bug count, or bug status.
    
    Returns:
        dict: Summary containing totalBugs, criticalBugs, highBugs, mediumBugs, lowBugs, and priorityBreakdown
    """
    try:
        logger.info("Calling get_bugs_summary tool")
        response = requests.post(f"{TOOL_SERVER_URL}/get_bugs_summary", timeout=10)
        response.raise_for_status()
        data = response.json()
        logger.info(f"get_bugs_summary returned: {data}")
        return data
    except Exception as e:
        logger.error(f"Error in get_bugs_summary: {str(e)}")
        return {"error": str(e)}


@tool
def get_tasks_for_user(username: str) -> dict:
    """
    Get the task and bug count for a specific team member.
    
    IMPORTANT: You MUST use the user's full name (e.g., 'Alice Smith', 'Bob Johnson', 'Charlie Lee').
    Do not use just first names.
    
    This tool returns:
    - Total number of open issues
    - Number of open tasks
    - Number of open bugs
    - List of recent tasks and bugs
    
    Use this when the user asks about a specific person's workload, tasks, or bugs.
    
    Args:
        username (str): The full name of the team member (e.g., "Alice Smith")
    
    Returns:
        dict: Summary containing username, totalIssues, openTasks, openBugs, tasks, and bugs
    """
    try:
        logger.info(f"Calling get_tasks_for_user tool with username: {username}")
        response = requests.post(
            f"{TOOL_SERVER_URL}/get_tasks_for_user",
            json={"username": username},
            timeout=10
        )
        response.raise_for_status()
        data = response.json()
        logger.info(f"get_tasks_for_user returned: {data}")
        return data
    except Exception as e:
        logger.error(f"Error in get_tasks_for_user: {str(e)}")
        return {"error": str(e)}


@tool
def get_overall_progress() -> dict:
    """
    Get overall team progress metrics and statistics.
    
    This tool returns:
    - Number of tasks completed in the last 7 days
    - Number of tasks currently in progress
    - Number of tasks in the backlog (To Do)
    - Story points completed
    - List of recent completions
    
    Use this when the user asks about team progress, velocity, or overall status.
    
    Returns:
        dict: Progress metrics containing completedLast7Days, inProgress, todo, completedStoryPoints, and recentCompletions
    """
    try:
        logger.info("Calling get_overall_progress tool")
        response = requests.post(f"{TOOL_SERVER_URL}/get_overall_progress", timeout=10)
        response.raise_for_status()
        data = response.json()
        logger.info(f"get_overall_progress returned: {data}")
        return data
    except Exception as e:
        logger.error(f"Error in get_overall_progress: {str(e)}")
        return {"error": str(e)}


# List of all available tools
ALL_TOOLS = [get_bugs_summary, get_tasks_for_user, get_overall_progress]

