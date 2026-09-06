import os
import requests
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.tools import tool
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain.agents import create_react_agent, AgentExecutor
from langsmith import Client

# Load environment variables
load_dotenv()

# Get the API Keys
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
LANGSMITH_API_KEY = os.getenv("LANGSMITH_API_KEY")

# Initialize the Tavily Search Tool
search_tool = TavilySearchResults(max_results=2) # max_results is the number of results to return

# Custom Tool - In this case, we are using the Custom Tool to get the weather of a city
@tool   # @tool is a decorator to register the function as a tool
def get_weather(city: str) -> str:
    """Get the weather of a city"""
    url = f"https://wttr.in/{city}?format=%C+%t"
    response = requests.get(url)

    if response.status_code == 200:
        return f"The weather in {city} is {response.text.strip()}."

    return "I don't know the weather for that location."

# Initialize the LLM
llm = ChatOpenAI(model="gpt-4.1-mini", temperature=0, api_key=OPENAI_API_KEY)

# Initialize the LangSmith Client
langsmith_client = Client(api_key=LANGSMITH_API_KEY)

# Get the ReAct Agent Prompt from the LangSmith Prompt Registry
prompt = langsmith_client.pull_prompt("hwchase17/react")

# Tools for the Agent - In this case, we are using the Tavily Search Tool and the Custom Tool
tools = [search_tool, get_weather]

# Create the ReAct Agent
# ReAct Agent - It is a type of Agent that uses the ReAct framework to create a chain of thought process
agent = create_react_agent(llm=llm, tools=tools, prompt=prompt) # prompt is the prompt for the Agent

# Create the Agent Executor
# Agent Executor - It orchestrates the Agent and the Tools to execute the task
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)  # verbose=True to see the Agent's thinking process

# Run the Agent Executor
response = agent_executor.invoke({
    "input": (
        "Latest news about US and Iran War? Also provide the time and date of the news."
        "What is the weather in Tokyo?"
        "Which tools you used to get the latest news about US and Iran War?"
        "Which tools you used to get the weather in Tokyo?"
    )
})

# Print the Response
print(response["output"])