from typing import TypedDict

from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, START, StateGraph
from langgraph.types import Command, interrupt


class CashbackApprovalState(TypedDict):
    customer_id: str
    amount: float
    reason: str
    approval_status: str
    message: str


# ============================================================
# 1. PROCESS REQUEST
# ============================================================

def process_request(state: CashbackApprovalState):

    print("\n[PROCESS REQUEST]")

    print(
        f"Customer: {state['customer_id']}"
    )

    print(
        f"Cashback adjustment: ₹{state['amount']}"
    )

    print(
        f"Reason: {state['reason']}"
    )

    return {
        "approval_status": "pending"
    }


# ============================================================
# 2. HUMAN APPROVAL NODE
# ============================================================

def human_approval(
    state: CashbackApprovalState,
):

    print("\n[HUMAN APPROVAL REQUIRED]")

    approval = interrupt(
        {
            "type": "cashback_approval",
            "customer_id": state["customer_id"],
            "amount": state["amount"],
            "reason": state["reason"],
            "message": (
                "Approve this cashback adjustment?"
            ),
        }
    )

    print(
        f"\nHuman decision: {approval}"
    )

    if approval == "approve":

        return {
            "approval_status": "approved"
        }

    return {
        "approval_status": "rejected"
    }


# ============================================================
# 3. ROUTING
# ============================================================

def route_after_approval(
    state: CashbackApprovalState,
):

    if state["approval_status"] == "approved":

        return "execute"

    return "reject"


# ============================================================
# 4. EXECUTE APPROVED ACTION
# ============================================================

def execute_cashback(
    state: CashbackApprovalState,
):

    print(
        "\n[EXECUTE CASHBACK ADJUSTMENT]"
    )

    message = (
        f"Cashback adjustment of "
        f"₹{state['amount']} approved "
        f"for customer "
        f"{state['customer_id']}."
    )

    print(message)

    return {
        "message": message
    }


# ============================================================
# 5. REJECT ACTION
# ============================================================

def reject_cashback(
    state: CashbackApprovalState,
):

    print(
        "\n[REJECT CASHBACK ADJUSTMENT]"
    )

    message = (
        f"Cashback adjustment rejected "
        f"for customer "
        f"{state['customer_id']}."
    )

    print(message)

    return {
        "message": message
    }


# ============================================================
# 6. BUILD GRAPH
# ============================================================

builder = StateGraph(
    CashbackApprovalState
)


builder.add_node(
    "process_request",
    process_request,
)

builder.add_node(
    "human_approval",
    human_approval,
)

builder.add_node(
    "execute",
    execute_cashback,
)

builder.add_node(
    "reject",
    reject_cashback,
)


# ============================================================
# 7. EDGES
# ============================================================

builder.add_edge(
    START,
    "process_request",
)

builder.add_edge(
    "process_request",
    "human_approval",
)


builder.add_conditional_edges(
    "human_approval",
    route_after_approval,
    {
        "execute": "execute",
        "reject": "reject",
    },
)


builder.add_edge(
    "execute",
    END,
)

builder.add_edge(
    "reject",
    END,
)


# ============================================================
# 8. CHECKPOINT
# ============================================================

memory = MemorySaver()


# ============================================================
# 9. COMPILE
# ============================================================

graph = builder.compile(
    checkpointer=memory,
)


# ============================================================
# 10. INITIAL EXECUTION
# ============================================================

if __name__ == "__main__":

    print("=" * 70)
    print(
        "LANGGRAPH HUMAN-IN-THE-LOOP"
    )
    print("=" * 70)

    config = {
        "configurable": {
            "thread_id": "cashback-approval-001"
        }
    }

    initial_state = {
        "customer_id": "customer-123",
        "amount": 500.0,
        "reason": (
            "Customer did not receive "
            "expected cashback."
        ),
        "approval_status": "",
        "message": "",
    }

    print(
        "\n[START WORKFLOW]"
    )

    result = graph.invoke(
        initial_state,
        config,
    )

    print(
        "\n[WORKFLOW INTERRUPTED]"
    )

    print(
        "Interrupt information:"
    )

    print(
        result["__interrupt__"]
    )

    # ========================================================
    # RESUME WITH HUMAN DECISION
    # ========================================================

    print(
        "\n[RESUMING WORKFLOW]"
    )

    final_result = graph.invoke(
        Command(
            resume="reject"
        ),
        config,
    )

    print(
        "\n" + "=" * 70
    )

    print(
        "FINAL RESULT"
    )

    print(
        "=" * 70
    )

    print(
        final_result
    )
# uv run python -m app.ai.langgraph.human_in_the_loop