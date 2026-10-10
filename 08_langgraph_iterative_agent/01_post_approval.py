from langchain_core.messages import SystemMessage, HumanMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START, END
from typing import Literal, TypedDict, Annotated
from pydantic import BaseModel, Field
from dotenv import load_dotenv
import operator

# Load the environment variables
load_dotenv()

# Define the LLMs
generator_llm = ChatOpenAI(model="gpt-4.1-mini")
evaluator_llm = ChatOpenAI(model="gpt-4.1-mini")
optimizer_llm = ChatOpenAI(model="gpt-5-mini")

# Define the evaluation schema from the LLM
class PostEvaluationSchema(BaseModel):
    """Schema for the post-evaluation of the post"""
    evaluation: Literal["approved", "need_improvement"] = Field(description="Evaluation of the post")
    feedback: str = Field(description="Feedback on the post")

# Define the evaluator LLM with the structured output
structured_evaluator_llm = evaluator_llm.with_structured_output(PostEvaluationSchema)

class PostState(TypedDict):
    """State for the post approval"""
    topic: str
    post: str
    evaluation: Literal["approved", "need_improvement"]
    feedback: str
    iteration: int
    max_iterations: int
    post_history: Annotated[list[str], operator.add]
    feedback_history: Annotated[list[str], operator.add]

def generate_post(state: PostState) -> PostState:
    """Generate a post on a given topic"""

    # Define the messages for the LLM
    messages = [
        SystemMessage(content="You are a funny and clever social media influencer."),
        HumanMessage(content=f"""
            Write a short, original, and engaging social media post about the topic: {state["topic"]}.

            Rules:
            - Do not use any hashtags.
            - Max 500 characters.
            - No emojis.
            - Do not use question-answer format.
            - Think in meme logic, punchlines or relatable jokes.
            - Use simple, day to day english.
        """)
    ]

    # Invoke the LLM
    response = generator_llm.invoke(messages).content

    # Return the state
    return {
        "post": response,
        "post_history": [response],
    }

def evaluate_post(state: PostState) -> PostState:
    """Evaluate a post on a given topic"""

    # Define the messages for the LLM
    messages = [
        SystemMessage(content="You are a helpful assistant that evaluates posts on a given topic."),
        HumanMessage(content=f"""
            Evaluate the following post: {state["post"]}

            Use the following rules to evaluate the post:
            - Is the post original and engaging?
            - Is the post funny and clever?
            - Is the post relevant to the topic?
            - Virality potential?

            Auto-reject if:
            - It exceeds 500 characters.
            - It uses any hashtags.
            - It uses question-answer format.
            - It is not funny and clever.
            - It is not relevant to the topic.
            - It has no virality potential.

            ### Output Format ###
            - evaluation: "approved" or "need_improvement"
            - feedback: Feedback on the post to improve it up to 100 words.
        """),
    ]

    # Invoke the LLM
    response = structured_evaluator_llm.invoke(messages)

    # Return the state
    return {
        "evaluation": response.evaluation,
        "feedback": response.feedback,
        "feedback_history": [response.feedback],
    }

def optimize_post(state: PostState) -> PostState:
    """Optimize a post on a given topic"""

    # Define the messages for the LLM
    messages = [
        SystemMessage(content="You are a helpful assistant that optimizes posts on a given topic."),
        HumanMessage(content=f"""
            Optimize the following original and engaging social media post: {state["post"]}

            Use the following feedback to optimize the post: {state["feedback"]}
            Topic of the post: {state["topic"]}

            The post should be optimized up to 500 characters and should be in the same language as the original post.
        """),
    ]

    # Invoke the LLM
    response = optimizer_llm.invoke(messages).content
    
    # Return the state
    return {
        "post": response,
        "post_history": [response],
        "iteration": state["iteration"] + 1,
    }

def check_evaluation(state: PostState) -> Literal["approved", "need_improvement"]:
    """Check the evaluation of the post"""
    
    if state["evaluation"] == "approved" or state["iteration"] >= state["max_iterations"]:
        return "approved"
    else:
        return "need_improvement"

# Build the graph
graph_builder = StateGraph(PostState)

# Add the nodes
graph_builder.add_node("generate_post", generate_post)
graph_builder.add_node("evaluate_post", evaluate_post)
graph_builder.add_node("optimize_post", optimize_post)

# Add the edges
graph_builder.add_edge(START, "generate_post")
graph_builder.add_edge("generate_post", "evaluate_post")
graph_builder.add_conditional_edges("evaluate_post", check_evaluation, {"approved": END, "need_improvement": "optimize_post"})
graph_builder.add_edge("optimize_post", "evaluate_post")

# Build the graph
graph = graph_builder.compile()

# Run the graph
result = graph.invoke({"topic": "Make my girlfriend laugh", "max_iterations": 3, "iteration": 1})

# Print the result
print(f"\nFinal post: \n{result['post']}")
print(f"\nFinal evaluation: \n{result['evaluation']}")
print(f"\nFinal feedback: \n{result['feedback']}")
print(f"\nFinal iteration: \n{result['iteration']}")
print(f"\nFinal post history: \n{result['post_history']}")
print(f"\nFinal feedback history: \n{result['feedback_history']}")