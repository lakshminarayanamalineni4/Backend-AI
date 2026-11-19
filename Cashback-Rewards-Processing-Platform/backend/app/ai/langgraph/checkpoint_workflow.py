from typing import TypedDict

from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import END, START, StateGraph


class WorkflowState(TypedDict):
    query: str
    attempts: int
    status: str
    answer: str


def process_query(state: WorkflowState) -> WorkflowState:
    print("\n[PROCESS QUERY]")

    print(f"Query: {state['query']}")

    return {
        **state,
        "status": "processing",
    }


def process_request(state: WorkflowState) -> WorkflowState:
    print("\n[PROCESS REQUEST]")

    attempts = state["attempts"] + 1

    print(f"Attempt: {attempts}")

    return {
        **state,
        "attempts": attempts,
        "status": "completed",
        "answer": (
            "Cashback is credited within 48 hours "
            "after transaction settlement."
        ),
    }


def build_graph():

    builder = StateGraph(WorkflowState)

    builder.add_node(
        "process_query",
        process_query,
    )

    builder.add_node(
        "process_request",
        process_request,
    )

    builder.add_edge(
        START,
        "process_query",
    )

    builder.add_edge(
        "process_query",
        "process_request",
    )

    builder.add_edge(
        "process_request",
        END,
    )

    # Create an in-memory checkpointer.
    checkpointer = InMemorySaver()

    # Compile graph with checkpoint support.
    graph = builder.compile(
        checkpointer=checkpointer,
    )

    return graph


def main():

    graph = build_graph()

    config = {
        "configurable": {
            "thread_id": "cashback-user-001",
        }
    }

    initial_state: WorkflowState = {
        "query": "When will I receive my cashback?",
        "attempts": 0,
        "status": "created",
        "answer": "",
    }

    print("=" * 70)
    print("FIRST WORKFLOW EXECUTION")
    print("=" * 70)

    result = graph.invoke(
        initial_state,
        config=config,
    )

    print("\nFINAL STATE:")
    print(result)

    print("\n" + "=" * 70)
    print("CHECKPOINT STATE")
    print("=" * 70)

    checkpoint = graph.get_state(config)

    print(checkpoint)

    print("\n" + "=" * 70)
    print("THREAD ID")
    print("=" * 70)

    print(config["configurable"]["thread_id"])


if __name__ == "__main__":
    main()
    
# uv run python -m app.ai.langgraph.checkpoint_workflow    