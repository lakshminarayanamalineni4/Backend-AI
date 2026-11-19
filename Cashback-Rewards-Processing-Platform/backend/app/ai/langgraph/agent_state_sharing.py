from typing_extensions import TypedDict

from langgraph.graph import END, START, StateGraph


# ============================================================
# SHARED STATE
# ============================================================


class AgentState(TypedDict, total=False):
    query: str
    research_result: str
    analysis: str
    final_answer: str


# ============================================================
# RESEARCH AGENT
# ============================================================


def research_agent(state: AgentState):
    """
    First agent.

    Reads:
        query

    Writes:
        research_result
    """

    query = state["query"]

    print("\n[RESEARCH AGENT]")
    print(f"Query: {query}")

    # In a real application this could call:
    #
    # - RAG
    # - Web search
    # - Database
    # - External API
    #
    # For now, we use a simple isolated result.

    if "cashback" in query.lower():

        research_result = (
            "Cashback is credited within 48 hours "
            "after successful transaction settlement."
        )

    else:

        research_result = (
            "No specialised cashback information "
            "was found."
        )

    print(f"Research result: {research_result}")

    return {
        "research_result": research_result,
    }


# ============================================================
# ANALYSIS AGENT
# ============================================================


def analysis_agent(state: AgentState):
    """
    Second agent.

    Reads:
        query
        research_result

    Writes:
        analysis
    """

    query = state["query"]

    research_result = state.get(
        "research_result",
        "",
    )

    print("\n[ANALYSIS AGENT]")

    print(
        f"Received research result: "
        f"{research_result}"
    )

    if research_result:

        analysis = (
            f"The research information directly addresses "
            f"the user's question: '{query}'. "
            f"The key information is: {research_result}"
        )

    else:

        analysis = (
            "The research agent did not provide "
            "sufficient information."
        )

    print(f"Analysis: {analysis}")

    return {
        "analysis": analysis,
    }


# ============================================================
# RESPONSE AGENT
# ============================================================


def response_agent(state: AgentState):
    """
    Final agent.

    Reads:
        query
        research_result
        analysis

    Writes:
        final_answer
    """

    query = state["query"]

    research_result = state.get(
        "research_result",
        "",
    )

    analysis = state.get(
        "analysis",
        "",
    )

    print("\n[RESPONSE AGENT]")

    print(f"Original query: {query}")

    print(
        f"Received research: "
        f"{research_result}"
    )

    print(
        f"Received analysis: "
        f"{analysis}"
    )

    final_answer = (
        f"Based on the available information: "
        f"{research_result}"
    )

    return {
        "final_answer": final_answer,
    }


# ============================================================
# BUILD GRAPH
# ============================================================


builder = StateGraph(AgentState)


# Add agents as nodes

builder.add_node(
    "research_agent",
    research_agent,
)

builder.add_node(
    "analysis_agent",
    analysis_agent,
)

builder.add_node(
    "response_agent",
    response_agent,
)


# ============================================================
# CONNECT WORKFLOW
# ============================================================


builder.add_edge(
    START,
    "research_agent",
)

builder.add_edge(
    "research_agent",
    "analysis_agent",
)

builder.add_edge(
    "analysis_agent",
    "response_agent",
)

builder.add_edge(
    "response_agent",
    END,
)


# Compile

graph = builder.compile()


# ============================================================
# TEST
# ============================================================


if __name__ == "__main__":

    query = "When will I receive my cashback?"

    print("=" * 70)
    print("MULTI-AGENT STATE SHARING WORKFLOW")
    print("=" * 70)

    result = graph.invoke(
        {
            "query": query,
        }
    )

    print("\n" + "=" * 70)
    print("FINAL STATE")
    print("=" * 70)

    print(result)

    print("\n" + "=" * 70)
    print("FINAL ANSWER")
    print("=" * 70)

    print(result["final_answer"])