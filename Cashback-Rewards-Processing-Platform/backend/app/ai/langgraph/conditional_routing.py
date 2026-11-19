from typing import TypedDict

from langgraph.graph import END, START, StateGraph


class WorkflowState(TypedDict):
    input: str
    result: str
    status: str
    message: str


def process_input(state: WorkflowState) -> WorkflowState:
    """Process the incoming input."""

    user_input = state["input"]

    if user_input.strip():
        return {
            **state,
            "result": user_input.strip(),
            "status": "success",
        }

    return {
        **state,
        "result": "",
        "status": "failure",
    }


def check_result(state: WorkflowState) -> str:
    """Decide which node should execute next."""

    if state["status"] == "success":
        return "success"

    return "failure"


def success_node(state: WorkflowState) -> WorkflowState:
    """Handle successful processing."""

    return {
        **state,
        "message": f"Successfully processed: {state['result']}",
    }


def failure_node(state: WorkflowState) -> WorkflowState:
    """Handle failed processing."""

    return {
        **state,
        "message": "Processing failed because the input was empty.",
    }


# Create graph
builder = StateGraph(WorkflowState)

# Add nodes
builder.add_node("process_input", process_input)
builder.add_node("success_node", success_node)
builder.add_node("failure_node", failure_node)

# Normal edge
builder.add_edge(START, "process_input")

# Conditional routing
builder.add_conditional_edges(
    "process_input",
    check_result,
    {
        "success": "success_node",
        "failure": "failure_node",
    },
)

# End edges
builder.add_edge("success_node", END)
builder.add_edge("failure_node", END)

# Compile graph
graph = builder.compile()


if __name__ == "__main__":
    print("\n=== SUCCESS CASE ===")

    success_result = graph.invoke(
        {
            "input": "How long does cashback take?",
            "result": "",
            "status": "",
            "message": "",
        }
    )

    print(success_result)

    print("\n=== FAILURE CASE ===")

    failure_result = graph.invoke(
        {
            "input": "",
            "result": "",
            "status": "",
            "message": "",
        }
    )

    print(failure_result)
    
# uv run python -m app.ai.langgraph.conditional_routing
