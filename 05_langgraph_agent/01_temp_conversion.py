from langgraph.graph import StateGraph, START, END
from typing import TypedDict

class TemperatureState(TypedDict):
    """State for temperature conversion"""
    celsius: float
    fahrenheit: float
    weather: str

def convert_temp(state: TemperatureState) -> TemperatureState:
    """Convert Celsius to Fahrenheit and round to 2 decimal places"""
    fahrenheit = (state["celsius"] * 9/5) + 32
    return {"fahrenheit": round(fahrenheit, 2)}

def weather_report(state: TemperatureState) -> TemperatureState:
    """Generate a weather report based on the temperature"""
    if state["fahrenheit"] > 80:
        return {"weather": "It's hot outside!"}
    elif state["fahrenheit"] < 50:
        return {"weather": "It's cold outside!"}
    else:
        return {"weather": "It's a nice day outside!"}

# Build the graph with the state type
graph_builder = StateGraph(TemperatureState)

# Add the node to the graph
graph_builder.add_node("convert_temp", convert_temp)
graph_builder.add_node("weather_report", weather_report)

# Add the edges to the graph
graph_builder.add_edge(START, "convert_temp")
graph_builder.add_edge("convert_temp", "weather_report")
graph_builder.add_edge("weather_report", END)

# Compile the graph
graph = graph_builder.compile()

# Main function
def main():
    print("Welcome to the temperature conversion and weather report agent!")
    while True:
        try:
            temp_in_celsius = float(input("Enter the temperature in Celsius: "))
            # Invoke the graph with the temperature
            result = graph.invoke({"celsius": temp_in_celsius})
            # Print the results
            print(f"{temp_in_celsius}°C is {result['fahrenheit']}°F")
            print(f"Weather report: {result['weather']}")
        except ValueError:
            print("Invalid input. Please enter a valid temperature.")
        finally:
            print("\nThank you for using the temperature conversion and weather report agent!")
            break

# Run the main function
main()