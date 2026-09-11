from langgraph.graph import StateGraph, START, END
from typing import TypedDict

class TemperatureState(TypedDict):
    """State for temperature conversion"""
    celsius: float
    fahrenheit: float

def convert_temp(state: TemperatureState) -> TemperatureState:
    """Convert Celsius to Fahrenheit"""
    return {
        "fahrenheit": (state["celsius"] * 9/5) + 32
    }

# Build the graph with the state type
graph_builder = StateGraph(TemperatureState)

# Add the node to the graph
graph_builder.add_node("convert_temp", convert_temp)

# Add the edges to the graph
graph_builder.add_edge(START, "convert_temp")
graph_builder.add_edge("convert_temp", END)

# Compile the graph
graph = graph_builder.compile()

# Invoke the graph with a Celsius temperature
temp_in_celsius = 40
result = graph.invoke({"celsius": temp_in_celsius})
print(f"{temp_in_celsius}°C is {result['fahrenheit']}°F")