from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain_core.messages import HumanMessage, BaseMessage
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain_tavily import TavilySearch
from typing import TypedDict, Annotated
from dotenv import load_dotenv
import requests
import math

# Load the environment variables
load_dotenv()

# Initialize the LLM
llm = ChatOpenAI(model="gpt-4.1-mini")

# Initialize the Tavily Search Tool
search_tool = TavilySearch(max_results=5, search_depth="advanced", topic="general")

@tool
def get_weather_tool(city: str) -> str:
    """Get the weather of a city using the wttr.in API"""
    try:
        url = f"https://wttr.in/{city}?format=%C+%t"
        response = requests.get(url)

        if response.status_code == 200:
            return f"The weather in {city} is {response.text.strip()}."

    except Exception as e:
        return f"Weather Error: {e}"

@tool
def calculate_tool(expression: str) -> str:
    """Calculate the result of an expression using the allowed operations"""
    try:
        allowed_operations = {
            "math": math,
            "abs": abs,
            "round": round,
            "min": min,
            "max": max,
            "sum": sum,
        }

        result = eval(expression, {"__builtins__": {}}, allowed_operations)
        return str(result)

    except Exception as e:
        return f"Calculation Error: {e}"

# Tools for the Agent
tools = [search_tool, get_weather_tool, calculate_tool]

# Bind the tools to the LLM
llm_with_tools = llm.bind_tools(tools)

# Define the State for the chatbot
class ChatState(TypedDict):
    """State for the chatbot"""
    messages: Annotated[list[BaseMessage], add_messages]

# Define the Chat Node
def chat_node(state: ChatState) -> ChatState:
    """Chat Node for the chatbot"""
    return {"messages": [llm_with_tools.invoke(state["messages"])]}

# Define the Tool Node
tool_node = ToolNode(tools)

# Define the Graph
build_graph = StateGraph(ChatState)

# Add the nodes to the graph
build_graph.add_node("chat_node", chat_node)
build_graph.add_node("tools", tool_node)  # tools_condition expects a node named "tools" when the model calls tools

# Add the edges to the graph
build_graph.add_edge(START, "chat_node")
build_graph.add_conditional_edges("chat_node", tools_condition)
build_graph.add_edge("tools", "chat_node") # We are sending the result of the tool node to the chat node so that the chat node can refine the response

# Define the checkpointer and the thread id
checkpointer = InMemorySaver()
thread_id = "chat_with_tools"

# Compile the graph with the checkpointer
graph = build_graph.compile(checkpointer)

# Run the chatbot in a loop
print("Welcome to the chatbot! Type 'exit' to end the conversation.")
while True:
    # Get the user input
    user_input = input("You: ")

    # Check if the user wants to exit
    if user_input.lower() == "exit":
        break

    # Define the config
    config = {"configurable": {"thread_id": thread_id}}

    # Invoke the graph
    result = graph.invoke({"messages": [HumanMessage(content=user_input)]}, config)

    # Print the content of the last message
    print("Bot: ", result["messages"][-1].content)