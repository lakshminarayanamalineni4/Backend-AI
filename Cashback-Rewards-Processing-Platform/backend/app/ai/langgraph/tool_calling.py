from langchain_core.tools import tool


@tool
def get_cashback_limit() -> str:
    """Get the maximum cashback allowed per transaction."""
    return "The maximum cashback per transaction is ₹500."


if __name__ == "__main__":
    print("=" * 60)
    print("LANGCHAIN TOOL TEST")
    print("=" * 60)

    print("Tool name:", get_cashback_limit.name)
    print("Tool description:", get_cashback_limit.description)
    print("Tool result:", get_cashback_limit.invoke({}))