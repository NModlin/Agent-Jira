"""
Jira client module for interacting with Jira API.
Provides methods to execute JQL queries and retrieve data.
"""
from jira import JIRA
from config import Config

class JiraClient:
    """Client for interacting with Jira API."""
    
    def __init__(self):
        """Initialize Jira client with credentials from config."""
        Config.validate()
        # Configure to use Jira REST API v3 instead of deprecated v2
        # get_server_info=True is required for cloud-specific methods like enhanced_search_issues
        options = {
            'server': Config.JIRA_URL,
            'rest_api_version': '3'  # Use API v3 instead of deprecated v2
        }
        self.jira = JIRA(
            options=options,
            basic_auth=(Config.JIRA_EMAIL, Config.JIRA_API_TOKEN),
            get_server_info=True  # Required for Jira Cloud enhanced_search_issues
        )
    
    def get_bugs_summary(self):
        """
        Get summary of all open bugs for the team.

        Returns:
            dict: Summary containing total bugs, critical bugs, etc.
        """
        # JQL query for all open bugs
        jql = f'project = {Config.JIRA_PROJECT} AND type = Bug AND status != Done'

        try:
            # Use enhanced_search_issues for Jira Cloud (supports API v3)
            issues = self.jira.enhanced_search_issues(jql, maxResults=1000)
            
            # Count bugs by priority
            priority_counts = {}
            for issue in issues:
                priority = issue.fields.priority.name if issue.fields.priority else 'None'
                priority_counts[priority] = priority_counts.get(priority, 0) + 1
            
            return {
                'totalBugs': len(issues),
                'criticalBugs': priority_counts.get('Critical', 0) + priority_counts.get('Highest', 0),
                'highBugs': priority_counts.get('High', 0),
                'mediumBugs': priority_counts.get('Medium', 0),
                'lowBugs': priority_counts.get('Low', 0) + priority_counts.get('Lowest', 0),
                'priorityBreakdown': priority_counts
            }
        except Exception as e:
            raise Exception(f"Error fetching bugs summary: {str(e)}")
    
    def get_tasks_for_user(self, username):
        """
        Get tasks and bugs for a specific user.
        
        Args:
            username (str): Full name of the user (e.g., "Alice Smith")
        
        Returns:
            dict: Summary of user's tasks and bugs
        """
        # JQL query for user's open tasks and bugs
        jql = f'assignee = "{username}" AND status != Done'
        
        try:
            # Use enhanced_search_issues for Jira Cloud (supports API v3)
            issues = self.jira.enhanced_search_issues(jql, maxResults=1000)
            
            # Separate tasks and bugs
            tasks = [issue for issue in issues if issue.fields.issuetype.name != 'Bug']
            bugs = [issue for issue in issues if issue.fields.issuetype.name == 'Bug']
            
            return {
                'username': username,
                'totalIssues': len(issues),
                'openTasks': len(tasks),
                'openBugs': len(bugs),
                'tasks': [{'key': task.key, 'summary': task.fields.summary} for task in tasks[:10]],
                'bugs': [{'key': bug.key, 'summary': bug.fields.summary} for bug in bugs[:10]]
            }
        except Exception as e:
            raise Exception(f"Error fetching tasks for user {username}: {str(e)}")
    
    def get_overall_progress(self):
        """
        Get overall team progress metrics.

        Returns:
            dict: Progress metrics including completed tasks, story points, etc.
        """
        # JQL queries for progress metrics
        completed_jql = f'project = {Config.JIRA_PROJECT} AND status = Done AND resolved >= -7d'
        in_progress_jql = f'project = {Config.JIRA_PROJECT} AND status = "In Progress"'
        todo_jql = f'project = {Config.JIRA_PROJECT} AND status = "To Do"'

        try:
            # Use enhanced_search_issues for Jira Cloud (supports API v3)
            completed_issues = self.jira.enhanced_search_issues(completed_jql, maxResults=1000)
            in_progress_issues = self.jira.enhanced_search_issues(in_progress_jql, maxResults=1000)
            todo_issues = self.jira.enhanced_search_issues(todo_jql, maxResults=1000)

            # Calculate story points (if available)
            # Use configured custom field ID
            completed_points = sum(
                getattr(issue.fields, Config.JIRA_STORY_POINTS_FIELD, 0) or 0
                for issue in completed_issues
            )
            
            return {
                'completedLast7Days': len(completed_issues),
                'inProgress': len(in_progress_issues),
                'todo': len(todo_issues),
                'completedStoryPoints': completed_points,
                'recentCompletions': [
                    {'key': issue.key, 'summary': issue.fields.summary} 
                    for issue in completed_issues[:5]
                ]
            }
        except Exception as e:
            raise Exception(f"Error fetching overall progress: {str(e)}")

