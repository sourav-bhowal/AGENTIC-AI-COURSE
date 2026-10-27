from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.checkpoint.sqlite import SqliteSaver
from langchain_core.messages import HumanMessage, BaseMessage
from langchain_openai import ChatOpenAI
from typing import TypedDict, Annotated
from dotenv import load_dotenv
import sqlite3

# Load the environment variables
load_dotenv()

# Define the LLM
llm = ChatOpenAI(model="gpt-4.1-mini", temperature=0)

# Define the database path
database = "chatbot.db"

# Create the database connection
conn = sqlite3.connect(database, check_same_thread=False)

# Define the checkpointer to save the state of the chatbot in SQLite
checkpointer = SqliteSaver(conn)

# Define the state
class ChatState(TypedDict):
    """State for the chatbot"""
    messages: Annotated[list[BaseMessage], add_messages]

# Define the node
def chat_node(state: ChatState) -> ChatState:
    """Node for the chatbot"""
    return {"messages": [llm.invoke(state["messages"])]}

# Define the graph
build_graph = StateGraph(ChatState)

# Define the nodes
build_graph.add_node("chat_node", chat_node)

# Define the edges
build_graph.add_edge(START, "chat_node")
build_graph.add_edge("chat_node", END)

# Compile the graph with the checkpoint to save the state of the chatbot in SQLite
graph = build_graph.compile(checkpointer)

# Define the thread id to save the state of the chatbot in SQLite
thread_id = "chat_thread_1"

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

    # Stream the result of the graph with the config
    result = graph.stream({"messages": [HumanMessage(content=user_input)]}, config, stream_mode="messages")
    print("Bot: ", end="", flush=True)

    # Print the result
    for message_chunk, metadata in result:
        print(message_chunk.content, end="", flush=True)
    print()