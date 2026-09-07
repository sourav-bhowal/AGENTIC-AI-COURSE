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
    ("system", "You are an expert research writer. Write clear, structured and insightful reports."),
    ("human", """Write a detailed research report on the topic below.

    Topic: {topic}

    Research Gathered:
    {research}

    Structure the report as:
    - Introduction
    - Key Findings (minimum 3 well-explained points)
    - Conclusion
    - Sources (list all URLs found in the research)

    Be detailed, factual and professional."""),
])

# Writer Chain - It will write the report based on the topic and research gathered
writer_chain = writer_prompt | llm | StrOutputParser()

# 4th Critic Prompt - This prompt is used to critique the report based on the topic and research gathered by the reader agent
critic_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a sharp and constructive research critic. Be honest and specific."),
    ("human", """Review the research report below and evaluate it strictly.

    Report:
    {report}

    Respond in this exact format:

    Score: X/10

    Strengths:
    - ...
    - ...

    Areas to Improve:
    - ...
    - ...

    One line verdict:
    ..."""),
])

# Critic Chain - It will critique the report based on the topic and research gathered by the reader agent
critic_chain = critic_prompt | llm | StrOutputParser()