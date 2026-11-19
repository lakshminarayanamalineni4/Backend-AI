from typing import TypedDict

from langgraph.graph import END, START, StateGraph


class WorkflowState(TypedDict):
    original_query: str
    current_query: str
    retrieved_documents: list[str]
    relevance_score: float
    attempts: int
    answer: str


def process_query(state: WorkflowState) -> WorkflowState:
    """
    Initialize the workflow with the user's original query.
    """

    print("\n[PROCESS QUERY]")
    print(f"Original query: {state['original_query']}")

    return {
        **state,
        "current_query": state["original_query"],
    }


def retrieve(state: WorkflowState) -> WorkflowState:
    """
    Simulate document retrieval.

    For this exercise, we intentionally simulate poor
    retrieval for the first query and better retrieval
    after rewriting.
    """

    query = state["current_query"]
    attempts = state["attempts"] + 1

    print("\n[RETRIEVE]")
    print(f"Query: {query}")
    print(f"Attempt: {attempts}")

    if "money back" in query.lower():
        documents = [
            "General refund information",
            "Payment processing information",
        ]

        relevance_score = 0.30

    else:
        documents = [
            "Cashback is credited within 48 hours after transaction settlement.",
            "Cashback rewards policy",
        ]

        relevance_score = 0.95

    return {
        **state,
        "retrieved_documents": documents,
        "relevance_score": relevance_score,
        "attempts": attempts,
    }


def check_relevance(state: WorkflowState) -> str:
    """
    Decide whether the retrieved documents are relevant enough.
    """

    print("\n[CHECK RELEVANCE]")
    print(f"Relevance score: {state['relevance_score']}")

    if state["relevance_score"] >= 0.80:
        print("Result: RELEVANT")
        return "relevant"

    print("Result: NOT RELEVANT")

    if state["attempts"] >= 3:
        print("Maximum attempts reached.")
        return "max_retries"

    return "not_relevant"


def rewrite_query(state: WorkflowState) -> WorkflowState:
    """
    Simulate query rewriting.

    In the real application this would call Gemini.
    """

    print("\n[REWRITE QUERY]")

    rewritten_query = (
        "How long does it take to receive my cashback?"
    )

    print(f"Rewritten query: {rewritten_query}")

    return {
        **state,
        "current_query": rewritten_query,
    }


def generate_answer(state: WorkflowState) -> WorkflowState:
    """
    Simulate final answer generation.
    """

    print("\n[GENERATE ANSWER]")

    answer = (
        "Cashback is credited within 48 hours "
        "after transaction settlement."
    )

    return {
        **state,
        "answer": answer,
    }


def build_graph():

    builder = StateGraph(WorkflowState)

    # Add nodes
    builder.add_node("process_query", process_query)
    builder.add_node("retrieve", retrieve)
    builder.add_node("rewrite_query", rewrite_query)
    builder.add_node("generate_answer", generate_answer)

    # START → Process Query
    builder.add_edge(
        START,
        "process_query",
    )

    # Process Query → Retrieve
    builder.add_edge(
        "process_query",
        "retrieve",
    )

    # Retrieve → Conditional Routing
    builder.add_conditional_edges(
        "retrieve",
        check_relevance,
        {
            "relevant": "generate_answer",
            "not_relevant": "rewrite_query",
            "max_retries": END,
        },
    )

    # Rewrite Query → Retrieve
    #
    # This creates the loop.
    builder.add_edge(
        "rewrite_query",
        "retrieve",
    )

    # Generate Answer → END
    builder.add_edge(
        "generate_answer",
        END,
    )

    return builder.compile()


def main():

    graph = build_graph()

    initial_state: WorkflowState = {
        "original_query": "when do I get my money back?",
        "current_query": "",
        "retrieved_documents": [],
        "relevance_score": 0.0,
        "attempts": 0,
        "answer": "",
    }

    result = graph.invoke(initial_state)

    print("\n" + "=" * 70)
    print("FINAL RESULT")
    print("=" * 70)

    print(f"Original Query: {result['original_query']}")
    print(f"Final Query: {result['current_query']}")
    print(f"Attempts: {result['attempts']}")
    print(f"Answer: {result['answer']}")


if __name__ == "__main__":
    main()
    
    
# uv run python -m app.ai.langgraph.retry_workflow    