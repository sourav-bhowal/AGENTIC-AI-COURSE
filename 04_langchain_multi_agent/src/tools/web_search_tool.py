from langchain.tools import tool
from dotenv import load_dotenv
from tavily import TavilyClient
import os

# Load environment variables
load_dotenv()

# Get the API Keys
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

# Initialize the Tavily Client
tavily_client = TavilyClient(api_key=TAVILY_API_KEY)

@tool
def web_search(query: str) -> str:
    """Search the web for information using the Tavily API. Returns the title, URL, and content of the results."""

    # Search the web for information using the Tavily API
    responses = tavily_client.search(query, max_results=5)

    # Initialize the output list
    output = []

    # Loop through the responses and add the title, URL, and content to the output
    for res in responses["results"]:
        output.append(f"Title: {res['title']}\nURL: {res['url']}\nContent: {res['content'][:300]}\n")

    # Join the output with newlines
    return "\n-----\n".join(output)

