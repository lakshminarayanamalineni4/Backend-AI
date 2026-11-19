from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.retrievers import BaseRetriever
from langchain_google_genai import ChatGoogleGenerativeAI

from app.core.config import settings


class InMemoryRetriever(BaseRetriever):
    """
    Simple in-memory retriever used only for learning.

    This does NOT replace FAISS or BM25.

    It simply returns predefined documents so we can
    understand how LangChain Retriever objects work.
    """

    documents: list[Document]

    def _get_relevant_documents(self, query: str) -> list[Document]:
        """
        Return relevant documents.

        For this learning exercise, we return all documents.

        A real retriever would perform:
        - Vector similarity search
        - BM25 search
        - Hybrid retrieval
        - etc.
        """

        return self.documents


def format_documents(documents: list[Document]) -> str:
    """
    Convert retrieved Document objects into a single
    context string for the LLM.
    """

    return "\n\n".join(
        document.page_content
        for document in documents
    )


def build_rag_chain():
    """
    Build a miniature LangChain RAG pipeline.

    Flow:

    Question
        ↓
    Retriever
        ↓
    Documents
        ↓
    Context Formatter
        ↓
    Prompt
        ↓
    Gemini
        ↓
    Output Parser
    """

    documents = [
        Document(
            page_content=(
                "Cashback is credited within 48 hours "
                "after successful transaction settlement."
            ),
            metadata={
                "source": "rewards_policy.txt",
            },
        ),
        Document(
            page_content=(
                "The maximum cashback per transaction "
                "is ₹500."
            ),
            metadata={
                "source": "rewards_policy.txt",
            },
        ),
        Document(
            page_content=(
                "Gold customers receive 10% cashback "
                "on eligible purchases."
            ),
            metadata={
                "source": "rewards_policy.txt",
            },
        ),
    ]

    retriever = InMemoryRetriever(
        documents=documents
    )

    prompt = ChatPromptTemplate.from_template(
                    """
                    You are a Cashback Rewards Assistant.

                    Answer the question using ONLY the provided context.

                    If the answer is not available in the context,
                    say:

                    "I could not find that information."

                    Context:
                    {context}

                    Question:
                    {question}

                    Answer:
                    """
    )

    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        google_api_key=settings.GEMINI_API_KEY,
        temperature=0,
    )

    output_parser = StrOutputParser()

    rag_chain = (
        {
            "context": retriever | format_documents,
            "question": RunnablePassthrough(),
        }
        | prompt
        | llm
        | output_parser
    )

    return rag_chain


def main():
    question = "How long does it take to receive cashback?"

    rag_chain = build_rag_chain()

    answer = rag_chain.invoke(question)

    print("=" * 70)
    print("LANGCHAIN MINI RAG CHAIN")
    print("=" * 70)

    print("\nQuestion:")
    print(question)

    print("\nAnswer:")
    print(answer)


if __name__ == "__main__":
    main()
    
# uv run python -m app.ai.langchain_learning.mini_rag_chain