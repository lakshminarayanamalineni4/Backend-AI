from typing import TypedDict

from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, START, StateGraph
from langgraph.types import Command, interrupt


# ============================================================
# STATE
# ============================================================

class WorkflowState(TypedDict):
    original_query: str
    processed_query: str
    query_type: str

    retrieved_data: str
    relevance_score: float

    attempts: int

    answer: str

    approval_status: str

    status: str


# ============================================================
# NODE 1: PROCESS QUERY
# ============================================================

def process_query(
    state: WorkflowState,
):

    print("\n[PROCESS QUERY]")

    query = state["original_query"].strip()

    print(
        f"Original query: {query}"
    )

    return {
        "processed_query": query,
        "attempts": 0,
        "status": "processing",
    }


# ============================================================
# NODE 2: CLASSIFY QUERY
# ============================================================

def classify_query(
    state: WorkflowState,
):

    print("\n[CLASSIFY QUERY]")

    query = state["processed_query"].lower()

    cashback_keywords = [
        "cashback",
        "cash back",
        "refund",
        "money back",
        "reward",
    ]

    if any(
        keyword in query
        for keyword in cashback_keywords
    ):

        query_type = "cashback"

    else:

        query_type = "general"

    print(
        f"Query type: {query_type}"
    )

    return {
        "query_type": query_type
    }


# ============================================================
# CONDITIONAL ROUTING
# ============================================================

def route_query(
    state: WorkflowState,
):

    if state["query_type"] == "cashback":

        return "cashback"

    return "general"


# ============================================================
# NODE 3: GENERAL QUESTION
# ============================================================

def general_question(
    state: WorkflowState,
):

    print(
        "\n[GENERAL QUESTION]"
    )

    answer = (
        "This is a general question. "
        "No cashback retrieval workflow "
        "is required."
    )

    return {
        "answer": answer,
        "status": "completed",
    }


# ============================================================
# NODE 4: RETRIEVE CASHBACK INFORMATION
# ============================================================

def retrieve_cashback(
    state: WorkflowState,
):

    attempt = state["attempts"] + 1

    print(
        "\n[RETRIEVE CASHBACK]"
    )

    print(
        f"Query: {state['processed_query']}"
    )

    print(
        f"Attempt: {attempt}"
    )

    # --------------------------------------------------------
    # Simulated tool call
    # --------------------------------------------------------

    query = (
        state["processed_query"]
        .lower()
    )

    if (
        "money back" in query
        or "when" in query
        or "cashback" in query
    ):

        retrieved_data = (
            "Cashback is credited within "
            "48 hours after transaction "
            "settlement."
        )

    else:

        retrieved_data = (
            "No highly relevant cashback "
            "information was found."
        )

    return {
        "retrieved_data": retrieved_data,
        "attempts": attempt,
    }


# ============================================================
# NODE 5: CHECK RELEVANCE
# ============================================================

def check_relevance(
    state: WorkflowState,
):

    print(
        "\n[CHECK RELEVANCE]"
    )

    data = state["retrieved_data"]

    if (
        "48 hours" in data
        and state["attempts"] >= 1
    ):

        score = 0.95

    else:

        score = 0.30

    print(
        f"Relevance score: {score}"
    )

    if score >= 0.80:

        print(
            "Result: RELEVANT"
        )

        status = "relevant"

    else:

        print(
            "Result: NOT RELEVANT"
        )

        status = "not_relevant"

    return {
        "relevance_score": score,
        "status": status,
    }


# ============================================================
# RETRY ROUTING
# ============================================================

def route_relevance(
    state: WorkflowState,
):

    if (
        state["status"] == "relevant"
    ):

        return "generate"

    if (
        state["attempts"] < 2
    ):

        return "rewrite"

    return "generate"


# ============================================================
# NODE 6: REWRITE QUERY
# ============================================================

def rewrite_query(
    state: WorkflowState,
):

    print(
        "\n[REWRITE QUERY]"
    )

    original = (
        state["processed_query"]
    )

    if (
        original
        == "when do I get my money back?"
    ):

        rewritten = (
            "How long does it take "
            "to receive my cashback?"
        )

    else:

        rewritten = (
            f"Information about "
            f"{original}"
        )

    print(
        f"Rewritten query: {rewritten}"
    )

    return {
        "processed_query": rewritten
    }


# ============================================================
# NODE 7: GENERATE ANSWER
# ============================================================

def generate_answer(
    state: WorkflowState,
):

    print(
        "\n[GENERATE ANSWER]"
    )

    if (
        state["query_type"]
        == "general"
    ):

        answer = state["answer"]

    else:

        answer = (
            "Based on the retrieved "
            "information: "
            f"{state['retrieved_data']}"
        )

    print(
        f"Generated answer: {answer}"
    )

    return {
        "answer": answer
    }


# ============================================================
# NODE 8: HUMAN APPROVAL
# ============================================================

