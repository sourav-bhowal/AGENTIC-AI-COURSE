from langgraph.graph import StateGraph, START, END
from langchain_openai import ChatOpenAI
from typing import TypedDict
from dotenv import load_dotenv

# Load the environment variables
load_dotenv()

# Define the LLM
llm = ChatOpenAI(model="gpt-4.1-mini", temperature=0)

class QAState(TypedDict):
    """State for the QA agent"""
    question: str
    answer: str

def answer_question(state: QAState) -> QAState:
    """Answer the question using the LLM"""
    response = llm.invoke(f"Answer the following question: {state['question']}")
    return {"answer": response.content}

# Build the graph with the state type
graph_builder = StateGraph(QAState)

# Add the node to the graph
graph_builder.add_node("answer_question", answer_question)

# Add the edges to the graph
graph_builder.add_edge(START, "answer_question")
graph_builder.add_edge("answer_question", END)

# Compile the graph
graph = graph_builder.compile()

# Main function
def main():
    """Main function to run the QA agent"""
    print("Welcome to the QA agent!")
    try:
        question = input("Enter a question: ")
        # Invoke the graph with the question
        result = graph.invoke({"question": question})
        # Print the answer
        print(f"Answer: {result['answer']}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        print("Thank you for using the QA agent!")

# Run the main function
main()