"""
Agent Server - Flask application
Provides API endpoint for chat with the LangGraph agent.
"""
from flask import Flask, request, jsonify
from flask_cors import CORS
from config import Config
from agent import agent_app
from langchain_core.messages import HumanMessage
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("server.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for frontend access

# Validate configuration and setup LangSmith
try:
    Config.validate()
    Config.setup_langsmith()
    logger.info("Configuration validated and LangSmith configured")
except Exception as e:
    logger.error(f"Configuration error: {str(e)}")
    raise


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'langsmith_enabled': Config.LANGCHAIN_TRACING_V2 == 'true',
        'jira_tool_server': Config.JIRA_TOOL_SERVER_URL
    }), 200


@app.route('/api/agent/chat', methods=['POST'])
def chat():
    """
    Chat endpoint for the LangGraph agent.
    
    Request body:
        {
            "query": "How many bugs does Alice have?"
        }
    
    Returns:
        JSON response with the agent's answer
    """
    try:
        data = request.get_json()
        query = data.get('query')
        
        if not query:
            return jsonify({'error': 'query is required'}), 400
        
        logger.info(f"Received query: {query}")
        
        # Create initial state with user message
        initial_state = {
            "messages": [HumanMessage(content=query)]
        }
        
        # Invoke the agent
        logger.info("Invoking agent...")
        import asyncio
        result = asyncio.run(agent_app.ainvoke(initial_state))
        
        # Extract the final response
        messages = result.get("messages", [])
        if not messages:
            return jsonify({'error': 'No response from agent'}), 500
        
        # Get the last AI message
        final_message = messages[-1]
        response_text = final_message.content if hasattr(final_message, 'content') else str(final_message)
        
        logger.info(f"Agent response: {response_text}")
        
        return jsonify({
            'response': response_text,
            'query': query
        }), 200
        
    except Exception as e:
        logger.error(f"Error in chat endpoint: {str(e)}", exc_info=True)
        return jsonify({'error': str(e)}), 500


@app.route('/api/agent/stream', methods=['POST'])
def stream_chat():
    """
    Streaming chat endpoint (for future enhancement).
    Currently returns the same as /chat but can be extended for SSE.
    """
    # For V1, we'll just use the regular chat endpoint
    # V2 can implement streaming with Server-Sent Events
    return chat()


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return jsonify({'error': 'Endpoint not found'}), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    logger.error(f"Internal error: {str(error)}")
    return jsonify({'error': 'Internal server error'}), 500


if __name__ == '__main__':
    try:
        logger.info(f"Starting Agent Server on port {Config.FLASK_PORT}")
        logger.info(f"LangSmith Project: {Config.LANGCHAIN_PROJECT}")
        logger.info(f"Jira Tool Server: {Config.JIRA_TOOL_SERVER_URL}")
        
        app.run(
            host='0.0.0.0',
            port=Config.FLASK_PORT,
            debug=Config.FLASK_DEBUG
        )
    except Exception as e:
        logger.error(f"Failed to start server: {str(e)}")
        exit(1)

