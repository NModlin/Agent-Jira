"""
Configuration module for Agent Server.
Loads environment variables and provides configuration settings.
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Configuration class for the Agent Server."""
    
    # LangSmith Configuration
    LANGCHAIN_TRACING_V2 = os.getenv('LANGCHAIN_TRACING_V2', 'false')
    LANGCHAIN_ENDPOINT = os.getenv('LANGCHAIN_ENDPOINT', 'https://api.smith.langchain.com')
    LANGCHAIN_API_KEY = os.getenv('LANGCHAIN_API_KEY')
    LANGCHAIN_PROJECT = os.getenv('LANGCHAIN_PROJECT', 'Jira-Cheer-Dashboard')
    
    # LLM Provider Configuration
    # Supported providers: groq, together, ollama, gemini, replicate
    LLM_PROVIDER = os.getenv('LLM_PROVIDER', 'groq').lower()

    # Groq Configuration (default)
    GROQ_API_KEY = os.getenv('GROQ_API_KEY')
    GROQ_MODEL = os.getenv('GROQ_MODEL', 'llama-3.1-70b-versatile')

    # Together AI Configuration
    TOGETHER_API_KEY = os.getenv('TOGETHER_API_KEY')
    TOGETHER_MODEL = os.getenv('TOGETHER_MODEL', 'meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo')

    # Ollama Configuration (local)
    OLLAMA_BASE_URL = os.getenv('OLLAMA_BASE_URL', 'http://localhost:11434')
    OLLAMA_MODEL = os.getenv('OLLAMA_MODEL', 'llama3.1')

    # Gemini Configuration (legacy)
    GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
    GEMINI_MODEL = os.getenv('GEMINI_MODEL', 'gemini-1.5-pro')

    # Replicate Configuration
    REPLICATE_API_TOKEN = os.getenv('REPLICATE_API_TOKEN')
    REPLICATE_MODEL = os.getenv('REPLICATE_MODEL', 'meta/meta-llama-3.1-405b-instruct')

    # Jira Tool Server Configuration
    JIRA_TOOL_SERVER_URL = os.getenv('JIRA_TOOL_SERVER_URL', 'http://localhost:5001')

    # Server Configuration
    FLASK_PORT = int(os.getenv('FLASK_PORT', 5002))
    FLASK_DEBUG = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'

    @classmethod
    def validate(cls):
        """Validate that all required configuration is present."""
        required_vars = ['LANGCHAIN_API_KEY']

        # Check provider-specific requirements
        if cls.LLM_PROVIDER == 'groq' and not cls.GROQ_API_KEY:
            required_vars.append('GROQ_API_KEY')
        elif cls.LLM_PROVIDER == 'together' and not cls.TOGETHER_API_KEY:
            required_vars.append('TOGETHER_API_KEY')
        elif cls.LLM_PROVIDER == 'gemini' and not cls.GOOGLE_API_KEY:
            required_vars.append('GOOGLE_API_KEY')
        elif cls.LLM_PROVIDER == 'replicate' and not cls.REPLICATE_API_TOKEN:
            required_vars.append('REPLICATE_API_TOKEN')
        # Ollama doesn't require API key

        missing_vars = [var for var in required_vars if var != 'LANGCHAIN_API_KEY' and not getattr(cls, var, None)]
        if not cls.LANGCHAIN_API_KEY:
            missing_vars.insert(0, 'LANGCHAIN_API_KEY')

        if missing_vars:
            raise ValueError(
                f"Missing required environment variables for provider '{cls.LLM_PROVIDER}': {', '.join(missing_vars)}\n"
                f"Please create a .env file based on .env.example"
            )
    
    @classmethod
    def setup_langsmith(cls):
        """Set up LangSmith environment variables for tracing."""
        os.environ['LANGCHAIN_TRACING_V2'] = cls.LANGCHAIN_TRACING_V2
        os.environ['LANGCHAIN_ENDPOINT'] = cls.LANGCHAIN_ENDPOINT
        os.environ['LANGCHAIN_API_KEY'] = cls.LANGCHAIN_API_KEY
        os.environ['LANGCHAIN_PROJECT'] = cls.LANGCHAIN_PROJECT

