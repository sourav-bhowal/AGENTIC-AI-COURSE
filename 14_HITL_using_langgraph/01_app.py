from langchain_openai import ChatOpenAI
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.types import interrupt, Command
from langgraph.checkpoint.memory import MemorySaver
from typing import TypedDict, Annotated
from dotenv import load_dotenv

# Load the environment variables
load_dotenv()

# Define the model
llm = ChatOpenAI(model="gpt-4.1-mini")

# Define the state
class ChatState(TypedDict):
    """State for the chatbot"""
    messages: Annotated[list[BaseMessage], add_messages]

# Define the chat node
def chat_node(state: ChatState) -> ChatState:
    """Chat node for the chatbot that checks if the question is approved by the user"""
    decision = interrupt({
        "type": "approval",
        "reason": "Model is about to answer a user question.",
        "question": state["messages"][-1].content,
        "instruction": "Approve this question? yes/no"
    })

    # Check if the question is approved by the user
    if decision["approved"] == "no":
        # If the question is not approved, return a message to the user
        return {"messages": [AIMessage(content="Question not approved. Please try again.")]}
    else:
        # If the question is approved, invoke the model to answer the question
        return {"messages": [llm.invoke(state["messages"])]}

# Define the graph
build_graph = StateGraph(ChatState)

# Add the nodes to the graph
build_graph.add_node("chat_node", chat_node)

# Add the edges to the graph
build_graph.add_edge(START, "chat_node")
build_graph.add_edge("chat_node", END)

# Define the checkpointer it is required for interrupt to work
checkpointer = MemorySaver()

# Compile the graph
graph = build_graph.compile(checkpointer)

# Define the config
config = {"configurable": {"thread_id": "123"}}

# Run the chatbot in a loop
print("Welcome to the chatbot! Type 'exit' to end the conversation.")
while True:
    # Get the user input
    user_input = input("You: ")

    # Check if the user wants to exit
    if user_input.lower() == "exit":
        break

    # Invoke the graph
    result = graph.invoke({"messages": [HumanMessage(content=user_input)]}, config)

    # Check if the graph returned an interrupt
    if "__interrupt__" in result:  
        # Get the payload from the interrupt which is a dictionary with the instruction and the question
        payload = result["__interrupt__"][0].value

        # Print the instruction and the question to the user
        print(payload["instruction"])
        print("Question:", payload["question"])

        # Get the approval from the user 
        approval = input("Approve? (yes/no): ").strip().lower()

        # Invoke the graph with the approval
        result = graph.invoke(Command(resume={"approved": approval}), config)

    # Print the assistant's response
    print("Assistant: ", result["messages"][-1].content)