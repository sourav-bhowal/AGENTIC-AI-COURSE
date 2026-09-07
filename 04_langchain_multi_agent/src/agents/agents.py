from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from src.tools.tools import web_search, web_scrape
from dotenv import load_dotenv

load_dotenv()

# Initialize the LLM
llm = ChatOpenAI(model="gpt-4.1-mini", temperature=0)

# Search Agent
def build_search_agent():
    return create_agent(
        model=llm,
        tools=[web_search],
    )

# Scrape Agent
def build_scrape_agent():
    return create_agent(
        model=llm,
        tools=[web_scrape],
    )
        