from typing import TypedDict

from langchain_core.tools import tool
from langgraph.graph import END, START, StateGraph


# ============================================================
# 1. LANGCHAIN TOOL
# ============================================================

@tool
def get_cashback_limit() -> str:
    """Get the maximum cashback allowed per transaction."""
    return "The maximum cashback per transaction is ₹500."


# ============================================================
# 2. LANGGRAPH STATE
# ============================================================

class ToolCallingState(TypedDict):
    query: str
    route: str
    tool_result: str
    answer: str


# ============================================================
# 3. ROUTER NODE
# ============================================================

def router_node(state: ToolCallingState):
    """
    Determine whether the user query is a cashback-related query
    or a general question.
    """

    query = state["query"].lower()

    cashback_keywords = [
        "cashback",
        "reward",
        "maximum cashback",
        "cashback limit",
    ]

    is_cashback_question = any(
        keyword in query
        for keyword in cashback_keywords
    )

    if is_cashback_question:
        route = "cashback"
    else:
        route = "general"

    print(f"\n[ROUTER]")
    print(f"Query: {state['query']}")
    print(f"Route: {route}")

    return {
        "route": route
    }


# ============================================================
# 4. CASHBACK TOOL NODE
# ============================================================

def cashback_tool_node(state: ToolCallingState):
    """
    Execute the LangChain cashback tool.
    """

    print("\n[CASHBACK TOOL]")

    result = get_cashback_limit.invoke({})

    print(f"Tool result: {result}")

    return {
        "tool_result": result
    }


# ============================================================
# 5. GENERAL ANSWER NODE
# ============================================================

def general_answer_node(state: ToolCallingState):
    """
    Generate a response for a general question.

    This is intentionally simple because the focus is
    LangGraph tool orchestration, not LLM generation.
    """

    print("\n[GENERAL ANSWER]")

    answer = (
        "This is a general question. "
        "No cashback tool was required."
    )

    return {
        "answer": answer
    }


# ============================================================
# 6. CASHBACK ANSWER NODE
# ============================================================

def cashback_answer_node(state: ToolCallingState):
    """
    Generate the final answer using the tool result.
    """

    print("\n[CASHBACK ANSWER]")

    answer = (
        f"According to the cashback system: "
        f"{state['tool_result']}"
    )

    return {
        "answer": answer
    }


# ============================================================
# 7. CONDITIONAL ROUTING FUNCTION
# ============================================================

def route_after_router(state: ToolCallingState):
    """
    Decide which node should execute after the router.
    """

    if state["route"] == "cashback":
        return "cashback_tool"

    return "general_answer"


# ============================================================
# 8. BUILD GRAPH
# ============================================================

builder = StateGraph(ToolCallingState)


# Add nodes

builder.add_node(
    "router",
    router_node,
)

builder.add_node(
    "cashback_tool",
    cashback_tool_node,
)

builder.add_node(
    "cashback_answer",
    cashback_answer_node,
)

builder.add_node(
    "general_answer",
    general_answer_node,
)


# ============================================================
# 9. DEFINE EDGES
# ============================================================

builder.add_edge(
    START,
    "router",
)


builder.add_conditional_edges(
    "router",
    route_after_router,
    {
        "cashback_tool": "cashback_tool",
        "general_answer": "general_answer",
    },
)


builder.add_edge(
    "cashback_tool",
    "cashback_answer",
)


builder.add_edge(
    "cashback_answer",
    END,
)


builder.add_edge(
    "general_answer",
    END,
)


# ============================================================
# 10. COMPILE GRAPH
# ============================================================

graph = builder.compile()


# ============================================================
# 11. TEST WORKFLOW
# ============================================================

if __name__ == "__main__":

    print("=" * 70)
    print("LANGGRAPH TOOL CALLING WORKFLOW")
    print("=" * 70)

    # --------------------------------------------------------
    # TEST 1: CASHBACK QUESTION
    # --------------------------------------------------------

    print("\n")
    print("=" * 70)
    print("TEST 1: CASHBACK QUESTION")
    print("=" * 70)

    result = graph.invoke(
        {
            "query": "What is the maximum cashback?",
            "route": "",
            "tool_result": "",
            "answer": "",
        }
    )

    print("\nFINAL RESULT")
    print(result)


    # --------------------------------------------------------
    # TEST 2: GENERAL QUESTION
    # --------------------------------------------------------

    print("\n")
    print("=" * 70)
    print("TEST 2: GENERAL QUESTION")
    print("=" * 70)

    result = graph.invoke(
        {
            "query": "What is the capital of France?",
            "route": "",
            "tool_result": "",
            "answer": "",
        }
    )

    print("\nFINAL RESULT")
    print(result)