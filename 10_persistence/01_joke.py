from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import InMemorySaver
from langchain_openai import ChatOpenAI
from typing import TypedDict
from dotenv import load_dotenv

# Load the environment variables
load_dotenv()

# Define the LLM
llm = ChatOpenAI(model="gpt-4.1-mini", temperature=0)

class JokeState(TypedDict):
    """State for the joke generator"""
    topic: str
    joke: str
    explanation: str

# Define the node
def generate_joke_node(state: JokeState) -> JokeState:
    """Node for generating a joke"""
    return {"joke": llm.invoke(f"Generate a joke about {state['topic']}").content}

def explain_joke_node(state: JokeState) -> JokeState:
    """Node for explaining a joke"""
    return {"explanation": llm.invoke(f"Explain the joke {state['joke']}").content}

# Define the graph
build_graph = StateGraph(JokeState)

# Define the nodes
build_graph.add_node("generate_joke_node", generate_joke_node)
build_graph.add_node("explain_joke_node", explain_joke_node)

# Define the edges
build_graph.add_edge(START, "generate_joke_node")
build_graph.add_edge("generate_joke_node", "explain_joke_node")
build_graph.add_edge("explain_joke_node", END)

# Define the checkpoint
checkpointer = InMemorySaver()

# Compile the graph
graph = build_graph.compile(checkpointer)

# Define the thread id
thread_id = "joke_thread_1"

# Define the config
config = {"configurable": {"thread_id": thread_id}}

# Run the graph
result = graph.invoke({"topic": "programming with AI"}, config)

# Print the result
print(f"Formatted result: \n\nJoke: {result['joke']}\n\nExplanation: {result['explanation']}")