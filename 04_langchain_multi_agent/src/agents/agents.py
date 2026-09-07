from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from src.tools.tools import web_search, web_scrape
from dotenv import load_dotenv

load_dotenv()

# Initialize the LLM
llm = ChatOpenAI(model="gpt-4.1-mini", temperature=0)

# 1st Search Agent - This agent is used to search the web and gather research
def build_search_agent():
    return create_agent(
        model=llm,
        tools=[web_search],
    )

# 2nd Reader Agent - This agent is used to scrape the content of a given url and gather research
def build_reader_agent():
    return create_agent(
        model=llm,
        tools=[web_scrape],
    )
        
# 3rd Writer Prompt - This prompt is used to write the report based on the topic and research gathered by the reader agent
writer_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an expert writer. Write clean, structured, and insightful reports"),
    ("human", f"""
        Write a detailed research report on the following topic below.

        Topic: {topic}

        Research Gathered: {research}

        Structure the report in the following format:
        - Introduction
        - Key Findings (3-5 key findings)
        - Conclusion
        - References (list of sources used in urls format)

        Be detailed and thorough in your report.
    """)
])

# Writer Chain - It will write the report based on the topic and research gathered
writer_chain = writer_prompt | llm | StrOutputParser()

# 4th Critic Prompt - This prompt is used to critique the report based on the topic and research gathered by the reader agent
critic_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an expert critic. Critique the report based on the topic and research gathered by the reader agent"),
    ("human", f"""
        Critique the report based on the topic and research gathered by the reader agent

        Report: {report}

        Critique the report in the following format:
        Score: X/10
        Strengths:
        - ...
        - ...
        Weaknesses:
        - ...
        - ...
        Improvements:
        - ...
        - ...
        One line verdict:
        ...
    """)
])

# Critic Chain - It will critique the report based on the topic and research gathered by the reader agent
critic_chain = critic_prompt | llm | StrOutputParser()