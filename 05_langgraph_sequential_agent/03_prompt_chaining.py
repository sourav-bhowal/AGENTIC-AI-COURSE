from langgraph.graph import StateGraph, START, END
from langchain_openai import ChatOpenAI
from typing import TypedDict
from dotenv import load_dotenv

# Load the environment variables
load_dotenv()

# Define the LLM
llm = ChatOpenAI(model="gpt-4.1-mini", temperature=0)

class BlogPostState(TypedDict):
    """State for the blog post agent"""
    title: str
    outline: str
    content: str
    evaluation: str

def generate_outline(state: BlogPostState) -> BlogPostState:
    """Generate the outline for the blog post by using the title"""
    prompt = f"Generate an outline for a blog post about {state['title']}. The outline should be a list of 3-5 points."
    response = llm.invoke(prompt)
    return {"outline": response.content}

def generate_content(state: BlogPostState) -> BlogPostState:
    """Generate the content for the blog post by using the title and the outline"""
    prompt = f"Generate the content for a blog post about {state['title']} based on the following outline: {state['outline']}. The content should be in markdown format."
    response = llm.invoke(prompt)
    return {"content": response.content}

def evaluate_content(state: BlogPostState) -> BlogPostState:
    """Evaluate the content of the blog post by using the title and the content"""
    prompt = f"Evaluate the content of the blog post about {state['title']} based on the following content: {state['content']}. The evaluation should be a in format X/10 where X is the score out of 10 and also provide a brief explanation of the evaluation within 50 words."
    response = llm.invoke(prompt)
    return {"evaluation": response.content}

# Build the graph with the state type
graph_builder = StateGraph(BlogPostState)

# Add the nodes to the graph
graph_builder.add_node("generate_outline", generate_outline)
graph_builder.add_node("generate_content", generate_content)
graph_builder.add_node("evaluate_content", evaluate_content)

# Add the edges to the graph
graph_builder.add_edge(START, "generate_outline")
graph_builder.add_edge("generate_outline", "generate_content")
graph_builder.add_edge("generate_content", "evaluate_content")
graph_builder.add_edge("evaluate_content", END)

# Compile the graph
graph = graph_builder.compile()

def main():
    """Main function to run the blog post agent"""
    print("Welcome to the blog post agent!")
    try:
        title = input("Enter the title of the blog post: ")
        # Invoke the graph with the title
        result = graph.invoke({"title": title})
        # Print the outline and content and evaluation
        print(f"Outline:\n {result['outline']}")
        print(f"Content:\n {result['content']}")
        print(f"Evaluation:\n {result['evaluation']}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        print("Thank you for using the blog post agent!")

# Run the main function
main()