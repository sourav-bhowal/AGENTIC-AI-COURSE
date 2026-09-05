import os
import requests
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.tools import tool
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain import hub
from langchain.agents import create_react_agent, AgentExecutor

# Load environment variables
load_dotenv()

# Get the API Keys
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

# Initialize the Tavily Search Tool
search_tool = TavilySearchResults(max_results=2) # max_results is the number of results to return

# Initialize the LLM
llm = ChatOpenAI(model="gpt-4.1-mini", temperature=0, api_key=OPENAI_API_KEY)

# Get the ReAct Agent Prompt from the LangChain Hub
prompt = hub.pull("hwchase17/react")

# Tools for the Agent - In this case, we are using the Tavily Search Tool
tools = [search_tool]

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
    )
})

# Print the Response
print(response["output"])