from typing import Literal

from langgraph.graph import END, START, StateGraph
from typing_extensions import TypedDict


# ============================================================
# STATE
# ============================================================


class MultiAgentState(TypedDict, total=False):
    query: str
    route: str
    agent_result: str
    final_answer: str


# ============================================================
# SUPERVISOR
# ============================================================


def supervisor_node(state: MultiAgentState):
    """
    Decide which specialized agent should handle the query.

    In a production system, this could be an LLM-based
    supervisor. For this isolated exercise, we use simple
    keyword routing so the LangGraph architecture is clear.
    """

    query = state["query"].lower()

    if "cashback" in query or "cash back" in query:
        route = "rewards"

    elif any(
        keyword in query
        for keyword in [
            "policy",
            "eligibility",
            "reward policy",
            "documentation",
        ]
    ):
        route = "rag"

    else:
        route = "general"

    print(f"\n[SUPERVISOR]")
    print(f"Query: {state['query']}")
    print(f"Selected agent: {route}")

    return {
        "route": route,
    }


# ============================================================
# REWARDS AGENT
# ============================================================


def rewards_agent_node(state: MultiAgentState):
    """
    Specialized agent responsible for cashback/rewards questions.

    In the real project, this agent could call existing cashback
    APIs or tools.
    """

    query = state["query"].lower()

    print("\n[REWARDS AGENT]")

    if "when" in query or "how long" in query:
        result = (
            "Cashback is credited within 48 hours "
            "after transaction settlement."
        )

    elif "maximum" in query or "max" in query:
        result = (
            "The maximum cashback amount is "
            "£500 per transaction."
        )

    else:
        result = (
            "The Rewards Agent received the query "
            "but no specific cashback policy was found."
        )

    return {
        "agent_result": result,
    }


# ============================================================
# RAG AGENT
# ============================================================


def rag_agent_node(state: MultiAgentState):
    """
    Specialized agent responsible for knowledge/document questions.

    This is intentionally mocked.

    In the real architecture, this node could call:

    Existing RAG Service
        ↓
    Query Rewriting
        ↓
    FAISS + BM25
        ↓
    Hybrid Search
        ↓
    RRF
        ↓
    Cross-Encoder
        ↓
    Context
        ↓
    Gemini
    """

    print("\n[RAG AGENT]")

    result = (
        "The RAG Agent would retrieve relevant enterprise "
        "knowledge using the existing RAG pipeline."
    )

    return {
        "agent_result": result,
    }


# ============================================================
# GENERAL AGENT
# ============================================================


def general_agent_node(state: MultiAgentState):
    """
    General-purpose agent for questions that do not require
    specialized RAG or rewards capabilities.
    """

    print("\n[GENERAL AGENT]")

    result = (
        f"The General Agent handled the question: "
        f"{state['query']}"
    )

    return {
        "agent_result": result,
    }


# ============================================================
# ROUTER
# ============================================================


def route_to_agent(
    state: MultiAgentState,
) -> Literal["rag", "rewards", "general"]:
    """
    Route the workflow to the selected specialized agent.
    """

    return state["route"]


# ============================================================
# FINAL RESPONSE AGENT
# ============================================================


def final_response_node(state: MultiAgentState):
    """
    Combine the worker-agent result into the final response.

    In production, this could be another LLM call responsible
    for generating a user-friendly final response.
    """

    print("\n[FINAL RESPONSE AGENT]")

    return {
        "final_answer": state["agent_result"],
    }


# ============================================================
# BUILD GRAPH
# ============================================================


builder = StateGraph(MultiAgentState)


# Add nodes

builder.add_node(
    "supervisor",
    supervisor_node,
)

builder.add_node(
    "rag_agent",
    rag_agent_node,
)

builder.add_node(
    "rewards_agent",
    rewards_agent_node,
)

builder.add_node(
    "general_agent",
    general_agent_node,
)

builder.add_node(
    "final_response",
    final_response_node,
)


# ============================================================
# EDGES
# ============================================================


# START → Supervisor

builder.add_edge(
    START,
    "supervisor",
)


# Supervisor → selected worker

builder.add_conditional_edges(
    "supervisor",
    route_to_agent,
    {
        "rag": "rag_agent",
        "rewards": "rewards_agent",
        "general": "general_agent",
    },
)


# Worker agents → Final Response

builder.add_edge(
    "rag_agent",
    "final_response",
)

builder.add_edge(
    "rewards_agent",
    "final_response",
)

builder.add_edge(
    "general_agent",
    "final_response",
)


# Final Response → END

builder.add_edge(
    "final_response",
    END,
)


# Compile

graph = builder.compile()


# ============================================================
# TEST
# ============================================================


def run_test(query: str):
    print("\n" + "=" * 70)
    print(f"INPUT: {query}")
    print("=" * 70)

    result = graph.invoke(
        {
            "query": query,
        }
    )

    print("\nFINAL STATE")
    print("-" * 70)

    print(result)

    print("\nFINAL ANSWER")
    print("-" * 70)

    print(result["final_answer"])


if __name__ == "__main__":

    # Test 1: Rewards Agent

    run_test(
        "When will I receive my cashback?"
    )

    # Test 2: RAG Agent

    run_test(
        "What is the cashback eligibility policy?"
    )

    # Test 3: General Agent

    run_test(
        "What is Python?"
    )
# uv run python -m app.ai.langgraph.multi_agent_workflow