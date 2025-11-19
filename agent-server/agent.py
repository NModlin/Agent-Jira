"""
LangGraph agent for Jira queries.
Uses various LLM providers (Groq, Together AI, Ollama, Gemini, etc.) to reason about user queries and call appropriate tools.
"""
from typing import TypedDict, Annotated, Sequence
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, ToolMessage
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from mcp_tools import ALL_TOOLS
from config import Config
import logging

logger = logging.getLogger(__name__)


def get_llm():
    """
    Get the configured LLM based on the LLM_PROVIDER environment variable.

    Supported providers:
    - groq: Fast inference with Llama models
    - together: Together AI with various Llama models
    - ollama: Local Llama models
    - gemini: Google Gemini (legacy)
    - replicate: Replicate API
    """
    provider = Config.LLM_PROVIDER
    logger.info(f"Initializing LLM with provider: {provider}")

    if provider == 'groq':
        from langchain_groq import ChatGroq
        return ChatGroq(
            groq_api_key=Config.GROQ_API_KEY,
            model_name=Config.GROQ_MODEL,
            temperature=0.7
        )

    elif provider == 'together':
        from langchain_together import ChatTogether
        return ChatTogether(
            together_api_key=Config.TOGETHER_API_KEY,
            model=Config.TOGETHER_MODEL,
            temperature=0.7
        )

    elif provider == 'ollama':
        from langchain_ollama import ChatOllama
        return ChatOllama(
            base_url=Config.OLLAMA_BASE_URL,
            model=Config.OLLAMA_MODEL,
            temperature=0.7
        )

    elif provider == 'gemini':
        from langchain_google_genai import ChatGoogleGenerativeAI
        return ChatGoogleGenerativeAI(
            model=Config.GEMINI_MODEL,
            google_api_key=Config.GOOGLE_API_KEY,
            temperature=0.7
        )

    elif provider == 'replicate':
        from langchain_community.chat_models import ChatReplicate
        return ChatReplicate(
            replicate_api_token=Config.REPLICATE_API_TOKEN,
            model=Config.REPLICATE_MODEL,
            temperature=0.7
        )

    else:
        raise ValueError(
            f"Unsupported LLM provider: {provider}. "
            f"Supported providers: groq, together, ollama, gemini, replicate"
        )

# Define the agent state
class AgentState(TypedDict):
    """State of the agent conversation."""
    messages: Annotated[Sequence[BaseMessage], "The messages in the conversation"]


# System prompt for the agent
SYSTEM_PROMPT = """You are a helpful Jira analyst assistant for the "Cheer Dashboard" team.

Your role is to help team members understand their Jira data by:
1. Answering questions about bugs, tasks, and team progress
2. Using the available tools to fetch real-time data from Jira
3. Providing clear, concise summaries of the data

Available tools:
- get_bugs_summary: Get summary of all open bugs
- get_tasks_for_user: Get tasks/bugs for a specific team member (MUST use full name like "Alice Smith")
- get_overall_progress: Get team progress metrics

Important guidelines:
- When asked about a specific person, ALWAYS use their full name (e.g., "Alice Smith", not just "Alice")
- Be conversational and friendly
- Summarize data in an easy-to-understand way
- If you don't have enough information, ask clarifying questions
- Always use tools to get real data rather than making assumptions

Team members you might be asked about:
- Alice Smith
- Bob Johnson  
- Charlie Lee
- Diana Martinez
- Eve Chen
"""


def create_agent():
    """Create and return the LangGraph agent."""

    # Initialize the LLM with tools
    llm = get_llm()
    llm_with_tools = llm.bind_tools(ALL_TOOLS)
    
    # Define the function that calls the model
    def call_model(state: AgentState) -> AgentState:
        """Call the LLM with the current state."""
        messages = state["messages"]
        
        # Add system prompt if this is the first message
        if len(messages) == 1 and isinstance(messages[0], HumanMessage):
            messages = [HumanMessage(content=SYSTEM_PROMPT)] + messages
        
        logger.info(f"Calling model with {len(messages)} messages")
        response = llm_with_tools.invoke(messages)
        logger.info(f"Model response: {response}")
        
        return {"messages": messages + [response]}
    
    # Define the function that determines whether to continue or end
    def should_continue(state: AgentState) -> str:
        """Determine if we should continue to tools or end."""
        last_message = state["messages"][-1]
        
        # If there are no tool calls, we're done
        if not hasattr(last_message, "tool_calls") or not last_message.tool_calls:
            logger.info("No tool calls, ending conversation")
            return "end"
        
        logger.info(f"Tool calls found: {last_message.tool_calls}")
        return "continue"
    
    # Create the tool node
    tool_node = ToolNode(ALL_TOOLS)
    
    # Build the graph
    workflow = StateGraph(AgentState)
    
    # Add nodes
    workflow.add_node("agent", call_model)
    workflow.add_node("tools", tool_node)
    
    # Set entry point
    workflow.set_entry_point("agent")
    
    # Add conditional edges
    workflow.add_conditional_edges(
        "agent",
        should_continue,
        {
            "continue": "tools",
            "end": END
        }
    )
    
    # Add edge from tools back to agent
    workflow.add_edge("tools", "agent")
    
    # Compile the graph
    app = workflow.compile()
    
    logger.info("Agent graph compiled successfully")
    return app


# Create the agent instance
agent_app = create_agent()

