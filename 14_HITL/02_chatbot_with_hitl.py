from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import StateGraph, START
from langgraph.graph.message import add_messages
from langchain_core.messages import HumanMessage, BaseMessage, SystemMessage
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain_tavily import TavilySearch
from typing import TypedDict, Annotated
from dotenv import load_dotenv
from langgraph.types import interrupt, Command
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

@tool
def purchase_stock_tool(symbol: str, quantity: int) -> dict:
    """
    Order a stock using the dummy function for HITL.

    Args:
        symbol: The symbol of the stock to order
        quantity: The quantity of the stock to order
    Returns:
        A dictionary with the status, message, symbol, and quantity
    """
    decision = interrupt({
        "type": "approval",
        "reason": "Model is about to order stock for " + symbol + " " + str(quantity) + " units",
        "instruction": "Approve this stock order? (yes/no)"
    })
    
    # Check if the decision is a dictionary and the approved key is "yes"
    if isinstance(decision, dict) and decision["approved"] == "yes":
        return {
            "status": "success",
            "message": f"Stock ordered successfully: {symbol} {quantity} units",
            "symbol": symbol,
            "quantity": quantity
        }
    else:
        return {
            "status": "cancelled",
            "message": f"Stock order cancelled. Please try again.",
            "symbol": symbol,
            "quantity": quantity
        }

# Tools for the Agent
tools = [search_tool, get_weather_tool, calculate_tool, purchase_stock_tool]

# Bind the tools to the LLM
llm_with_tools = llm.bind_tools(tools)

# Define the State for the chatbot
class ChatState(TypedDict):
    """State for the chatbot"""
    messages: Annotated[list[BaseMessage], add_messages]

# Define the Chat Node
def chat_node(state: ChatState) -> ChatState:
    """Chat Node for the chatbot"""

    # Define the system message
    system_message = SystemMessage(
        content=(
            "You are a helpful assistant that can use the following tools to answer questions.\n\n"

            "Tool usage instructions:\n\n"
            "- Use `search_tool` to search the web for information.\n"
            "- Use `get_weather_tool` to get the weather of a city.\n"
            "- Use `calculate_tool` to calculate the result of an expression.\n"
            "- Use `purchase_stock_tool` to purchase a stock. This is a dummy function for HITL.\n"

            "Always use the tools to answer questions. If you don't know the answer, say 'I don't know' and don't make up information."
            "Answer general questions directly without using the tools."
        )
    )

    # Combine the system message with the messages from the state
    messages = [system_message, *state["messages"]] # *state["messages"] is used to unpack the messages from the state

    # Invoke the LLM with the messages
    response = llm_with_tools.invoke(messages)

    # Return the response to the state
    return {"messages": [response]}

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
checkpointer = MemorySaver()
thread_id = "chat_with_tools_and_hitl"

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

    # Check if the graph returned an interrupt
    if "__interrupt__" in result:
        # Get the payload from the interrupt which is a dictionary with the instruction and the reason
        payload = result["__interrupt__"][0].value
        print("Bot: " + payload["instruction"] + " " + payload["reason"])

        # Get the approval from the user
        approval = input("Approve? (yes/no): ").strip().lower()

        # Invoke the graph with the approval
        result = graph.invoke(Command(resume={"approved": approval}), config)

    # Print the content of the last message
    print("Bot: ", result["messages"][-1].content)