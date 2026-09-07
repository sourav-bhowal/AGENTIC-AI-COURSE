from src.agents.agents import build_search_agent, build_reader_agent, writer_chain, critic_chain

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
        "messages": [("user", f"Search the web for information on the topic: {topic}")],
    })

    # Store the search results in the state
    state["search_results"] = search_result["messages"][-1].content

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
            f"scrape the content of the most relevant urls and gather research. \n\n"
            f"Search Results: \n{state['search_results'][:800]}"
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