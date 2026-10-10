from langgraph.graph import StateGraph, START, END
from typing import Literal, TypedDict

class ContentModerationState(TypedDict):
    """State for the content moderation workflow"""
    post_content: str
    user_reputation: str
    formatted_post: str
    content_flag: str
    result: str

def format_post_content(state: ContentModerationState) -> ContentModerationState:
    """Format the post content"""
    formatted_post = f"User ({state['user_reputation']}) posted the following content: {state['post_content']}"
    return {"formatted_post": formatted_post}

def analyze_content(state: ContentModerationState) -> ContentModerationState:
    """Analyze the content and flag the content if it is not appropriate"""
    content = state["post_content"].lower()
    if "hate" in content or "violence" in content or "sexual" in content or "nudity" in content:
        flag = "REJECTED"
    elif state["user_reputation"] == "low":
        flag = "FLAGGED_FOR_REVIEW"
    else:
        flag = "APPROVED"
    return {"content_flag": flag}

def approve_post(state: ContentModerationState) -> ContentModerationState:
    """Approve the post"""
    result = "Post is approved"
    return {"result": result}

def flag_for_review(state: ContentModerationState) -> ContentModerationState:
    """Flag the post for review due to low user reputation"""
    result = "Post is flagged for review due to low user reputation"
    return {"result": result}

def reject_post(state: ContentModerationState) -> ContentModerationState:
    """Reject the post due to inappropriate content"""
    result = "Post is rejected due to inappropriate content"
    return {"result": result}

def check_conditions(state: ContentModerationState) -> Literal["approve_post", "flag_for_review", "reject_post"]:
    """Check the content flag and return the appropriate node"""
    if state["content_flag"] == "APPROVED":
        return "approve_post"
    elif state["content_flag"] == "FLAGGED_FOR_REVIEW":
        return "flag_for_review"
    elif state["content_flag"] == "REJECTED":
        return "reject_post"

# Define the graph
build_graph = StateGraph(ContentModerationState)

# Define the nodes
build_graph.add_node("format_post_content", format_post_content)
build_graph.add_node("analyze_content", analyze_content)
build_graph.add_node("approve_post", approve_post)
build_graph.add_node("flag_for_review", flag_for_review)
build_graph.add_node("reject_post", reject_post)

# Define the edges
build_graph.add_edge(START, "format_post_content")
build_graph.add_edge("format_post_content", "analyze_content")
build_graph.add_conditional_edges("analyze_content", check_conditions)
build_graph.add_edge("approve_post", END)
build_graph.add_edge("flag_for_review", END)
build_graph.add_edge("reject_post", END)

# Build the graph
graph = build_graph.compile()

# Run the graph
initial_state = {
    "post_content": "Hi everyone, I am a new user and I am here to share my thoughts with you all.",
    "user_reputation": "low"
}
result = graph.invoke(initial_state)
print("Formatted Post: ", result["formatted_post"])
print("Content Flag: ", result["content_flag"])
print("Result: ", result["result"])