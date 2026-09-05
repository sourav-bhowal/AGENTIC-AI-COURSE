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
search_tool = TavilySearchResults(max_results=2)

# Initialize the LLM
llm = ChatOpenAI(model="gpt-4.1-mini", temperature=0, api_key=OPENAI_API_KEY)

# Get the React Agent Prompt
prompt = hub.pull("hwchase17/react")    # prompt is the prompt for the Agent we get it from the LangChain Hub

# Tools for the Agent
tools = [search_tool]

# Create the Agent
agent = create_react_agent(llm=llm, tools=tools, prompt=prompt) # prompt is the prompt for the Agent

# Execute the Agent
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)  # verbose=True to see the Agent's thinking process

# Run the Agent 
response = agent_executor.invoke({
    "input": (
        "Latest news about US and Iran War? Also provide the time and date of the news."
    )
})

# Print the Response
print(response["output"])