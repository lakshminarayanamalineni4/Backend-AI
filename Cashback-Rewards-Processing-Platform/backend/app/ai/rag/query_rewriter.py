"""
Query rewriting for RAG retrieval.

Purpose:

    Convert a raw user question into a clearer,
    retrieval-oriented query before search.

Why this matters:

    Users often ask vague, conversational, or
    incomplete questions.

    Example:

        "when do I get my money back?"

    A rewritten retrieval query might be:

        "How long does it take to receive cashback
         after a successful transaction?"

    Better queries improve:

    - Dense retrieval (FAISS)
    - Sparse retrieval (BM25)
    - Hybrid RRF ranking
    - Cross-Encoder reranking

Important:

    Query rewriting happens BEFORE retrieval.

    It does not replace the existing pipeline:

        FAISS
          ↓
        BM25
          ↓
        Hybrid RRF
          ↓
        Cross-Encoder
          ↓
        LLM Answer

This module is intentionally independent so it
can be tested without running the full RAG flow.
"""

from functools import lru_cache

from app.ai.llm.gemini_service import (
    generate_response,
)


class QueryRewriterService:
    """
    Service responsible for rewriting user queries
    into clearer retrieval-oriented questions.
    """

    def build_prompt(
        self,
        query: str,
    ) -> str:
        """
        Build the prompt used to rewrite a query.

        The model is instructed to:

        - preserve the original meaning
        - make the query clearer for retrieval
        - expand vague wording into domain terms
        - return only the rewritten query
        """

        return f"""
You are a query rewriting assistant for a
Cashback Rewards knowledge base.

Rewrite the user's question into one clear,
self-contained retrieval question that will help
search policy documents.

Rules:

1. Preserve the original intent exactly.
2. If the question is already clear, keep it
   almost unchanged.
3. Expand vague phrases into clear domain terms
   when appropriate.
   Examples:
   - "money back" -> "cashback"
   - "when do I get it" ->
     "How long does it take to receive cashback?"
   - "max cashback" ->
     "What is the maximum cashback per transaction?"
4. Prefer a full natural-language question,
   not a short keyword phrase.
5. Do not answer the question.
6. Do not invent constraints that are not implied
   by the original question.
7. Return ONLY the rewritten query as plain text.
   Do not include quotes, labels, or explanation.

User question:
{query}

Rewritten query:
"""

    def rewrite(
        self,
        query: str,
    ) -> dict[str, str]:
        """
        Rewrite a raw user query.

        Parameters
        ----------
        query:
            Original natural-language user question.

        Returns
        -------
        dict[str, str]
            {
                "original_query": "...",
                "rewritten_query": "...",
            }
        """

        if not query or not query.strip():
            raise ValueError(
                "Query cannot be empty."
            )

        original_query = query.strip()

        prompt = self.build_prompt(
            original_query
        )

        rewritten_query = generate_response(
            prompt
        ).strip()

        # Guard against empty model output.
        # Fall back to the original query so
        # retrieval can still proceed.
        if not rewritten_query:
            rewritten_query = original_query

        return {
            "original_query": original_query,
            "rewritten_query": rewritten_query,
        }


@lru_cache(maxsize=1)
def get_query_rewriter_service() -> QueryRewriterService:
    """
    Create and cache the query rewriter service.
    """

    return QueryRewriterService()


def rewrite_query(
    query: str,
) -> dict[str, str]:
    """
    Public helper for rewriting a user query.
    """

    return get_query_rewriter_service().rewrite(
        query
    )


if __name__ == "__main__":

    test_queries = [
        "when do I get my money back?",
        "max cashback?",
    ]

    print(
        "\n" + "=" * 70
    )

    print(
        "QUERY REWRITER INDEPENDENT TEST"
    )

    print(
        "=" * 70
    )

    for query in test_queries:

        result = rewrite_query(
            query
        )

        print(
            "\n" + "-" * 70
        )

        print(
            "Original:",
            result[
                "original_query"
            ],
        )

        print(
            "Rewritten:",
            result[
                "rewritten_query"
            ],
        )

# uv run python -m app.ai.rag.query_rewriter
