"""
Evaluation script for the Jira AI agent.
Uses LangSmith to run evaluations on test datasets.
"""
from langsmith import Client
from langsmith.evaluation import evaluate
from langchain_core.messages import HumanMessage
from agent import agent_app
from config import Config
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize LangSmith client
Config.setup_langsmith()
client = Client()


def correctness_evaluator(run, example):
    """
    Evaluate if the agent's response is correct.
    
    Checks:
    - Bug queries mention bugs
    - User queries mention tasks/bugs
    - Progress queries mention metrics
    """
    try:
        # Get the response
        messages = run.outputs.get("messages", [])
        if not messages:
            return {"score": 0, "key": "correctness", "comment": "No response"}
        
        response = messages[-1].content.lower()
        
        # Get the query
        query_messages = example.inputs.get("messages", [])
        if not query_messages:
            return {"score": 0, "key": "correctness", "comment": "No query"}
        
        query = query_messages[0].content.lower()
        
        # Check for bug queries
        if "bug" in query:
            if "bug" in response:
                return {"score": 1, "key": "correctness", "comment": "Mentions bugs"}
            else:
                return {"score": 0, "key": "correctness", "comment": "Doesn't mention bugs"}
        
        # Check for user-specific queries
        user_names = ["alice", "bob", "charlie", "diana", "eve"]
        if any(name in query for name in user_names):
            if "task" in response or "bug" in response or "issue" in response:
                return {"score": 1, "key": "correctness", "comment": "Mentions workload"}
            else:
                return {"score": 0, "key": "correctness", "comment": "Doesn't mention workload"}
        
        # Check for progress queries
        if "progress" in query or "team" in query:
            progress_keywords = ["completed", "progress", "story point", "backlog"]
            if any(keyword in response for keyword in progress_keywords):
                return {"score": 1, "key": "correctness", "comment": "Mentions progress metrics"}
            else:
                return {"score": 0, "key": "correctness", "comment": "Doesn't mention progress"}
        
        # Default: assume correct if we got a response
        return {"score": 1, "key": "correctness", "comment": "Got response"}
        
    except Exception as e:
        logger.error(f"Error in correctness_evaluator: {str(e)}")
        return {"score": 0, "key": "correctness", "comment": f"Error: {str(e)}"}


def has_tool_call_evaluator(run, example):
    """
    Evaluate if the agent called a tool.
    Most queries should result in a tool call.
    """
    try:
        # Check if any tool was called
        # This is a simplified check - in production you'd inspect the trace more carefully
        messages = run.outputs.get("messages", [])
        
        # Look for tool messages in the conversation
        has_tool = any(
            hasattr(msg, "tool_calls") and msg.tool_calls 
            for msg in messages
        )
        
        if has_tool:
            return {"score": 1, "key": "has_tool_call", "comment": "Called a tool"}
        else:
            return {"score": 0, "key": "has_tool_call", "comment": "No tool called"}
            
    except Exception as e:
        logger.error(f"Error in has_tool_call_evaluator: {str(e)}")
        return {"score": 0, "key": "has_tool_call", "comment": f"Error: {str(e)}"}


def response_length_evaluator(run, example):
    """
    Evaluate if the response is an appropriate length.
    Too short might be incomplete, too long might be verbose.
    """
    try:
        messages = run.outputs.get("messages", [])
        if not messages:
            return {"score": 0, "key": "response_length", "comment": "No response"}
        
        response = messages[-1].content
        word_count = len(response.split())
        
        # Ideal range: 10-100 words
        if 10 <= word_count <= 100:
            score = 1
            comment = f"Good length ({word_count} words)"
        elif word_count < 10:
            score = 0.5
            comment = f"Too short ({word_count} words)"
        else:
            score = 0.7
            comment = f"A bit long ({word_count} words)"
        
        return {"score": score, "key": "response_length", "comment": comment}
        
    except Exception as e:
        logger.error(f"Error in response_length_evaluator: {str(e)}")
        return {"score": 0, "key": "response_length", "comment": f"Error: {str(e)}"}


def run_evaluation(dataset_name="Jira Agent Tests", experiment_prefix="jira-agent"):
    """
    Run evaluation on the specified dataset.
    
    Args:
        dataset_name: Name of the dataset in LangSmith
        experiment_prefix: Prefix for the experiment name
    """
    logger.info(f"Running evaluation on dataset: {dataset_name}")
    
    # Define the function to evaluate
    def predict(inputs):
        """Run the agent on the inputs."""
        return agent_app.invoke(inputs)
    
    # Run evaluation
    results = evaluate(
        predict,
        data=dataset_name,
        evaluators=[
            correctness_evaluator,
            has_tool_call_evaluator,
            response_length_evaluator
        ],
        experiment_prefix=experiment_prefix,
        max_concurrency=1  # Run one at a time to avoid rate limits
    )
    
    logger.info("Evaluation complete!")
    logger.info(f"Results: {results}")
    
    return results


if __name__ == "__main__":
    # Run evaluation
    try:
        results = run_evaluation()
        print("\n" + "="*50)
        print("Evaluation Results")
        print("="*50)
        print(f"Results: {results}")
        print("\nView detailed results at: https://smith.langchain.com")
    except Exception as e:
        logger.error(f"Evaluation failed: {str(e)}")
        print(f"\nError: {str(e)}")
        print("\nMake sure:")
        print("1. LangSmith is configured correctly")
        print("2. A dataset named 'Jira Agent Tests' exists")
        print("3. The agent server dependencies are installed")

