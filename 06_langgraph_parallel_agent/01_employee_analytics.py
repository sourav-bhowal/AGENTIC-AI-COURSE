from langgraph.graph import StateGraph, START, END
from typing import TypedDict
from dotenv import load_dotenv

# Load the environment variables
load_dotenv()

class EmployeeState(TypedDict):
    """State for the employee analytics agent"""
    employee_id: str
    employee_name: str
    monthly_salary: int
    working_hours: int
    completed_tasks: int

    yearly_salary: int
    bonus: int
    project_status: str
    summary: str

def calculate_yearly_salary(state: EmployeeState) -> EmployeeState:
    """Calculate the yearly salary of the employee based on the monthly salary"""
    yearly_salary = state["monthly_salary"] * 12
    return {"yearly_salary": yearly_salary}

def project_evaluation(state: EmployeeState) -> EmployeeState:
    """Evaluate the project status of the employee based on the completed tasks and the working hours"""
    project_status = "On time" if state["completed_tasks"] / state["working_hours"] > 0.9 else "Late"
    return {"project_status": project_status}

def calculate_bonus(state: EmployeeState) -> EmployeeState:
    """Calculate the bonus of the employee based on the yearly salary"""
    bonus = state["yearly_salary"] * 0.02 if state["project_status"] == "On time" else 0
    return {"bonus": bonus}

def summary(state: EmployeeState) -> EmployeeState:
    """Generate a summary of the employee's performance"""
    summary = f"The employee {state['employee_name']} has a yearly salary of {state['yearly_salary']} and a bonus of {state['bonus']}. The project status is {state['project_status']}."
    return {"summary": summary}

# Build the graph
build_graph = StateGraph(EmployeeState)

# Add the nodes to the graph
build_graph.add_node("calculate_yearly_salary", calculate_yearly_salary)
build_graph.add_node("calculate_bonus", calculate_bonus)
build_graph.add_node("project_evaluation", project_evaluation)
build_graph.add_node("summary", summary)

# Add the edges to the graph
# Parallel nodes to calculate the yearly salary and the project status
build_graph.add_edge(START, "calculate_yearly_salary")
build_graph.add_edge(START, "project_evaluation")

# Sequential nodes to calculate the bonus based on the project status and the yearly salary
build_graph.add_edge("calculate_yearly_salary", "calculate_bonus")
build_graph.add_edge("project_evaluation", "calculate_bonus")
build_graph.add_edge("calculate_bonus", "summary")

# Final node to generate the summary
build_graph.add_edge("summary", END)

# Compile the graph
graph = build_graph.compile()

# Main function
def main():
    """Main function to run the employee analytics agent"""
    print("Welcome to the employee analytics agent!")
    try:
        employee_id = input("Enter the employee ID: ")
        employee_name = input("Enter the employee name: ")
        monthly_salary = int(input("Enter the monthly salary: "))
        working_hours = int(input("Enter the working hours: "))
        completed_tasks = int(input("Enter the completed tasks: "))

        _state = {
            "employee_id": employee_id,
            "employee_name": employee_name,
            "monthly_salary": monthly_salary,
            "working_hours": working_hours,
            "completed_tasks": completed_tasks
        }
        result = graph.invoke(_state)
        print(f"Yearly Salary: {result['yearly_salary']}")
        print(f"Bonus: {result['bonus']}")
        print(f"Project Status: {result['project_status']}")
        print(f"Summary: {result['summary']}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        print("Thank you for using the employee analytics agent!")

# Run the main function
main()