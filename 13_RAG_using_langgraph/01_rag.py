from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.messages import HumanMessage, BaseMessage
from langchain_community.document_loaders import PyPDFLoader
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_community.vectorstores import FAISS
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, START
from typing import TypedDict, Annotated
from langchain_core.tools import tool
from dotenv import load_dotenv

# Load the environment variables
load_dotenv()

# Initialize the LLM model
llm = ChatOpenAI(model="gpt-4.1-mini")

# Initialize the embeddings model
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

# Load the PDF file
file_path = "resume.pdf"
pdf = PyPDFLoader(file_path)
docs = pdf.load()

# Initialize the text splitter
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)

# Split the documents
chunks = text_splitter.split_documents(docs)

# Initialize the vector store
vector_store = FAISS.from_documents(chunks, embeddings)

# Initialize the retriever using the vector store 
# with similarity search and k=4 means return 4 most similar chunks
retriever = vector_store.as_retriever(search_type="similarity", search_kwargs={"k": 4})

@tool
def search_resume(query: str) -> str:
    """
    Search the resume for the given query.
    This function uses the retriever to search the resume for the given query.

    Args:
        query: The query to search the resume for
    Returns:
        The relevant information found in the resume
    """
    docs = retriever.invoke(query)

    if not docs:
        return "No relevant information found in the resume."

    formatted_docs = []

    # Format the documents
    for index, doc in enumerate(docs, start=1):
        source = doc.metadata.get("source", "Unknown Source")   # Get the source of the document
        page = doc.metadata.get("page", "Unknown Page")         # Get the page of the document

        # Add the document to the list
        formatted_docs.append(
            f"Document {index}:\n"
            f"Source: {source}\n"
            f"Page: {page}\n"
            f"Page Content: {doc.page_content}"
        )

    # Join the documents into a string
    return "\n\n".join(formatted_docs)

# Define the tools
tools = [search_resume]

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
build_graph.add_node("tools", tool_node)

# Add the edges to the graph
build_graph.add_edge(START, "chat_node")
build_graph.add_conditional_edges("chat_node", tools_condition)
build_graph.add_edge("tools", "chat_node")

# Compile the graph
graph = build_graph.compile()

# Run the chatbot in a loop
print("Welcome to the chatbot! Type 'exit' to end the conversation.")
while True:
    # Get the user input
    user_input = input("You: ")

    # Check if the user wants to exit
    if user_input.lower() == "exit":
        break

    # Invoke the graph
    result = graph.invoke({"messages": [HumanMessage(content=user_input)]})

    # Print the content of the last message
    print("Bot: ", result["messages"][-1].content)