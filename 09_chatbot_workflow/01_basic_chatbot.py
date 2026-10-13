from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.messages import HumanMessage, BaseMessage
from langchain_openai import ChatOpenAI
from typing import TypedDict, Annotated
from dotenv import load_dotenv

# Load the environment variables
load_dotenv()

# Define the LLM
llm = ChatOpenAI(model="gpt-4.1-mini", temperature=0)

# Define the checkpoint to save the state of the chatbot in RAM
checkpoint = MemorySaver()

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

# Compile the graph
graph = build_graph.compile(checkpointer=checkpoint)

# Define the thread id to save the state of the chatbot in RAM
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

    # Invoke the graph with the config
    result = graph.invoke({"messages": [HumanMessage(content=user_input)]}, config)
    print("Bot: ", result["messages"][-1].content)