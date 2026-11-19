from typing import List

from langchain_core.documents import Document
from langchain_core.retrievers import BaseRetriever


class CashbackRetriever(BaseRetriever):
    """
    Simple custom LangChain retriever.

    This is an isolated learning example that demonstrates
    how an existing retrieval system can be exposed through
    LangChain's Retriever abstraction.
    """

    documents: List[Document]

    def _get_relevant_documents(self, query: str) -> List[Document]:
        """
        Retrieve relevant documents for the given query.

        In a production system, this method could call:

        FAISS
        BM25
        Hybrid Search
        RRF
        Cross-Encoder

        For this exercise, we use simple keyword matching.
        """

        query_words = set(query.lower().split())

        results = []

        for document in self.documents:
            document_words = set(
                document.page_content.lower().split()
            )

            overlap = query_words.intersection(document_words)

            if overlap:
                results.append(
                    (
                        len(overlap),
                        document,
                    )
                )

        results.sort(
            key=lambda item: item[0],
            reverse=True,
        )

        return [
            document
            for _, document in results
        ]


def main():
    documents = [
        Document(
            page_content=(
                "Cashback is credited within 48 hours "
                "after transaction settlement."
            ),
            metadata={
                "source": "Rewards Policy",
                "category": "cashback",
            },
        ),
        Document(
            page_content=(
                "The maximum cashback per transaction "
                "is £500."
            ),
            metadata={
                "source": "Rewards Policy",
                "category": "limits",
            },
        ),
        Document(
            page_content=(
                "Gold customers receive 10% cashback "
                "on eligible purchases."
            ),
            metadata={
                "source": "Rewards Policy",
                "category": "membership",
            },
        ),
    ]

    retriever = CashbackRetriever(
        documents=documents
    )

    query = "How long does cashback take?"

    results = retriever.invoke(query)

    print("=" * 60)
    print("LANGCHAIN CUSTOM RETRIEVER TEST")
    print("=" * 60)

    print(f"\nQuery: {query}")

    print("\nRetrieved Documents:")

    for index, document in enumerate(
        results,
        start=1,
    ):
        print("\n" + "-" * 60)

        print(f"Rank: {index}")

        print(
            f"Text: {document.page_content}"
        )

        print(
            f"Metadata: {document.metadata}"
        )


if __name__ == "__main__":
    main()
    
# uv run python -m app.ai.langchain_learning.custom_retriever