"""
Jira Tool Server - Flask application
Provides secure API endpoints for Jira queries.
"""
from flask import Flask, request, jsonify
from flask_cors import CORS
from config import Config
from jira_client import JiraClient
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for frontend access

# Initialize Jira client
try:
    jira_client = JiraClient()
    logger.info("Jira client initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize Jira client: {str(e)}")
    jira_client = None


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'jira_connected': jira_client is not None
    }), 200


@app.route('/api/jira/get_bugs_summary', methods=['POST'])
def get_bugs_summary():
    """
    Get summary of all open bugs for the team.
    
    Returns:
        JSON response with bug summary
    """
    if not jira_client:
        return jsonify({'error': 'Jira client not initialized'}), 500
    
    try:
        logger.info("Fetching bugs summary")
        summary = jira_client.get_bugs_summary()
        logger.info(f"Successfully fetched bugs summary: {summary['totalBugs']} bugs")
        return jsonify(summary), 200
    except Exception as e:
        logger.error(f"Error in get_bugs_summary: {str(e)}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/jira/get_tasks_for_user', methods=['POST'])
def get_tasks_for_user():
    """
    Get tasks and bugs for a specific user.
    
    Request body:
        {
            "username": "Alice Smith"
        }
    
    Returns:
        JSON response with user's tasks and bugs
    """
    if not jira_client:
        return jsonify({'error': 'Jira client not initialized'}), 500
    
    try:
        data = request.get_json()
        username = data.get('username')
        
        if not username:
            return jsonify({'error': 'username is required'}), 400
        
        logger.info(f"Fetching tasks for user: {username}")
        tasks = jira_client.get_tasks_for_user(username)
        logger.info(f"Successfully fetched tasks for {username}: {tasks['totalIssues']} issues")
        return jsonify(tasks), 200
    except Exception as e:
        logger.error(f"Error in get_tasks_for_user: {str(e)}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/jira/get_overall_progress', methods=['POST'])
def get_overall_progress():
    """
    Get overall team progress metrics.
    
    Returns:
        JSON response with progress metrics
    """
    if not jira_client:
        return jsonify({'error': 'Jira client not initialized'}), 500
    
    try:
        logger.info("Fetching overall progress")
        progress = jira_client.get_overall_progress()
        logger.info(f"Successfully fetched progress: {progress['completedLast7Days']} completed")
        return jsonify(progress), 200
    except Exception as e:
        logger.error(f"Error in get_overall_progress: {str(e)}")
        return jsonify({'error': str(e)}), 500


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return jsonify({'error': 'Endpoint not found'}), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    return jsonify({'error': 'Internal server error'}), 500


if __name__ == '__main__':
    try:
        Config.validate()
        logger.info(f"Starting Jira Tool Server on port {Config.FLASK_PORT}")
        app.run(
            host='0.0.0.0',
            port=Config.FLASK_PORT,
            debug=Config.FLASK_DEBUG
        )
    except ValueError as e:
        logger.error(f"Configuration error: {str(e)}")
        exit(1)

