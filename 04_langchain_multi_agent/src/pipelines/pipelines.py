from langchain_core.messages import ToolMessage
from src.agents.agents import build_search_agent, build_reader_agent, writer_chain, critic_chain

def extract_tool_outputs(messages) -> str:
    """Prefer raw tool outputs (Title/URL/Snippet) over the agent's final summary."""
    tool_contents = [
        msg.content for msg in messages
        if isinstance(msg, ToolMessage) and msg.content
    ]
    if tool_contents:
        return "\n\n".join(tool_contents)
    return messages[-1].content if messages else ""


def run_research_pipeline(topic: str) -> dict:

    # Initialize the state
    state = {}

    print("\n"+" ="*50)
    print("step 1 - search agent is working ...")
    print("="*50)

    # 1st Search Agent - This agent is used to search the web and gather research
    search_agent = build_search_agent()

    # Invoke the search agent to search the web and gather research
    search_result = search_agent.invoke({
        "messages": [("user", (
            f"Search the web for information on the topic: {topic}. "
            "Return the search tool results exactly as Title, URL, and Snippet. "
            "Do not summarize or omit URLs."
        ))],
    })

    # Store raw tool search results (Title/URL/Snippet), not the agent's paraphrase
    state["search_results"] = extract_tool_outputs(search_result["messages"])

    # Print the search results
    print("\n Search Results: \n", state["search_results"])

    print("\n"+" ="*50)
    print("step 2 - reader agent is working ...")
    print("="*50)

    # 2nd Reader Agent - This agent is used to scrape the content of a given url and gather research
    reader_agent = build_reader_agent()

    # Invoke the reader agent to scrape the content of a given url and gather research
    reader_result = reader_agent.invoke({
        "messages": [("user", 
            f"Based on the following search results about '{topic}', "
            f"scrape the most relevant URLs listed below (use only these URLs, do not invent any). "
            f"Gather deeper research content from them.\n\n"
            f"Search Results: \n{state['search_results']}"
        )],
    })

    # Store the reader results in the state
    state["reader_results"] = reader_result["messages"][-1].content

    # Print the reader results
    print("\n Reader Results: \n", state["reader_results"])

    print("\n"+" ="*50)
    print("step 3 - writer agent is working ...")
    print("="*50)

    # 3rd Writer Prompt - This prompt is used to write the report based on the topic and research gathered by the reader agent
    research_combined = (
        f"Search Results: \n{state['search_results']} \n\n"
        f"Detailed Research Content: \n{state['reader_results']}"
    )

    # Invoke the writer chain to write the report based on the topic and research gathered by the reader agent
    state["report"] = writer_chain.invoke({
        "topic": topic,
        "research": research_combined,
    })

    # Print the report
    print("\n Report: \n", state["report"])

    print("\n"+" ="*50)
    print("step 4 - critic agent is working ...")
    print("="*50)

    # 4th Critic Agent - This agent is used to critique the report based on the topic and research gathered by the reader agent
    state["feedback"] = critic_chain.invoke({
        "report": state["report"],
    })

    # Print the feedback
    print("\n Feedback: \n", state["feedback"])

    print("\n"+" ="*50)
    print("Research Pipeline Completed")
    print("="*50)

    # Return the state
    return state