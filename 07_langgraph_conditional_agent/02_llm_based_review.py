from langgraph.graph import StateGraph, START, END
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from typing import Literal, TypedDict
from pydantic import BaseModel, Field

# Load the environment variables
load_dotenv()

# Define the LLM
llm = ChatOpenAI(model="gpt-4.1-mini", temperature=0)

class SentimentSchema(BaseModel):
    """Schema for the sentiment of the review returned by the LLM"""
    sentiment: Literal["positive", "negative"] = Field(description="Sentiment of the review")

class DiagnosisSchema(BaseModel):
    """Schema for the diagnosis of the review returned by the LLM"""
    issue_type: Literal["UX", "Performance", "Bug", "Accessibility", "Security", "Other"] = Field(description="Type of issue in the review")
    tone: Literal["Friendly", "Professional", "Formal", "Casual", "Angry"] = Field(description="Tone of the review")
    urgency: Literal["Low", "Medium", "High"] = Field(description="Urgency of the review")

# Define the structured LLM
sentiment_llm = llm.with_structured_output(SentimentSchema)
diagnosis_llm = llm.with_structured_output(DiagnosisSchema)

class ReviewState(TypedDict):
    """State for the review"""
    review: str
    sentiment: Literal["positive", "negative"]
    diagnosis: dict
    response: str

def find_sentiment(state: ReviewState) -> ReviewState:
    """Find the sentiment of the review"""
    prompt = f"Find the sentiment of the following review: {state['review']}"
    sentiment = sentiment_llm.invoke(prompt).sentiment
    return {"sentiment": sentiment}

def positive_response(state: ReviewState) -> ReviewState:
    """Generate a positive response to the review"""
    prompt = f"Generate a positive response to the following review: {state['review']}"
    response = llm.invoke(prompt).content
    return {"response": response}

def run_diagnosis(state: ReviewState) -> ReviewState:
    """Run the diagnosis on the negative review"""
    prompt = f"Diagnose the following negative review: {state['review']} and the sentiment is: {state['sentiment']}"
    diagnosis = diagnosis_llm.invoke(prompt)
    return {"diagnosis": diagnosis.model_dump()}

def negative_response(state: ReviewState) -> ReviewState:
    """Generate a negative response to the review"""
    prompt = f"Generate a negative response to the following review: {state['review']} and the diagnosis is: {state['diagnosis']}"
    response = llm.invoke(prompt).content
    return {"response": response}

def check_sentiment(state: ReviewState) -> Literal["positive_response", "run_diagnosis"]:
    """Check the sentiment of the review and return the appropriate node"""
    if state["sentiment"] == "positive":
        return "positive_response"
    elif state["sentiment"] == "negative":
        return "run_diagnosis"

# Define the graph
build_graph = StateGraph(ReviewState)

# Define the nodes
build_graph.add_node("find_sentiment", find_sentiment)
build_graph.add_node("positive_response", positive_response)
build_graph.add_node("run_diagnosis", run_diagnosis)
build_graph.add_node("negative_response", negative_response)

# Define the edges with the conditional logic
build_graph.add_edge(START, "find_sentiment")
build_graph.add_conditional_edges("find_sentiment", check_sentiment)
build_graph.add_edge("positive_response", END)
build_graph.add_edge("run_diagnosis", "negative_response")
build_graph.add_edge("negative_response", END)

# Compile the graph
graph = build_graph.compile()

# Run the graph
initial_state = {
    "review": "I hate the product! It's so hard to use and the customer service is terrible."
}

# Run the graph
result = graph.invoke(initial_state)
print(result)