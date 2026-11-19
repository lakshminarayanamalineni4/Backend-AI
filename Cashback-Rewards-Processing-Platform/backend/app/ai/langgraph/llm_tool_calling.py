from typing import Annotated

from langchain_core.messages import (
    BaseMessage,
    HumanMessage,
    SystemMessage,
)
from langchain_core.tools import tool
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode
from typing_extensions import TypedDict

from app.core.config import settings


# ============================================================
# 1. DEFINE LANGCHAIN TOOL
# ============================================================

@tool
def get_cashback_limit() -> str:
    """
    Get the maximum cashback amount allowed per transaction.
    """

    return "The maximum cashback per transaction is ₹500."


# ============================================================
# 2. TOOLS LIST
# ============================================================

tools = [
    get_cashback_limit,
]


# ============================================================
# 3. LOAD GEMINI MODEL (LangChain chat model for bind_tools)
# ============================================================

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=settings.GEMINI_API_KEY,
    temperature=0,
)


# ============================================================
# 4. BIND TOOLS TO LLM
# ============================================================

llm_with_tools = llm.bind_tools(tools)


# ============================================================
# 5. DEFINE STATE
# ============================================================

class AgentState(TypedDict):
    messages: Annotated[
        list[BaseMessage],
        add_messages,
    ]


# ============================================================
# 6. LLM NODE
# ============================================================

def call_model(state: AgentState):

    print("\n[LLM NODE]")

    system_message = SystemMessage(
        content=(
            "You are a cashback rewards assistant. "
            "Use the available tools when the user asks "
            "for information that requires them."
        )
    )

    messages = [
        system_message,
        *state["messages"],
    ]

    response = llm_with_tools.invoke(messages)

    print("LLM response:")
    print(response)

    if getattr(response, "tool_calls", None):
        print("\nLLM requested tool calls:")

        for tool_call in response.tool_calls:
            print(
                f"Tool: {tool_call['name']}"
            )
            print(
                f"Arguments: {tool_call['args']}"
            )

    return {
        "messages": [response]
    }


# ============================================================
# 7. ROUTING FUNCTION
# ============================================================

def should_continue(state: AgentState):

    last_message = state["messages"][-1]

    if getattr(last_message, "tool_calls", None):

        print(
            "\n[ROUTER] Tool call detected."
        )

        return "tools"

    print(
        "\n[ROUTER] No tool call detected."
    )

    return END


# ============================================================
# 8. CREATE TOOL NODE
# ============================================================

tool_node = ToolNode(tools)


# ============================================================
# 9. BUILD GRAPH
# ============================================================

builder = StateGraph(AgentState)


builder.add_node(
    "llm",
    call_model,
)

builder.add_node(
    "tools",
    tool_node,
)


# ============================================================
# 10. DEFINE EDGES
# ============================================================

builder.add_edge(
    START,
    "llm",
)


builder.add_conditional_edges(
    "llm",
    should_continue,
    {
        "tools": "tools",
        END: END,
    },
)


builder.add_edge(
    "tools",
    "llm",
)


# ============================================================
# 11. COMPILE
# ============================================================

graph = builder.compile()


# ============================================================
# 12. TEST
# ============================================================

if __name__ == "__main__":
    import sys

    # Windows consoles often default to cp1252; allow ₹ and other Unicode.
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    print("=" * 70)
    print("LLM TOOL CALLING WITH LANGGRAPH")
    print("=" * 70)

    result = graph.invoke(
        {
            "messages": [
                HumanMessage(
                    content=(
                        "What is the maximum cashback "
                        "per transaction?"
                    )
                )
            ]
        }
    )

    print("\n")
    print("=" * 70)
    print("FINAL ANSWER")
    print("=" * 70)

    final_message = result["messages"][-1]

    print(
        final_message.content
    )
# uv run python -m app.ai.langgraph.llm_tool_calling