def human_approval(
    state: WorkflowState,
):

    print(
        "\n[HUMAN APPROVAL REQUIRED]"
    )

    decision = interrupt(
        {
            "type": "answer_review",
            "query": state["original_query"],
            "answer": state["answer"],
            "message": (
                "Approve this answer?"
            ),
        }
    )

    print(
        f"Human decision: {decision}"
    )

    if decision == "approve":

        return {
            "approval_status": "approved",
            "status": "completed",
        }

    return {
        "approval_status": "rejected",
        "status": "rejected",
    }


# ============================================================
# HUMAN APPROVAL ROUTING
# ============================================================

def route_approval(
    state: WorkflowState,
):

    if (
        state["approval_status"]
        == "approved"
    ):

        return "approved"

    return "rejected"


# ============================================================
# NODE 9: FINAL APPROVED RESPONSE
# ============================================================

def approved_response(
    state: WorkflowState,
):

    print(
        "\n[APPROVED RESPONSE]"
    )

    print(
        "Answer approved."
    )

    return {
        "status": "completed"
    }


# ============================================================
# NODE 10: REJECTED RESPONSE
# ============================================================

def rejected_response(
    state: WorkflowState,
):

    print(
        "\n[REJECTED RESPONSE]"
    )

    print(
        "Answer rejected. "
        "Escalating for human review."
    )

    return {
        "status": "escalated"
    }


# ============================================================
# BUILD GRAPH
# ============================================================

builder = StateGraph(
    WorkflowState
)


# ============================================================
# ADD NODES
# ============================================================

builder.add_node(
    "process_query",
    process_query,
)

builder.add_node(
    "classify_query",
    classify_query,
)

builder.add_node(
    "general_question",
    general_question,
)

builder.add_node(
    "retrieve_cashback",
    retrieve_cashback,
)

builder.add_node(
    "check_relevance",
    check_relevance,
)

builder.add_node(
    "rewrite_query",
    rewrite_query,
)

builder.add_node(
    "generate_answer",
    generate_answer,
)

builder.add_node(
    "human_approval",
    human_approval,
)

builder.add_node(
    "approved_response",
    approved_response,
)

builder.add_node(
    "rejected_response",
    rejected_response,
)


# ============================================================
# EDGES
# ============================================================

builder.add_edge(
    START,
    "process_query",
)

builder.add_edge(
    "process_query",
    "classify_query",
)


# ============================================================
# CONDITIONAL ROUTING
# ============================================================

builder.add_conditional_edges(
    "classify_query",
    route_query,
    {
        "cashback":
            "retrieve_cashback",

        "general":
            "general_question",
    },
)


# ============================================================
# CASHBACK RETRIEVAL
# ============================================================

builder.add_edge(
    "retrieve_cashback",
    "check_relevance",
)


# ============================================================
# RETRY LOOP
# ============================================================

builder.add_conditional_edges(
    "check_relevance",
    route_relevance,
    {
        "generate":
            "generate_answer",

        "rewrite":
            "rewrite_query",
    },
)


builder.add_edge(
    "rewrite_query",
    "retrieve_cashback",
)


# ============================================================
# GENERAL → ANSWER
# ============================================================

builder.add_edge(
    "general_question",
    "generate_answer",
)


# ============================================================
# ANSWER → HUMAN APPROVAL
# ============================================================

builder.add_edge(
    "generate_answer",
    "human_approval",
)


# ============================================================
# APPROVAL ROUTING
# ============================================================

builder.add_conditional_edges(
    "human_approval",
    route_approval,
    {
        "approved":
            "approved_response",

        "rejected":
            "rejected_response",
    },
)


# ============================================================
# END
# ============================================================

builder.add_edge(
    "approved_response",
    END,
)

builder.add_edge(
    "rejected_response",
    END,
)


# ============================================================
# CHECKPOINTING
# ============================================================

memory = MemorySaver()


# ============================================================
# COMPILE
# ============================================================

graph = builder.compile(
    checkpointer=memory,
)


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":

    print("=" * 70)

    print(
        "MULTI-STEP LANGGRAPH WORKFLOW"
    )

    print("=" * 70)

    config = {
        "configurable": {
            "thread_id":
                "multi-step-cashback-001"
        }
    }

    initial_state = {

        "original_query":
            "when do I get my money back?",

        "processed_query":
            "",

        "query_type":
            "",

        "retrieved_data":
            "",

        "relevance_score":
            0.0,

        "attempts":
            0,

        "answer":
            "",

        "approval_status":
            "",

        "status":
            "",
    }


    # ========================================================
    # FIRST EXECUTION
    # ========================================================

    result = graph.invoke(
        initial_state,
        config,
    )


    print(
        "\n" + "=" * 70
    )

    print(
        "WORKFLOW PAUSED"
    )

    print(
        "=" * 70
    )

    print(
        result["__interrupt__"]
    )


    # ========================================================
    # HUMAN APPROVAL
    # ========================================================

    final_result = graph.invoke(

        Command(
            resume="approve"
        ),

        config,
    )


    print(
        "\n" + "=" * 70
    )

    print(
        "FINAL WORKFLOW RESULT"
    )

    print(
        "=" * 70
    )

    print(
        final_result
    )