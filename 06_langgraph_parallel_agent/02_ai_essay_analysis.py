from langgraph.graph import StateGraph, START, END
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from typing import Annotated, TypedDict
from pydantic import BaseModel, Field
import operator

# Load the environment variables
load_dotenv()

# Define the LLM
llm = ChatOpenAI(model="gpt-4.1-mini", temperature=0)

class EvaluationCriteria(BaseModel):
    """Evaluation criteria for the essay"""
    feedback: str = Field(description="The feedback for the essay", min_length=10, max_length=1000)
    score: int = Field(description="The score for the essay out of 10", ge=0, le=10)

# Initialize the LLM with the structured output capability to return the EvaluationCriteria object
structured_llm = llm.with_structured_output(EvaluationCriteria)

class EssayState(TypedDict):
    """State for the essay analysis agent"""
    essay: str
    language_feedback: str
    analysis_feedback: str
    clarity_feedback: str
    overall_feedback: str
    individual_scores: Annotated[list[int], operator.add] # The scores for each individual criterion of the essay and add them up to get the total score
    average_score: float

def evaluate_language(state: EssayState) -> EssayState:
    """Evaluate the language quality and style of the essay"""
    prompt = f"Evaluate the language quality and style of the following essay and provide feedback on the essay also provide a score out of 10 for the language quality and style \n Essay: {state['essay']}"
    output = structured_llm.invoke(prompt)
    return {"language_feedback": output.feedback, "individual_scores": [output.score]}

def evaluate_analysis(state: EssayState) -> EssayState:
    """Evaluate the analysis of the essay"""
    prompt = f"Evaluate the analysis of the following essay and provide feedback on the analysis also provide a score out of 10 for the analysis: \n Essay: {state['essay']}"
    output = structured_llm.invoke(prompt)
    return {"analysis_feedback": output.feedback, "individual_scores": [output.score]}

def evaluate_clarity(state: EssayState) -> EssayState:
    """Evaluate the clarity of the essay"""
    prompt = f"Evaluate the clarity of the following essay and provide feedback on the clarity also provide a score out of 10 for the clarity: \n Essay: {state['essay']}"
    output = structured_llm.invoke(prompt)
    return {"clarity_feedback": output.feedback, "individual_scores": [output.score]}

def evaluate_overall(state: EssayState) -> EssayState:
    """Evaluate the overall quality of the essay"""
    prompt = f"Based on the following feedback for the essay, provide a overall feedback on the essay: \n Language Feedback: {state['language_feedback']} \n Analysis Feedback: {state['analysis_feedback']} \n Clarity Feedback: {state['clarity_feedback']}"
    output = structured_llm.invoke(prompt)
    average_score = sum(state["individual_scores"]) / len(state["individual_scores"])
    return {"overall_feedback": output.feedback, "average_score": round(average_score, 2)}

# Define the graph
build_graph = StateGraph(EssayState)

# Define the nodes
build_graph.add_node("evaluate_language", evaluate_language)
build_graph.add_node("evaluate_analysis", evaluate_analysis)
build_graph.add_node("evaluate_clarity", evaluate_clarity)
build_graph.add_node("evaluate_overall", evaluate_overall)

# Define the parallel nodes to evaluate the language, analysis, and clarity
build_graph.add_edge(START, "evaluate_language")
build_graph.add_edge(START, "evaluate_analysis")
build_graph.add_edge(START, "evaluate_clarity")

# Sequential nodes to evaluate the overall quality of the essay
build_graph.add_edge("evaluate_language", "evaluate_overall")
build_graph.add_edge("evaluate_analysis", "evaluate_overall")
build_graph.add_edge("evaluate_clarity", "evaluate_overall")

# Sequential node to generate the overall feedback and the average score
build_graph.add_edge("evaluate_overall", END)

# Compile the graph
graph = build_graph.compile()

# Main function
def main():
    """Main function to run the essay analysis agent"""
    print("Welcome to the essay analysis agent!")
    try:
        essay = input("Enter the essay: ")
        result = graph.invoke({"essay": essay})
        print("\nOverall Feedback: \n", result["overall_feedback"])
        print("\nLanguage Feedback: \n", result["language_feedback"])
        print("\nAnalysis Feedback: \n", result["analysis_feedback"])
        print("\nClarity Feedback: \n", result["clarity_feedback"])
        print("\nIndividual Scores: \n", result["individual_scores"])
        print("\nAverage Score: \n", result["average_score"])
    except Exception as e:
        print(f"Error: {e}")
    finally:
        print("\nThank you for using the essay analysis agent!")

# Run the main function
main()