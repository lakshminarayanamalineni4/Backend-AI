from typing_extensions import TypedDict

from langgraph.graph import END, START, StateGraph


# ============================================================
# SUBGRAPH STATE
# ============================================================


class ResearchState(TypedDict, total=False):
    query: str
    research_result: str
    analysis: str


# ============================================================
# SUBGRAPH NODE 1
# ============================================================


def research_node(state: ResearchState):
    """
    First node inside the Research Subgraph.
    """

    query = state["query"]

    print("\n[SUBGRAPH: RESEARCH]")

    print(f"Query: {query}")

    if "cashback" in query.lower():

        research_result = (
            "Cashback is credited within 48 hours "
            "after transaction settlement."
        )

    else:

        research_result = (
            "No specific cashback information was found."
        )

    return {
        "research_result": research_result,
    }


# ============================================================
# SUBGRAPH NODE 2
# ============================================================


def analysis_node(state: ResearchState):
    """
    Second node inside the Research Subgraph.

    Reads the output of research_node.
    """

    research_result = state.get(
        "research_result",
        "",
    )

    print("\n[SUBGRAPH: ANALYSIS]")

    print(
        f"Research result: {research_result}"
    )

    analysis = (
        f"The research result indicates: "
        f"{research_result}"
    )

    return {
        "analysis": analysis,
    }


# ============================================================
# BUILD RESEARCH SUBGRAPH
# ============================================================


research_builder = StateGraph(
    ResearchState
)


research_builder.add_node(
    "research",
    research_node,
)

research_builder.add_node(
    "analysis",
    analysis_node,
)


research_builder.add_edge(
    START,
    "research",
)

research_builder.add_edge(
    "research",
    "analysis",
)

research_builder.add_edge(
    "analysis",
    END,
)


# Compile the subgraph

research_subgraph = (
    research_builder.compile()
)


# ============================================================
# PARENT GRAPH STATE
# ============================================================


class ParentState(TypedDict, total=False):
    query: str
    research_result: str
    analysis: str
    final_answer: str


# ============================================================
# PARENT GRAPH
# ============================================================


def final_response_node(
    state: ParentState,
):
    """
    Node in the parent graph.

    It receives output produced by the subgraph.
    """

    print("\n[PARENT GRAPH: FINAL RESPONSE]")

    research_result = state.get(
        "research_result",
        "",
    )

    analysis = state.get(
        "analysis",
        "",
    )

    final_answer = (
        f"Research: {research_result}\n"
        f"Analysis: {analysis}"
    )

    return {
        "final_answer": final_answer,
    }


# ============================================================
# BUILD PARENT GRAPH
# ============================================================


parent_builder = StateGraph(
    ParentState
)


# Add the compiled subgraph as a node

parent_builder.add_node(
    "research_subgraph",
    research_subgraph,
)


parent_builder.add_node(
    "final_response",
    final_response_node,
)


# ============================================================
# PARENT GRAPH EDGES
# ============================================================


parent_builder.add_edge(
    START,
    "research_subgraph",
)

parent_builder.add_edge(
    "research_subgraph",
    "final_response",
)

parent_builder.add_edge(
    "final_response",
    END,
)


# Compile parent graph

parent_graph = (
    parent_builder.compile()
)


# ============================================================
# TEST
# ============================================================


if __name__ == "__main__":

    print("=" * 70)
    print("SUBGRAPH WORKFLOW")
    print("=" * 70)

    result = parent_graph.invoke(
        {
            "query": (
                "When will I receive my cashback?"
            )
        }
    )

    print("\n" + "=" * 70)
    print("FINAL STATE")
    print("=" * 70)

    print(result)

    print("\n" + "=" * 70)
    print("FINAL ANSWER")
    print("=" * 70)

    print(
        result["final_answer"]
    )
# uv run python -m app.ai.langgraph.subgraph_workflow