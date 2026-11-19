from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI

from app.core.config import settings


def build_chain():
    """
    Build a simple LangChain pipeline:

    User Input
        ↓
    Prompt Template
        ↓
    Gemini LLM
        ↓
    String Output Parser
    """

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are a helpful AI assistant. "
                "Answer clearly and concisely.",
            ),
            (
                "human",
                "{question}",
            ),
        ]
    )

    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        google_api_key=settings.GEMINI_API_KEY,
        temperature=0,
    )

    output_parser = StrOutputParser()

    chain = prompt | llm | output_parser

    return chain


def run_chain(question: str) -> str:
    """
    Execute the LangChain pipeline.
    """

    chain = build_chain()

    response = chain.invoke(
        {
            "question": question,
        }
    )

    return response


def main():
    question = "What is RAG in Generative AI?"

    answer = run_chain(question)

    print("=" * 70)
    print("LANGCHAIN BASIC CHAIN")
    print("=" * 70)

    print("\nQuestion:")
    print(question)

    print("\nAnswer:")
    print(answer)


if __name__ == "__main__":
    main()
    
# uv run python -m app.ai.langchain_learning.basic_chain